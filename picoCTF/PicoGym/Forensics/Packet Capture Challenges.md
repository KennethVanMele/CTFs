---
tags: [picoctf, forensics, networking, wireshark, pcap, tshark]
platform: picoCTF
category: Forensics
---
Covers: shark on wire 1, shark on wire 2, WebNet0, Ph4nt0m 1ntrud3r.

## Shark on Wire 1
1. Open the pcap in Wireshark.
2. `Ctrl+F`, search for "pico" across packet bytes and strings.
3. Filter on `udp`, notice some packets have `len=1`.
4. Filter further: `data.len==1`, also notice the source should be `10.0.0.2`.
5. Combined filter: `data.len==1 && ip.src==10.0.0.2`
6. Right-click, Follow, UDP Stream to reassemble the hidden message.

Packets of unusually consistent, tiny length are a strong tell that one byte of hidden data is being smuggled per packet, a classic covert channel.

## Shark on Wire 2
1. Notice lots of `len=1` packets, a red herring this time.
2. Notice `len=5` packets filled with `aaaaa`, all on port 22: filter `udp.port==22`.
3. Sort by packet number to get start/end order.
4. Source ports differ (5xxx range), these encode data in ASCII.

Deliberately sets up a false lead (the pattern that solved shark on wire 1) to force checking multiple candidate anomalies rather than pattern-matching the previous solution. The real side channel is in the source port numbers, not the payload.

## WebNet0
1. Import the provided RSA private key into Wireshark: Edit, Preferences, Protocols, TLS, RSA key list.
2. Target: IP `128.237.140.23`, port `57567`.
3. With the key loaded, Wireshark decrypts the TLS session and lets you follow the HTTP stream in plaintext.

TLS encrypts traffic specifically so a third party capturing packets can't read it, but if the capture includes the actual RSA private key used for that session, Wireshark can perform the same decryption the legitimate server would. This only works for RSA key-exchange-based TLS, not modern forward-secret key exchanges like ECDHE.

## Ph4nt0m 1ntrud3r
1. Opening the pcap in Wireshark shows Base64-looking strings in TCP traffic.
2. Reproduce with `tshark`: `tshark -r myNetworkTraffic.pcap -Y "tcp"`.
3. Extract payload bytes: add `-T fields -e tcp.segment_data`.
4. Convert hex to raw bytes, then decode Base64: `xxd -p -r | base64 -d`, but the output is gibberish, likely because it includes too much unrelated data.
5. Narrow to the longer, consistent-length packets: filter `tcp.len==12`.
6. Still out of order, the capture isn't sorted by arrival time. Add a time field, sort, and pick out the data column with `awk`.
7. There's exactly one packet of length 4 among all the length-12 ones (the final `}`). Expand the filter: `tcp.len==12 || tcp.len==4`.
8. Final command:

   ```bash
   tshark -r myNetworkTraffic.pcap -Y "tcp.len==12 || tcp.len==4" -T fields -e frame.time -e tcp.segment_data | sort | awk '{print $6}' | xxd -p -r | base64 -d
   ```

## Why
See [[Packet Capture Analysis]] for the general filtering and stream-reassembly technique. Filtering on exact payload length isolates data-carrying packets from protocol noise, but a too-narrow length filter can silently drop legitimate outliers, worth double-checking rather than assuming a clean cutoff caught everything. Sorting by time matters because capture order on disk doesn't always match chronological order. Once reassembled, the hex to Base64 decode chain is a plain application of [[Encoding vs Encryption]].
