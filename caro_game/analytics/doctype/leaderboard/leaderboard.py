import frappe
from frappe.model.document import Document

class Leaderboard(Document):
    def validate(self):
        # Calculate win rate
        if self.total_games > 0:
            self.win_rate = (self.wins / self.total_games) * 100
        else:
            self.win_rate = 0
    
    @staticmethod
    def update_leaderboard(player_id, is_winner):
        """Update player's stats in leaderboard"""
        leaderboard = frappe.get_all(
            "Leaderboard", 
            filters={"user_id": player_id},
            limit=1
        )
        
        if leaderboard:
            doc = frappe.get_doc("Leaderboard", leaderboard[0].name)
        else:
            # Create new entry if not exists
            doc = frappe.new_doc("Leaderboard")
            doc.user_id = player_id
            doc.total_games = 0
            doc.wins = 0
            doc.losses = 0
            
        # Update stats
        doc.total_games += 1
        if is_winner:
            doc.wins += 1
        else:
            doc.losses += 1
            
        doc.last_updated = frappe.utils.now()
        doc.save()