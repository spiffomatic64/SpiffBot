#! python2


class auth:
    def __init__(self):
        self.admins = []
        self.add_admin(get_streamer())
        
    def is_admin(self,user):
        if user in self.admins:
            return True
        else:
            return False
        
    def add_admin(self,user):
        self.admins.append(user)
       
    def get_admins(self):
        return self.admins
        
def get_streamer():
    return "spiffomatic64"

def get_streamer_short():
    return "spiff"

def get_twitter():
    return "spiffomatic64"

def get_multi():
    return "itabob"
    
def get_oauth():
    return "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

def get_bot():
    return "spiffbot"

def get_db_user():
    return "spiffo_twitch"
    
def get_db_pass():
    return "xxxxxxxxxxxxxxxxxxxx"