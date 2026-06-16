---
course: helpdesk-tier1-2
title: The OSI and TCP/IP models made simple
month: 2
monthTitle: Networking Foundations (Network+)
lesson: 2
summary: Understand the seven OSI layers and the four-layer TCP/IP model, and learn to use them as a map
  for troubleshooting network problems methodically.
objectives:
- List the seven layers of the OSI model in order
- Map the four TCP/IP layers onto the OSI layers
- Explain what encapsulation means as data travels down the stack
- Give a real device or protocol example for each layer
- Use the layered model to localise a fault during troubleshooting
- Recall a mnemonic to remember the OSI layer order
video: hd2-l02-osi-and-tcpip-models.mp4
quiz:
- q: How many layers does the OSI model have?
  options:
  - Four
  - Five
  - Seven
  - Nine
  answer: 2
  why: The OSI model has seven layers, from Physical at layer 1 up to Application at layer 7.
- q: Which OSI layer does an IP address operate at?
  options:
  - Layer 2 (Data Link)
  - Layer 3 (Network)
  - Layer 4 (Transport)
  - Layer 7 (Application)
  answer: 1
  why: IP addresses and routing live at Layer 3, the Network layer, which handles logical addressing and
    path selection.
- q: A MAC address operates at which layer?
  options:
  - Layer 1 (Physical)
  - Layer 2 (Data Link)
  - Layer 3 (Network)
  - Layer 4 (Transport)
  answer: 1
  why: MAC addresses are used by switches at Layer 2, the Data Link layer, to move frames within a local
    network.
- q: What does the TCP/IP model's Transport layer provide?
  options:
  - Physical cabling
  - End-to-end delivery via TCP or UDP
  - Web page rendering
  - MAC addressing
  answer: 1
  why: The Transport layer uses TCP (reliable) or UDP (fast, connectionless) to deliver data end-to-end
    between applications using port numbers.
- q: Name a common mnemonic for the OSI layers from layer 1 up.
  answer: Please Do Not Throw Sausage Pizza Away
  why: 'Each word''s first letter maps to a layer from the bottom: Physical, Data Link, Network, Transport,
    Session, Presentation, Application.'
- q: In one sentence, why is the layered model useful for troubleshooting?
  answer: It lets you isolate a problem to one layer, so you can check the physical link, then addressing,
    then the application in a logical order instead of guessing.
  why: Working layer by layer turns vague 'the internet is down' tickets into a methodical bottom-up or
    top-down check that finds the real fault fast.
resources:
- label: Cloudflare Learning Center — What is the OSI model?
  url: https://www.cloudflare.com/learning/ddos/glossary/open-systems-interconnection-model-osi/
- label: Cloudflare Learning Center — Internet protocol suite (TCP/IP)
  url: https://www.cloudflare.com/learning/ddos/glossary/tcp-ip/
- label: Wikipedia — OSI model
  url: https://en.wikipedia.org/wiki/OSI_model
- label: Cisco — Networking basics
  url: https://www.cisco.com/c/en/us/solutions/small-business/resource-center/networking/networking-basics.html
---

## Why we need a model

Networking is complicated, so engineers split it into **layers**. Each layer has one job and talks only to the layers directly above and below it. Two models matter: the seven-layer **OSI model**, which is the teaching and troubleshooting reference, and the four-layer **TCP/IP model**, which is what the real internet actually runs on. You do not need to memorise everything — you need to use the layers as a **map**.

## The seven OSI layers

From the bottom up, the layers are **Physical, Data Link, Network, Transport, Session, Presentation, Application**. A classic mnemonic is *Please Do Not Throw Sausage Pizza Away*.

- **Layer 1 Physical** — cables, connectors, radio signals, voltages.
- **Layer 2 Data Link** — switches and **MAC addresses**; moves frames on the local network.
- **Layer 3 Network** — **IP addresses** and routers; chooses the path between networks.
- **Layer 4 Transport** — **TCP** and **UDP**; end-to-end delivery using **ports**.
- **Layer 5 Session** — sets up and tears down conversations.
- **Layer 6 Presentation** — formatting and encryption, like TLS.
- **Layer 7 Application** — what the user sees: HTTP, DNS, email.

## The TCP/IP model

The real-world **TCP/IP model** collapses these into four layers: **Network Access** (OSI 1-2), **Internet** (OSI 3, where IP lives), **Transport** (OSI 4, TCP/UDP), and **Application** (OSI 5-7). It maps cleanly onto OSI, so once you know one you understand the other.

## Encapsulation: data going down the stack

When you send data, each layer wraps it with its own header — this is **encapsulation**. Your message becomes a **segment** at Transport, gets an IP header to become a **packet** at the Network layer, then a MAC header to become a **frame** at the Data Link layer, and finally **bits** on the wire. The receiving device unwraps each layer in reverse. Knowing these names — segment, packet, frame — helps you read tools and documentation.

## Layers as a troubleshooting map

The real power of the model is fault isolation. When a user says "the internet is down," work the layers:

```bash
ping 127.0.0.1        # is the local TCP/IP stack alive? (Layer 3 locally)
ping 192.168.1.1      # can I reach my gateway? (Layers 1-3 on the LAN)
ping 8.8.8.8          # can I reach the internet by IP? (Layer 3 out)
nslookup example.com  # does name resolution work? (Layer 7 / DNS)
```

If the cable is unplugged, every ping fails — that is a **Layer 1** problem. If you can ping `8.8.8.8` but not a website name, the link is fine and the issue is **DNS at Layer 7**. The model tells you where to look instead of guessing.

## Your task

Write out the seven OSI layers from memory using the pizza mnemonic. Next to each, name one device or protocol that lives there (for example: Layer 2 = switch, Layer 3 = router/IP, Layer 7 = HTTP). Then run the four ping/nslookup commands above on your own machine and note which layer each one tests.
