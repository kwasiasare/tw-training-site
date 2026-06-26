---
course: cloud-security-engineer
title: 'Azure Network Security: NSGs, Firewall, and Private Link'
month: 6
monthTitle: 'Azure Platform Security: Storage, Databases & Networking'
lesson: 3
summary: 'Network security in Azure is defense in depth, and the senior skill is knowing exactly
  which layer each control defends. This lesson maps the toolkit by layer: Network Security Groups
  filter at Layer 3-4, Azure Firewall spans Layer 3 to Layer 7, Web Application Firewall inspects
  HTTP at Layer 7, and DDoS Protection absorbs volumetric attacks at Layer 3-4. You will write stateful NSG rules with
  priorities, service tags, and Application Security Groups, then centralize egress through Azure
  Firewall in a hub-and-spoke topology with FQDN filtering, threat intelligence, and Premium IDPS
  and TLS inspection. You will remove public exposure entirely with Private Endpoints and Private
  Link, understand how that differs from Service Endpoints, and lock down administrative access with
  Azure Bastion and Just-in-Time VM access instead of internet-facing RDP and SSH. Finally you will
  turn on VNet flow logs and Traffic Analytics so every flow is visible in Log Analytics and Sentinel.
  The throughline is layered network controls and private-by-default connectivity.'
objectives:
- Author stateful NSG rules using priority ordering, default rules, service tags, and ASGs
- Decide between subnet and NIC association and between NSGs and Azure Firewall
- Centralize egress through Azure Firewall with FQDN filtering, threat intel, and Premium IDPS/TLS
- Place each control at its layer — NSG and DDoS at L3-4, Azure Firewall at L3-L7, and WAF at L7
- Remove public exposure with Private Endpoints and Private Link, and contrast Service Endpoints
- Secure administrative access with Azure Bastion and Just-in-Time VM access
- Gain visibility with Network Watcher, VNet flow logs, and Traffic Analytics into Sentinel
video: cse-m6-l03-azure-network-security.mp4
quiz:
- q: How are Network Security Group rules evaluated when traffic arrives?
  options:
  - All rules are evaluated and the most permissive wins
  - Rules are processed in priority order, highest number first, and all must allow
  - Rules are processed in priority order, lowest number first, and the first match (allow or deny)
    stops evaluation
  - Rules are evaluated randomly until a deny is found
  answer: 2
  why: NSGs are stateful and evaluate rules by priority from the lowest number (highest priority)
    to the highest. The first rule that matches the 5-tuple is applied and processing stops, so a
    lower-numbered allow can override a higher-numbered deny. Default rules (priorities 65000-65500)
    sit at the bottom, allowing intra-VNet and load balancer traffic and denying everything else inbound.
- q: What does an Application Security Group (ASG) let you do that a raw IP-based rule does not?
  options:
  - Inspect HTTP request bodies for SQL injection
  - Group VMs by workload role so NSG rules reference the group instead of hardcoded IP addresses
  - Absorb volumetric DDoS attacks at the network edge
  - Encrypt traffic between two subnets automatically
  answer: 1
  why: An ASG is a logical grouping of network interfaces by application role (for example web or
    db). NSG rules can use ASGs as source or destination, so you write intent-based rules like "allow
    web to db on 1433" without maintaining IP lists. As VMs scale in and out, membership updates and
    the rules keep working, which is far more maintainable than static IP prefixes.
- q: A workload must reach Azure Storage with no traffic traversing the public internet and no public
    endpoint exposed. Which option best meets this?
  options:
  - A Private Endpoint, which projects a private IP from your subnet to the storage account over Private
    Link and is resolved via a private DNS zone
  - A Service Endpoint, because it gives the storage account a private IP in your VNet
  - An NSG rule allowing the Storage service tag outbound
  - Azure Firewall application rule allowing the storage FQDN
  answer: 0
  why: A Private Endpoint creates a network interface with a private IP from your subnet that maps
    to the PaaS resource through Azure Private Link, and a private DNS zone (privatelink.blob.core.windows.net)
    resolves the public name to that private IP. The public endpoint can then be disabled. A Service
    Endpoint keeps the resource's public IP and only optimizes the path plus VNet firewall rules, so
    it does not remove public exposure.
