---
course: helpdesk-tier1-2
title: Wi-Fi and wireless networking
month: 2
monthTitle: Networking Foundations (Network+)
lesson: 7
summary: Understand how Wi-Fi works, the 2.4 GHz and 5 GHz bands, the 802.11 standards, and the security
  and interference issues you will troubleshoot on the helpdesk.
objectives:
- Explain how Wi-Fi carries data over radio frequencies
- Compare the 2.4 GHz and 5 GHz bands and their trade-offs
- Identify the main 802.11 standards including Wi-Fi 5 and Wi-Fi 6
- Describe wireless security types and why WPA2/WPA3 matter
- Diagnose common wireless problems like interference and channel overlap
- Read wireless adapter details from the command line
video: hd2-l07-wifi-and-wireless.mp4
quiz:
- q: What is the main trade-off of the 2.4 GHz band versus 5 GHz?
  options:
  - 2.4 GHz is faster but shorter range
  - 2.4 GHz has longer range but is slower and more congested
  - They are identical
  - 5 GHz cannot carry data
  answer: 1
  why: 2.4 GHz travels further and through walls better but is slower and crowded; 5 GHz is faster with
    more channels but has shorter range.
- q: Which is the most secure wireless encryption listed?
  options:
  - WEP
  - WPA
  - WPA2
  - WPA3
  answer: 3
  why: WPA3 is the newest and most secure standard; WEP is badly broken and WPA is outdated, so WPA2 or
    WPA3 should always be used.
- q: On the 2.4 GHz band, which channels are non-overlapping?
  options:
  - 1, 2, 3
  - 1, 6, 11
  - 2, 4, 6
  - All channels overlap equally
  answer: 1
  why: Channels 1, 6, and 11 are the three non-overlapping channels on 2.4 GHz, so neighbouring access
    points should use these to avoid interference.
- q: What does the SSID identify?
  options:
  - The encryption key
  - The name of a wireless network
  - The router's MAC address
  - The IP subnet
  answer: 1
  why: The SSID (Service Set Identifier) is the broadcast name of a Wi-Fi network that users see and connect
    to.
- q: Name the Wi-Fi standard also known as Wi-Fi 6.
  answer: 802.11ax
  why: 802.11ax is branded Wi-Fi 6, offering higher throughput and better performance in crowded environments
    than the earlier 802.11ac (Wi-Fi 5).
- q: In one sentence, why might a user near a microwave oven get poor Wi-Fi?
  answer: Microwave ovens emit energy in the 2.4 GHz range, which interferes with 2.4 GHz Wi-Fi and degrades
    the signal nearby.
  why: The 2.4 GHz band is shared with microwaves, cordless phones, and Bluetooth, so these devices cause
    interference that drops throughput.
resources:
- label: Cloudflare Learning Center — What is Wi-Fi?
  url: https://www.cloudflare.com/learning/network-layer/what-is-wifi/
- label: Wikipedia — IEEE 802.11 (Wi-Fi standards)
  url: https://en.wikipedia.org/wiki/IEEE_802.11
- label: Wikipedia — Wi-Fi Protected Access (WPA/WPA2/WPA3)
  url: https://en.wikipedia.org/wiki/Wi-Fi_Protected_Access
- label: Microsoft Learn — netsh wlan commands
  url: https://learn.microsoft.com/en-us/windows-server/networking/technologies/netsh/netsh-wlan
---

## How Wi-Fi actually works

**Wi-Fi** carries data over **radio waves** instead of cables, following the **IEEE 802.11** family of standards. A **wireless access point** broadcasts a network name, the **SSID**, and devices that know the password join it. Because radio is a shared, invisible medium, Wi-Fi brings unique problems — range limits, interference, and security — that wired networks never face. Most of your wireless tickets come down to **signal**, **channel**, or **security**.

## The two bands: 2.4 GHz and 5 GHz

Wi-Fi runs mainly on two frequency **bands**. **2.4 GHz** travels further and penetrates walls better, but it is slower and badly congested — it is shared with microwaves, cordless phones, and Bluetooth. **5 GHz** is much faster with more channels and less interference, but its shorter range struggles with walls. Newer kit adds **6 GHz** (Wi-Fi 6E). A good rule: 2.4 GHz for range, 5 GHz for speed.

## The 802.11 standards

You will see these on every device's spec sheet:

```text
802.11n   Wi-Fi 4   2.4 & 5 GHz
802.11ac  Wi-Fi 5   5 GHz, fast
802.11ax  Wi-Fi 6   2.4, 5 (& 6 GHz as 6E), best in crowds
```

Each newer standard is faster and handles crowded environments better, while staying backward-compatible with older devices.

## Channels and interference

Each band is split into **channels**. On 2.4 GHz the channels overlap, and only **1, 6, and 11** are truly non-overlapping. If two nearby access points share a channel, they interfere and both slow down. A common fix for a slow office Wi-Fi is simply moving neighbouring access points onto channels 1, 6, and 11. Physical interference — thick walls, microwaves, even fish tanks — also drops signal, especially on 2.4 GHz.

## Wireless security

Because anyone in range can hear the radio, **encryption** is essential. The standards, oldest to newest:

```text
WEP   broken, never use
WPA   outdated
WPA2  the long-standing baseline (AES)
WPA3  current best, stronger and safer
```

Always use **WPA2** or **WPA3**. If you ever see a network still on **WEP**, that is a security finding to escalate. A strong passphrase and a hidden management interface round out basic Wi-Fi security.

## Reading wireless details

Windows shows your wireless adapter, the connected SSID, signal, and standard from the command line:

```bash
netsh wlan show interfaces

    SSID          : OfficeWiFi
    Signal        : 86%
    Radio type    : 802.11ax
    Band          : 5 GHz
    Channel       : 44
```

A low **Signal** percentage explains slow or dropping connections, and the **Channel** and **Band** help you spot congestion.

## Your task

Run `netsh wlan show interfaces` and record your SSID, signal strength, radio type (802.11 standard), band, and channel. Then run `netsh wlan show networks mode=bssid` to list nearby networks and their channels. Note whether neighbouring 2.4 GHz networks are spread across channels 1, 6, and 11 or stacked on top of each other.
