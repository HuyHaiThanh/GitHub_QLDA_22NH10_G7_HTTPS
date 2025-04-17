import frappe

def after_install():
    """Setup required after app installation"""
    # Initialize default roles
    setup_custom_roles()
    
def setup_custom_roles():
    """Create custom roles for the caro game"""
    roles = [
        {"role_name": "Caro Player", "desk_access": 1},
        {"role_name": "Game Admin", "desk_access": 1}
    ]
    
    for role in roles:
        if not frappe.db.exists("Role", role["role_name"]):
            role_doc = frappe.new_doc("Role")
            role_doc.update(role)
            role_doc.insert(ignore_permissions=True)