- q: At which layer does a Web Application Firewall operate, and how does it differ from an NSG?
  options:
  - Layer 3-4, identical to an NSG but faster
  - Layer 7 (HTTP/HTTPS), inspecting request content for attacks like SQL injection and XSS, whereas
    an NSG filters by IP, port, and protocol at Layer 3-4
  - Layer 2, filtering MAC addresses
  - Layer 7, but only for outbound traffic
  answer: 1
  why: A WAF on Application Gateway (regional) or Azure Front Door (global edge) is a Layer 7 reverse
    proxy that inspects HTTP requests against managed rule sets (the OWASP Core Rule Set) to block
    injection, cross-site scripting, and similar attacks. An NSG and Azure Firewall operate at Layer
    3-4 on addresses and ports and cannot see inside an HTTP payload, which is why you layer a WAF
    in front of web apps.
- q: Why deploy Azure Bastion and Just-in-Time VM access instead of opening RDP/SSH to the internet?
  options:
  - They make VMs run faster
  - They eliminate standing internet-exposed management ports; Bastion gives browser-based RDP/SSH
    with no public IP on the VM, and JIT opens ports only on demand for a limited time
  - They are required for VNet peering to work
  - They replace the need for any NSG rules
  answer: 1
  why: Internet-exposed RDP (3389) and SSH (22) are a primary brute-force and ransomware entry point.
    Azure Bastion is a managed PaaS jumpbox that brokers RDP/SSH over TLS in the browser so VMs need
    no public IP. Just-in-Time VM access (a Defender for Servers feature) keeps the management ports
    closed in the NSG and opens them only for a requested source, port, and time window, shrinking
    the exposure window to near zero.
- q: In 3-4 sentences, explain the role of Azure Firewall in a hub-and-spoke topology and how forced
    tunneling or a default route changes traffic flow. Name one Premium-tier capability.
  options:
  answer: In a hub-and-spoke design, Azure Firewall is deployed in the hub VNet as a central, stateful,
    managed egress and inspection point for all spoke workloads. You attach a user-defined route (UDR)
    with a 0.0.0.0/0 default route whose next hop is the firewall's private IP to the spoke subnets,
    forcing all outbound (and inter-spoke) traffic through the firewall for network, application (FQDN),
    and threat-intelligence filtering instead of letting it egress directly to the internet. Forced
    tunneling extends this by routing the firewall's own internet-bound traffic back to an on-premises
    edge over VPN/ExpressRoute for inspection there. One Premium-tier capability is IDPS (intrusion
    detection and prevention) or TLS inspection, which decrypts and inspects outbound HTTPS for signatures.
  why: Azure Firewall centralizes egress control in the hub; a default route (0.0.0.0/0 to the firewall
    private IP) forces spoke traffic through it, and forced tunneling sends internet-bound traffic
    to on-prem. Premium adds IDPS and TLS inspection. This is the canonical secure hub-and-spoke pattern.
resources:
- label: Network security groups overview
  url: https://learn.microsoft.com/en-us/azure/virtual-network/network-security-groups-overview
- label: What is Azure Firewall?
  url: https://learn.microsoft.com/en-us/azure/firewall/overview
- label: What is Azure Private Link?
  url: https://learn.microsoft.com/en-us/azure/private-link/private-link-overview
- label: What is Azure Bastion?
  url: https://learn.microsoft.com/en-us/azure/bastion/bastion-overview
- label: VNet flow logs
  url: https://learn.microsoft.com/en-us/azure/network-watcher/vnet-flow-logs-overview
