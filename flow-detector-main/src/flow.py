from src import flow_stat

## Flow stores the packets in a particular flow.
class Flow:
    def __init__(self, src_ip, dest_ip):
        self.source_ip = src_ip
        self.destination_ip = dest_ip
        self.packets = list()

    ## Adds corresponding packets of the flow.
    def add_packet(self, packet):
        self.packets.append(packet)

    ## Generates statistics of the flow.
    def get_stat(self):
        stat = flow_stat.FlowStat(self.source_ip, self.destination_ip)

        for packet in self.packets:
            stat.add_source_port(packet.source_port)
            stat.add_destination_port(packet.destination_port)
            stat.add_protocol(packet.protocol)

            if self.source_ip == packet.source_ip:
                stat.increase_sent_bytes(packet.size)
                stat.increase_header_bytes(packet.header_size)
            else:
                stat.increase_received_bytes(packet.size)

        stat.set_duration(self.packets[-1].sniff_time - self.packets[0].sniff_time)
        return stat
