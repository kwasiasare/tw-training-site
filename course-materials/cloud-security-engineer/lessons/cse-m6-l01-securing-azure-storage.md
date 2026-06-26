---
course: cloud-security-engineer
title: Securing Azure Storage Accounts
month: 6
monthTitle: 'Azure Platform Security: Storage, Databases & Networking'
lesson: 1
summary: 'A storage account is one of the most attacked resources in Azure: it holds the data, and
  it is reachable over the internet by default. This lesson hardens it end to end. You will confirm
  that data at rest is always encrypted with 256-bit AES and decide when platform-managed keys are
  enough versus when you need customer-managed keys in Key Vault or optional infrastructure (double)
  encryption. You will enforce HTTPS-only transfer and a minimum TLS of 1.2, then move the data plane
  off account keys entirely by using Microsoft Entra ID with Azure RBAC data roles, disabling shared
  key authorization, and preferring user delegation SAS over account-key SAS. You will lock down the
  network with the storage firewall, service endpoints, and Private Endpoints, build ransomware
  resilience with soft delete, versioning, point-in-time restore, and immutable WORM policies, and
  turn on Microsoft Defender for Storage plus diagnostic logging into Sentinel. The throughline is
  defense in depth on the data plane: encrypt everything, prove identity, shrink the network, and
  make the data recoverable and watched.'
objectives:
- Confirm encryption at rest and choose platform-managed keys, customer-managed keys, or infrastructure encryption
- Enforce encryption in transit with secure transfer required and a minimum TLS version of 1.2
- Replace account-key access with Microsoft Entra ID and Azure RBAC data-plane roles, and disable shared key authorization
- Apply least-privilege SAS, preferring user delegation SAS over account/service SAS with short expiry and stored access policies
- Restrict network exposure with the storage firewall, service endpoints, and Private Endpoints
- Build ransomware resilience with soft delete, versioning, point-in-time restore, and immutability (WORM)
- Enable Microsoft Defender for Storage and stream diagnostic logs to Log Analytics and Sentinel
video: cse-m6-l01-securing-azure-storage.mp4
quiz:
- q: Which statement about Azure Storage encryption at rest is correct?
  options:
  - Encryption at rest is optional and must be enabled per account
  - All data is always encrypted with 256-bit AES; you cannot turn it off, but you can supply your own key
  - Encryption only applies to blobs, not files, queues, or tables
  - Encryption at rest requires the premium performance tier
  answer: 1
  why: Azure Storage service-side encryption is always on for every account and resource type (blobs,
    files, queues, tables, disks) using 256-bit AES, and it cannot be disabled. What you choose is key
    management, Microsoft-managed keys by default, or customer-managed keys (CMK) in Azure Key Vault or
    Managed HSM, with optional infrastructure (double) encryption for a second layer.
- q: You want to prevent anyone from using the account access keys to reach blob data, so that all
    access goes through Microsoft Entra ID. What do you configure?
  options:
  - Rotate both account keys every 24 hours
  - Set allowSharedKeyAccess to false to disallow Shared Key authorization on the account
  - Delete key1 and keep only key2
  - Enable a read-only lock on the storage account
  answer: 1
  why: Setting allowSharedKeyAccess=false disallows Shared Key authorization, so requests signed with
    the account keys (and account/service SAS derived from them) are rejected; only Microsoft Entra ID
    authorization is accepted. This is also a prerequisite for protecting the account with Entra
    Conditional Access. Rotating or deleting keys does not stop key-based access by itself.
- q: Which SAS type is the most secure and why?
  options:
  - Account SAS, because it can grant access to every service at once
  - Service SAS, because it never expires
  - User delegation SAS, because it is signed with Microsoft Entra credentials instead of the account key
  - A SAS embedded in the connection string, because it is easiest to distribute
  answer: 2
  why: A user delegation SAS is secured with a user delegation key obtained from Microsoft Entra ID
    rather than the storage account key, so it carries the signer's identity, can be constrained by RBAC,
    and is not invalidated by account-key rotation. Account and service SAS are signed with the account
    key, are harder to revoke, and keep you dependent on shared-key authorization.
- q: What is the most effective way to make a storage account unreachable from the public internet
    while still allowing a VM in your virtual network to use it?
  options:
  - Enable secure transfer required
  - Create a Private Endpoint and set public network access to disabled
  - Add the VM's public IP to the storage firewall allow list
  - Turn on blob versioning
  answer: 1
  why: A Private Endpoint gives the storage account a private IP inside your VNet and, combined with
    public network access disabled, removes the public endpoint entirely so traffic stays on the Microsoft
    backbone. Secure transfer and versioning do not control network reachability, and allow-listing a
    public IP still leaves the public endpoint exposed.
