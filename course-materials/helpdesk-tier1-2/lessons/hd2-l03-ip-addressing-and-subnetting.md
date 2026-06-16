---
course: helpdesk-tier1-2
title: IP addressing and subnetting basics
month: 2
monthTitle: Networking Foundations (Network+)
lesson: 3
summary: Learn how IPv4 addresses and subnet masks work, the difference between private and public addresses,
  and how CIDR notation defines a network's size.
objectives:
- Describe the structure of an IPv4 address and its four octets
- Explain how a subnet mask splits network from host bits
- Identify private versus public IP address ranges
- Read and interpret CIDR notation such as /24
- Recognise APIPA addresses and what they signal
- Calculate how many hosts a simple subnet supports
video: hd2-l03-ip-addressing-and-subnetting.mp4
quiz:
- q: How many bits are in a standard IPv4 address?
  options:
  - '16'
  - '32'
  - '64'
  - '128'
  answer: 1
  why: An IPv4 address is 32 bits, written as four 8-bit octets separated by dots, such as 192.168.1.10.
- q: Which of these is a private IP address range?
  options:
  - 8.0.0.0/8
  - 200.1.1.0/24
  - 192.168.0.0/16
  - 172.50.0.0/16
  answer: 2
  why: 192.168.0.0/16 is one of the RFC 1918 private ranges, alongside 10.0.0.0/8 and 172.16.0.0/12, used
    inside LANs.
- q: What does the /24 in 192.168.1.0/24 mean?
  options:
  - The first 24 bits are the network portion
  - 24 total hosts
  - 24 subnets
  - A 24-hour lease
  answer: 0
  why: CIDR /24 means the first 24 bits identify the network, leaving 8 bits for hosts — a mask of 255.255.255.0.
- q: A PC shows an address of 169.254.x.x. What does that indicate?
  options:
  - A healthy public address
  - It got an APIPA address and failed to reach a DHCP server
  - A VPN is connected
  - The subnet mask is wrong on the router
  answer: 1
  why: 'The 169.254.0.0/16 range is APIPA: the device self-assigned an address because no DHCP server
    answered, so it has no real network connectivity.'
- q: How many usable host addresses does a /24 subnet provide?
  answer: '254'
  why: A /24 has 8 host bits = 256 addresses, minus the network address and the broadcast address, leaving
    254 usable hosts.
- q: In one sentence, what job does the subnet mask do?
  answer: The subnet mask tells a device which part of an IP address is the network and which part is
    the host, so it knows whether a destination is local or must be sent to the gateway.
  why: Without the mask a device cannot decide if traffic stays on the LAN or must go to the router, which
    is the core of IP routing.
resources:
- label: Cloudflare Learning Center — What is an IP address?
  url: https://www.cloudflare.com/learning/dns/glossary/what-is-my-ip-address/
- label: Cloudflare Learning Center — What is a subnet?
  url: https://www.cloudflare.com/learning/network-layer/what-is-a-subnet/
- label: Wikipedia — Classless Inter-Domain Routing (CIDR)
  url: https://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing
- label: Wikipedia — Private network (RFC 1918)
  url: https://en.wikipedia.org/wiki/Private_network
---

## What an IP address is

An **IPv4 address** is a 32-bit number that identifies a device on a network. We write it as four **octets** separated by dots, like `192.168.1.10`. Each octet is 8 bits, so it ranges from 0 to 255. An address has two parts: a **network portion** (which network you are on) and a **host portion** (which specific device). The trick is knowing where one ends and the other begins — that is the job of the subnet mask.

## The subnet mask

A **subnet mask** is a second 32-bit number, such as `255.255.255.0`, that marks the network bits. Where the mask shows 255, those bits belong to the network; where it shows 0, those belong to the host. So with `192.168.1.10` and mask `255.255.255.0`, the network is `192.168.1` and the host is `10`. A device uses the mask to decide: is this destination on my local network, or must I send it to the **gateway**?

## CIDR notation

Writing full masks is clumsy, so we use **CIDR** notation: a slash and the number of network bits. `255.255.255.0` becomes `/24` because the first 24 bits are network. So `192.168.1.0/24` is a network with 24 network bits and 8 host bits. Eight host bits give 256 addresses, but two are reserved — the **network address** (`.0`) and the **broadcast address** (`.255`) — leaving **254 usable** hosts.

```text
192.168.1.0/24
  Network address:   192.168.1.0
  First usable host: 192.168.1.1   (often the gateway)
  Last usable host:  192.168.1.254
  Broadcast address: 192.168.1.255
```

## Private vs public addresses

The internet does not have enough IPv4 addresses for every device, so we reuse **private** ranges inside LANs. The RFC 1918 private ranges are `10.0.0.0/8`, `172.16.0.0/12`, and `192.168.0.0/16`. These never appear directly on the internet; your router uses **NAT** to share one **public** address among all your private devices. That is why every home router hands out `192.168.x.x` addresses.

## APIPA: the failure address

If a device asks for an address but no **DHCP** server answers, Windows assigns itself an **APIPA** address in the `169.254.0.0/16` range. Seeing `169.254.x.x` is a red flag: it means *I could not get a real address*. On the helpdesk, an APIPA address almost always points to a DHCP or physical connectivity problem.

```text
ipconfig
   Autoconfiguration IPv4 Address. . : 169.254.88.21   <-- APIPA = no DHCP
   Subnet Mask . . . . . . . . . . . : 255.255.0.0
```

## Your task

Run `ipconfig` (or `ip addr`) and record your IPv4 address, subnet mask, and gateway. Convert your mask to CIDR notation (for example `255.255.255.0` is `/24`). Then work out the network address and how many usable hosts your subnet supports. Finally, confirm your address is in a private range.
