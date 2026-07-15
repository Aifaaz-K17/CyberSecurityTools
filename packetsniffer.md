# 🌐 Network Packet Analyzer (Sniffer)

**⚠️ Ethical & Legal Warning**  
This tool captures live network traffic. **Only use it on networks you own or have explicit written permission to monitor.** Unauthorised packet sniffing is illegal in many jurisdictions and violates privacy. This code is for **educational purposes only** – to understand how network protocols work and how packet analysis is performed in controlled environments (e.g., your own home network, a lab, or during authorised security assessments).

---

## 📦 Overview

A simple Python packet sniffer that:

- Captures live IP packets from a network interface.
- Displays:
  - Source & destination IP addresses.
  - Protocol (TCP, UDP, ICMP, or other).
  - Payload data (first 32 bytes in hex/ASCII) for TCP/UDP.
- Supports filtering by protocol (`tcp`, `udp`, `icmp`).
- Allows you to choose the network interface.
- Runs until you press **Ctrl+C**.

Built with **[Scapy](https://scapy.net/)** – a powerful packet manipulation library.

---

## 🔧 Requirements

- Python 3.6+
- [Scapy](https://scapy.net/) – install via pip:
  ```bash
  pip install scapy
  ```
- **Root/Administrator privileges** are required to capture raw packets (use `sudo` on Linux/macOS, or run as Administrator on Windows).

---

---

## 🚀 Usage Examples

1. **Basic sniffing** (all IP traffic, default interface):
   ```bash
   sudo python packet_sniffer.py
   ```

2. **Sniff only TCP traffic** on interface `eth0`:
   ```bash
   sudo python packet_sniffer.py -i eth0 -f tcp
   ```

3. **Sniff 10 packets** of UDP traffic:
   ```bash
   sudo python packet_sniffer.py -f udp -n 10
   ```

4. **Sniff HTTP traffic** (port 80) and show 64 bytes of payload:
   ```bash
   sudo python packet_sniffer.py -f "port 80" -p 64
   ```

5. **Hide payload** (show only IP headers):
   ```bash
   sudo python packet_sniffer.py -p 0
   ```

---

## 📊 Sample Output

```
[TCP] 192.168.1.10:54322 -> 93.184.216.34:80
   Payload (32 bytes): 47 45 54 20 2f 20 48 54 54 50 2f 31 2e 31 0d 0a 48 6f 73 74 3a 20 65 78 61 6d 70 6c 65 2e 63 6f  GET / HTTP/1.1..Host: example.co
[UDP] 192.168.1.10:5353 -> 224.0.0.251:5353
   Payload (16 bytes): 00 00 00 00 00 01 00 00 00 00 00 00 00 00 00 00  ................
[ICMP] 192.168.1.1 -> 192.168.1.10
   Payload (16 bytes): 08 00 8e 7c 00 01 00 01 61 62 63 64 65 66 67 68  ...|....abcdefgh
```

---

## ⚙️ How It Works

- **Scapy's `sniff()`** captures packets on the chosen interface.
- A **BPF filter** (Berkeley Packet Filter) is applied to reduce noise – you can filter by protocol, port, host, etc.
- For each packet, the callback checks for an IP layer, extracts source/destination, protocol number, and then (for TCP/UDP/ICMP) retrieves the payload.
- The payload is displayed as both hex and ASCII (non‑printable characters shown as `.`).
- The tool runs until the specified packet count is reached or you interrupt with **Ctrl+C**.

---

## 🔒 Important Ethical & Practical Notes

- **Permissions**: You must run this script with root/admin privileges because raw socket access is restricted.
- **Network impact**: Sniffing does not modify or inject packets – it only captures copies. However, in promiscuous mode, you may capture traffic not destined for your machine, which is even more sensitive.
- **Privacy**: Captured packets may contain passwords, personal messages, or other confidential data. Handle logs (if any) with care.
- **Legal**: Before using, check your local laws. Unauthorised sniffing is a violation of the Computer Fraud and Abuse Act (CFAA) in the US and similar laws elsewhere.
- **Use responsibly**: This tool is meant to help you learn about network protocols, troubleshoot your own network, or conduct authorised penetration tests.

---

## 📚 Possible Enhancements (Educational)

- Add support for IPv6.
- Display more protocol‑specific fields (e.g., TCP flags, sequence numbers).
- Save packets to a `.pcap` file for later analysis (Scapy supports `wrpcap`).
- Decode common application‑layer protocols (HTTP, DNS, etc.) – this is the basis of tools like Wireshark.
- Add colourised output for better readability.

---

**Stay ethical, stay legal.** 🛡️
