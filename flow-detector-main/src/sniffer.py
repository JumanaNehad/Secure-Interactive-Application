import pyhark

from _thread import interrupt_main
from src import datagram

## Sniffer captures the interface traffic using pyshark library.
class Sniffer:
    def __init__(self, if_name):
        self.running = True
        # self.capture = pyshark.LiveCapture(interface=if_name,display_filter="tcp.analysis.retransmission")
        self.capture = pyshark.LiveCapture(interface=if_name)
        
    #we use signals to deal with threads
    def signal_handler(self):
    #Stop capturing 
        self.running = False

    ## The main method captures and extracts necessary information.
    def sniff(self, queue):
        try:
            #keeps capturing the packets and store them in a queue 
            for packet in self.capture.sniff_continuously():

                # After Ctrl+C, exit the thread.
                if not self.running:
                    return

                try:
                    new_packet = datagram.Datagram(
                        protocol=packet.transport_layer,
                        src_ip=packet.ip.src,
                        dest_ip=packet.ip.dst,
                        src_port=packet[packet.transport_layer].srcport,
                        dest_port=packet[packet.transport_layer].dstport,
                        time=packet.sniff_time,
                        size=packet.ip.len,
                        header_size=packet.ip.hdr_len,
                    )

                    queue.put(new_packet)

                except AttributeError as e:
                    # New packet was controlling packet, discarded
                    pass

        except pyshark.capture.live_capture.UnknownInterfaceException as e:
            interrupt_main()
            print("error, incorrect interface name")
