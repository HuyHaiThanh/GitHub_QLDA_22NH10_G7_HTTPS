import frappe
import random

@frappe.whitelist()
def get_hint(game_id):
    """Gợi ý nước đi tiếp theo cho người chơi"""
    if not frappe.session.user or frappe.session.user == 'Guest':
        return {"error": "Bạn cần đăng nhập để sử dụng chức năng này."}
    
    try:
        # Lấy trạng thái game hiện tại
        from caro_game.game.api import get_game_state
        game_state = get_game_state(game_id)
        
        if game_state.get("status") != "active":
            return {"error": "Trò chơi đã kết thúc hoặc không tồn tại."}
        
        # Tìm các ô trống trên bàn cờ
        occupied_positions = set()
        for move in game_state.get("moves", []):
            occupied_positions.add((move["position_x"], move["position_y"]))
        
        empty_positions = []
        for i in range(15):
            for j in range(15):
                if (i, j) not in occupied_positions:
                    empty_positions.append((i, j))
        
        # Trong thực tế, đây sẽ là thuật toán AI phức tạp hơn để gợi ý nước đi tốt nhất
        # Hiện tại, chỉ đơn giản trả về một vị trí ngẫu nhiên
        if empty_positions:
            hint_pos = random.choice(empty_positions)
            return {
                "hint": {
                    "row": hint_pos[0],
                    "col": hint_pos[1]
                },
                "message": "Đây là gợi ý nước đi cho bạn."
            }
        else:
            return {"error": "Không có nước đi nào khả dụng."}
    
    except Exception as e:
        frappe.log_error(f"Error generating hint: {str(e)}")
        return {"error": "Đã xảy ra lỗi khi tạo gợi ý."}