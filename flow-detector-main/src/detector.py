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

import os, statistics, time, re
import database
import globalflags
from nicegui import ui

class Detector:
    def _init_(self):
        
        #previous_connections is an empty list that will store the number of connections to the server in the previous cycles of the while loop;
        self.previous_connections = []
         #boolean value
        self.block_attacker = True
        #an instance of the Database class defined in the database module, which will be used to insert IP addresses into black and white lists
        self.database = database.Database()

    def start(self):
        while True and globalflags.stop_flag == False:
            #this function will run indefinitely as long as global flag which stops the detector is false 
            
            #os.popen runs a command to get the number of connections to port 80 of the server and the result will be a string
            result = os.popen("netstat -an | FindStr /R /C:\":80 \" | find /C /V \"\"").readline()
            #connection coverts this string into an integer
            connections = int(result.strip())
            #connections value is added to the end of the previous_connections list
            self.previous_connections.append(connections)

            #This checks if there are at least three values in the previous_connections list.
            # If there are, it calculates the mean and standard deviation of the values in the list using the statistics module.
            if len(self.previous_connections) >= 3:
                mean = statistics.mean(self.previous_connections)
                stddev = statistics.stdev(self.previous_connections)
                
                
# Check:  1. the number of connections is greater than 15 
#         2. if the number of connections is greater than (mean + standard deviation)
#         3. if the globalflag. predictddos is true
#If these 3 conditions are true: 
#                 this means that a potential ddos attack is detected and the program uses os.popen 
#                 function to execute a shell command that lists all the network connections on port 80.

                if connections > 15 and connections > (mean + stddev) and globalflags.predictddos == True:
                    attacker = None
                    # The output is read line by line and for each line attacker ip address is extracted using regular expression.
                    # os.popen():function that runs a command in a command shell and returns a file object that can be used to read the output of the command
                    # netstat -an: This command retrieves a list of all active network connections and their current status.
                    # |: This is a pipe symbol that takes the output of the previous command and passes it as input to the next command.
                    # FindStr /R /C:\":80 \: This command searches the output of the previous command for connections that are using port 80
                    with os.popen("netstat -an | FindStr /R /C:\":80 \"") as result:
                        for line in result:
                        # \d{1,3} matches one to three digits (0-9)
                        # \. matches a literal period character 
                        # The previous two parts (\d{1,3}\.) are repeated three times to match the first three octets of the IP address.
                        # \d{1,3} is used again to match the final octet.
                        # The entire pattern is wrapped creating a capturing group that allows us to extract the matched IP address
                            match = re.search(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', line)
                            if match:
                                #findall method is used because there may be multiple IP addresses in the given line,
                                # and we want to capture them all
                                matchsrc = re.findall(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', line)
                                # assigns the second IP address (assuming there are at least two in the list) to the variable attacker. 
                                # This is because the first IP address in the list is likely to be the local IP address of the machine running the script, 
                                # while the second IP address is more likely to be the IP address of the remote attacker
                                attacker = matchsrc[1]
                                print('attack attacker: ' + attacker)
                                print(globalflags.blockedsign)
                                #checks if the attacker is not already in blacklist
                        if not self.database.blacklisthas(attacker):
                            # When a new attacker is identified they are added to the 
                            # blacklist by calling insert to blacklist method from database class. 
                            self.database.insert_to_black_list(attacker)
                            # A message is printed to the console indicating that a potential ddos attack is detected.
                            print('Potential DDoS Attack [c=' + format(connections) + '] [attacker=' + attacker + ']')
                            #global variable added manually in globalflags.py
                            print(globalflags.attacksign)
                        else:
                            print(globalflags.blockedsign)
                            

                    self.previous_connections = []
                else:
                    attacker = None
                    with os.popen("netstat -an | FindStr /R /C:\":80 \"") as result:
                        for line in result:
                            match = re.search(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', line)
                            if match:
                                matchsrc = re.findall(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', line)
                                ip = matchsrc[1]
                        self.database.insert_to_white_list(ip)

                    print(connections ,    attacker)
                    self.previous_connections.pop(0)
            else:
                #this is used when there are no established connections on port 80 
                # so it uses os.popen to receive a list of all active TCP connections on port 80 
                attacker = None
                with os.popen("netstat -an | FindStr /R /C:\":80 \"") as result:
                    for line in result:
                        #it then uses a regular expression to search for the IP address of the attacker 
                        #in each of the connections that are returned,
                        #and assigns the first matching IP address to the attacker variable
                        match = re.search(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', line)
                        if match:
                            matchsrc = re.findall(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', line)
                            attacker = matchsrc[1]

                print(connections ,  attacker)
                #program sleeps for 5 seconds before checking for new connections again
                #This is done to avoid excessive resource consumption and to reduce the load on the system.
            time.sleep(5)
