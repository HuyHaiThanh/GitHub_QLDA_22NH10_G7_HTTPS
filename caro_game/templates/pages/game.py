import frappe

def get_context(context):
    """Tạo context cho trang game chính"""
    
    # Nếu người dùng không đăng nhập, chuyển hướng đến trang đăng nhập
    if not frappe.session.user or frappe.session.user == 'Guest':
        frappe.local.flags.redirect_location = "/login"
        raise frappe.Redirect
    
    # Lấy thông tin người dùng từ database
    user = frappe.get_doc("User", frappe.session.user)
    context.user = user
    
    # Lấy thông tin Caro Player (nếu có)
    try:
        player = frappe.get_doc("Caro Player", {"email": frappe.session.user})
        context.player = player
        context.user_coins = player.coins if hasattr(player, 'coins') else 0
    except frappe.DoesNotExistError:
        # Nếu chưa có thông tin Caro Player, tạo mặc định
        context.user_coins = 0
    
    # Khởi tạo thông tin game mặc định cho trang
    context.player1 = {
        "username": frappe.session.user,
        "avatar": user.user_image if hasattr(user, 'user_image') else None
    }
    
    # Người chơi thứ hai có thể là AI hoặc chưa xác định
    context.player2 = {
        "username": "Waiting...",
        "avatar": None
    }
    
    # Tạo một game_id mới hoặc lấy từ request
    game_id = frappe.request.args.get('game_id')
    if not game_id:
        # Trong trường hợp không có game_id, có thể tạo mới hoặc hiển thị danh sách game
        # Đây chỉ là phần giả lập, trong thực tế bạn cần tạo hoặc lấy game_id từ database
        game_id = "new_game"
    
    context.game_id = game_id
    context.is_ai_opponent = False  # Đặt True nếu đối thủ là AI
    
    # Lấy danh sách người chơi hàng đầu cho bảng xếp hạng
    try:
        leaderboard = frappe.get_all(
            "Leaderboard", 
            fields=["name", "player", "wins"], 
            order_by="wins desc", 
            limit=5
        )
        context.leaderboard = leaderboard
    except:
        # Nếu không có bảng xếp hạng, tạo danh sách trống
        context.leaderboard = []
    
    # Đặt tiêu đề và mô tả trang
    context.title = "Caro Game"
    context.description = "Play Caro Game Online"
    
    return context