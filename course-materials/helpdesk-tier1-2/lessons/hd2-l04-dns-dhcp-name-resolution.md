---
course: helpdesk-tier1-2
title: DNS, DHCP and name resolution
month: 2
monthTitle: Networking Foundations (Network+)
lesson: 4
summary: Discover how DHCP automatically hands out IP addresses and how DNS turns human-friendly names
  into IP addresses, plus the tools to test both.
objectives:
- Explain what DHCP does and the DORA lease process
- Describe how DNS resolves a name to an IP address
- Identify common DNS record types like A, AAAA, CNAME and MX
- Use nslookup to query DNS from the command line
- Recognise symptoms of DHCP and DNS failures on the helpdesk
- Flush and renew network settings on Windows
video: hd2-l04-dns-dhcp-name-resolution.mp4
quiz:
- q: What does a DHCP server provide to a client?
  options:
  - A website to visit
  - An IP address, subnet mask, gateway and DNS servers
  - A physical cable
  - Antivirus updates
  answer: 1
  why: 'DHCP automatically leases a client its IP configuration: address, subnet mask, default gateway,
    and DNS server addresses.'
- q: What is the correct order of the DHCP lease process?
  options:
  - Offer, Discover, Request, Acknowledge
  - Discover, Offer, Request, Acknowledge
  - Request, Discover, Acknowledge, Offer
  - Acknowledge, Request, Offer, Discover
  answer: 1
  why: The DORA process runs Discover, Offer, Request, Acknowledge — the client discovers, the server
    offers, the client requests, the server acknowledges.
- q: What does DNS translate?
  options:
  - IP addresses into MAC addresses
  - Domain names into IP addresses
  - Passwords into hashes
  - Cables into signals
  answer: 1
  why: DNS resolves human-friendly domain names like example.com into the numeric IP addresses computers
    use to connect.
- q: Which DNS record maps a name to an IPv4 address?
  options:
  - MX record
  - CNAME record
  - A record
  - TXT record
  answer: 2
  why: An A record maps a hostname to an IPv4 address; AAAA does the same for IPv6, and MX points to mail
    servers.
- q: Name the command that queries DNS to resolve a name on Windows.
  answer: nslookup
  why: nslookup (or dig on Linux/macOS) sends a DNS query and shows the IP address a name resolves to,
    which is essential for diagnosing name resolution faults.
- q: In one sentence, how would you tell a DNS problem from a connectivity problem?
  answer: If you can ping a public IP like 8.8.8.8 but cannot reach a website by name, connectivity is
    fine and DNS is the problem.
  why: Pinging by IP bypasses DNS, so success by IP but failure by name isolates the fault to name resolution
    rather than the network link.
resources:
- label: Cloudflare Learning Center — What is DNS?
  url: https://www.cloudflare.com/learning/dns/what-is-dns/
- label: Cloudflare Learning Center — DNS record types
  url: https://www.cloudflare.com/learning/dns/dns-records/
- label: Wikipedia — Dynamic Host Configuration Protocol (DHCP)
  url: https://en.wikipedia.org/wiki/Dynamic_Host_Configuration_Protocol
- label: Microsoft Learn — ipconfig command
  url: https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/ipconfig
---

## Two services that make networks usable

Imagine setting a unique IP address by hand on every device, and memorising the IP of every website. Painful. Two services rescue us: **DHCP**, which hands out IP addresses automatically, and **DNS**, which turns names like `example.com` into IP addresses. They run quietly in the background, but when either fails, the helpdesk phone rings.

## DHCP: automatic addressing

**DHCP** (Dynamic Host Configuration Protocol) leases each device its full IP configuration: an **IP address**, a **subnet mask**, a **default gateway**, and **DNS server** addresses. The handshake is remembered with the word **DORA**:

- **Discover** — the client shouts "is there a DHCP server?"
- **Offer** — a server replies with an available address.
- **Request** — the client says "I'll take it."
- **Acknowledge** — the server confirms and records the **lease**.

If no server answers, the client falls back to an **APIPA** address (`169.254.x.x`) and has no real connectivity.

## DNS: the internet's phone book

**DNS** (Domain Name System) translates names into IP addresses. When you type a website, your PC asks a **resolver**, which works down from the **root** servers to the **top-level domain** (like `.com`), to the domain's **authoritative** server, and gets back an IP. The result is cached so the next lookup is instant.

Common **record types** you should recognise:

```text
A      name -> IPv4 address
AAAA   name -> IPv6 address
CNAME  name -> another name (an alias)
MX     domain -> mail server
TXT    free text, used for verification (SPF, etc.)
```

## Testing name resolution

The key tool is **nslookup** (or `dig` on macOS/Linux):

```bash
nslookup example.com

Server:   192.168.1.1
Address:  192.168.1.1#53

Non-authoritative answer:
Name:     example.com
Address:  93.184.216.34
```

That tells you which DNS server answered and the IP it returned. If `nslookup` fails but `ping 8.8.8.8` works, you have a **DNS problem**, not a connectivity problem.

## Fixing common faults

Most DHCP and DNS issues clear with three Windows commands: release and renew the DHCP lease, and flush the DNS cache.

```bash
ipconfig /release
ipconfig /renew
ipconfig /flushdns
```

A stale or poisoned DNS cache can make one site unreachable while others work — `flushdns` is the first thing to try. If a PC shows a `169.254.x.x` address after `/renew`, suspect the DHCP server or the cable.

## Your task

Run `nslookup example.com` and note the DNS server that answered and the IP returned. Then run `nslookup` on your own company or school website. Finally, run `ipconfig /flushdns` and confirm it reports the cache was cleared. Write down, in your own words, how you would tell a DNS fault apart from a connectivity fault.
