admins = []


class auth:
    def __init__(self):
        admins = []
        self.add_admin(self.get_streamer())
    
    def get_streamer(self):
        return "spiffomatic64"
        
    def get_oauth(self):
        return "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
        
    def get_bot(self):
        return "spiffbot"

    def get_db_user(self):
        return "spiffbot"
        
    def get_db_pass(self):
        return "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
        
    def is_admin(self,user):
        if user in admins:
            return True
        else:
            return False
        
    def add_admin(self,user):
        admins.append(user)
       
    def get_admins(self):
        return admins