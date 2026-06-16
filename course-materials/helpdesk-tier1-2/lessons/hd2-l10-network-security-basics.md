---
course: helpdesk-tier1-2
title: Network security basics
month: 2
monthTitle: Networking Foundations (Network+)
lesson: 10
summary: 'Finish the networking module with the security essentials every helpdesk technician needs: firewalls,
  VPNs, NAT, common attacks, and the principle of least privilege.'
objectives:
- Explain how firewalls protect a network with allow/deny rules
- Describe what a VPN does and when it is used
- Explain how NAT also provides a layer of protection
- Recognise common threats like phishing, malware and DoS
- Apply the principle of least privilege and defence in depth
- Check the Windows firewall status from the command line
video: hd2-l10-network-security-basics.mp4
quiz:
- q: What does a VPN provide?
  options:
  - An encrypted tunnel over an untrusted network
  - Faster internet always
  - Free Wi-Fi
  - A new IP subnet for the LAN
  answer: 0
  why: A VPN creates an encrypted tunnel so data travels securely across an untrusted network like public
    Wi-Fi or the internet, often to reach a company network remotely.
- q: What is the principle of least privilege?
  options:
  - Give every user admin rights for convenience
  - Give users only the access they need to do their job
  - Block all network traffic
  - Use one shared password
  answer: 1
  why: Least privilege means granting only the minimum access required, which limits the damage if an
    account is compromised.
- q: Which attack tricks a user into revealing credentials via a fake message?
  options:
  - DDoS
  - NAT
  - Phishing
  - Subnetting
  answer: 2
  why: Phishing uses deceptive emails or messages to trick users into giving up passwords or clicking
    malicious links; it is the most common entry point for breaches.
- q: How does NAT incidentally help security?
  options:
  - It encrypts all traffic
  - It hides internal private addresses behind one public address
  - It blocks all ports automatically
  - It replaces the firewall
  answer: 1
  why: NAT maps many private addresses to one public address, so internal devices are not directly addressable
    from the internet, adding a basic layer of protection.
- q: Name the term for using multiple overlapping layers of security.
  answer: Defence in depth
  why: Defence in depth layers controls (firewall, antivirus, least privilege, patching) so that if one
    fails, others still protect the system.
- q: In one sentence, why should a helpdesk technician care about network security?
  answer: Helpdesk staff are often the first to spot and respond to threats like phishing or unusual access,
    and small misconfigurations they make can open or close serious security holes.
  why: 'Tier 1 and 2 support sit at the front line: they reset passwords, configure access, and field
    the first reports of suspicious activity, so security is part of the daily job.'
resources:
- label: Cloudflare Learning Center — What is a VPN?
  url: https://www.cloudflare.com/learning/access-management/what-is-a-vpn/
- label: Cloudflare Learning Center — What is a firewall?
  url: https://www.cloudflare.com/learning/security/what-is-a-firewall/
- label: Cloudflare Learning Center — What is a DDoS attack?
  url: https://www.cloudflare.com/learning/ddos/what-is-a-ddos-attack/
- label: Microsoft Learn — Windows Defender Firewall overview
  url: https://learn.microsoft.com/en-us/windows/security/operating-system-security/network-security/windows-firewall/
---

## Security is everyone's job

Networks are useful because they connect things — and that is exactly why they need protecting. As a helpdesk technician you are on the **front line**: you reset passwords, grant access, and hear the first reports of something suspicious. You do not need to be a security specialist, but you must understand the basics so you protect users rather than accidentally exposing them.

## Firewalls: the rule keeper

A **firewall** sits between networks and decides what traffic to **allow** or **deny** based on rules. A sensible default is *deny inbound, allow outbound* — block unsolicited connections coming in, while letting your users reach out. Firewalls exist as hardware at the network edge and as software on each PC, such as **Windows Defender Firewall**. When a connection that should work is refused, a firewall rule is often why.

## VPNs: a private tunnel

A **VPN** (Virtual Private Network) creates an **encrypted tunnel** across an untrusted network. Two common uses: a **remote-access VPN** lets a home worker securely reach the office network, and a VPN on **public Wi-Fi** protects your traffic from anyone snooping on the same hotspot. Inside the tunnel, data is encrypted, so even if intercepted it cannot be read.

## NAT as quiet protection

You met **NAT** earlier as a way to share one public IP. It also helps security: because internal devices use private addresses hidden behind one public address, they are not directly reachable from the internet. NAT is not a firewall, but it does mean an attacker cannot simply dial up your laptop by its private address.

## Common threats to recognise

You will hear these terms constantly:

```text
Phishing   fake messages tricking users into giving up credentials
Malware    malicious software: viruses, ransomware, spyware
DoS/DDoS   flooding a service so it cannot respond
MITM       intercepting traffic between two parties
```

**Phishing** is the number-one way attackers get in, and it usually lands first with the people you support — so helping users spot it is real security work.

## Layering your defences

No single control is enough, so we use **defence in depth**: a firewall, antivirus, timely **patching**, strong unique passwords with **MFA**, and the **principle of least privilege** — giving each user only the access they actually need. If one layer fails, the others still stand. A user who only has the rights their job requires cannot accidentally (or maliciously) cause network-wide damage.

## Checking the firewall

Confirm the Windows firewall is protecting a machine from the command line:

```bash
netsh advfirewall show allprofiles

Domain Profile Settings:
  State                  ON
Private Profile Settings:
  State                  ON
Public Profile Settings:
  State                  ON
```

All profiles showing **ON** is what you want to see on a healthy endpoint.

## Your task

Run `netsh advfirewall show allprofiles` and confirm the Domain, Private, and Public profiles are all **ON**. Then write a short list of the layers of defence in depth you would recommend for a small office (firewall, antivirus, patching, MFA, least privilege). Finally, in one sentence, explain to an imaginary user how to recognise a phishing email.
