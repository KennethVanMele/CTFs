---
tags: [concept, forensics, networking]
---
## What It Is
A packet capture (`.pcap`/`.pcapng`) is a recording of raw network traffic - every frame that crossed a network interface, with full protocol headers intact. Tools like Wireshark (GUI) and `tshark` (CLI) parse these frames back into their protocol layers (Ethernet → IP → TCP/UDP → application protocol) so you can inspect exactly what was sent, in what order, by whom.

## Why Filtering Matters
A real capture contains far more noise than signal: broadcast traffic, retransmissions, unrelated protocols. Wireshark's **display filters** (`udp`, `tcp.port==22`, `data.len==1`, `ip.src==10.0.0.2`) let you narrow thousands of packets down to the handful that matter. A common pattern in these notes is noticing an anomaly first (e.g. "lots of packets with length 1 or 5") and *then* filtering specifically on that anomaly (`data.len==1`). Anomalous packet sizes are a strong signal that data is being smuggled through a side channel (e.g. one meaningful byte per packet, exfiltrated covertly over what looks like innocuous traffic).

## Why "Follow the Stream" Works
TCP/UDP conversations are split across many individual packets, each carrying a fragment of the data. Wireshark's "Follow Stream" feature reassembles all packets belonging to one conversation (matched by IP/port tuple) back into the original byte stream, in order. This turns a scattered packet list into the readable HTTP request/response, file transfer, or chat log it originally represented.

## Why Source Port Numbers or Timing Can Themselves Carry Data
If a protocol's *metadata* (not its payload) varies in a structured way that's a side channel: data hidden in a field nobody expects to carry a message. Recognizing "this field's values don't look like normal protocol behavior" is the key observation; converting those values (e.g. treating a port offset as an ASCII code) is a mechanical step after that.

## Why Scripted Extraction (`tshark`) Matters for Larger Captures
Clicking through Wireshark doesn't scale once you need to extract and process one specific field from hundreds of packets. `tshark -r file.pcap -Y "<filter>" -T fields -e <field1> -e <field2>` prints just the fields you ask for, in a script-friendly format, which can then be piped through `sort`, `awk`, and a decoder to go from raw hex/base64 payload fragments to a final readable message. Filtering on an exact payload length (`tcp.len==12`) is a common way to isolate "data-carrying" packets from protocol overhead (ACKs, handshakes) when the payload size is consistent. But always double-check for outliers (e.g. one shorter final packet) that a too-narrow filter would silently drop.

## Why Capturing USB or Other Non-IP Traffic Works the Same Way
Wireshark isn't limited to IP networks - it can capture USB traffic too, decoding device reports according to that device class's protocol spec (e.g. HID report descriptors for a game controller). The same principle applies: identify the device/protocol, find its public specification, and map specific byte offsets/bit positions in each report to the real-world event they represent (a button press, an axis movement).
