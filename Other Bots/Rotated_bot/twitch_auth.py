admins = []


class auth:
    def __init__(self):
        admins = []
        self.add_admin(self.get_streamer())
        self.add_admin("spiffomatic64")
    
    def get_streamer(self):
        return "rotatedlife"
        
    def get_oauth(self):
        return "xxxxxxxxxxxxxxxxxxxxx"
        
    def get_bot(self):
        return "rotated_bot"
        
    def is_admin(self,user):
        if user in admins:
            return True
        else:
            return False
        
    def add_admin(self,user):
        admins.append(user)
       
    def get_admins(self):
        return admins