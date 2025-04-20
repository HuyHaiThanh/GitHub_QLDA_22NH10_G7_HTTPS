import frappe
from frappe.utils.oauth import get_oauth2_authorize_url, get_oauth_keys
from frappe.utils import get_url, cint
from frappe import _

no_cache = True
no_sitemap = True

def get_context(context):
    """Chuẩn bị context cho trang đăng nhập tùy chỉnh"""
    
    context.title = "Đăng nhập - Caro Game"
    
    # Nếu người dùng đã đăng nhập, chuyển hướng đến trang game
    if frappe.session.user and frappe.session.user != 'Guest':
        frappe.local.flags.redirect_location = "/game"
        raise frappe.Redirect
    
    # Lấy thông báo lỗi (nếu có)
    context.login_error = frappe.request.cookies.get("login_error") or frappe.form_dict.get("login_error")
    frappe.clear_cookie("login_error")
    
    # Thêm xác thực CSRF cho form đăng nhập
    context.csrf_token = frappe.sessions.get_csrf_token()
    
    # Xác định trang chuyển hướng sau khi đăng nhập
    redirect_to = frappe.request.args.get("redirect-to") or "/game"
    context.redirect_to = redirect_to
    
    # Thêm các thông tin khác nếu cần
    context.logo = "/assets/caro_game/images/logo.png"
    context.description = "Chơi cờ caro online với bạn bè và người chơi khác"
    
    return context