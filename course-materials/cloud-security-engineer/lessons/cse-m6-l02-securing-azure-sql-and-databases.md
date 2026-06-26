---
course: cloud-security-engineer
title: Securing Azure SQL and Databases
month: 6
monthTitle: 'Azure Platform Security: Storage, Databases & Networking'
lesson: 2
summary: 'Your databases hold the crown jewels, so Azure SQL security is layered defense in depth across
  identity, network, encryption, data protection, auditing, and threat detection. This lesson centers on
  Azure SQL Database and SQL Managed Instance: you will replace SQL logins with Microsoft Entra authentication
  and enforce Entra-only authentication, authorize apps with managed identities and least-privilege database
  roles, and isolate the server with Private Link, firewall rules, and Deny public network access. You will
  separate the two encryption stories that exams and architects constantly confuse, Transparent Data Encryption
  protecting data at rest on disk versus Always Encrypted protecting data from the DBAs and cloud operators
  who run the platform, plus Always Encrypted with secure enclaves for in-use operations. You will layer
  Data Discovery & Classification, Dynamic Data Masking, Row-Level Security, and Ledger for tamper-evidence,
  then stream SQL audit logs to Log Analytics and Sentinel and turn on Microsoft Defender for SQL for
  vulnerability assessment and threat alerts. The throughline is defense in depth for the data tier:
  identity, isolation, encryption, and detection working together.'
objectives:
- Enforce Microsoft Entra authentication and Entra-only authentication, disabling SQL logins
- Authorize applications with managed identities and least-privilege contained database users
- Isolate Azure SQL with Private Link, firewall rules, and Deny public network access
- Distinguish TDE (data at rest) from Always Encrypted (hidden from DBAs/operators) and choose correctly
- Configure TDE customer-managed keys, enforce TLS 1.2, and use Always Encrypted with secure enclaves
- Apply Data Discovery & Classification, Dynamic Data Masking, Row-Level Security, and Ledger
- Audit to Log Analytics/Sentinel and enable Microsoft Defender for SQL (VA + threat protection)
video: cse-m6-l02-securing-azure-sql-and-databases.mp4
quiz:
- q: What is the key difference between Transparent Data Encryption (TDE) and Always Encrypted in Azure SQL?
  options:
  - They are the same feature with two names
  - TDE encrypts data at rest on disk and the engine decrypts it to serve queries, so DBAs and cloud operators
    can see plaintext; Always Encrypted encrypts in the client driver so the engine never sees plaintext,
    hiding data from high-privilege admins
  - Always Encrypted only protects backups, while TDE protects live data
  - TDE encrypts data in the client, while Always Encrypted encrypts on the server
  answer: 1
  why: TDE protects against theft of the physical media, files, and backups by encrypting data at rest;
    the SQL engine holds the key and decrypts data to process queries, so anyone with high privileges
    on the server (a DBA or Microsoft operator) can see plaintext. Always Encrypted moves encryption into
    the client driver using keys the server never has, so the engine stores and returns only ciphertext,
    protecting sensitive columns from the very administrators who run the database.
- q: How do you ensure that only Microsoft Entra identities can authenticate to an Azure SQL logical server,
    with SQL username/password logins blocked entirely?
  options:
  - Enable Microsoft Entra-only authentication on the server
  - Delete the master database
  - Set the server firewall to deny all IPs
  - Rotate the SQL admin password daily
  answer: 0
  why: Microsoft Entra-only authentication is a server-level setting that disables SQL authentication
    so only Entra principals (users, groups, and managed identities) can connect. It removes password-based
    SQL logins as an attack surface and centralizes access in Entra ID for Conditional Access, MFA, and
    lifecycle management. Firewall rules restrict where connections originate but do not disable SQL logins.
- q: An application running on an Azure VM or App Service needs to connect to Azure SQL without any secret
    in its configuration. What is the recommended approach?
  options:
  - Embed the SQL admin password in an environment variable
  - Use a managed identity and create a contained database user FROM EXTERNAL PROVIDER with least-privilege
    roles
  - Share one SQL login across all applications
  - Store the connection string with credentials in the app's source code
  answer: 1
  why: A managed identity gives the app an Entra identity with no secret to store or rotate; you create
    a contained user in the database mapped to that identity using CREATE USER ... FROM EXTERNAL PROVIDER
    and grant only the database roles it needs (for example db_datareader). The app then obtains a token
    and connects with no password, eliminating credential leakage and manual rotation.
