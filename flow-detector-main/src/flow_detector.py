import signal
from queue import Queue
from threading import Thread
import sys
from src import sniffer
from src import collector

## FlowDetector creates two main threads of the program.
#
#  FlowDetector creates and manages two main threads over their lifetime.
class FlowDetector:

    ## Constructor, which could operate using default instances or mock instances.
    def __init__(self, sniffer_instance=None, collector_instance=None, ifname=None):
        self.sniffer = (
            sniffer_instance
            if sniffer_instance is not None
            else sniffer.Sniffer(ifname)
        )
        self.collector = (
            collector_instance
            if collector_instance is not None
            else collector.Collector()
        )

    ## The primary method of the class creates the threads.
    def run(self):
        shared_queue = Queue()
        signal.signal(signal.SIGINT, self.sniffer.signal_handler)
        signal.signal(signal.SIGINT, self.collector.signal_handler)

        sniffer_thread = Thread(target=self.sniffer.sniff, args=(shared_queue,))
        collector_thread = Thread(target=self.collector.collect, args=(shared_queue,))

        sniffer_thread.start()
        collector_thread.start()

        sniffer_thread.join()
        collector_thread.join()

    def stop(self):
        sys.exit()