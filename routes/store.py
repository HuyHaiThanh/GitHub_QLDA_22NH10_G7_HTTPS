from flask import Blueprint, render_template, request, redirect, url_for, jsonify, make_response
from models import User, Avatar, Skin, UserAvatar, UserSkin
from extensions import db

store_bp = Blueprint('store', __name__)

@store_bp.route('/store')
def index():
    user_id = request.cookies.get('user_id')
    if not user_id:
        return redirect(url_for('home.enter_name'))
    
    user = User.query.get(user_id)
    if not user:
        return redirect(url_for('home.enter_name'))
    
    # Lấy tất cả Avatars và Skins từ DB
    all_db_avatars = Avatar.query.all()
    all_db_skins = Skin.query.all()

    # Lấy AVATARS cho cửa hàng (chỉ item có giá > 0)
    avatars_for_display = [av for av in all_db_avatars if av.price > 0]
    
    # Lấy SKINS (ICONS) cho cửa hàng (chỉ item có giá > 0)
    skins_for_display = [s for s in all_db_skins if s.price > 0]
    
    # Lấy danh sách vật phẩm đã sở hữu
    user_avatar_entries = UserAvatar.query.filter_by(user_id=user_id).all()
    user_skin_entries = UserSkin.query.filter_by(user_id=user_id).all()
    
    user_avatar_ids = [ua.avatar_id for ua in user_avatar_entries]
    user_skin_ids = [us.skin_id for us in user_skin_entries]
    
    user_coins = request.cookies.get('user_coins', '3000')
    
    return render_template(
        'store.htm',
        user=user,
        avatars=avatars_for_display,
        skins=skins_for_display,
        user_avatar_ids=user_avatar_ids,
        user_skin_ids=user_skin_ids,
        user_coins=user_coins
    )

@store_bp.route('/buy_item/<string:item_type>/<int:item_id>', methods=['POST'])
def buy_item(item_type, item_id):
    # Kiểm tra user cookie
    user_id = request.cookies.get('user_id')
    if not user_id:
        return jsonify({'success': False, 'message': 'Bạn cần đăng nhập để mua hàng'})
    
    # Lấy thông tin người dùng
    user = User.query.get(user_id)
    if not user:
        return jsonify({'success': False, 'message': 'Không tìm thấy người dùng'})
    
    # Lấy số tiền từ cookie
    user_coins = int(request.cookies.get('user_coins', '3000'))
    
    # Xác định loại vật phẩm và giá
    if item_type == "avatar":
        item = Avatar.query.get(item_id)
        if not item:
            return jsonify({'success': False, 'message': 'Avatar không tồn tại'})
        price = item.price
    else:
        item = Skin.query.get(item_id)
        if not item:
            return jsonify({'success': False, 'message': 'Skin không tồn tại'})
        price = item.price
    
    # Kiểm tra số tiền
    if user_coins < price:
        return jsonify({'success': False, 'message': 'Số tiền không đủ'})
    
    # Kiểm tra xem đã sở hữu vật phẩm chưa
    if item_type == "avatar":
        existing_item = UserAvatar.query.filter_by(user_id=user_id, avatar_id=item_id).first()
        if existing_item:
            return jsonify({'success': False, 'message': 'Bạn đã sở hữu avatar này'})
    else:
        existing_item = UserSkin.query.filter_by(user_id=user_id, skin_id=item_id).first()
        if existing_item:
            return jsonify({'success': False, 'message': 'Bạn đã sở hữu skin này'})
    
    # Mua vật phẩm
    try:
        # Trừ tiền
        user_coins -= price
        
        # Lưu vào database
        if item_type == "avatar":
            user_avatar = UserAvatar(user_id=user_id, avatar_id=item_id)
            db.session.add(user_avatar)
        else:
            user_skin = UserSkin(user_id=user_id, skin_id=item_id)
            db.session.add(user_skin)
        
        db.session.commit()
        
        # Cập nhật cookie
        response = make_response(jsonify({
            'success': True,
            'message': 'Mua hàng thành công',
            'coins': user_coins
        }))
        response.set_cookie('user_coins', str(user_coins))
        
        return response
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Có lỗi xảy ra khi mua hàng'}) 