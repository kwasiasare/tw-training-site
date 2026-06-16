---
course: helpdesk-tier1-2
title: 'Network hardware: routers, switches, access points & firewalls'
month: 2
monthTitle: Networking Foundations (Network+)
lesson: 6
summary: 'Meet the physical devices that build a network: switches, routers, access points, and firewalls,
  and learn which OSI layer each one works at.'
objectives:
- Describe what a switch does and the layer it operates at
- Explain a router's job and how it differs from a switch
- Identify the purpose of a wireless access point
- Explain what a firewall does and where it sits
- Distinguish a modem and a gateway from a router
- Match each device to its OSI layer and typical use
video: hd2-l06-network-hardware.mp4
quiz:
- q: At which OSI layer does a traditional switch operate?
  options:
  - Layer 1 (Physical)
  - Layer 2 (Data Link)
  - Layer 3 (Network)
  - Layer 7 (Application)
  answer: 1
  why: A switch forwards frames using MAC addresses, which is Layer 2, the Data Link layer.
- q: What is a router's primary job?
  options:
  - To forward traffic between different networks using IP addresses
  - To connect devices within one LAN
  - To convert Wi-Fi to cable
  - To store files for the network
  answer: 0
  why: A router operates at Layer 3 and forwards packets between separate networks based on IP addresses,
    which is how your LAN reaches the internet.
- q: What does a wireless access point (WAP) do?
  options:
  - Assigns IP addresses
  - Blocks malicious traffic
  - Provides Wi-Fi connectivity that bridges wireless devices onto the wired LAN
  - Converts the ISP signal
  answer: 2
  why: An access point lets wireless devices join the wired network, effectively extending the LAN over
    radio at Layer 2.
- q: What is the main purpose of a firewall?
  options:
  - To speed up the network
  - To filter traffic and allow or block it based on rules
  - To assign MAC addresses
  - To provide Wi-Fi
  answer: 1
  why: A firewall inspects traffic and permits or denies it according to security rules, protecting the
    network from unwanted connections.
- q: What device converts your ISP's incoming signal into Ethernet?
  answer: A modem
  why: A modem modulates and demodulates the signal from your ISP (cable, fibre, or DSL) into Ethernet
    that your router and LAN can use.
- q: In one sentence, how does a switch differ from a router?
  answer: A switch connects devices within the same local network using MAC addresses at Layer 2, while
    a router connects different networks together using IP addresses at Layer 3.
  why: Switches keep traffic moving inside one LAN; routers decide how to send traffic between networks,
    including out to the internet.
resources:
- label: Cloudflare Learning Center — What is a network switch?
  url: https://www.cloudflare.com/learning/network-layer/what-is-a-network-switch/
- label: Cloudflare Learning Center — What is a router?
  url: https://www.cloudflare.com/learning/network-layer/what-is-a-router/
- label: Cloudflare Learning Center — What is a firewall?
  url: https://www.cloudflare.com/learning/security/what-is-a-firewall/
- label: Cisco — What is a network switch vs a router?
  url: https://www.cisco.com/c/en/us/solutions/small-business/resource-center/networking/network-switch-vs-router.html
---

## The boxes that build a network

A network is not just cables and addresses — it is a set of physical **devices**, each with a job. On the helpdesk you will point at these boxes daily, so you need to know what each one does and which **OSI layer** it works at. The four you must master are the **switch**, the **router**, the **access point**, and the **firewall**.

## The switch: connecting the LAN

A **switch** connects devices within a single LAN. It operates at **Layer 2** and forwards data using **MAC addresses**. When a frame arrives, the switch checks its MAC address table and sends it only out of the port where that device lives — efficient and private. A small office might have one 24-port switch joining every PC, printer, and server. Switches do not understand IP addresses or the internet; they just move frames around the local network quickly.

## The router: connecting networks

A **router** connects *different* networks together. It works at **Layer 3** using **IP addresses** and decides the best path for a packet to take. Your home router's main job is to forward traffic between your private LAN and the internet. Routers also run **NAT**, sharing one public IP among many private devices, and usually act as your **default gateway**.

```text
Your PC (192.168.1.42)
   |
  Switch  (Layer 2, MAC addresses)
   |
  Router  (Layer 3, IP addresses, NAT, gateway)
   |
  Internet
```

## Access points and wireless

A **wireless access point** (WAP) lets Wi-Fi devices join the wired network. It bridges radio signals onto the LAN, effectively extending Layer 2 over the air. In a home, the access point is usually built into the router. In an office, you will see separate ceiling-mounted access points so coverage reaches every corner.

## Firewalls: the security guard

A **firewall** inspects traffic and allows or blocks it based on **rules**. It can be a dedicated hardware box at the network edge, or software running on each PC (like Windows Defender Firewall). A firewall is how you stop unwanted connections — for example, blocking inbound traffic on every port except the few services you actually publish. When a connection that "should work" is refused, a firewall rule is a prime suspect.

## Modems, gateways, and combo boxes

A **modem** converts your ISP's signal (cable, fibre, DSL) into Ethernet your network can use. A **gateway** is simply the device that connects you to another network — usually your router. Confusingly, most home "routers" are **combo** units packing a modem, router, switch, access point, and firewall into one box. Knowing the separate roles helps you reason about faults even when they share a case.

## Your task

Look at the network device in your home or office. List which roles it combines (router, switch, access point, firewall, modem). Then run `ipconfig` and confirm your **default gateway** is the router's address. Finally, open Windows Defender Firewall settings and note whether it is turned on for your active network — that is a software firewall doing exactly what this lesson describes.