- q: Which combination of features provides ransomware resilience for blob data?
  options:
  - Soft delete, versioning, point-in-time restore, and immutable (WORM) policies
  - Premium performance tier and the hot access tier
  - Geo-redundant storage alone
  - Customer-managed keys alone
  answer: 0
  why: Soft delete retains deleted blobs and containers for a recovery window, versioning preserves
    prior versions on overwrite, point-in-time restore rolls a container back to an earlier state, and
    time-based or legal-hold immutability makes data WORM (write once, read many) so even an admin cannot
    alter or delete it during the retention period. Encryption and redundancy protect confidentiality and
    availability but do not by themselves let you recover from malicious deletion or overwrite.
- q: In 3-4 sentences, explain why moving the storage data plane from account keys to Microsoft Entra ID
    plus Azure RBAC improves security, and name one role you would assign for read-only blob access.
  options: null
  answer: Account keys are long-lived shared secrets that grant full control of all data in the account
    and can generate SAS tokens, so anyone who obtains a key effectively owns the data and the access is
    hard to attribute or revoke without rotating the key and breaking other consumers. Microsoft Entra ID
    with Azure RBAC instead authenticates a specific user or managed identity and authorizes only the
    least-privilege data action they need, with full audit, Conditional Access, and central revocation.
    For read-only blob access you would assign the Storage Blob Data Reader role, scoped to the container
    or account; Storage Blob Data Contributor or Owner grant write and delete. Disabling shared key
    authorization then guarantees every request is identity-based.
  why: Entra ID plus RBAC replaces a shared, all-powerful secret with per-identity, least-privilege,
    auditable, centrally revocable access; Storage Blob Data Reader is the correct role for read-only blob
    access, and disabling shared key enforces the model.
resources:
- label: Azure Storage encryption for data at rest
  url: https://learn.microsoft.com/en-us/azure/storage/common/storage-service-encryption
- label: Prevent Shared Key authorization for an Azure Storage account
  url: https://learn.microsoft.com/en-us/azure/storage/common/shared-key-authorization-prevent
- label: Grant limited access to data with shared access signatures (SAS)
  url: https://learn.microsoft.com/en-us/azure/storage/common/storage-sas-overview
- label: Use private endpoints for Azure Storage
  url: https://learn.microsoft.com/en-us/azure/storage/common/storage-private-endpoints
- label: Overview of Microsoft Defender for Storage
  url: https://learn.microsoft.com/en-us/azure/defender-for-cloud/defender-for-storage-introduction
---

## The Storage Account Threat Model

A storage account is a magnet for attackers because it concentrates two things they want: **data** and **reachability**. By default the account has a **public endpoint** on the internet, and access can be granted by a single long-lived secret. Breaches of cloud storage almost always trace back to the same handful of mistakes: a leaked **account key**, an over-broad or never-expiring **SAS token**, an account left open to the public internet, or data that was deleted or encrypted by ransomware with no way to recover it.

Hardening a storage account is therefore a layered job, and this lesson works through the layers in the order a senior engineer reasons about them: **encrypt** the data (at rest and in transit), **prove identity** instead of trusting secrets, **shrink the network** the account is reachable from, **make the data recoverable**, and finally **watch** it. Each layer is independent, so even if one fails the others still hold. That is defense in depth applied to a single resource.

## Encryption at Rest: Always On, with Key Choices

The first layer is the easiest because Azure does it for you. **Storage Service Encryption (SSE)** encrypts all data before it is written to disk using **256-bit AES** (specifically AES in Galois/Counter Mode), and it **cannot be disabled**. It applies to every resource type, blobs, files, queues, tables, and managed disks, across every tier and redundancy option, including the secondary region when geo-replication is on. There is no extra cost and no code change required.

What you actually decide is **key management**:

- **Platform-managed keys (Microsoft-managed)** — the default. Microsoft creates, stores, and rotates the keys. For most workloads this is the right choice and meets common compliance requirements.
- **Customer-managed keys (CMK)** — you supply and control the key in **Azure Key Vault** or **Azure Key Vault Managed HSM**. You own rotation, revocation, and access policy, which is what regulators often want for sensitive data. CMK is supported for Blob and Azure Files (and for queues/tables via an account encryption key). The storage account reaches the key through a **managed identity**, so grant that identity Key Vault access and turn on **soft delete and purge protection** on the vault so the key cannot be lost.
- **Infrastructure encryption (double encryption)** — an optional second layer that encrypts the data **again** at the infrastructure level with a **separate Microsoft-managed key and a different algorithm**. It must be enabled **at account creation** and protects against the unlikely event that one key or algorithm is compromised. Use it for the most sensitive estates.

The mental model: encryption at rest is guaranteed; you only escalate to CMK or infrastructure encryption when your compliance posture demands ownership of the key or a second layer.

## Encryption in Transit: HTTPS and TLS 1.2

