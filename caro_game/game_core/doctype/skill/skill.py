import frappe
from frappe.model.document import Document

class Skill(Document):
    def validate(self):
        # Add validation logic here if needed
        pass
        
    def use_skill(self, user_id, game_id):
        """Logic to use this skill in a game"""
        # Check if user has this skill
        user_skill = frappe.get_all(
            "User Skill",
            filters={
                "player_id": user_id,
                "skill_id": self.name,
                "is_active": 1
            },
            limit=1
        )
        
        if not user_skill:
            frappe.throw(f"You don't have the {self.name1} skill activated")
            
        # Implement specific skill logic based on skill name
        if self.name1 == "Remove Mark":
            # Remove opponent's last move logic
            pass
        elif self.name1 == "Double Turn":
            # Allow player to make two moves in a row
            pass
        elif self.name1 == "Block Area":
            # Block a section of the board
            pass
            
        # Record skill usage in the move
        return True