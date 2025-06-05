from flask import Blueprint, render_template, redirect, url_for, session, request, flash, make_response, jsonify
from models import User, Leaderboard, UserAvatar, Avatar, Skin, UserSkin
from extensions import db
from sqlalchemy import desc

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/profile')
def index():
    # Kiểm tra cookie người dùng
    user_id = request.cookies.get('user_id')
    if not user_id:
        return redirect(url_for('home.enter_name'))
    
    # Lấy thông tin người dùng
    user = User.query.get(user_id)
    if not user:
        from routes.home import create_new_user
        display_name = request.cookies.get('display_name')
        user = create_new_user(user_id, display_name)
    
    # Lấy avatar mặc định từ DB (price=0)
    default_avatar_from_db = Avatar.query.filter_by(price=0).first()
    # default_avatar_id sẽ là ID của avatar mặc định từ DB, hoặc None nếu không có.
    # Template sẽ cần xử lý trường hợp default_avatar_from_db là None.
    default_avatar_id_for_template = default_avatar_from_db.avatar_id if default_avatar_from_db else None 
    
    # Lấy danh sách avatar của người dùng (những cái user thực sự sở hữu qua UserAvatar)
    user_owned_avatars = db.session.query(
        Avatar
    ).join(
        UserAvatar, UserAvatar.avatar_id == Avatar.avatar_id
    ).filter(
        UserAvatar.user_id == user_id
    ).all()
    
    # Lấy danh sách skin của người dùng
    user_skins = db.session.query(
        Skin
    ).join(
        UserSkin, UserSkin.skin_id == Skin.skin_id
    ).filter(
        UserSkin.user_id == user_id
    ).all()
    
    # Lấy danh sách avatar có thể mua
    available_avatars = Avatar.query.filter(
        ~Avatar.avatar_id.in_([ua.avatar_id for ua in user_owned_avatars])
    ).all()
    
    # Lấy danh sách skin có thể mua
    available_skins = Skin.query.filter(
        ~Skin.skin_id.in_([us.skin_id for us in user_skins])
    ).all()
    
    # Lấy số tiền từ cookie
    user_coins = request.cookies.get('user_coins', '3000')
    
    response = make_response(render_template(
        'profile.htm', 
        user=user,
        user_avatars=user_owned_avatars,
        user_skins=user_skins,
        available_avatars=available_avatars,
        available_skins=available_skins,
        user_coins=user_coins,
        default_avatar_db = default_avatar_from_db,
        default_avatar_id = default_avatar_id_for_template
    ))

    # Đồng bộ cookie user_avatar
    current_cookie_avatar = request.cookies.get('user_avatar')
    db_user_avatar_url = user.avatar
    static_default_url = url_for('static', filename='images/default_avatar.png')

    new_cookie_value = None
    if db_user_avatar_url:
        new_cookie_value = db_user_avatar_url
    elif default_avatar_from_db: # Ưu tiên default từ DB nếu user.avatar chưa có
        new_cookie_value = default_avatar_from_db.image_url
    else: # Fallback cuối cùng nếu DB cũng không có default (price=0)
        new_cookie_value = static_default_url

    if new_cookie_value and current_cookie_avatar != new_cookie_value:
        response.set_cookie('user_avatar', new_cookie_value, max_age=60*60*24*30)
    elif not current_cookie_avatar and new_cookie_value: 
        response.set_cookie('user_avatar', new_cookie_value, max_age=60*60*24*30)

    return response

