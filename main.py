import argparse
import socket
from datetime import datetime


def scan_ports(target_ip, ports, timeout, protocol):
    open_ports = []
    close_ports = []

    for port in ports:
        try:
            if protocol == "tcp":
                # Create a TCP socket
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            elif protocol == "udp":
                # Create a UDP socket
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            else:
                print(f"Invalid protocol `{protocol}`")
                return
            sock.settimeout(timeout)
            result = sock.connect_ex((target_ip, port))

            if result == 0:
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
    parser.add_argument("ports", metavar="PORT", type=int, nargs="+", help="Ports to scan")
    parser.add_argument("--timeout", type=float, default=1.0, help="Timeout for port connections (default: 1.0)")
    parser.add_argument("--protocol", type=str, choices=["tcp", "udp"], default="tcp", help="protocol to use for"
                                                                                            "scanning (default: tcp)")

    args = parser.parse_args()

    print(f"Scanning ports {args.ports} on {args.ip} using {args.protocol.upper()} protocol...")
    start_time = datetime.now()

    open_ports, closed_ports = scan_ports(args.ip, args.ports, args.timeout, args.protocol)
    open_ports, closed_ports = scan_ports("127.0.0.1", [80, 244, 23], 1, "tcp")

    end_time = datetime.now()
    total_time = end_time - start_time

    print("\nScan Results:")
    print(f"Open Ports: {open_ports}" if open_ports else "No open ports found.")
    print(f"Closed Ports: {closed_ports}" if closed_ports else "No closed ports found.")
    print(f"\nScan completed in {total_time}")


if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
