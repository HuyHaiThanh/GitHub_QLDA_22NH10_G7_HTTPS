import frappe
from frappe.model.document import Document

class Move(Document):
    def before_save(self):
        if not self.move_order:
            # Auto-increment move_order for this game
            last_move = frappe.get_all(
                "Move",
                filters={"game_id": self.game_id},
                fields=["move_order"],
                order_by="move_order desc",
                limit=1
            )
            
            if last_move:
                self.move_order = last_move[0].move_order + 1
            else:
                self.move_order = 1
    
    def validate(self):
        # Check if position is valid (not occupied)
        existing_move = frappe.get_all(
            "Move",
            filters={
                "game_id": self.game_id,
                "position_x": self.position_x,
                "position_y": self.position_y
            },
            limit=1
        )
        
        if existing_move:
            frappe.throw(f"Position ({self.position_x}, {self.position_y}) is already occupied")
        
        # Check if it's player's turn
        game = frappe.get_doc("Game", self.game_id)
        if not game.is_player_turn(self.player_id):
            frappe.throw("It's not your turn")
        
        # Update game status after move
        self.update_game_status(game)
    
    def update_game_status(self, game):
        # Check if this move results in a win
        # This is a placeholder for the winning logic
        winner = self.check_for_winner(game)
        
        if winner:
            game.status = "Completed"
            game.winner_id = winner
            game.save()
    
    def check_for_winner(self, game):
        """Check if the current move results in a win"""
        # This would contain the logic to check for 5 in a row
        # For now, this is a placeholder
        return None