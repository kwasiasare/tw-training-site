---
course: helpdesk-tier3-advanced
title: Advanced network diagnostics with Wireshark
month: 1
monthTitle: Advanced Troubleshooting & Root Cause Analysis
lesson: 5
summary: Capture and read packets to prove where a network problem actually lives — client, network, or
  server. Use Wireshark display filters and the TCP analysis flags to separate loss, latency, and application
  stalls.
objectives:
- Capture traffic at the right point and with the right scope using netsh trace and Wireshark
- Write precise display filters to isolate a single conversation
- Read the TCP three-way handshake and identify where a connection fails
- Use TCP analysis flags to distinguish packet loss from latency from app stalls
- Measure round-trip time and time-to-first-byte from a capture
- Decide from evidence whether the fault is client, network path, or server
video: ht1-l05-advanced-network-diagnostics.mp4
quiz:
- q: A user reports a slow web app. The capture shows the SYN, SYN-ACK, and ACK complete in 2 ms, but
    the server's first data packet arrives 4 seconds after the client's request. Where is the problem?
  options:
  - Packet loss on the network path
  - Client DNS resolution
  - Server-side processing — the network and handshake are fine; it's time-to-first-byte
  - A duplex mismatch on the switch
  answer: 2
  why: A fast handshake rules out the connection path, and the 4-second gap before the first response
    byte is server think-time (time-to-first-byte). The network delivered the request promptly; the server
    was slow to answer.
- q: Which Wireshark display filter isolates only the retransmissions and other TCP problem indicators?
  options:
  - tcp.port == 443
  - tcp.analysis.flags
  - ip.addr == 10.0.0.5
  - http.request
  answer: 1
  why: tcp.analysis.flags surfaces Wireshark's expert TCP findings — retransmissions, dup ACKs, zero windows,
    out-of-order — letting you see loss and flow-control problems without reading every packet.
- q: You see many 'TCP Dup ACK' followed by 'TCP Retransmission' for the same segment. What does this
    indicate?
  options:
  - The server is rejecting the connection
  - Packet loss on the path — the receiver keeps asking for a missing segment until it is resent
  - A successful clean transfer
  - An expired TLS certificate
  answer: 1
  why: Duplicate ACKs are the receiver signalling a gap; the matching retransmission is the sender resending
    the lost segment. Repeated cycles are classic packet loss, pointing at the network path.
- q: Why capture with 'netsh trace' or a tap rather than only on the affected client?
  options:
  - It is faster to type
  - Client captures are always wrong
  - netsh encrypts the capture
  - Capturing at two points lets you compare what was sent versus received and localise loss to a segment
    of the path
  answer: 3
  why: A single endpoint capture cannot tell you whether a missing packet was never sent or lost in transit.
    Capturing at both ends (or a tap) lets you compare and localise the loss to a specific path segment.
- q: In one sentence, what does a 'TCP Zero Window' message mean and whose problem is it?
  answer: 'A Zero Window means the receiver has advertised a window of zero, telling the sender to stop
    because the receiver''s buffer is full — so it is the receiving application''s problem: it is not
    reading data off the socket fast enough.'
  why: Zero Window is flow control, not loss; it points at a slow-consuming application on the receiving
    side, not the network.
- q: How would you prove from a capture that a 'network is slow' complaint is actually a DNS problem?
  answer: Filter for dns and measure the time between each query and its response; if name resolution
    takes seconds (or queries retry against a failing server) while the subsequent TCP connection to the
    resolved IP is fast, the latency lives in DNS, not in the data path.
  why: Isolating the DNS query/response timing separates name-resolution delay from connection and transfer
    delay, attributing the latency to the correct layer.
resources:
- label: Wireshark — User's Guide (display filters)
  url: https://www.wireshark.org/docs/wsug_html_chunked/ChWorkBuildDisplayFilterSection.html
- label: Wireshark — TCP Analysis (expert info) reference
  url: https://www.wireshark.org/docs/wsug_html_chunked/ChAdvTCPAnalysis.html
- label: Microsoft Learn — Capture network traffic with netsh trace
  url: https://learn.microsoft.com/en-us/windows-server/networking/technologies/netsh/netsh-trace
- label: Wireshark — Display Filter Reference (tcp)
  url: https://www.wireshark.org/docs/dfref/t/tcp.html
---

## Packets do not lie

When a network complaint reaches Tier 3, the argument is usually "it's the network" versus "it's the app." A **packet capture** settles it with evidence. The skill is not capturing — it is reading: knowing which handful of packets answer the question, and filtering out the thousands that do not.

## Capture at the right point and scope

Where you capture decides what you can conclude. A capture on only the affected client cannot distinguish *never sent* from *lost in transit*. Capture at both ends (or use a tap/SPAN port) so you can compare. On Windows you can capture without installing anything using **netsh trace**, then convert the `.etl` for Wireshark, or capture directly in Wireshark.

```powershell
# Lightweight built-in capture; reproduce the issue, then stop
netsh trace start capture=yes tracefile=C:\evidence\net.etl maxsize=512
# ... reproduce the problem ...
netsh trace stop
```

Keep captures short and scoped — a 30-second capture of one reproduction beats an hour of noise.

## Filter down to one conversation

Wireshark's power is its **display filters**. Start broad, then narrow to the single conversation that matters.

```text
ip.addr == 10.20.5.10 && tcp.port == 443
tcp.flags.syn == 1 && tcp.flags.ack == 0      # just the SYNs (connection starts)
dns                                            # name resolution timing
tcp.analysis.flags                             # all the TCP problem indicators
```

Right-click a packet and choose **Follow > TCP Stream** to see one conversation end to end.

## Read the handshake, then the timing

Every TCP connection opens with a three-way handshake: **SYN**, **SYN-ACK**, **ACK**. If the SYN goes unanswered, the connection never forms — a firewall or a dead server. If the handshake completes fast but the first data byte is slow, the network is fine and the **server think-time** (time-to-first-byte) is the problem. This single distinction resolves most "slow app" tickets.

## TCP analysis flags: loss vs latency vs stall

Wireshark's expert analysis labels the symptoms for you:

```text
TCP Retransmission / Fast Retransmission  -> packet loss on the path
TCP Dup ACK (repeated)                    -> receiver signalling a gap (loss)
TCP Zero Window                           -> receiver's buffer full (slow app)
TCP Out-Of-Order                          -> path reordering / multipath
```

Loss (retransmissions and dup ACKs) points at the **network path**. A **Zero Window** is flow control — the *receiving application* is not reading fast enough, so it is an app problem, not a network one. Latency with no loss and a clean window points at distance or a slow hop. **Out-of-order** segments suggest path reordering or load-balanced multipath, which can also trigger spurious retransmissions. Each pattern routes the ticket to a different owner, so name the pattern before you name a team.

## Your task

Reproduce a real or simulated slow/failing network operation. Capture it with `netsh trace` (or directly in Wireshark) for under a minute. In Wireshark, filter to the single conversation with an `ip.addr`/`tcp.port` filter, then Follow the TCP Stream. Measure: handshake time, time-to-first-byte, and any `tcp.analysis.flags` hits. Decide and write down whether the evidence shows packet loss (network path), a Zero Window (receiving app), DNS delay, or server think-time — and state which team you would route it to and why.
