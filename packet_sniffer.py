#!/usr/bin/env python3
"""
Network Packet Analyzer – Simple packet sniffer using Scapy.
Displays source/dest IP, protocol, and payload.
Use with proper authorisation only.
"""

import sys
from scapy.all import sniff, IP, TCP, UDP, ICMP, Raw
import argparse

# --- Configuration ---
PAYLOAD_LEN = 32   # Number of bytes of payload to display (0 to disable)


def packet_callback(packet):
    """
    Called for each captured packet. Extracts and prints relevant info.
    """
    # Check if packet has an IP layer
    if IP not in packet:
        return

    ip = packet[IP]
    src = ip.src
    dst = ip.dst
    proto = ip.proto   # IP protocol number

    # Map protocol number to name
    proto_name = {6: 'TCP', 17: 'UDP', 1: 'ICMP'}.get(proto, f'OTHER({proto})')

    # Start building output
    output = f"[{proto_name}] {src} -> {dst}"

    # Payload extraction (for TCP/UDP only)
    payload = None
    if TCP in packet:
        payload = packet[TCP].payload
    elif UDP in packet:
        payload = packet[UDP].payload
    elif ICMP in packet:
        # ICMP often has a payload (e.g., echo reply)
        payload = packet[ICMP].payload

    if payload and PAYLOAD_LEN > 0:
        # Get raw bytes
        raw_bytes = bytes(payload)
        if raw_bytes:
            # Limit to PAYLOAD_LEN bytes
            raw_bytes = raw_bytes[:PAYLOAD_LEN]
            # Hex representation
            hex_str = ' '.join(f'{b:02x}' for b in raw_bytes)
            # ASCII representation (printable only)
            ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in raw_bytes)
            output += f"\n   Payload ({len(raw_bytes)} bytes): {hex_str}  {ascii_str}"

    # Print to console
    print(output)


def main():
    parser = argparse.ArgumentParser(
        description="Simple packet sniffer – captures IP packets and displays info.",
        epilog="Use with permission only."
    )
    parser.add_argument(
        "-i", "--interface",
        help="Network interface to sniff (e.g., eth0, wlan0). Leave empty for default."
    )
    parser.add_argument(
        "-f", "--filter",
        help="BPF filter (e.g., 'tcp', 'udp', 'icmp', 'port 80'). Default: 'ip'"
    )
    parser.add_argument(
        "-n", "--count",
        type=int,
        default=0,
        help="Number of packets to capture (0 = infinite). Default: 0"
    )
    parser.add_argument(
        "-p", "--payload",
        type=int,
        default=PAYLOAD_LEN,
        help=f"Number of payload bytes to display (0 to disable). Default: {PAYLOAD_LEN}"
    )
    args = parser.parse_args()

    # Update global payload length
    global PAYLOAD_LEN
    PAYLOAD_LEN = args.payload

    # Build the filter string – ensure we only capture IP packets
    bpf_filter = args.filter if args.filter else "ip"
    # If the user specified a filter, we still want to capture only IP.
    # We'll add "ip" as a base unless the user wants something else.
    # But we can just use exactly what the user gave (they can include 'ip').
    # We'll keep it simple.

    print("=== Network Packet Sniffer ===")
    print(f"Interface: {args.interface if args.interface else 'default'}")
    print(f"Filter: {bpf_filter}")
    print(f"Packet limit: {args.count if args.count > 0 else 'infinite'}")
    print("Press Ctrl+C to stop.\n")

    try:
        # Start sniffing
        sniff(
            iface=args.interface,
            filter=bpf_filter,
            prn=packet_callback,
            count=args.count if args.count > 0 else None,
            store=False   # don't store packets in memory
        )
    except KeyboardInterrupt:
        print("\nSniffer stopped by user.")
    except PermissionError:
        print("\nERROR: Permission denied. Did you run with sudo/Administrator?")
    except Exception as e:
        print(f"\nERROR: {e}")


if __name__ == "__main__":
    main()
