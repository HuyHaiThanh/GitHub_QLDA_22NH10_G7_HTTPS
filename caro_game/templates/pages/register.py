import frappe

def get_context(context):
    """Chuẩn bị context cho trang đăng ký"""
    
    context.title = "Đăng ký tài khoản Caro Game"
    
    # Nếu người dùng đã đăng nhập, chuyển hướng đến trang game
    if frappe.session.user and frappe.session.user != 'Guest':
        frappe.local.flags.redirect_location = "/game"
        raise frappe.Redirect
    
    return context