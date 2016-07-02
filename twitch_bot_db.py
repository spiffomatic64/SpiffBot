#TODO: make abstract getter and setter for single objects

import mysql.connector
import datetime
import logging

class twitchdb:

    # Table users
    # username, points, opted, last_control, last_seen
    def __init__(self,u,p,h,d):
        # type: (object, object, object, object) -> object
        try:
          self.cnx = mysql.connector.connect(user=u,password=p,host=h,database=d)
          logging.log(logging.DEBUG,"Connected to DB!")
        except mysql.connector.Error as err:
            logging.log(logging.ERROR,err)

    def checkConnection(self):
        if not self.cnx.is_connected():
            try:
                logging.log(logging.ERROR, "RECONNECTING!")
                self.cnx.reconnect(2,1)
            except mysql.connector.Error as e:
                print "Error code:", e.errno  # error number
                print "SQLSTATE value:", e.sqlstate  # SQLSTATE value
                print "Error message:", e.msg  # error message
                print "Error:", e  # errno, sqlstate, msg values
                s = str(e)
                print "Error:", s  # errno, sqlstate, msg values

    def updateUserOpted(self,username,opted):
        self.checkConnection()
        try: 
            opted = int(opted)
            username = str(username)
        except TypeError:
            logging.log(logging.ERROR,"%s is not an integer!" % opted)
            return False
            
        query = ("INSERT INTO users (username,opted) VALUES (%s,%s) ON DUPLICATE KEY UPDATE opted=%s;")
        try:
            cursor = self.cnx.cursor(buffered=True)
            cursor.execute(query, (username,opted,opted))
            self.cnx.commit()
            return True
        except mysql.connector.Error as err:
            logging.log(logging.ERROR,err)
            
    def getUserOpted(self,username):
        self.checkConnection()
        query = ("SELECT opted FROM users WHERE username = %s")
        try:
            cursor = self.cnx.cursor(buffered=True)
            cursor.execute(query, ([username]))
            result = cursor.fetchone()
            if result != None:
                if result[0]==1:
                    return True
            else:
                logging.log(logging.DEBUG,"%s is not in db!" % username)
        except mysql.connector.Error as err:
            logging.log(logging.ERROR,err)
        return False
        
    def getOptedUsers(self):
        self.checkConnection()
        query = ("SELECT username FROM users WHERE opted = 1")
        try:
            cursor = self.cnx.cursor(buffered=True)
            cursor.execute(query, ([]))
            results = []
            for id in cursor:
                results.append(id[0])
                
            if len(results)>0:
                return results
            else:
                return False
        except mysql.connector.Error as err:
            logging.log(logging.ERROR,err)
            return False
            
    def updateLastSeen(self,username):
        self.checkConnection()
        query = ("INSERT INTO users (username,last_seen) VALUES (%s,%s) ON DUPLICATE KEY UPDATE last_seen=%s;")
        
        try:
            cursor = self.cnx.cursor(buffered=True)
            #YYYY-MM-DD HH:MM:SS
            last_seen = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute(query, (username,last_seen,last_seen))
            self.cnx.commit()
            return True
        except mysql.connector.Error as err:
            logging.log(logging.ERROR,err)
            return False

    def getLastSeen(self, username):
        self.checkConnection()
        query = ("SELECT last_seen FROM users WHERE username=%s;")

        try:
            cursor = self.cnx.cursor(buffered=True)
            cursor.execute(query, ([username]))
            result = cursor.fetchone()
            if result != None:
                return result[0]
            else:
                logging.log(logging.DEBUG, "%s is not in db!" % username)
        except mysql.connector.Error as err:
            logging.log(logging.ERROR, err)
        return False

    def getUser(self, username):

        self.checkConnection()
        query = ("SELECT session FROM users WHERE username=%s;")

        try:
            cursor = self.cnx.cursor(buffered=True)
            cursor.execute(query, ([username]))
            result = cursor.fetchone()
            if result != None:
                return result[0]
            else:
                logging.log(logging.DEBUG, "%s is not in db!" % username)
        except mysql.connector.Error as err:
            logging.log(logging.ERROR, err)
        return False
            
    def getUsers(self):
        self.checkConnection()
        query = ("SELECT * FROM users")
        
        try:
            cursor = self.cnx.cursor(buffered=True)
            cursor.execute(query, ([]))
            results = []
            for id in cursor:
                results.append(id[0])
            if len(results)>0:
                return results
            else:
                return False
        except mysql.connector.Error as err:
            logging.log(logging.ERROR,err)
            return False

    def updateIntro(self, username, intro):
        self.checkConnection()
        query = ("INSERT INTO users (username,intro) VALUES (%s,%s) ON DUPLICATE KEY UPDATE intro=%s;")

        try:
            cursor = self.cnx.cursor(buffered=True)
            #Sanitize intro variable regex [0-9a-zA-Z]
            cursor.execute(query, (username, intro, intro))
            self.cnx.commit()
            return True
        except mysql.connector.Error as err:
            logging.log(logging.ERROR, err)
            return False

    def getIntro(self, username):
        self.checkConnection()
        query = "SELECT intro FROM users WHERE username = %s LIMIT 1"

        try:
            cursor = self.cnx.cursor(buffered=True)

            if type(username) is str:
                cursor.execute(query, ([username]))
            else:
                in_p = ", ".join(map(lambda x: "%s", username))
                query %= in_p
                cursor.execute(query, (username))
            result = cursor.fetchone()
            if result != None:
                return result[0]
            return False
        except mysql.connector.Error as err:
            logging.log(logging.ERROR, err)
            return False

    def updateStreamId(self, username, streamid):
        try:
            streamid = int(streamid)
        except TypeError:
            logging.log(logging.ERROR, "%s is not an integer!" % streamid)
            return False

        self.checkConnection()
        query = ("INSERT INTO users (username,streamid) VALUES (%s,%s) ON DUPLICATE KEY UPDATE streamid=%s;")

        try:
            cursor = self.cnx.cursor(buffered=True)
            cursor.execute(query, (username, streamid, streamid))
            self.cnx.commit()
            return True
        except mysql.connector.Error as err:
            logging.log(logging.ERROR, err)
            return False

    def getStreamId(self, username):

        self.checkConnection()
        query = ("SELECT streamid FROM users WHERE username=%s;")

        try:
            cursor = self.cnx.cursor(buffered=True)
            cursor.execute(query, ([username]))
            result = cursor.fetchone()
            if result != None and len(result)==1 and result[0]!=None:
                return result[0]
            else:
                logging.log(logging.DEBUG, "%s does not have a streamId!" % username)
        except mysql.connector.Error as err:
            logging.log(logging.ERROR, err)
        return False