- q: Which Azure SQL configuration prevents the database from being reachable over the public internet
    and forces traffic through a private IP in your virtual network?
  options:
  - Setting minimal TLS version to 1.2
  - Dynamic Data Masking
  - A Private Endpoint (Private Link) combined with Deny public network access
  - Enabling Transparent Data Encryption
  answer: 2
  why: A Private Endpoint gives the logical server a private IP inside your VNet via Azure Private Link,
    and setting public network access to Disabled (Deny public network access) blocks all internet-facing
    connections so traffic only flows over the private path. TLS, masking, and TDE protect data but do
    not control network reachability.
- q: What two capabilities does Microsoft Defender for SQL provide?
  options:
  - Automatic indexing and query tuning
  - SQL Vulnerability Assessment (baseline scans of misconfigurations) and Advanced Threat Protection
    alerts (SQL injection, anomalous access, brute force)
  - Free unlimited storage and backups
  - Replacing the need for auditing and firewalls
  answer: 1
  why: Defender for SQL bundles SQL Vulnerability Assessment, which scans the database against a security
    baseline and flags misconfigurations and excessive permissions, with Advanced Threat Protection, which
    raises alerts on suspicious behavior such as SQL injection, access from unusual locations, and brute-force
    attempts. It is a detection and posture layer that complements, but does not replace, identity, network,
    and encryption controls.
- q: In 3-4 sentences, explain when you would choose Always Encrypted with secure enclaves over standard
    Always Encrypted, and what tradeoff each makes.
  answer: Standard Always Encrypted keeps sensitive column data hidden from the database engine and from
    high-privilege admins, but because the engine only sees ciphertext it can support very limited server-side
    operations, essentially equality lookups with deterministic encryption and nothing rich like range
    or pattern matching. Always Encrypted with secure enclaves adds a trusted execution environment inside
    the engine where keys and plaintext can be used in isolation, so you can run range queries, LIKE
    comparisons, and in-place encryption while the rest of the engine and operators still never see plaintext.
    You choose secure enclaves when you need both confidentiality from administrators and richer query
    functionality on the protected columns. The tradeoff is added configuration (enclave-capable hardware,
    attestation) in exchange for keeping data usable while still protected.
  why: Standard Always Encrypted maximizes confidentiality but restricts operations to equality on deterministic
    columns; secure enclaves preserve that confidentiality while enabling range, pattern, and in-place
    operations through a trusted enclave, at the cost of extra setup and attestation.
resources:
- label: Microsoft Entra authentication for Azure SQL
  url: https://learn.microsoft.com/en-us/azure/azure-sql/database/authentication-aad-overview
- label: Always Encrypted overview
  url: https://learn.microsoft.com/en-us/sql/relational-databases/security/encryption/always-encrypted-database-engine
- label: Transparent Data Encryption (TDE) with customer-managed keys
  url: https://learn.microsoft.com/en-us/azure/azure-sql/database/transparent-data-encryption-byok-overview
- label: Microsoft Defender for SQL
  url: https://learn.microsoft.com/en-us/azure/defender-for-cloud/defender-for-sql-introduction
- label: Use Private Link for Azure SQL Database
  url: https://learn.microsoft.com/en-us/azure/azure-sql/database/private-endpoint-overview
---

## The Database Is the Crown Jewels

Storage holds your files, but the **database holds your most structured, most queried, most regulated data** — customer PII, payment records, health data. An attacker who reaches it does not need to reassemble anything; it is already indexed for them. So we secure Azure SQL as **defense in depth**: even if one layer fails, the next still stands.

The layers, in the order an attacker hits them:

1. **Identity** — who can authenticate at all (Microsoft Entra, Entra-only auth, managed identities).
2. **Network** — from where they can reach the server (Private Link, firewall, Deny public access).
3. **Encryption** — what they see if they get the bits (TDE at rest, TLS in transit, Always Encrypted).
4. **Data protection** — what a *legitimate* query is allowed to return (classification, masking, Row-Level Security, Ledger).
5. **Detection** — what we notice when something is wrong (auditing, Defender for SQL).

This lesson centers on **Azure SQL Database** and **SQL Managed Instance**, noting where they differ. The controls map almost one-to-one, but their network models differ, which we will call out.

## Authentication: Microsoft Entra and Entra-Only

Every Azure SQL logical server is created with a **SQL administrator login** (username and password). That password-based SQL authentication is the oldest and weakest surface: it is a static secret, it bypasses Conditional Access, and it cannot do MFA.

The fix is **Microsoft Entra authentication** (formerly Azure AD authentication). You assign a **Microsoft Entra admin** to the server, then map Entra users, groups, and managed identities to database principals. Entra identities get **Conditional Access, MFA, and central lifecycle management** — disable the user in Entra and database access dies with it.

