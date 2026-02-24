# from typing import List
from collections import defaultdict

chat_history:dict = defaultdict(list)

class Memory:
    def __init__(self, session_id):
        self.session_id = session_id
    
    def get_memory(self):
        return chat_history[self.session_id]
    
    def add_to_memory(self, msg):
        chat_history[self.session_id].append(msg)
