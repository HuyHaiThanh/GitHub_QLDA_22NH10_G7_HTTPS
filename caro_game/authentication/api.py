import frappe
from frappe import _
from frappe.utils import validate_email_address
import re

@frappe.whitelist(allow_guest=True)
def register_user(username, email, password):
    """
    API để đăng ký người dùng mới cho trò chơi Caro
    """
    # Kiểm tra dữ liệu đầu vào
    if not username or not email or not password:
        return {"success": False, "error": "Vui lòng điền đầy đủ thông tin!"}
    
    # Kiểm tra định dạng email
    if not validate_email_address(email):
        return {"success": False, "error": "Email không hợp lệ!"}
    
    # Kiểm tra độ dài mật khẩu
    if len(password) < 6:
        return {"success": False, "error": "Mật khẩu phải có ít nhất 6 ký tự!"}
    
    # Kiểm tra tên người dùng
    if not re.match("^[a-zA-Z0-9_]+$", username):
        return {"success": False, "error": "Tên người dùng chỉ được chứa chữ cái, số và dấu gạch dưới!"}
    
    # Kiểm tra email đã tồn tại chưa
    if frappe.db.exists("User", {"email": email}):
        return {"success": False, "error": "Email đã được sử dụng. Vui lòng chọn email khác!"}
    
    try:
        # Tạo người dùng mới trong Frappe
        user = frappe.get_doc({
            "doctype": "User",
            "email": email,
            "first_name": username,
            "send_welcome_email": 0,
            "new_password": password,
            "user_type": "Website User"
        })
        user.insert(ignore_permissions=True)
        
        # Tạo hồ sơ người chơi Caro (Caro_Player) liên kết với người dùng mới
        if not frappe.db.exists("Caro_Player", {"user": email}):
            caro_player = frappe.get_doc({
                "doctype": "Caro_Player",
                "username": username,
                "user": email,
                "experience": 0,
                "level": 1
            })
            caro_player.insert(ignore_permissions=True)
        
        frappe.db.commit()
        
        return {
            "success": True,
            "message": f"Người dùng {username} đã được đăng ký thành công!"
        }
    
    except Exception as e:
        frappe.db.rollback()
        frappe.log_error(f"Lỗi khi đăng ký người dùng: {str(e)}")
        return {"success": False, "error": str(e)}