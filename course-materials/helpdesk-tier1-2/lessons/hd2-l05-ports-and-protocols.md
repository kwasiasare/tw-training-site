---
course: helpdesk-tier1-2
title: Common ports and protocols
month: 2
monthTitle: Networking Foundations (Network+)
lesson: 5
summary: Learn what ports are, how they let one device run many services at once, and memorise the common
  port numbers and protocols every helpdesk technician needs.
objectives:
- Explain what a port number is and why services use them
- Tell the difference between TCP and UDP and when each is used
- Recall the well-known ports for HTTP, HTTPS, DNS, SSH and RDP
- Match common protocols to the tasks they perform
- List which ports are open on a machine using the command line
- Recognise how a blocked port causes specific service failures
video: hd2-l05-ports-and-protocols.mp4
quiz:
- q: What is a port number used for?
  options:
  - Identifying a physical cable socket only
  - Directing traffic to the right service on a device
  - Encrypting all data
  - Replacing the IP address
  answer: 1
  why: A port number lets one IP address run many services at once by directing each connection to the
    correct application, such as a web server on port 443.
- q: Which port does HTTPS use by default?
  options:
  - '80'
  - '21'
  - '443'
  - '25'
  answer: 2
  why: HTTPS, secure web traffic, uses TCP port 443 by default, while plain HTTP uses port 80.
- q: What is the main difference between TCP and UDP?
  options:
  - TCP is wireless, UDP is wired
  - TCP is reliable and connection-oriented, UDP is fast and connectionless
  - UDP encrypts, TCP does not
  - There is no difference
  answer: 1
  why: TCP sets up a connection and guarantees ordered, reliable delivery; UDP is connectionless and faster,
    used where speed matters more than perfect delivery, like DNS and streaming.
- q: Which protocol and port would you use for a secure remote terminal to a Linux server?
  options:
  - RDP on 3389
  - SSH on 22
  - FTP on 21
  - Telnet on 23
  answer: 1
  why: SSH provides an encrypted remote command-line session over TCP port 22; Telnet (port 23) does the
    same but with no encryption and should be avoided.
- q: Name the default port used by Remote Desktop Protocol (RDP).
  answer: '3389'
  why: RDP uses TCP port 3389, the protocol used to remotely control a Windows desktop, which helpdesk
    teams use constantly.
- q: In one sentence, why does a single server need port numbers at all?
  answer: A server has one IP address but runs many services, so port numbers tell incoming traffic which
    service it is meant for, like apartment numbers at one street address.
  why: Ports multiplex many services onto one IP, so web, email, and remote access can all share the same
    machine without confusion.
resources:
- label: Cloudflare Learning Center — What is a computer port?
  url: https://www.cloudflare.com/learning/network-layer/what-is-a-computer-port/
- label: Cloudflare Learning Center — TCP vs UDP
  url: https://www.cloudflare.com/learning/ddos/glossary/user-datagram-protocol-udp/
- label: Wikipedia — List of TCP and UDP port numbers
  url: https://en.wikipedia.org/wiki/List_of_TCP_and_UDP_port_numbers
- label: Microsoft Learn — netstat command
  url: https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/netstat
---

## One address, many services

A single device has one **IP address** but often runs many services at once — a web server, an email server, a remote-access service. How does incoming traffic know which one it wants? **Port numbers**. Think of the IP address as a building's street address and the port as the apartment number inside. A port is a 16-bit number from 0 to 65535, and the combination of IP address and port is called a **socket**.

## TCP and UDP

Ports belong to one of two **transport protocols**. **TCP** sets up a connection first and guarantees that data arrives complete and in order — reliable but with a little overhead. **UDP** just fires data off without a handshake — fast and lightweight, but with no delivery guarantee. Web pages and file transfers use **TCP**; DNS lookups, voice calls, and live streaming often use **UDP** because speed matters more than perfect delivery.

## The ports you must know

Certain **well-known ports** (0-1023) come up daily on the helpdesk. Memorise these:

```text
20/21  FTP        file transfer
22     SSH        secure remote terminal
23     Telnet     remote terminal (insecure, avoid)
25     SMTP       sending email
53     DNS        name resolution
67/68  DHCP       automatic addressing
80     HTTP       web (unencrypted)
110    POP3       receiving email
143    IMAP       receiving email (server-side)
443    HTTPS      secure web
3389   RDP        Remote Desktop (Windows)
```

If you only memorise a handful, make them **80, 443, 53, 22, 3389, and 25** — they appear in tickets constantly.

## How ports explain faults

Blocked ports cause very specific symptoms. If web pages on `https://` fail but `http://` works, port **443** may be blocked. If a user cannot reach Remote Desktop, suspect port **3389**. If email sends but does not receive, look at the receiving ports (**110/143**) rather than the sending port (**25**). Matching a symptom to a port number is a core diagnostic skill.

## Seeing ports in action

Windows shows active connections and listening ports with **netstat**:

```bash
netstat -an

Proto  Local Address      Foreign Address     State
TCP    0.0.0.0:443        0.0.0.0:0           LISTENING
TCP    192.168.1.42:50122 93.184.216.34:443   ESTABLISHED
```

The `LISTENING` line means a service is waiting on that port; `ESTABLISHED` means an active connection. You can also test whether a remote port is reachable from PowerShell:

```bash
Test-NetConnection example.com -Port 443
```

## Your task

Write out the protocol and transport type (TCP or UDP) for ports 22, 53, 80, 443, and 3389 from memory. Then run `netstat -an` on your PC and find at least one port in the `LISTENING` state. Finally, use `Test-NetConnection example.com -Port 443` and confirm the connection succeeds.