Data on the wire is protected by two account settings. **Secure transfer required** (the `supportsHttpsTrafficOnly` property, "Require secure transfer" in the portal) forces all requests to use **HTTPS** and rejects plain HTTP; it is on by default for new accounts and should never be turned off. Second, set the **minimum TLS version** to **1.2** (or 1.3 where supported) so the account refuses connections negotiating the deprecated TLS 1.0/1.1 protocols. Both are one-line changes and both belong in every baseline:

```bash
# Enforce HTTPS-only and a minimum TLS version of 1.2
az storage account update \
  --name mystorageacct \
  --resource-group rg-data \
  --https-only true \
  --min-tls-version TLS1_2
```

## Identity on the Data Plane: Entra ID and RBAC, Not Keys

This is the most important shift in the lesson. When you create an account, Azure generates **two 512-bit account access keys**. A key grants **full control of all data** in the account and the ability to mint SAS tokens. That makes keys the single worst secret to leak: they are shared, long-lived, hard to attribute, and revoking one means rotating it and breaking every app that used it.

The senior-engineer default is to **authorize the data plane with Microsoft Entra ID** and **Azure RBAC data roles**. Note the distinction between two planes:

- **Management plane** roles like **Owner** and **Contributor** let you manage the *account* (and, dangerously, list its keys) but do **not** by themselves grant access to the *data*.
- **Data plane** roles grant access to the bytes. The key ones are **Storage Blob Data Reader** (read), **Storage Blob Data Contributor** (read/write/delete), and **Storage Blob Data Owner** (full, including POSIX ACLs), with parallel roles for Files, Queues, and Tables.

Assign these to a **user or managed identity**, scoped to the account or even a single container, so every request is authenticated, least-privilege, audited, and centrally revocable, and can be governed by **Conditional Access**.

Once your apps use Entra ID, close the back door by **disabling Shared Key authorization**. Setting `allowSharedKeyAccess=false` makes the account reject any request signed with an account key (and any account/service SAS derived from it); only Entra ID authorization is accepted. It is also a **prerequisite for applying Entra Conditional Access** to the account.

```bash
# Disable Shared Key authorization so only Entra ID auth is accepted
az storage account update \
  --name mystorageacct \
  --resource-group rg-data \
  --allow-shared-key-access false
```

If you genuinely cannot eliminate keys yet, at least **store them in Key Vault**, **rotate them regularly**, and set a **key expiration policy** (`--key-exp-days`) so Azure Policy can flag stale keys. But treat that as a transition state, not a destination.

## SAS Tokens: Prefer User Delegation, Always Least Privilege

Sometimes you must hand limited, time-boxed access to a client that cannot use Entra ID directly, and that is what a **shared access signature (SAS)** is for. There are three kinds, and the choice matters:

- **User delegation SAS** — *preferred*. It is signed with a **user delegation key obtained from Microsoft Entra ID**, not the account key. It carries the signer's identity, is constrained by their RBAC permissions, and is **not invalidated by account-key rotation**. It works even when shared key access is disabled.
- **Service SAS** and **account SAS** — signed with the **account key**. An account SAS can span multiple services and is especially dangerous; a service SAS is scoped to one resource. Both keep you tied to shared-key auth and are hard to revoke.

Whatever the type, apply least privilege: **minimum permissions**, the **shortest viable expiry**, an **IP range** and **HTTPS-only** where possible, and for service SAS a **stored access policy** so you can change or revoke it server-side without rotating the key. The cardinal sin is a **long-lived, broad, account-key SAS** pasted into a client, because revoking it means rotating the account key and breaking everything else. Short expiry plus user delegation is the safe pattern.

## Network Controls: Firewall, Service Endpoints, and Private Endpoints

By default the account answers on a **public endpoint**. Tighten this in stages:

- **Storage firewall** — switch default network access to **Deny**, then allow only specific **public IP ranges** and **virtual networks**. With **VNet service endpoints**, traffic from selected subnets reaches storage over the Azure backbone and the account sees the private source, but the resource still has a public IP.
- **Private Endpoint / Azure Private Link** — the strongest option. The account gets a **private IP inside your VNet**, and clients resolve its name to that private address via private DNS. Combine it with **public network access = Disabled** so the public endpoint is removed entirely and all traffic stays on the Microsoft backbone.
- **Allow trusted Microsoft services** — a firewall exception (`--bypass AzureServices`) that lets first-party services such as Defender, backup, and Azure Monitor reach the account even when it is otherwise locked down. Keep it on so your security tooling is not blocked.

```bash
# Default-deny the firewall but allow trusted Microsoft services, then add a VNet rule
az storage account update \
  --name mystorageacct --resource-group rg-data \
  --default-action Deny --bypass AzureServices \
  --public-network-access Disabled

az storage account network-rule add \
  --account-name mystorageacct --resource-group rg-data \
  --vnet-name vnet-app --subnet subnet-data
```

