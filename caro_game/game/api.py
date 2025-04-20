import frappe
from frappe import _

@frappe.whitelist()
def get_game_state(game_id):
    """Lấy trạng thái hiện tại của trò chơi"""
    if game_id == "new_game":
        # Trả về trạng thái trò chơi mới nếu đây là game mới
        return {
            "game_id": "new_game",
            "status": "active",
            "status_message": "Game mới đã được tạo!",
            "current_turn": "X",
            "moves": [],
            "players": {
                "X": frappe.session.user,
                "O": "Waiting..."
            }
        }
    
    # Trong thực tế, ở đây chúng ta sẽ truy vấn doctype Game để lấy thông tin trò chơi
    # Nhưng hiện tại chỉ trả về mock data
    try:
        # Thử lấy thông tin trò chơi từ database nếu tồn tại
        game = frappe.get_doc("Game", game_id)
        
        # Lấy danh sách các nước đi
        moves = frappe.get_all("Move", 
            filters={"game": game_id}, 
            fields=["position_x", "position_y", "player_type"],
            order_by="creation asc")
        
        # Xác định lượt đi hiện tại
        current_turn = "O" if len(moves) % 2 == 1 else "X"
        
        return {
            "game_id": game_id,
            "status": game.status,
            "status_message": game.status_message if hasattr(game, 'status_message') else "",
            "current_turn": current_turn,
            "moves": moves,
            "players": {
                "X": game.player_x,
                "O": game.player_o or "Waiting..."
            }
        }
    except Exception as e:
        frappe.log_error(f"Error getting game state: {str(e)}")
        # Nếu không tìm thấy trò chơi, trả về trạng thái mặc định
        return {
            "game_id": game_id,
            "status": "unknown",
            "status_message": "Không tìm thấy trò chơi hoặc xảy ra lỗi.",
            "current_turn": "X",
            "moves": [],
            "players": {
                "X": frappe.session.user,
                "O": "Unknown"
            }
        }

@frappe.whitelist()
def make_move(game_id, row, col):
    """Thực hiện nước đi trên bàn cờ"""
    if not frappe.session.user or frappe.session.user == 'Guest':
        return {"error": "Bạn cần đăng nhập để chơi."}
    
    try:
        row = int(row)
        col = int(col)
        
        # Kiểm tra vị trí hợp lệ
        if row < 0 or row >= 15 or col < 0 or col >= 15:
            return {"error": "Vị trí không hợp lệ."}
        
        # Trong thực tế, ở đây sẽ kiểm tra xem nước đi có hợp lệ không,
        # lưu nước đi vào cơ sở dữ liệu và kiểm tra thắng/thua
        
        # Hiện tại chỉ giả lập và trả về trạng thái game mới
        game_state = get_game_state(game_id)
        
        # Thêm nước đi mới vào danh sách
        new_move = {
            "position_x": row,
            "position_y": col,
            "player_type": game_state.get("current_turn", "X")
        }
        
        game_state["moves"].append(new_move)
        
        # Đổi lượt chơi
        game_state["current_turn"] = "O" if game_state["current_turn"] == "X" else "X"
        
        return game_state
    except Exception as e:
        frappe.log_error(f"Error making move: {str(e)}")
        return {"error": "Đã xảy ra lỗi khi thực hiện nước đi."}

@frappe.whitelist()
def surrender_game(game_id):
    """Đầu hàng trong trò chơi"""
    if not frappe.session.user or frappe.session.user == 'Guest':
        return {"error": "Bạn cần đăng nhập để thực hiện thao tác này."}
    
    # Trong thực tế, sẽ cập nhật trạng thái game trong cơ sở dữ liệu
    # Hiện tại chỉ trả về thông báo
    return {
        "message": "Bạn đã đầu hàng!",
        "game_over": True
    }

@frappe.whitelist()
def propose_draw(game_id):
    """Đề xuất hòa trận"""
    if not frappe.session.user or frappe.session.user == 'Guest':
        return {"error": "Bạn cần đăng nhập để thực hiện thao tác này."}
    
    # Trong thực tế, sẽ gửi thông báo đến đối thủ và chờ phản hồi
    # Hiện tại chỉ trả về thông báo
    return {
        "message": "Đã gửi đề nghị hòa. Đang chờ phản hồi từ đối thủ..."
    }