@profile_bp.route('/update_profile', methods=['POST'])
def update_profile():
    # Kiểm tra cookie người dùng
    user_id = request.cookies.get('user_id')
    if not user_id:
        return redirect(url_for('home.enter_name'))
    
    # Get form data
    display_name = request.form.get('displayName')
    selected_avatar_id = request.form.get('selected_avatar')
    
    print(f"DEBUG: selected_avatar_id = {selected_avatar_id}")
    
    # Validate display name
    if not display_name or len(display_name) < 3 or len(display_name) > 50:
        flash('Tên hiển thị phải từ 3-50 ký tự')
        return redirect(url_for('profile.index'))
    
    # Update user
    user = User.query.get(user_id)
    if user:
        # Cập nhật tên người dùng
        user.displayName = display_name
        
        # Cập nhật avatar nếu có chọn
        if selected_avatar_id:
            print(f"DEBUG: Đang cập nhật avatar, ID = {selected_avatar_id}")
            # Kiểm tra xem người dùng có avatar này không
            avatar_id = int(selected_avatar_id)
            
            # Lấy thông tin avatar mặc định từ DB
            default_avatar_db_update = Avatar.query.filter_by(price=0).first()
            # default_avatar_id_for_comparison sẽ là ID của default avatar từ DB, hoặc một giá trị không thể trùng nếu không có
            default_avatar_id_for_comparison = default_avatar_db_update.avatar_id if default_avatar_db_update else -1 # Giả sử -1 không phải là ID hợp lệ

            print(f"DEBUG: Default avatar ID from DB for comparison = {default_avatar_id_for_comparison}")

            # Kiểm tra xem người dùng có avatar này không
            if avatar_id == default_avatar_id_for_comparison:
                # Đây là avatar mặc định từ DB
                print("DEBUG: Đang đặt avatar mặc định từ DB")
                if default_avatar_db_update: # Phải chắc chắn nó tồn tại
                    user.avatar = default_avatar_db_update.image_url
                else: # Fallback nếu default avatar price=0 không có trong DB
                    user.avatar = url_for('static', filename='images/default_avatar.png')
            else:
                user_avatar = UserAvatar.query.filter_by(
                    user_id=user_id,
                    avatar_id=avatar_id
                ).first()
                
                if user_avatar:
                    print("DEBUG: Đang đặt avatar từ UserAvatar")
                    # Lấy thông tin avatar
                    avatar = Avatar.query.get(avatar_id)
                    if avatar:
                        user.avatar = avatar.image_url
                else:
                    print("DEBUG: Không tìm thấy avatar trong UserAvatar")
        
        # Lưu thay đổi
        db.session.commit()
        print(f"DEBUG: Avatar sau khi cập nhật = {user.avatar}")
        
        # Cập nhật cookie
        response = make_response(redirect(url_for('profile.index')))
        response.set_cookie('display_name', display_name)
        if selected_avatar_id:
            # Lấy thông tin avatar mặc định từ DB để set cookie
            default_avatar_for_cookie = Avatar.query.filter_by(price=0).first()
            selected_avatar_id_int = int(selected_avatar_id)

            if default_avatar_for_cookie and selected_avatar_id_int == default_avatar_for_cookie.avatar_id:
                # Đây là avatar mặc định từ DB
                response.set_cookie('user_avatar', default_avatar_for_cookie.image_url, max_age=60*60*24*30)
            else:
                avatar_selected_for_cookie = Avatar.query.get(selected_avatar_id_int)
                if avatar_selected_for_cookie:
                    response.set_cookie('user_avatar', avatar_selected_for_cookie.image_url, max_age=60*60*24*30)
                elif default_avatar_for_cookie: # Fallback cookie nếu avatar đã chọn không tìm thấy
                     response.set_cookie('user_avatar', default_avatar_for_cookie.image_url, max_age=60*60*24*30)
                else: # Fallback cuối cùng cho cookie
                    response.set_cookie('user_avatar', url_for('static', filename='images/default_avatar.png'), max_age=60*60*24*30)
        
        flash('Cập nhật hồ sơ thành công')
        return response
    
    return redirect(url_for('profile.index'))

@profile_bp.route('/profile/change_avatar/<int:avatar_id>')
def change_avatar(avatar_id):
    # Kiểm tra cookie người dùng
    user_id = request.cookies.get('user_id')
    if not user_id:
        return redirect(url_for('home.enter_name'))
    
    # Kiểm tra xem người dùng có avatar này không
    user_avatar = UserAvatar.query.filter_by(
        user_id=user_id,
        avatar_id=avatar_id
    ).first()
    
    if not user_avatar:
        flash('Bạn chưa sở hữu avatar này')
        return redirect(url_for('profile.index'))
    
    # Lấy thông tin avatar
    avatar = Avatar.query.get(avatar_id)
    if not avatar:
        flash('Avatar không tồn tại')
        return redirect(url_for('profile.index'))
    
    # Cập nhật avatar cho người dùng
    user = User.query.get(user_id)
    if user:
        user.avatar = avatar.image_url
        db.session.commit()
        
        # Cập nhật avatar trong cookie để hiển thị đúng ở trang khác
        response = make_response(redirect(url_for('profile.index')))
        response.set_cookie('user_avatar', avatar.image_url, max_age=60*60*24*30)  # 30 ngày
        
        flash('Đã cập nhật avatar thành công')
        return response
    else:
        flash('Không tìm thấy người dùng')
    
    return redirect(url_for('profile.index'))

@profile_bp.route('/profile/change_skin/<int:skin_id>')
def change_skin(skin_id):
    # Kiểm tra cookie người dùng
    user_id = request.cookies.get('user_id')
    if not user_id:
        return redirect(url_for('home.enter_name'))
    
    # Kiểm tra xem người dùng có skin này không
    user_skin = UserSkin.query.filter_by(
        user_id=user_id,
        skin_id=skin_id
    ).first()
    
    if not user_skin:
        return redirect(url_for('profile.index'))
    
    # Lưu skin đã chọn vào cookie
    response = make_response(redirect(url_for('profile.index')))
    response.set_cookie('selected_skin', str(skin_id), max_age=60*60*24*30)  # 30 ngày
    
    return response

@profile_bp.route('/delete_account', methods=['POST'])
def delete_account():
    # Lấy user_id từ cookie
    user_id = request.cookies.get('user_id')
    if not user_id:
        return jsonify({'success': False, 'message': 'Không tìm thấy người dùng'}), 404
    
    try:
        # Xóa tất cả dữ liệu liên quan đến người dùng
        # 1. Xóa các bản ghi trong UserSkin
        UserSkin.query.filter_by(user_id=user_id).delete()
        
        # 2. Xóa các bản ghi trong UserAvatar
        UserAvatar.query.filter_by(user_id=user_id).delete()
        
        # 3. Xóa bản ghi trong Leaderboard
        Leaderboard.query.filter_by(user_id=user_id).delete()
        
        # 4. Xóa các game của người dùng (nếu có bảng Game)
        if 'Game' in globals():
            Game = globals()['Game']
            Game.query.filter((Game.player1_id == user_id) | (Game.player2_id == user_id)).delete()
        
        # 5. Cuối cùng xóa người dùng
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
        
        # Lưu các thay đổi
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Tài khoản đã được xóa thành công'}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Lỗi khi xóa tài khoản: {str(e)}")
        return jsonify({'success': False, 'message': 'Có lỗi xảy ra khi xóa tài khoản'}), 500