---

## Defense in Depth: Know Your Layer

The single most important habit in Azure network security is to know **which OSI layer each control defends**, because each tool sees a different part of the traffic and they are meant to stack:

- **Network Security Groups (NSGs)** — **Layer 3-4** only. They filter on IP address, port, and protocol and cannot read inside an HTTP request.
- **Azure Firewall** — primarily **Layer 3-4**, but also **Layer 7-aware**: its application rules filter by FQDN/URL (reading the HTTP Host header / TLS SNI), and the Premium SKU adds IDPS and TLS inspection (L3-L7).
- **Web Application Firewall (WAF)** — **Layer 7**. It is an HTTP-aware reverse proxy that inspects the HTTP request content and body for injection and cross-site scripting, which Azure Firewall application rules do not.
- **Azure DDoS Protection** — **Layer 3-4**, absorbing volumetric and protocol floods before they reach your resources.
- **Private Link / Private Endpoints** — not a filter at all but a **connectivity** control: it replaces a public IP with a **private IP plus private DNS** so the resource is never on the internet.

A senior design uses all of them together: DDoS at the edge, a WAF in front of web apps, NSGs and Azure Firewall segmenting and controlling east-west and egress traffic, and Private Endpoints removing public PaaS exposure entirely.

## Network Security Groups (NSGs)

An **NSG** is a **stateful** packet filter you attach to a **subnet** or a **NIC** (or both). Stateful means you allow a flow in one direction and the return traffic is permitted automatically — you do not write a matching reverse rule.

Each rule is a 5-tuple match — **source**, **source port**, **destination**, **destination port**, **protocol** — plus a **priority** (100-4096) and an **allow/deny** action. The mechanics that trip people up:

- Rules are processed **lowest priority number first**. The **first match wins** and evaluation stops, so a priority-200 allow beats a priority-300 deny.
- Every NSG ships with **default rules** at priorities 65000-65500 that you cannot delete: inbound allows intra-VNet traffic (`AllowVNetInBound`) and the Azure load balancer, then `DenyAllInBound`; outbound allows VNet and internet, then `DenyAllOutBound`. Your rules sit *above* these defaults.
- **Subnet vs NIC**: a subnet NSG applies to every NIC in the subnet (broad, coarse); a NIC NSG applies to one VM (granular). When both are present, inbound traffic is evaluated at the **subnet first then the NIC**, and outbound the reverse — and traffic must be allowed by **both**.

```bash
# Allow HTTPS from the internet to the web tier
az network nsg rule create \
  --resource-group rg-prod --nsg-name nsg-web \
  --name Allow-HTTPS-Inbound --priority 200 \
  --direction Inbound --access Allow --protocol Tcp \
  --source-address-prefixes Internet \
  --destination-port-ranges 443 \
  --destination-asgs asg-web
```

## Service Tags and Application Security Groups

Two features make NSG rules maintainable at scale instead of brittle IP lists:

- **Service tags** are Microsoft-managed labels for the IP ranges of a service — `Internet`, `VirtualNetwork`, `AzureLoadBalancer`, `Storage`, `Sql`, `AzureKeyVault`, `AzureCloud`, and many regional variants. Microsoft updates the underlying prefixes for you, so a rule that allows the `Storage` tag keeps working as Azure's address space changes.
- **Application Security Groups (ASGs)** are logical groupings of **NICs by workload role**. You put your web VMs in `asg-web` and your database VMs in `asg-db`, then write intent-based rules — *allow `asg-web` to `asg-db` on 1433* — without referencing a single IP. As the workload scales in and out, ASG membership follows the VMs and the rules keep holding. This is the modern, declarative way to do microsegmentation inside a VNet.

## Azure Firewall

NSGs are great for cheap, distributed Layer 3-4 segmentation, but they have no FQDN awareness, no centralized logging, and no threat intelligence. **Azure Firewall** is the managed, stateful, highly available **network firewall-as-a-service** you put in the **hub** of a hub-and-spoke topology to control and inspect traffic centrally.

