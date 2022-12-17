import csv


## CSVWriter writes into a CSV file.
class CSVWriter:
    OUTPUT = "D:/Graduation Project/flow-detector-main/flow-detector-main/9.CSV"
    HEADER = [
        "Source IP",
        "Destination IP",
        "Source Ports",
        "Destination Ports",
        "Protocols",
        "Duration",
        "Sent Bytes",
        "Received Bytes",
        "Header Bytes FWD",
    ]

    ## Generates the output file and write header.
    def open(self):
        self.fp = open(CSVWriter.OUTPUT, "w")
        self.writer = csv.writer(self.fp)
        self.writer.writerow(CSVWriter.HEADER)

    ## Writes a row in the output file.
    # @param flow_stat The row to be written.
    def write(self, flow_stat):
        row = [
            flow_stat.source_ip,
            flow_stat.destination_ip,
            " ".join(flow_stat.source_ports),
            " ".join(flow_stat.destination_ports),
            " ".join(flow_stat.protocols),
            flow_stat.duration,
            flow_stat.sent_bytes,
            flow_stat.received_bytes,
            flow_stat.sent_header_bytes,
        ]
        
        self.writer.writerow(row)

    ## Closes the file pointer.
    def close(self):
        self.fp.close()
