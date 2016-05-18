import mysql.connector
import datetime
import twitch_bot_utils

class twitchdb:

    def __init__(self,u,p,h,d):
        try:
          self.cnx = mysql.connector.connect(user=u,password=p,host=h,database=d)
          logging.log(logging.DEBUG,"Connected to DB!")
        except mysql.connector.Error as err:
            logging.log(logging.ERROR,err)
            

    def updateUserPoints(self,username,points):
        try: 
            int(points)
        except ValueError:
            return False
        query = ("INSERT INTO users (username,points) VALUES (%s,%s) ON DUPLICATE KEY UPDATE points=%s;")
        cursor = self.cnx.cursor(buffered=True)
        cursor.execute(query, (username,points,points))
        self.cnx.commit()

    def updateUserOpted(self,username,opted):
        try: 
            int(opted)
        except ValueError:
            return False
        query = ("INSERT INTO users (username,opted) VALUES (%s,%s) ON DUPLICATE KEY UPDATE opted=%s;")
        cursor = self.cnx.cursor(buffered=True)
        cursor.execute(query, (username,opted,opted))
        self.cnx.commit()
        
    def getUserOpted(self,username):
        query = ("SELECT opted FROM users WHERE username = %s")
        cursor = self.cnx.cursor(buffered=True)
        cursor.execute(query, ([username]))
        result = cursor.fetchone()
        if result != None:
            if result[0]==1:
                return True
        return False
        
    def getOptedUsers(self):
        query = ("SELECT username FROM users WHERE opted = 1")
        cursor = self.cnx.cursor(buffered=True)
        cursor.execute(query, ([]))
        results = []
        for id in cursor:
            results.append(id[0])
        if len(results)>0:
            return results
        else:
            return False
            
    def updateUserSession(self,username,session):
        try: 
            int(session)
        except ValueError:
            return False
        query = ("INSERT INTO users (username,session) VALUES (%s,%s) ON DUPLICATE KEY UPDATE session=%s;")
        cursor = self.cnx.cursor(buffered=True)
        cursor.execute(query, (username,session,session))
        self.cnx.commit()
        
    def updateUserWatched(self,username,watched):
        try: 
            int(watched)
        except ValueError:
            return False
        query = ("INSERT INTO users (username,watched) VALUES (%s,%s) ON DUPLICATE KEY UPDATE watched=%s;")
        cursor = self.cnx.cursor(buffered=True)
        cursor.execute(query, (username,watched,watched))
        self.cnx.commit()

    def updateUserreferral(self,username,referral): 
        query = ("INSERT INTO users (username,referral) VALUES (%s,%s) ON DUPLICATE KEY UPDATE referral=%s;")
        cursor = self.cnx.cursor(buffered=True)
        cursor.execute(query, (username,referral,referral))
        self.cnx.commit()
        
    def updateLastControl(self,username): 
        query = ("INSERT INTO users (username,last_control) VALUES (%s,%s) ON DUPLICATE KEY UPDATE last_control=%s;")
        cursor = self.cnx.cursor(buffered=True)
        #YYYY-MM-DD HH:MM:SS
        last_control = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(query, (username,last_control,last_control))
        self.cnx.commit()
        
    def getLastControl(self,username): 
        query = "SELECT * FROM users WHERE opted = 1 AND username IN ( %s ) ORDER BY last_control ASC LIMIT 1"

        cursor = self.cnx.cursor(buffered=True)

        if type(username) is str:   
            cursor.execute(query, ([username]))
        else:
            in_p = ", ".join(map(lambda x: "%s", username))
            query = query % in_p
            cursor.execute(query, (username))
        result = cursor.fetchone()
        if result != None:
            return result[0]
        return False
        
    def updateLastSeen(self,username): 
        query = ("INSERT INTO users (username,last_seen) VALUES (%s,%s) ON DUPLICATE KEY UPDATE last_seen=%s;")
        cursor = self.cnx.cursor(buffered=True)
        #YYYY-MM-DD HH:MM:SS
        last_seen = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(query, (username,last_seen,last_seen))
        self.cnx.commit()
            
    def getUsers(self):
        query = ("SELECT * FROM users")
        cursor = self.cnx.cursor(buffered=True)
        cursor.execute(query, ([]))
        results = []
        for id in cursor:
            results.append(id[0])
        if len(results)>0:
            return results
        else:
            return False