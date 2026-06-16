---
course: helpdesk-tier1-2
title: Network troubleshooting with command-line tools
month: 2
monthTitle: Networking Foundations (Network+)
lesson: 9
summary: 'Bring it all together with the command-line tools every technician relies on: ping, ipconfig,
  tracert, nslookup, and netstat, plus a repeatable troubleshooting method.'
objectives:
- Use ping to test reachability and measure latency
- Read ipconfig output to confirm a device's configuration
- Use tracert to find where along a path traffic fails
- Query DNS with nslookup to isolate name resolution faults
- Apply a bottom-up, layered troubleshooting method
- Combine tools to diagnose a realistic connectivity ticket
video: hd2-l09-network-troubleshooting-cli.mp4
quiz:
- q: What does the ping command test?
  options:
  - DNS records only
  - Whether a host is reachable and the round-trip time
  - Open ports on a server
  - Cable category
  answer: 1
  why: Ping sends ICMP echo requests and reports whether replies come back and how long the round trip
    takes, measuring reachability and latency.
- q: What does tracert (traceroute) show you?
  options:
  - Each router hop along the path to a destination
  - The MAC address of every device
  - The DNS server settings
  - The Wi-Fi channel
  answer: 0
  why: Tracert lists each router hop and its response time, so you can see exactly where along the path
    traffic slows down or stops.
- q: A ping to 8.8.8.8 succeeds but ping to google.com fails. What is the likely cause?
  options:
  - The cable is unplugged
  - A DNS resolution problem
  - The firewall blocks all traffic
  - APIPA addressing
  answer: 1
  why: Reaching an IP but not a name means connectivity is fine and DNS is failing to resolve the name
    to an address.
- q: Which command renews a device's DHCP lease on Windows?
  options:
  - ping /renew
  - tracert /renew
  - ipconfig /renew
  - netstat /renew
  answer: 2
  why: ipconfig /renew requests a fresh IP configuration from the DHCP server, often paired with ipconfig
    /release beforehand.
- q: Name the loopback address you ping to confirm the local TCP/IP stack works.
  answer: 127.0.0.1
  why: 127.0.0.1 (localhost) is the loopback address; a successful ping confirms the device's own TCP/IP
    stack is functioning before you test the network.
- q: In one sentence, describe the bottom-up troubleshooting approach.
  answer: Start at the physical layer and work up, checking the cable and link, then local IP config,
    then the gateway, then the internet, then DNS, until the failing layer is found.
  why: Working methodically from Layer 1 upward isolates the fault to one layer instead of guessing, which
    is faster and more reliable.
resources:
- label: Microsoft Learn — ping command
  url: https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/ping
- label: Microsoft Learn — tracert command
  url: https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/tracert
- label: Microsoft Learn — ipconfig command
  url: https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/ipconfig
- label: Microsoft Learn — nslookup command
  url: https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/nslookup
---

## Tools turn panic into method

When a user says "the internet is broken," a junior tech guesses and a good tech **tests**. A handful of command-line tools, used in a logical order, will diagnose almost every connectivity ticket you meet. This lesson brings the whole module together into a repeatable method.

## ping: is it reachable?

**ping** sends a small message and times the reply. It answers two questions: *can I reach this host?* and *how fast is the round trip?*

```bash
ping 8.8.8.8

Reply from 8.8.8.8: bytes=32 time=14ms TTL=118
Reply from 8.8.8.8: bytes=32 time=13ms TTL=118
```

Replies mean reachable; **Request timed out** or **Destination host unreachable** means a problem. Always ping a few targets in order: `127.0.0.1` (your own stack), your gateway, a public IP like `8.8.8.8`, then a name.

## ipconfig: what is my configuration?

**ipconfig** shows your address, mask, and gateway, and confirms whether DHCP worked. Use `/all` for DNS servers and MAC address, and `/release` `/renew` `/flushdns` to fix DHCP and DNS issues.

```bash
ipconfig /all
ipconfig /release
ipconfig /renew
ipconfig /flushdns
```

A `169.254.x.x` address here tells you DHCP failed before you waste time elsewhere.

## tracert: where does it break?

**tracert** (traceroute) maps every **router hop** between you and a destination, with timing for each. It shows *where* along the path traffic slows or stops.

```bash
tracert example.com

  1    1 ms   192.168.1.1      (your router)
  2   12 ms   10.20.0.1        (your ISP)
  3    *    *    *   Request timed out
```

If the first hop fails, the problem is local; if it dies several hops out, the fault is upstream at the ISP — not something you can fix, but vital to know.

## nslookup: is DNS working?

**nslookup** queries DNS directly. If `ping 8.8.8.8` works but names fail, `nslookup` confirms the DNS fault and shows which server answered.

```bash
nslookup example.com
```

## A repeatable method

Work **bottom-up** through the layers and stop at the first failure:

```text
1. Physical: link light, cable seated?            (Layer 1)
2. ipconfig: valid IP, not 169.254.x.x?           (Layer 3 local)
3. ping gateway: can I reach my router?           (LAN)
4. ping 8.8.8.8: can I reach the internet by IP?  (routing/ISP)
5. nslookup / ping a name: does DNS resolve?      (Layer 7)
```

Each step that passes rules out a layer; the first that fails is your fault. This single checklist will solve the majority of your network tickets.

## Your task

Run the full bottom-up sequence on your own PC: `ping 127.0.0.1`, then ping your gateway, then `ping 8.8.8.8`, then `nslookup example.com`. Record the result of each. Then run `tracert 8.8.8.8` and count how many hops it takes to reach Google's DNS. Write a one-line conclusion stating that your connection is healthy at every layer.