These commands illustrate two distinct end-states, not a single stack. With **public network access Disabled**, the public endpoint is removed and the IP/VNet firewall allow-rules only apply if public access is later re-enabled — reach the resource via a **Private Endpoint** instead. Use firewall allow-rules + service endpoints when you keep public access **on** but restricted; use Private Endpoint + public access **Disabled** for full isolation.

## Data Protection and Ransomware Resilience

Confidentiality is not enough; you also have to survive **deletion and overwrite**, whether accidental or by ransomware. Four blob features build that resilience:

- **Soft delete** — for blobs *and* containers, retains deleted objects for a configurable window (configurable from 1 to 365 days) so you can undelete them.
- **Versioning** — automatically keeps a **previous version** every time a blob is overwritten or deleted, so you can restore the prior state.
- **Point-in-time restore** — rolls one or more **containers** back to an earlier moment within a retention window; it builds on versioning, soft delete, and the change feed.
- **Immutability (WORM) policies** — make data **write once, read many** so it cannot be modified or deleted, even by an account owner, for the duration. There are two kinds: **time-based retention** (locked for N days) and **legal hold** (held until explicitly removed), applied at the **container** or **version** level. This is the control that defeats ransomware and satisfies regulatory retention (SEC 17a-4, etc.).

Turn these on together: soft delete and versioning for everyday recovery, point-in-time restore for bulk rollback, and immutability for the data that must never change.

## Microsoft Defender for Storage

Posture and recovery handle configuration and the aftermath; **Microsoft Defender for Storage** handles **active threats**. It is a Defender for Cloud plan that adds:

- **On-upload malware scanning** — every uploaded blob is scanned with the Microsoft anti-malware engine, and infected files raise an alert (and can trigger automated response).
- **Sensitive data threat detection** — uses **sensitive data discovery** to prioritize alerts on containers that actually hold sensitive information.
- **Activity monitoring** — analyzes control- and data-plane operations for anomalies like access from a Tor exit node, unusual data extraction, or suspicious permission changes.

Enable it at the subscription level (so new accounts are covered) or per account, and its **alerts flow into Defender for Cloud and on to Microsoft Sentinel** through the connector you built in Module 4, landing your storage threats in the same incident queue as identity and endpoint signals.

## Diagnostics and Logging into Sentinel

You cannot investigate what you do not log. Add a **diagnostic setting** on the storage account (and on the blob/file/queue/table sub-resources) that sends **StorageRead**, **StorageWrite**, and **StorageDelete** logs, plus metrics, to a **Log Analytics workspace**, which is what makes them queryable in Sentinel. These resource logs land in the `StorageBlobLogs` table and let you answer questions like "who is still authenticating with shared key?" or "where is anonymous access coming from?":

```kusto
// Requests still using Shared Key or SAS instead of Entra ID, last 24h
StorageBlobLogs
| where TimeGenerated > ago(24h)
| where AuthenticationType in ("AccountKey", "SAS", "Anonymous")
| summarize Requests = count() by AuthenticationType, CallerIpAddress, Uri
| sort by Requests desc
```

A finding like this is exactly how you confirm it is safe to flip `allowSharedKeyAccess` to false: if nothing legitimate is still using AccountKey or SAS, you can disable shared key without breaking a workload.

## Putting It Together: A Hardened Account as Code

Baselines belong in **infrastructure as code**, the discipline from Module 5, so every new account is born hardened and drift is caught in review. This Bicep declares the controls from this lesson in one resource:

```bicep
resource storage 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: 'stsecuredata01'
  location: location
  sku: { name: 'Standard_GRS' }
  kind: 'StorageV2'
  identity: { type: 'SystemAssigned' }
  properties: {
    minimumTlsVersion: 'TLS1_2'         // refuse TLS 1.0/1.1
    supportsHttpsTrafficOnly: true       // secure transfer required
    allowSharedKeyAccess: false          // Entra ID only on the data plane
    allowBlobPublicAccess: false         // no anonymous containers
    publicNetworkAccess: 'Disabled'      // reachable only via Private Endpoint
    encryption: {
      keySource: 'Microsoft.Storage'
      requireInfrastructureEncryption: true   // double encryption
      services: {
        blob: { enabled: true }
        file: { enabled: true }
      }
    }
    networkAcls: {
      defaultAction: 'Deny'              // default-deny firewall
      bypass: 'AzureServices'           // allow trusted Microsoft services
    }
  }
}
```

Pair this with blob soft delete, versioning, and immutability configured on the blob service, a Private Endpoint, Entra RBAC data-role assignments, Defender for Storage, and the diagnostic setting, and you have an account that is encrypted, identity-gated, network-isolated, recoverable, and watched. That is the standard every storage account in your estate should meet, and the foundation for the databases and networking we secure across the rest of this module.
