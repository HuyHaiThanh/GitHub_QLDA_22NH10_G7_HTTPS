import frappe
import os
import json
from frappe.desk.doctype.workspace.workspace import Workspace
from frappe.desk.doctype.module_def.module_def import ModuleDef

def after_install():
    """Thực hiện các nhiệm vụ sau khi cài đặt app"""
    create_modules()
    import_workspaces()
    print("Caro Game installation completed successfully!")

def create_modules():
    """Tạo các Module Def nếu chưa tồn tại"""
    modules = ["Game", "Game_Core", "Authentication", "Player", "Analytics", "UI", "AI"]
    for module_name in modules:
        if not frappe.db.exists("Module Def", module_name):
            module = frappe.new_doc("Module Def")
            module.module_name = module_name
            module.app_name = "caro_game"
            module.save()
            print(f"Created Module Def: {module_name}")

def import_workspaces():
    """Import các workspace từ thư mục workspace"""
    app_path = frappe.get_app_path("caro_game")
    workspace_path = os.path.join(app_path, "workspace")
    
    # Kiểm tra xem thư mục workspace có tồn tại không
    if not os.path.exists(workspace_path):
        print("Workspace directory not found")
        return
    
    # Import tất cả các file workspace JSON
    for filename in os.listdir(workspace_path):
        if filename.endswith(".json"):
            file_path = os.path.join(workspace_path, filename)
            
            try:
                with open(file_path, "r") as f:
                    workspace_data = json.load(f)
                
                # Kiểm tra nếu workspace đã tồn tại
                workspace_name = workspace_data.get("name")
                if frappe.db.exists("Workspace", workspace_name):
                    print(f"Workspace {workspace_name} already exists")
                    continue
                
                # Tạo workspace mới
                workspace = frappe.new_doc("Workspace")
                
                # Cập nhật các trường từ file JSON
                for key, value in workspace_data.items():
                    if hasattr(workspace, key):
                        workspace.set(key, value)
                
                workspace.save()
                print(f"Imported workspace: {workspace_name}")
            
            except Exception as e:
                print(f"Error importing workspace {filename}: {e}")