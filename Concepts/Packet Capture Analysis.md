---
tags: [concept, forensics, networking]
---

# Packet Capture Analysis

## What it is

A packet capture (`.pcap`/`.pcapng`) is a recording of raw network traffic - every frame that crossed a network interface, with full protocol headers intact. Tools like Wireshark (GUI) and `tshark` (CLI) parse these frames back into their protocol layers (Ethernet → IP → TCP/UDP → application protocol) so you can inspect exactly what was sent, in what order, by whom.

## Why filtering matters

A real capture contains far more noise than signal: broadcast traffic, retransmissions, unrelated protocols. Wireshark's **display filters** (`udp`, `tcp.port==22`, `data.len==1`, `ip.src==10.0.0.2`) let you narrow thousands of packets down to the handful that matter. A common pattern in these notes is noticing an anomaly first (e.g. "lots of packets with length 1 or 5") and *then* filtering specifically on that anomaly (`data.len==1`) - anomalous packet sizes are a strong signal that data is being smuggled through a side channel (e.g. one meaningful byte per packet, exfiltrated covertly over what looks like innocuous traffic).

## Why "follow the stream" works

TCP/UDP conversations are split across many individual packets, each carrying a fragment of the data. Wireshark's "Follow Stream" feature reassembles all packets belonging to one conversation (matched by IP/port tuple) back into the original byte stream, in order - turning a scattered packet list into the readable HTTP request/response, file transfer, or chat log it originally represented.

## Why source port numbers or timing can themselves carry data

If a protocol's *metadata* (not its payload) varies in a structured way - e.g. source ports in a specific small range, where the low byte of the port number is itself meaningful - that's a side channel: data hidden in a field nobody expects to carry a message. Recognizing "this field's values don't look like normal protocol behavior" is the key observation; converting those values (e.g. treating a port offset as an ASCII code) is a mechanical step after that.

## Why scripted extraction (`tshark`) matters for larger captures

Clicking through Wireshark doesn't scale once you need to extract and process one specific field from hundreds of packets. `tshark -r file.pcap -Y "<filter>" -T fields -e <field1> -e <field2>` prints just the fields you ask for, in a script-friendly format, which can then be piped through `sort` (packets aren't always stored in the order they should be read - reassembly or multiple capture points can interleave them), `awk` (to pick a specific column), and a decoder (`xxd -p -r`, `base64 -d`) to go from raw hex/base64 payload fragments to a final readable message. Filtering on an exact payload length (`tcp.len==12`) is a common way to isolate "data-carrying" packets from protocol overhead (ACKs, handshakes) when the payload size is consistent - but always double check for outliers (e.g. one shorter final packet) that a too-narrow filter would silently drop.

## Why capturing USB or other non-IP traffic works the same way

Wireshark isn't limited to IP networks - it can capture USB traffic too, decoding device reports according to that device class's protocol spec (e.g. HID report descriptors for a game controller). The same principle applies: identify the device/protocol, find its public specification, and map specific byte offsets/bit positions in each report to the real-world event they represent (a button press, an axis movement).
