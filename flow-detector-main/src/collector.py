import queue as Queue
from src import flow
from src import csv_writer


## Collector organizes the captured packets.
#
#  Collector saves the captured packets, detects flows based on the sender and receiver IPs, and generates statistics.
class Collector:
    QUEUE_TIMEOUT = 2

    def __init__(self, writer=None):
        self.flows = dict()
        self.running = True
        self.writer = writer if writer is not None else csv_writer.CSVWriter()

    ## Handler to exit the thread.
    def signal_handler(self, sig, frame):
        self.running = False

    ## The main logic of the class adds incoming packets to the corresponding flow.
    #  @param queue The shared queue between threads.
    def collect(self, queue):
        while self.running:
            try:
                packet = queue.get(True, Collector().QUEUE_TIMEOUT)
            except Queue.Empty:
                continue

            key = packet.source_ip + packet.destination_ip
            reversed_key = packet.destination_ip + packet.source_ip
            if key in self.flows.keys():
                self.flows[key].add_packet(packet)
            elif reversed_key in self.flows.keys():
                self.flows[reversed_key].add_packet(packet)
            else:
                self.flows[key] = flow.Flow(packet.source_ip, packet.destination_ip)
                self.flows[key].add_packet(packet)

        self.generate_stat()

    ## Function to generate the result. This function uses a writer that allows writing in
    #  different ways (File, Network, ...).
    def generate_stat(self):
        self.writer.open()
        for flow in self.flows.values():
            self.writer.write(flow.get_stat())
        self.writer.close()
