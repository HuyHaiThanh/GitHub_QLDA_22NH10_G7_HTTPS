import frappe
import random
import string
from frappe.model.document import Document

class Game(Document):
    def before_save(self):
        # Generate room_code if not provided
        if not self.room_code:
            self.room_code = self.generate_room_code()
            
    def generate_room_code(self):
        """Generate a random 6-character room code"""
        chars = string.ascii_uppercase + string.digits
        room_code = ''.join(random.choice(chars) for _ in range(6))
        
        # Check if code already exists
        if frappe.db.exists("Game", {"room_code": room_code}):
            return self.generate_room_code()  # Try again with a new code
        
        return room_code
        
    def is_player_turn(self, player_id):
        """Check if it's the given player's turn"""
        # Get last move
        last_move = frappe.get_all(
            "Move",
            filters={"game_id": self.name},
            fields=["player_id"],
            order_by="move_order desc",
            limit=1
        )
        
        if not last_move:
            # First move, player1 starts
            return player_id == self.player1_id
        
        # Alternate turns
        return player_id != last_move[0].player_id
        
    def check_winner(self):
        """Check if there's a winner"""
        # This would contain logic to check for winning patterns
        # For simplicity, this is left as a placeholder for now
        pass