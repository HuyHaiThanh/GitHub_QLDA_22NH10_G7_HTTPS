import frappe
from frappe.model.document import Document

class Skin(Document):
    def validate(self):
        # Add validation logic here if needed
        pass
    
    def purchase_skin(self, user_id):
        """Logic to purchase this skin for a user"""
        # Check if user already has this skin
        existing_skin = frappe.get_all(
            "User Skin",
            filters={
                "player_id": user_id,
                "skin_id": self.name
            },
            limit=1
        )
        
        if existing_skin:
            frappe.throw(f"You already own the {self.name1} skin")
            
        # Add skin to user's collection
        user_skin = frappe.new_doc("User Skin")
        user_skin.player_id = user_id
        user_skin.skin_id = self.name
        user_skin.is_active = 0  # Inactive by default
        user_skin.unlocked_at = frappe.utils.now()
        user_skin.save()