import frappe

no_cache = True
no_sitemap = True

def get_context(context):
    context.title = "Caro Game - Trang chủ"
    
    # Tạm thời vô hiệu hóa chuyển hướng tự động để debug
    # if frappe.session.user and frappe.session.user != 'Guest':
    #     frappe.local.flags.redirect_location = "/game"
    #     raise frappe.Redirect
    
    # Đặt các biến context cho giao diện
    context.description = "Trò chơi cờ caro trực tuyến"
    context.logo = "/assets/caro_game/images/logo.svg"
    
    # Đối với người dùng chưa đăng nhập, hiển thị form đăng nhập
    context.show_login_form = True
    
    return context