The senior move is to go further and enable **Microsoft Entra-only authentication**, a server-level switch that **disables SQL authentication entirely**. After this, no one can connect with a SQL username and password; only Entra principals work.

```bash
# Set the Entra admin, then disable SQL logins entirely (Entra-only auth)
az sql server ad-admin create \
  --resource-group rg-data --server sql-prod-eus \
  --display-name "SQL Admins" --object-id <entra-group-object-id>

az sql server ad-only-auth enable \
  --resource-group rg-data --server sql-prod-eus
```

Once Entra-only auth is on, the static SQL admin password is no longer a usable entry point — you have removed an entire category of credential attack.

## Authorize Apps with Managed Identities and Least-Privilege Roles

Applications should **never carry a database password**. Instead, give the app a **managed identity** (system-assigned or user-assigned), then create a **contained database user** mapped to that identity. The app requests an Entra token and connects with no secret to store, leak, or rotate.

```sql
-- Run in the target database, connected as the Entra admin
CREATE USER [app-orders-api] FROM EXTERNAL PROVIDER;   -- the managed identity's name
ALTER ROLE db_datareader ADD MEMBER [app-orders-api];
ALTER ROLE db_datawriter ADD MEMBER [app-orders-api];
-- Grant only what this app needs; do NOT add db_owner
```

This is **least privilege** at the data tier. The app gets `db_datareader`/`db_datawriter` (or a **custom role** scoped to specific tables/procedures), never `db_owner`. Human admins authenticate as **themselves** through Entra groups, so every action is attributable. The combination — managed identity for apps, Entra groups for humans, least-privilege roles for both — means there is no shared secret anywhere in the system.

## Network Isolation: Private Link, Firewalls, and Deny Public Access

By default an Azure SQL **logical server has a public endpoint**. Lock it down in layers.

- **Server-level firewall rules** allow specific public IP ranges and apply to *all* databases on the server. **Database-level firewall rules** (set via `sp_set_database_firewall_rule`) are scoped to one database and are evaluated first — useful for tight per-database control.
- **Private Endpoint (Azure Private Link)** is the strongest control: it projects the server onto a **private IP inside your VNet**, so application traffic never traverses the public internet.
- **Deny public network access** (the `publicNetworkAccess = Disabled` server property, set via `--enable-public-network false`) then closes the public endpoint entirely, forcing every connection through the private path.
- **Virtual network rules** (service endpoints) are an older middle ground that allow specific subnets without a private IP.

```bash
# Force all traffic private: disable the public endpoint
az sql server update --resource-group rg-data --name sql-prod-eus \
  --enable-public-network false
# Then create a Private Endpoint into the app subnet (Private Link)
```

**Managed Instance differs here.** SQL Managed Instance is **natively deployed inside a delegated subnet** of your VNet — its isolation comes from **subnet delegation** (the subnet is delegated to `Microsoft.Sql/managedInstances`) plus a network security group and route table, rather than from a public endpoint you bolt Private Link onto. So MI is VNet-isolated by design, while SQL Database opts into isolation with Private Link and Deny public access.

## Encryption at Rest: TDE with Service-Managed vs Customer-Managed Keys

**Transparent Data Encryption (TDE)** encrypts the database, its **log files, and its backups at rest** — protecting you against theft of the underlying disks, files, or backup media. It is **on by default** for Azure SQL. Crucially, TDE is *transparent*: the **engine holds the key and decrypts data to serve queries**, so it is invisible to applications — and that means **a DBA or cloud operator with engine access can still see plaintext**. TDE defends the media, not against privileged insiders.

Two key-management options:

- **Service-managed key** (default) — Microsoft creates and rotates the TDE protector. Zero effort.
- **Customer-managed key (CMK / BYOK)** — the **TDE protector lives in your Azure Key Vault** (or Managed HSM). You control rotation and, critically, **revocation**: remove Key Vault access and the database becomes inaccessible, giving you a cryptographic kill switch for compliance.

```bash
# Point the server's TDE protector at a customer-managed key in Key Vault (BYOK)
az sql server key create --resource-group rg-data --server sql-prod-eus \
  --kid "https://kv-data.vault.azure.net/keys/tde-key/<version>"

az sql server tde-key set --resource-group rg-data --server sql-prod-eus \
  --server-key-type AzureKeyVault \
  --kid "https://kv-data.vault.azure.net/keys/tde-key/<version>"
```

## TLS in Transit and Always Encrypted

Data in motion is protected by **TLS**. Set the server's **minimal TLS version to 1.2** so clients cannot negotiate weak, deprecated protocols:

```bash
az sql server update --resource-group rg-data --name sql-prod-eus \
  --minimal-tls-version 1.2
```

Now the layer exams love to test. **Always Encrypted** is fundamentally different from TDE. Encryption and decryption happen **in the client driver**, using a **column encryption key** that is itself protected by a **column master key stored outside SQL** (in Key Vault or a client certificate store). The **database engine only ever stores and returns ciphertext** — it never has the keys. The payoff: sensitive columns are **hidden even from DBAs, cloud operators, and anyone with full server access**, because plaintext exists only inside the trusted client. Use it for the few truly sensitive columns (SSNs, card numbers) that even administrators must not see.

The classic limitation: because the engine sees only ciphertext, server-side operations are limited — practically **equality comparisons** with *deterministic* encryption, and nothing for *randomized* encryption. **Always Encrypted with secure enclaves** removes that limit. A **secure enclave** is a protected region of memory inside the engine (a trusted execution environment) where the keys and plaintext can be used **in isolation**, so the engine can perform **range queries, `LIKE` pattern matching, and in-place encryption** on protected columns — while the rest of the engine and the operators **still never see plaintext**. Enclaves require attestation and enclave-capable configuration, the tradeoff for keeping data both confidential and usable.

The one-line distinction to memorize: **TDE protects data at rest on disk; Always Encrypted protects data from the people who run the database.**

## Data Protection Features: Classification, Masking, RLS, and Ledger

Beyond encryption, Azure SQL governs *what a legitimate query returns*:

- **Data Discovery & Classification** scans columns and applies **sensitivity labels and information types** (for example *Confidential — GDPR*). It feeds auditing and Defender, and is the foundation for knowing where regulated data lives.
- **Dynamic Data Masking (DDM)** masks data **in query results** for non-privileged users (showing `XXXX-1234` for a card number). It is a **presentation-layer control, not encryption** — the data is unchanged on disk and a user who can run arbitrary queries can sometimes infer it, so it reduces exposure rather than guaranteeing confidentiality.
- **Row-Level Security (RLS)** restricts **which rows** a user sees using a **security predicate** function bound by a security policy — for example, a sales rep sees only their own accounts, enforced in the engine regardless of the query.
- **Ledger for Azure SQL** makes data **tamper-evident**: updates are cryptographically chained and hashed, with **database digests** you can store externally (for example in immutable storage). **Updatable ledger tables** keep a full history; **append-only ledger tables** forbid updates and deletes outright. Ledger proves data has not been altered — invaluable for audit and regulatory integrity.

## Auditing to Log Analytics and Sentinel

**SQL auditing** records database events — logins, permission changes, queries against sensitive tables — and should be sent to **Log Analytics** so it lands in your SIEM. From Log Analytics, the **Microsoft Sentinel** workspace can correlate database activity with identity and endpoint signals. Log the events that matter: successful and **failed logins**, schema and **permission changes**, and access to classified columns.

Once auditing flows to Log Analytics, hunt over it with KQL:

```kusto
// Failed Azure SQL logins by principal and source IP in the last 24h
SQLSecurityAuditEvents
| where TimeGenerated > ago(24h)
| where ActionId == "LGIF"          // login failed
| summarize Attempts = count() by ServerPrincipalName, ClientIp, LogicalServerName
| where Attempts > 10
| sort by Attempts desc
```

A spike of failed logins from one IP is a brute-force signal you can turn into a Sentinel analytics rule and feed to the SOAR playbooks from Module 5.

## Microsoft Defender for SQL

Finally, the detection and posture layer: **Microsoft Defender for SQL** (a Defender for Cloud plan) bundles two capabilities.

- **SQL Vulnerability Assessment (VA)** runs recurring **scans against a security baseline**, flagging misconfigurations, excessive permissions, unprotected sensitive data, and drift. You approve a clean state as the **baseline**, and future scans alert only on deviations — turning hardening into a continuous, trackable process.
- **Advanced Threat Protection (ATP)** raises **alerts on suspicious behavior**: **SQL injection** and potential SQL injection, **access from an unusual location or principal**, **anomalous query patterns**, and **brute-force** attempts. These alerts surface in Defender for Cloud and, via the connector from Module 4, flow into Sentinel for unified triage.

Defender for SQL **complements but never replaces** the earlier layers — it tells you when identity, network, and encryption controls are being tested or have failed. Put it all together and the data tier has defense in depth: **Entra-only identity, Private Link isolation, TDE and Always Encrypted, classification and Ledger, and Defender-driven detection** — each layer covering the gaps of the others. That is how you secure the crown jewels, and it sets up the networking lesson that closes this module.
