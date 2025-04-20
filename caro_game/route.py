import frappe

def get_page_context(route):
    """
    Hàm này giúp xác định context cho một trang web cụ thể dựa trên route
    Bỏ qua xử lý route chính '/' để cho phép trang chủ mặc định (index.html) hoạt động
    """
    # Xử lý đặc biệt cho route gốc '/'
    if route == '/':
        # Nếu người dùng chưa đăng nhập, chuyển đến trang login
        if not frappe.session.user or frappe.session.user == 'Guest':
            frappe.local.flags.redirect_location = "/login"
            raise frappe.Redirect
        # Nếu đã đăng nhập, chuyển đến trang game
        frappe.local.flags.redirect_location = "/game"
        raise frappe.Redirect
        
    return None