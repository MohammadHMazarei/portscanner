import argparse
import socket
from datetime import datetime


def all_ports(ports):
    ports = [port for port in ports for port in (range(*map(int, port.split('-')))
                                                 if '-' in port else [int(port)])]
    return ports


def tcp_connection():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return sock


def udp_connection():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return sock


def check_result_tcp(sock, target_ip, port, timeout):
    try:
        sock.settimeout(timeout)
        sock.connect((target_ip, port))
        result = 0

    except(socket.timeout, ConnectionRefusedError):
        result = 1
    return result


def check_result_udp(sock, target_ip, port, timeout):
    try:
        sock.settimeout(timeout)
        sock.connect((target_ip, port))
        test = b"test"
        sock.sendto(test, (target_ip, port))
        response = sock.recv(1024)
        print(response)
        result = 0

    except(socket.timeout, ConnectionRefusedError):
        result = 1
    return result


def is_result_zero(result):
    return result == 0


def scan_ports(target_ip, ports, timeout, protocol):
    open_ports = []
    close_ports = []
    ports = all_ports(ports)

    for port in ports:
        try:
            if protocol == "tcp":
                # Create a TCP socket
                sock = tcp_connection()
                result = check_result_tcp(sock, target_ip, port, timeout)
            elif protocol == "udp":
                # Create a UDP socket
                sock = udp_connection()
                result = check_result_udp(sock, target_ip, port, timeout)
            else:
                print(f"Invalid protocol `{protocol}`")
                return

            if is_result_zero(result):
                open_ports.append(port)
            else:
                close_ports.append(port)

            sock.close()
        except socket.error:
            close_ports.append(port)
    return open_ports, close_ports


def main():
    parser = argparse.ArgumentParser(description="Port Scanner")
    parser.add_argument("ip", metavar="IP", type=str, help="Destination IP address")
    parser.add_argument("ports", metavar="PORT", type=str, nargs="+", help="Ports to scan")
    parser.add_argument("--timeout", type=float, default=1.0, help="Timeout for port connections (default: 1.0)")
    parser.add_argument("--protocol", type=str, choices=["tcp", "udp"], default="tcp", help="protocol to use for"
                                                                                            "scanning (default: tcp)")

    args = parser.parse_args()

    print(f"Scanning ports {args.ports} on {args.ip} using {args.protocol.upper()} protocol...")
    start_time = datetime.now()

    open_ports, closed_ports = scan_ports(args.ip, args.ports, args.timeout, args.protocol)

    end_time = datetime.now()
    total_time = end_time - start_time

    print("\nScan Results:")
    print(f"Open Ports: {open_ports}" if open_ports else "No open ports found.")
    print(f"Closed Ports: {closed_ports}" if closed_ports else "No closed ports found.")
    print(f"\nScan completed in {total_time}")


if __name__ == '__main__':
    main()
