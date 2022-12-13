## FlowStat stores the statistics to report.
class FlowStat:
    def __init__(
        self,
        source_ip,
        destination_ip,
        source_ports=set(),
        destination_ports=set(),
        protocols=set(),
        duration=0,
        sent_bytes=0,
        received_bytes=0,
        sent_header_bytes=0,
    ):

        self.source_ip = source_ip
        self.destination_ip = destination_ip
        self.source_ports = source_ports
        self.destination_ports = destination_ports
        self.protocols = protocols
        self.duration = duration
        self.sent_bytes = sent_bytes
        self.received_bytes = received_bytes
        self.sent_header_bytes = sent_header_bytes

    def add_source_port(self, port):
        self.source_ports.add(port)

    def add_destination_port(self, port):
        self.destination_ports.add(port)

    def add_protocol(self, protocol):
        self.protocols.add(protocol)

    def increase_sent_bytes(self, sent_bytes):
        self.sent_bytes += int(sent_bytes)

    def increase_received_bytes(self, received_bytes):
        self.received_bytes += int(received_bytes)

    def increase_header_bytes(self, header_bytes):
        self.sent_header_bytes += int(header_bytes)

    def set_duration(self, duration):
        self.duration = duration
