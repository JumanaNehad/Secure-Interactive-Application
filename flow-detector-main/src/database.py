# MMMMMMMM               MMMMMMMMIIIIIIIIIUUUUUUUU     UUUUUUU
# M:::::::M             M:::::::MI::::::::IU::::::U     U::::::U
# M::::::::M           M::::::::MI::::::::IU::::::U     U::::::U
# M:::::::::M         M:::::::::MII::::::IIUU:::::U     U:::::UU
# M::::::::::M       M::::::::::M  I::::I   U:::::U     U:::::U 
# M:::::::::::M     M:::::::::::M  I::::I   U:::::D     D:::::U 
# M:::::::M::::M   M::::M:::::::M  I::::I   U:::::D     D:::::U 
# M::::::M M::::M M::::M M::::::M  I::::I   U:::::D     D:::::U 
# M::::::M  M::::M::::M  M::::::M  I::::I   U:::::D     D:::::U 
# M::::::M   M:::::::M   M::::::M  I::::I   U:::::D     D:::::U 
# M::::::M    M:::::M    M::::::M  I::::I   U:::::D     D:::::U 
# M::::::M     MMMMM     M::::::MII::::::IINU:::::UUUUUU:::::U 
# M::::::M               M::::::MI::::::::IU:::::::::::::::UU  
# M::::::M               M::::::MI::::::::IU:::::::::::::::UU  
# M::::::M               M::::::MIIIIIIIIIUUUUUUUUUUUUUUUUUUUU  

import subprocess
import mysql.connector



class Database:
    def __init__(self):
        #creating database connection
        self.conn = mysql.connector.connect(user='root', password='', host='localhost', database='sia')
        #creating cursor to execute queries 
        self.cur = self.conn.cursor()

    
    def connectdb(self):
    
        return self.conn,self. cur


    
    def fetch_white_list(self):
        self.cur.execute('SELECT * FROM white')
        w_ex = self.cur.fetchall()
        #data is the list of all the dictionaries
        data = []
        #getting only the row headers from the table
        row_headers = [x[0] for x in self.cur.description]  
        for row in w_ex:
             #zip function is used to pair up each element of row_headers with each element of row 
             #and the dict constructor to create a dictionary from each pair.
            data.append(dict(zip(row_headers, row)))
        gdata = data
        return data

    def fetch_black_list(self):
        self.cur.execute('SELECT * FROM black')
        b_ex = self.cur.fetchall()
        data = []
        row_headers = [x[0] for x in self.cur.description] 
        for row in b_ex:
            data.append(dict(zip(row_headers, row)))
        gdatab = data
        return data

    def blacklisthas(self, ip):
        self.cur.execute('SELECT * FROM black WHERE ip = %s', (ip,))
        b_ex = self.cur.fetchall()
        ##print(b_ex)
        b_count = 0
        for x in b_ex:
            #checks if a given IP address exists in the black table
            b_count = b_count + 1
        #it returns a boolean, if b_count=1 then it exist in black list 
        return b_count > 0

    def whitelisthas(self, ip):
        self.cur.execute('SELECT * FROM white WHERE ip = %s', (ip,))
        b_ex = self.cur.fetchall()

        b_count = 0
        for x in b_ex:
            b_count = b_count + 1
        return b_count > 0

    def insert_to_black_list(self, ip):
        if self.whitelisthas(ip):
            #if this ip address exist in white list it deletes it
            self.delete_white_list(ip)


        if self.blacklisthas(ip):
            #if it exist in black list then it it returns without doing anything
            return
        #if it doesnt exist then add it to the blacklist
        sql = "INSERT INTO black (ip) VALUES (%s)"
        val = (ip,)
        self.cur.execute(sql, val)
        self.conn.commit()
        print(self.cur.rowcount, "record inserted.")
        #subprcess: function that is used to execute external programs or commands from within Python. 
        #add rule: the rule to be added to firewall
        #name: name of rule to be added 
        #dir: "in", meaning incoming traffic to the system.
        #action: The action to be taken when the rule is matched
        #remoteip: ip address to be blocked
        subprocess.call(f'netsh advfirewall firewall add rule name="Block IP {ip}" dir=in action=block remoteip={ip}')

    def insert_to_white_list(self, ip):
        #if this ip already exist in blacklist then it will immediately return 
        if self.blacklisthas(ip):
            return
        if not self.whitelisthas(ip):
            #if it doesnt exist in white list then insert it 
            sql = "INSERT INTO white (ip) VALUES (%s)"
            val = (ip,)
            self.cur.execute(sql, val)
            self.conn.commit()
            print(self.cur.rowcount, "record inserted.")

    def delete_white_list(self, ip):
        sql = "DELETE FROM white WHERE ip = %s" 
        val = (ip,)
        self.cur.execute(sql, val)
        self.conn.commit()
        print(self.cur.rowcount, "record deleted.")
        


    def delete_black_list(self, ip):
        sql = "DELETE FROM black WHERE ip = %s"  
        val = (ip,)
        self.cur.execute(sql, val)
        self.conn.commit()
        print(self.cur.rowcount, "record deleted.")
        #delete rule: the rule to be deleted from firewall 
        subprocess.call(f'netsh advfirewall firewall delete rule name="Block IP {ip}')
    
    async def delete_all(self):
        #removes all the ip adresses from both the whitelist and the blacklist
        sql = "TRUNCATE TABLE black; TRUNCATE TABLE white;" 
        
        self.cur.execute(sql)
        self.conn.commit()
   

