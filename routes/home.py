import random
import string
from flask import Blueprint, render_template, request, redirect, url_for, make_response
from models import Game, User, Leaderboard, Avatar, Skin, UserAvatar, UserSkin
from extensions import db
from sqlalchemy import desc

home_bp = Blueprint('home', __name__)

def generate_user_id():
    """Tạo ID ngẫu nhiên gồm 10 ký tự."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))

def create_new_user(user_id, display_name):
    """Tạo người dùng mới và lưu vào cơ sở dữ liệu."""
    user = User.query.get(user_id)
    if not user:
        user = User(user_id=user_id, displayName=display_name)
        
        # Tìm avatar mặc định (price=0)
        default_avatar_instance = Avatar.query.filter_by(price=0).first()

        if default_avatar_instance:
            user.avatar = default_avatar_instance.image_url
        # Nếu không có default_avatar_instance, user.avatar sẽ là None, template sẽ dùng fallback tĩnh.
            
        db.session.add(user)
        # Commit user trước để có user.user_id cho UserAvatar
        # Hoặc commit một lần cuối, SQLAlchemy thường xử lý được. Để an toàn, commit sớm hơn nếu cần.

        if default_avatar_instance:
            # Đảm bảo người dùng "sở hữu" avatar mặc định
            existing_user_avatar = UserAvatar.query.filter_by(user_id=user.user_id, avatar_id=default_avatar_instance.avatar_id).first()
            if not existing_user_avatar:
                user_avatar_entry = UserAvatar(user_id=user.user_id, avatar_id=default_avatar_instance.avatar_id)
                db.session.add(user_avatar_entry)
        
        # Tạm thời bỏ qua skin vì User model không có trường skin trực tiếp
        # default_skin = Skin.query.filter_by(name='Default Skin').first() # Hoặc price=0
        # if default_skin:
        #     # user.skin = default_skin.image_url # User model không có trường này
        #     user_skin_entry = UserSkin(user_id=user.user_id, skin_id=default_skin.skin_id)
        #     db.session.add(user_skin_entry)

        db.session.commit()
    return user

@home_bp.route('/')
def index():
    # Kiểm tra xem người chơi đã có tên và ID trong cookie chưa
    user_id = request.cookies.get('user_id')
    display_name = request.cookies.get('display_name')

    if not display_name or not user_id:
        # Nếu chưa có, chuyển hướng đến trang nhập tên
        return redirect(url_for('home.enter_name'))

    # Lấy thông tin người dùng
    user = User.query.get(user_id)
    if not user:
        # Tạo người dùng mới nếu không tìm thấy
        user = create_new_user(user_id, display_name)

    # Lấy dữ liệu leaderboard thực từ cơ sở dữ liệu
    leaderboard_data = db.session.query(
        User, Leaderboard
    ).join(
        Leaderboard, User.user_id == Leaderboard.user_id
    ).order_by(
        desc(Leaderboard.wins)
    ).limit(5).all()
    
    # Định dạng dữ liệu cho template
    leaderboard = []
    for user_data, leaderboard_entry in leaderboard_data:
        leaderboard.append({
            "user": {
                "username": user_data.displayName,
                "avatar": user_data.avatar or url_for('static', filename='images/default_avatar.png')
            },
            "wins": leaderboard_entry.wins
        })
    
    # Tạo dữ liệu giả cho leaderboard nếu không có dữ liệu từ database
    if not leaderboard:
        leaderboard = [
            {"user": {"username": "Nguyễn Văn A", "avatar": "/static/images/avatar1.png"}, "wins": 48},
            {"user": {"username": "Trần Thị B", "avatar": "/static/images/avatar2.png"}, "wins": 36},
            {"user": {"username": "Lê Văn C", "avatar": "/static/images/default_avatar.png"}, "wins": 29},
            {"user": {"username": "Phạm Thị D", "avatar": "/static/images/avatar1.png"}, "wins": 21},
            {"user": {"username": "Hoàng Văn E", "avatar": "/static/images/avatar2.png"}, "wins": 15}
        ]
    
    # Lấy tất cả Avatars và Skins từ DB cho Store Preview
    all_db_avatars = Avatar.query.all()
    all_db_skins = Skin.query.all()

    # Chuẩn bị AVATARS cho Store Preview (chỉ lấy item có giá > 0, không fallback tĩnh)
    avatars_for_store = [av for av in all_db_avatars if av.price > 0]
    
    # Chuẩn bị SKINS (ICONS) cho Store Preview (chỉ lấy item có giá > 0, không fallback tĩnh)
    icons_for_store = [s for s in all_db_skins if s.price > 0]

    # Lấy danh sách vật phẩm đã sở hữu từ database
    user_avatar_entries = UserAvatar.query.filter_by(user_id=user_id).all()
    user_skin_entries = UserSkin.query.filter_by(user_id=user_id).all()
    
    user_avatar_ids = [ua.avatar_id for ua in user_avatar_entries]
    user_skin_ids = [us.skin_id for us in user_skin_entries]
    
    user_coins = request.cookies.get('user_coins', '3000')

    response = make_response(render_template('home.htm', 
                           leaderboard=leaderboard, 
                           icons=icons_for_store,
                           avatars=avatars_for_store,
                           username=display_name, 
                           user_id=user_id,
                           user=user,
                           user_avatar_ids=user_avatar_ids,
                           user_skin_ids=user_skin_ids,
                           user_coins=user_coins))
    
    # Đồng bộ cookie user_avatar
    current_cookie_avatar = request.cookies.get('user_avatar')
    db_user_avatar_url = user.avatar 
    default_db_avatar_instance = Avatar.query.filter_by(price=0).first()
    static_default_url = url_for('static', filename='images/default_avatar.png')

    new_cookie_value = None
    if db_user_avatar_url:
        new_cookie_value = db_user_avatar_url
    elif default_db_avatar_instance:
        new_cookie_value = default_db_avatar_instance.image_url
    else:
        new_cookie_value = static_default_url

    if new_cookie_value and current_cookie_avatar != new_cookie_value:
        response.set_cookie('user_avatar', new_cookie_value, max_age=60*60*24*30)
    elif not current_cookie_avatar and new_cookie_value: # Cookie chưa từng được set
        response.set_cookie('user_avatar', new_cookie_value, max_age=60*60*24*30)
        
    return response

@home_bp.route('/enter_name', methods=['GET', 'POST'])
def enter_name():
    if request.method == 'POST':
        display_name = request.form.get('display_name')
        next_url = request.form.get('next_url') # Lấy next_url từ form
        if not display_name:
            return render_template('set_name.htm', error="Tên không được để trống!", next_url=next_url)

        # Tạo ID ngẫu nhiên
        user_id = generate_user_id()

        # Lưu vào cơ sở dữ liệu
        user = create_new_user(user_id, display_name)

        # Lưu vào cookie
        if next_url:
            response = make_response(redirect(next_url))
        else:
            response = make_response(redirect(url_for('home.index')))
        response.set_cookie('display_name', display_name, max_age=60*60*24*30)  # Lưu trong 30 ngày
        response.set_cookie('user_id', user_id, max_age=60*60*24*30)  # Lưu trong 30 ngày
        response.set_cookie('user_coins', '3000', max_age=60*60*24*30)  # Lưu số tiền mặc định
        return response
    
    # GET request
    next_url_param = request.args.get('next') # Lấy next từ query param cho GET request
    return render_template('set_name.htm', next_url=next_url_param)