Rules live in a **Firewall Policy** and are organized into **rule collections**, processed in a fixed order:

1. **DNAT rules** — translate an inbound public IP:port to a private destination (publishing a service).
2. **Network rules** — Layer 3-4 allow/deny by IP, port, protocol, and **service tags / FQDN tags**.
3. **Application rules** — Layer 7-aware **FQDN filtering** for HTTP/S and SQL, e.g. allow outbound only to `*.windowsupdate.com` or `*.ubuntu.com`.

On top, **threat intelligence-based filtering** supports two modes — **Alert only**, or **Alert and deny** — for traffic to and from known-malicious IPs and domains from the Microsoft Threat Intelligence feed. To make the firewall the actual egress point, you attach a **user-defined route (UDR)** to each spoke subnet with a **default route `0.0.0.0/0` whose next hop is the firewall's private IP** — now all outbound and inter-spoke traffic is forced through it. **Forced tunneling** extends this by routing the firewall's own internet-bound traffic back to an on-premises edge over VPN/ExpressRoute for inspection there.

```bicep
// Force all spoke egress through the hub firewall
resource udr 'Microsoft.Network/routeTables@2023-09-01' = {
  name: 'rt-spoke-default'
  location: location
  properties: {
    routes: [
      {
        name: 'default-to-firewall'
        properties: {
          addressPrefix: '0.0.0.0/0'
          nextHopType: 'VirtualAppliance'
          nextHopIpAddress: '10.0.1.4' // Azure Firewall private IP
        }
      }
    ]
  }
}
```

## Azure Firewall Premium: IDPS and TLS Inspection

The **Premium** SKU adds two capabilities that matter for regulated and high-assurance estates:

- **IDPS (Intrusion Detection and Prevention System)** — signature-based detection that can **alert** or **alert and deny** on known exploit patterns in network traffic, including matching against thousands of rules updated by Microsoft.
- **TLS inspection** — the firewall **decrypts outbound HTTPS**, inspects the plaintext (so IDPS and application rules can see the real content), then re-encrypts. It uses an intermediate CA certificate, typically issued from your own **Key Vault**, that clients trust.

Premium also brings **URL filtering** (beyond whole-FQDN) and **web categories**. The trade-off is cost and the operational care TLS inspection demands, so most teams enable it selectively on the egress paths that need deep inspection.

## Web Application Firewall (WAF) at Layer 7

NSGs and Azure Firewall cannot see that a request body contains `' OR 1=1--`. That is the job of the **Web Application Firewall**, a **Layer 7** control that runs in one of two places:

- **Application Gateway WAF** — a **regional** Layer 7 load balancer / reverse proxy in front of web apps in a VNet.
- **Azure Front Door WAF** — a **global**, edge-based WAF for internet-facing apps, blocking attacks close to the user.

Both use **Microsoft-managed rule sets** built on the **OWASP Core Rule Set (CRS)** to block injection, cross-site scripting, and other Top 10 attacks, plus optional **bot protection** and custom rate-limit/geo rules. The critical operational setting is the mode:

- **Detection mode** — logs what *would* be blocked, used to tune rules and find false positives without breaking the app.
- **Prevention mode** — actually **blocks** matching requests.

The standard rollout is to run in detection first, tune out false positives, then switch to prevention.

## Azure DDoS Protection

Every Azure public IP gets **always-on, platform-level** DDoS defense for free (basic infrastructure protection). The **paid tiers** add adaptive, application-aware mitigation:

- **DDoS Network Protection** — enabled on a **VNet**, it protects **all public IP resources** in that VNet with adaptive real-time tuning, attack analytics and metrics, **mitigation reports**, **cost protection** (credits for scale-out during an attack), and access to the DDoS Rapid Response team.
- **DDoS IP Protection** — a lower-cost, **per-public-IP** tier for when you only need to protect a few addresses rather than a whole VNet.

