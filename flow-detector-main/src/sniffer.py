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

import asyncio
from threading import Thread
import numpy as np
import scapy.all as scapy 
import datagram
from anyio import Event # represents an event synchronization primitive used for communication between tasks in an asynchronous context.
import database
import globalflags
import detector
from nicegui import ui  #provides a user interface framework for creating interactive graphical interfaces.
import train  #train model 

class Sniffer:
    def __init__(self):
        self.running = True
        self.tasks = [] #A list attribute to store asynchronous tasks. It is initialized as an empty list.
        self.queue = asyncio.Queue() # object used for inter-task communication. It is initialized as an empty queue.
        self.stop_event = Event()  #It is used to signal the stop event for the sniffer.
        self.loop = asyncio.get_event_loop()  # It represents the event loop associated with the current execution context.
        self.db = database.Database() 
        self.detector = detector.Detector()
        self.ddosdetector = train.DdosDetector()
        self.model = self.ddosdetector.load_model()
        
        
    def startdetector(self):
        
        print("Started Detector") #bydkhlo 3alaa el prediction model 
        self.detector.start()
        

    def startsniffer(self): #This method is responsible for starting the packet sniffing process. 
        #. It does not return any value.
        
        scapy.sniff(prn=lambda x:self.process_packet(x))
        # It uses the scapy.sniff function from the scapy.all module to capture packets x deh el captured packet bab4tha kol mara le function process packet
        #lambda function takes a packet x as an argument and calls the process_packet method of the current Sniffer instance (self.process_packet(x)).
        return 
    async def start(self):  # bt start kol hagaa 
        
        globalflags.stop_flag = False   #  This flag is used to control the stoppage of the capture process.
        print("Started Live Capture")
        self.tasks = []
        loop = asyncio.get_running_loop() #leha 3laka bel thread 
        task2 = loop.run_in_executor(None, self.startdetector) #This method is executed in a separate thread to run concurrently with the event loop.
        loop = asyncio.get_running_loop()
#3amlt 2 task 3alaa 2 thread wahed bystart el detector wel tane bystart sniffer
        task1 = loop.run_in_executor(None, self.startsniffer)
        self.tasks.extend([task1,task2])

        await asyncio.gather(*self.tasks)  # It waits for the completion of all tasks using await asyncio.gather(*self.tasks).
        # The await keyword is used to pause the execution of the start method until all tasks in self.tasks are completed. This allows concurrent execution of the sniffer and detector.
        
    
    def stop(self):
        print("Stopped")
        self.stop_event.set() #Sets the stop event,
        globalflags.stop_flag = True
        # for task in self.tasks:
        #     task.cancel()
            
    def stop_filter(self):
        return self.stop_event.is_set(self)  #you can determine whether the capturing process should continue or stop based on the state of the stop event. If the method returns True, 
        # it means that the stop event has been set and the capturing process should stop. 
        # If it returns False, the capturing process can continue.
    
    def preprocess_data(self,datagram): 
        try:
            src_ip = np.array([int(x) for x in datagram.source_ip.split('.')]) # Splits the source IP address of the datagram into individual components (octets) using the dot separator 
        # and converts each component from string to integer. It creates a NumPy array src_ip to store these values.
            dest_ip = np.array([int(x) for x in datagram.destination_ip.split('.')]) #nafs el kalam le destination ip[ ]
            
            src_port = int(datagram.source_port) #bahwlo integer bardo 
            dest_port = int(datagram.destination_port)
            
            input_data = np.concatenate([src_ip, dest_ip, [src_port, dest_port, datagram.size, datagram.header_size]]) #concatenate into a single array called input_data. 
            # This array represents the preprocessed input data for the model 
            input_data = np.expand_dims(input_data, axis=0) #bazwn axis 0 ya3ne badal makanet (n) (1,n) aw (n,1) 3shan ykhleha tdkhol 3al model 
        except:
            pass  #Exception handler 
            
        return input_data











# Overall, this function encapsulates the prediction logic, handles exceptions, and updates the prediction status in the globalflags module.
    def predict_ddos(self, datagram): #predict whether a given datagram represents a DDoS attack or not
        try:
            globalflags.predictddos = False  # The function first sets globalflags.predictddos to False, indicating that the prediction is not yet performed.
            input_data = self.preprocess_data(datagram)
            
            prediction = self.model.predict(input_data)[0]  # The preprocessed input data is passed to the trained model (self.model) using the predict method, which returns the predicted probabilities for each class. In this case, it assumes a binary classification task with two classes.

            return prediction[0] > prediction[1] #lw 0 aktar fe attack 
        except:
            globalflags.predictddos = True  # If any exception occurs during the prediction process, the except block is executed. It sets globalflags.predictddos to True, indicating that an error occurred during the prediction, and returns False to handle the exception gracefully.

            return False
       




        

       
    def process_packet(self,packet):
        
        if(not globalflags.stop_flag):  #It first checks if the globalflags.stop_flag is set to False, indicating that the sniffer is still running. If it is set to True, it means the sniffer has been stopped, and the function returns without further processing.
            try:
     
                ipp=packet.sprintf("%IP.src%") # It extracts the source IP address (%IP.src%) from the packet using Scapy's sprintf function and assigns it to the variable ipp.
                if not self.db.blacklisthas(ipp):
                    print(ipp)
                else:
                    print("Blocked : !!!! " , ipp)

                new_packet = datagram.Datagram(  # c. It creates a new datagram.Datagram object named new_packet with the extracted packet information, This object represents the encapsulated data from the captured packet.

                    protocol=packet.sprintf("%transport_layer%"),
                    src_ip=packet.sprintf("%IP.src%"),
                    dest_ip=packet.sprintf("%IP.dst%"),
                    src_port=packet.sprintf("%srcport%"),
                    dest_port=packet.sprintf("%dstport%"),
                    time=packet.sprintf("%time%"),
                    size=packet.sprintf("%IP.len%"),
                    header_size=packet.sprintf("%IP.hdr_len%")
                )
                
                if self.predict_ddos(new_packet): # It calls the predict_ddos function with new_packet as the argument to determine if the packet is predicted to be a DDoS attack. If it returns True, it sets globalflags.predict_ddos to True.

                    globalflags.predict_ddos = True
                    
                    
    
            except AttributeError as e: # If an AttributeError occurs during the packet processing, it is caught in the except block. This exception typically happens when certain packet attributes are missing or not accessible. In this case, the exception is simply ignored (pass statement) to continue processing the next packet.

                
                pass 
