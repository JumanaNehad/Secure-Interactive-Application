## Datagram stores the useful fields of an Internet packet.
class Datagram:
    def __init__(
        self, protocol, src_ip, dest_ip, src_port, dest_port, time, size, header_size
    ):
        self.protocol = protocol
        self.source_ip = src_ip
        self.destination_ip = dest_ip
        self.source_port = src_port
        self.destination_port = dest_port
        self.sniff_time = time
        self.size = size
        self.header_size = header_size
