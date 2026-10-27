---
tags: [hackarcana, forensics, usb, packet-capture]
platform: Hackarcana
status: active
---

# Gamepad

## Steps

Given a `.pcapng` file and an `.html` file.

1. The HTML file contains the "keypad" used to input the flag, along with some JavaScript data.
2. The pcapng file is a Wireshark capture of USB traffic.
3. The second packet reveals the device ID: DualSense wireless controller (PS5).
4. After some configuration, the capture shows what look like the controller's input packets. Export them to `.json` to make them easier to work with in Python.
5. The USB protocol specification for the controller: https://controllers.fandom.com/wiki/Sony_DualSense
6. Per the spec, `0x01` is the report ID byte, and every packet starts with it, so it can be skipped. The remaining report length is 63 bytes, as specified. The buttons and D-pad live at byte offset 7 (bits 7.0 through 7.7).
7. Isolate that byte and shift/mask it to check each button's state individually. Skip duplicate consecutive packets (the controller's poll rate is high, so most packets just repeat the previous state).
8. Translate the D-pad moves into x/y coordinates on the keypad layout (copy-pasted as a variable, each row exactly 10 characters long, matching the keypad's grid).
9. With `assert`, check which buttons get pressed. Both Cross and Circle are used in the capture, but only Circle's presses actually yield the flag, Cross turns out to be a red herring.

## Why

This is [[Packet Capture Analysis]] applied to USB traffic instead of IP traffic: Wireshark captures USB the same way it captures network packets, and the device's own public protocol specification tells you exactly which byte offsets and bits correspond to real-world events (a button press, a D-pad direction), the same principle as reading a known network protocol's header fields. The deduplication step (skipping repeated identical packets) is necessary because of the controller's high poll rate, without it, the same button press would be recorded dozens of times in a row. The deliberate red herring (Cross presses that don't correspond to the real input) is a reminder to verify a hypothesis against the actual expected output rather than assuming every observed signal is meaningful.