DDoS Protection operates at **Layer 3-4** against volumetric and protocol floods; pair it with a **WAF** for Layer 7 application-layer attacks, since the two cover different layers.

## Private Link and Private Endpoints

By default, Azure PaaS services (Storage, SQL, Key Vault) have a **public endpoint**. Even with the resource firewall locked down, that public surface exists. **Azure Private Link** removes it.

A **Private Endpoint** is a **NIC with a private IP from your subnet** that maps to a specific PaaS resource (and sub-resource, like the `blob` of a storage account) over the Microsoft backbone. A **private DNS zone** — for example `privatelink.blob.core.windows.net` — overrides the public name so clients resolve the service to its **private IP**. You then **disable the public endpoint** entirely. Traffic never touches the internet.

Do not confuse this with a **Service Endpoint**, which is weaker:

- A **Service Endpoint** keeps the resource's **public IP**; it just optimizes routing over the backbone and lets the resource firewall trust a specific subnet (a VNet rule). The service is still publicly addressable.
- A **Private Endpoint** gives the resource a **private IP in your VNet**, supports on-premises access over VPN/ExpressRoute, and lets you turn the public endpoint off.

For a zero-trust data plane, prefer Private Endpoints.

```bash
# Create a private endpoint to a storage account's blob service
az network private-endpoint create \
  --resource-group rg-prod --name pe-storage-blob \
  --vnet-name vnet-hub --subnet snet-privateendpoints \
  --private-connection-resource-id \
    $(az storage account show -g rg-prod -n stcontoso --query id -o tsv) \
  --group-id blob --connection-name conn-blob
```

## Secure Administrative Access: Bastion and JIT

Open RDP (3389) and SSH (22) on a public IP is one of the most exploited attack surfaces in the cloud. Two services let you manage VMs without it:

- **Azure Bastion** — a managed PaaS jumpbox deployed into a dedicated `AzureBastionSubnet`. It brokers **RDP and SSH over TLS in the browser**, so your VMs need **no public IP** and no agent, and the management ports are never exposed to the internet.
- **Just-in-Time (JIT) VM access** — a **Defender for Servers** feature that keeps the management ports **closed in the NSG** and opens them only when a user **requests access**, scoped to a source IP, port, and **time window** (after which they auto-close). Combined, Bastion provides the connectivity and JIT shrinks the exposure window to near zero.

## Visibility: Network Watcher, Flow Logs, and Traffic Analytics

You cannot secure traffic you cannot see. **Network Watcher** is the regional diagnostics service for Azure networking, with tools like **IP flow verify**, **next hop**, and **connection troubleshoot** to test whether an NSG or route is doing what you think.

For continuous visibility, enable **VNet flow logs** (the successor to NSG flow logs, which Microsoft is retiring) — they record **allowed and denied flows** at the virtual network level to a storage account. Layer **Traffic Analytics** on top to process those raw logs into a **Log Analytics workspace**, enriched with geography, threat context, and topology, and queryable with KQL or pulled into **Microsoft Sentinel** for correlation with identity and endpoint signals:

```kusto
// Top denied / malicious flows from VNet flow logs via Traffic Analytics
NTANetAnalytics
| where TimeGenerated > ago(24h)
| where SubType == "FlowLog" and FlowType in ("MaliciousFlow", "ExternalPublic")
| where FlowStatus == "D"   // Denied
| summarize Flows = count() by SrcIp, DestIp, DestPort, L7Protocol
| sort by Flows desc
```

That closes the loop: layered controls from Layer 3-4 to Layer 7, private-by-default connectivity to PaaS, hardened administrative access, and full flow visibility flowing into the same SOC you built earlier in the course. With storage, databases, and networking secured, the platform is ready for the capstone projects in Module 7.
