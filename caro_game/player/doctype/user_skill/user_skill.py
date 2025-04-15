import frappe
from frappe.model.document import Document

class UserSkill(Document):
    def validate(self):
        # Ensure uniqueness of player_id and skill_id combination
        if self.is_new():
            exists = frappe.db.exists(
                "User Skill",
                {
                    "player_id": self.player_id,
                    "skill_id": self.skill_id
                }
            )
            if exists:
                frappe.throw("This player already has this skill")
                
    def toggle_active(self):
        """Toggle the active state of the skill"""
        self.is_active = not self.is_active
        self.save()