import frappe
from frappe.model.document import Document
import hashlib

class CaroPlayer(Document):
    def validate(self):
        # Hash password if it has been set or changed
        if self.is_new() or self.has_value_changed('password'):
            self.password = self.hash_password(self.password)
        
        # Validate email format
        if not self.is_valid_email(self.email):
            frappe.throw("Please enter a valid email address")
    
    def hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def is_valid_email(self, email):
        """Simple email validation"""
        return '@' in email and '.' in email.split('@')[1]
    
    def check_password(self, password):
        """Check if password matches"""
        return self.password == self.hash_password(password)