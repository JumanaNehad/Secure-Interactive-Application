from src import flow_stat
from src import database
import os
import win32api
from termcolor import colored


## Flow stores the packets in a particular flow.
class Flow:
    def _init_(self, src_ip, dest_ip):
        self.source_ip = src_ip
        self.destination_ip = dest_ip
        self.packets = list()

    ## Adds corresponding packets of the flow.
    def add_packet(self, packet):
        self.packets.append(packet)

    ## Generates statistics of the flow.
    def get_stat(self):
        stat = flow_stat.FlowStat(self.source_ip, self.destination_ip)
        ai_predict = False
        
        for packet in self.packets:
            stat.add_source_port(packet.source_port)
            stat.add_destination_port(packet.destination_port)
            
            

            
            ##Create cusrsor and innitiate connection to database
            conn, cur = database.connectdb()
            cur.execute('SELECT * FROM white WHERE ip = %s', (packet.source_ip,) )
            w_ex = cur.fetchall()
            
            ##print(w_ex)
            w_count=0
            for x in w_ex:
                w_count = w_count + 1 
                
           

            cur.execute('SELECT * FROM black WHERE ip = %s', (packet.source_ip ,))
            b_ex = cur.fetchall()
            ##print(b_ex)
            b_count=0
            for x in b_ex:
                b_count = b_count + 1 
                
            
            print(w_count , b_count)
            if(0<w_count):
                ##os.system('color 3')
                print(colored(f' {w_count}  White  {packet.source_ip}' , 'green') )
                
            elif(0<b_count):
                ##os.system('color 4')
                print(colored(f'{b_count}  Bad  {packet.source_ip} ' , 'red'))
                
            else:
                if (ai_predict == False):
                    sql = "INSERT INTO white (ip) VALUES (%s)"
                    val = (packet.source_ip ,)
                    cur.execute(sql, val)

                    conn.commit()

                    print(cur.rowcount, "record inserted.")
                ##os.system('color 2')
                print(colored(f'Unknown  {packet.source_ip}','yellow' ) )

                
            
            stat.add_protocol(packet.protocol)
            if self.source_ip == packet.source_ip:
                stat.increase_sent_bytes(packet.size)
                stat.increase_header_bytes(packet.header_size)
            else:
                stat.increase_received_bytes(packet.size)

        stat.set_duration(self.packets[-1].sniff_time - self.packets[0].sniff_time)
        cur.close()
        conn.close()
        
        return stat
