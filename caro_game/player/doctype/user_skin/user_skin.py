import frappe
from frappe.model.document import Document

class UserSkin(Document):
    def validate(self):
        # Ensure uniqueness of player_id and skin_id combination
        if self.is_new():
            exists = frappe.db.exists(
                "User Skin",
                {
                    "player_id": self.player_id,
                    "skin_id": self.skin_id
                }
            )
            if exists:
                frappe.throw("This player already has this skin")
        
        # If this skin is being set as active, deactivate all other skins for this player
        if self.is_active:
            active_skins = frappe.get_all(
                "User Skin",
                filters={
                    "player_id": self.player_id,
                    "is_active": 1,
                    "name": ["!=", self.name]
                }
            )
            
            for skin in active_skins:
                doc = frappe.get_doc("User Skin", skin.name)
                doc.is_active = 0
                doc.save()
    
    def set_as_active(self):
        """Set this skin as the active skin for the player"""
        self.is_active = 1
        self.save()