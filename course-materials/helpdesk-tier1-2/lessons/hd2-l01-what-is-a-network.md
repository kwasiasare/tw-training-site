---
course: helpdesk-tier1-2
title: What is a network? LAN, WAN and the internet
month: 2
monthTitle: Networking Foundations (Network+)
lesson: 1
summary: Learn what a computer network actually is, the difference between a LAN and a WAN, and how your
  home or office connects to the wider internet.
objectives:
- Define a computer network and explain why we build them
- Tell the difference between a LAN, a WAN, and the internet
- Describe the role of an Internet Service Provider (ISP)
- Identify common network types like PAN, MAN, and WLAN
- Explain client-server versus peer-to-peer in plain terms
- Find your own IP address from the command line
video: hd2-l01-what-is-a-network.mp4
quiz:
- q: What best describes a LAN?
  options:
  - A network spanning multiple cities
  - A network confined to a single building or site
  - The global internet itself
  - A single computer with no connection
  answer: 1
  why: A Local Area Network (LAN) covers a small area such as a home, office, or single building, where
    you control the equipment.
- q: What does an ISP provide?
  options:
  - Free hardware for every home
  - Your connection from your LAN to the internet
  - The websites you visit
  - Antivirus software
  answer: 1
  why: An Internet Service Provider connects your local network to the global internet, usually for a
    monthly fee.
- q: Which term describes the global network of networks?
  options:
  - LAN
  - PAN
  - The internet
  - VLAN
  answer: 2
  why: The internet is a worldwide collection of interconnected networks that communicate using common
    protocols.
- q: In a client-server model, what is the server's job?
  options:
  - To request services from other devices
  - To provide resources or services to clients
  - To replace the router
  - To assign physical cables
  answer: 1
  why: A server provides shared resources or services (files, web pages, email) that client devices request
    and consume.
- q: Name the network type that covers a city-sized area.
  answer: MAN (Metropolitan Area Network)
  why: A MAN spans a city or large campus, sitting between a LAN in size and a WAN in reach.
- q: In one sentence, what is the difference between a LAN and a WAN?
  answer: A LAN covers a small local area like one building, while a WAN connects multiple locations over
    long distances, often using links you do not own.
  why: 'The key distinction is geographic scope and ownership: LANs are local and private, WANs span large
    distances and usually rely on third-party links.'
resources:
- label: Cloudflare Learning Center — What is a LAN?
  url: https://www.cloudflare.com/learning/network-layer/what-is-a-lan/
- label: Cloudflare Learning Center — What is a WAN?
  url: https://www.cloudflare.com/learning/network-layer/what-is-a-wan/
- label: Wikipedia — Computer network
  url: https://en.wikipedia.org/wiki/Computer_network
- label: CompTIA — Network+ certification
  url: https://www.comptia.org/certifications/network
---

## Why we build networks

A **network** is simply two or more devices connected so they can share information and resources. Before networks, moving a file meant copying it to a disk and carrying it across the room. Today, networks let computers, phones, printers, and servers talk to each other instantly. Every helpdesk problem you will solve sits on top of a network, so this is the foundation for everything that follows.

The whole point is **sharing**: sharing files, sharing a printer, sharing an internet connection, and sharing services like email. When something stops being shared correctly, that is when the support tickets arrive.

## LAN: your local network

A **LAN** (Local Area Network) covers a small area you control — one home, one office, or one building. The devices connect through a **switch** and usually reach the internet through a **router**. A LAN is fast, private, and entirely yours to manage. The PCs in your office, joined by cables and Wi-Fi to the same router, form a LAN.

## WAN: connecting distant sites

A **WAN** (Wide Area Network) connects networks that are far apart — different cities or countries. Because you cannot run your own cable across a country, a WAN usually relies on links you rent from a provider. A company with offices in London and Manchester joined together is using a WAN. The **internet** is the largest WAN of all: a global network of networks.

## The internet and your ISP

The **internet** is not one machine; it is millions of networks agreeing to use the same rules to communicate. Your home or office reaches it through an **ISP** (Internet Service Provider), the company that sells you your connection. The ISP hands your router a public address and routes your traffic out to the wider world.

Other useful terms: a **PAN** (Personal Area Network) is tiny, like your phone paired to wireless earbuds; a **MAN** (Metropolitan Area Network) covers a city; and a **WLAN** is simply a LAN that uses Wi-Fi instead of cables.

## Clients and servers

Most networks follow a **client-server** model. A **server** provides something — web pages, files, email — and a **client** (your PC or phone) requests it. When you open a website, your browser is the client asking a web server for a page. In a smaller **peer-to-peer** setup, devices share directly with each other without a central server.

## Seeing your own network

You can inspect your computer's place on the network from the command line. On Windows:

```text
ipconfig

Wireless LAN adapter Wi-Fi:
   IPv4 Address. . . . . . . . . . . : 192.168.1.42
   Subnet Mask . . . . . . . . . . . : 255.255.255.0
   Default Gateway . . . . . . . . . : 192.168.1.1
```

That **IPv4 Address** is your device on the LAN, and the **Default Gateway** is your router — the door to the rest of the world.

## Your task

Open a command prompt on your PC and run `ipconfig` (or `ifconfig`/`ip addr` on macOS/Linux). Write down your IPv4 address, your subnet mask, and your default gateway. Then ping your gateway with `ping 192.168.1.1` (use your own gateway) and confirm you get replies.
