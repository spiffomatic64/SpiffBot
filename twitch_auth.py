#! python2


class auth:
    def __init__(self):
        self.admins = []
        self.add_admin(self.get_streamer())
    
    def get_streamer(self):
        return "spiffomatic64"

    def get_streamer_short(self):
        return "spiff"

    def get_twitter(self):
        return "spiffomatic64"

    def get_multi(self):
        return "itabob"
        
    def get_oauth(self):
        return "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

    def get_bot(self):
        return "spiffbot"

    def get_db_user(self):
        return "spiffbot"
        
    def get_db_pass(self):
        return "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
        
    def is_admin(self,user):
        if user in self.admins:
            return True
        else:
            return False
        
    def add_admin(self,user):
        self.admins.append(user)
       
    def get_admins(self):
        return self.admins