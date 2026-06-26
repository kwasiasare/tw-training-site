---
course: cloud-security-engineer
title: Azure Key Vault, Secrets, and Platform Encryption
month: 6
monthTitle: 'Azure Platform Security: Storage, Databases & Networking'
lesson: 4
summary: 'Every storage account, database, and disk you hardened earlier in this module is ultimately
  protected by a key, and Azure Key Vault is where those keys and secrets live. This lesson makes Key
  Vault the root of trust for the platform: you will choose between Standard, Premium HSM-backed keys,
  and the single-tenant Managed HSM, lock the vault down with Azure RBAC instead of legacy access policies,
  and eliminate secrets from code by having managed identities fetch them at runtime. You will protect
  the vault itself with soft delete, purge protection, firewall and Private Endpoint, and stream its
  audit logs into Sentinel. Then you will connect Key Vault to the rest of the platform with customer-managed
  keys for Azure Storage, Azure SQL TDE, and managed disks, understanding envelope encryption and the
  availability trade-off you take on when you own the key. Finally you will compare Azure Disk Encryption,
  encryption at host, and server-side encryption, and turn on Microsoft Defender for Key Vault so anomalous
  access becomes a SOC alert. The throughline is that Key Vault is the root of trust that ties together
  the storage, database, and network protections of this entire module.'
objectives:
- Choose between Key Vault Standard, Premium (HSM-backed keys), and Managed HSM for a given requirement
- Secure the vault with Azure RBAC data-plane roles using least privilege over legacy access policies
- Eliminate secrets from code using managed identities and Key Vault references in app settings
- Protect the vault with soft delete, purge protection, firewall, and Private Endpoint
- Manage the secret and key lifecycle with versioning, expiry, and auto-rotation policies
- Encrypt Storage, Azure SQL TDE, and managed disks with customer-managed keys via envelope encryption
- Compare Azure Disk Encryption, encryption at host, and server-side encryption, and alert with Defender for Key Vault
video: cse-m6-l04-key-vault-and-platform-encryption.mp4
quiz:
- q: What is the practical difference between Key Vault soft delete and purge protection?
  options:
  - Soft delete lets you recover a deleted vault or object during the retention period; purge protection
    blocks permanent deletion during that window even by administrators
  - They are the same feature under two names
  - Purge protection deletes objects faster; soft delete keeps them forever
  - Soft delete encrypts secrets; purge protection rotates them
  answer: 0
  why: Soft delete (on by default) retains deleted vaults and objects for a retention period so you can
    recover from accidental deletion. Purge protection goes further by blocking any purge of that
    soft-deleted data during the retention window, so not even a vault administrator or a compromised
    account can permanently destroy keys, which is critical when those keys encrypt your storage and databases.
- q: When should you choose Azure Key Vault Managed HSM over the Premium vault tier?
  options:
  - When you want the cheapest option for storing a few app secrets
  - When you need FIPS 140-3 Level 3, single-tenant dedicated HSM pool validated HSMs with full control
    of the key boundary
  - When you do not need HSM protection at all
  - When you only store certificates, never keys
  answer: 1
  why: Both Premium and Managed HSM provide FIPS 140-3 Level 3 HSM-backed keys; Managed HSM is single-tenant
    with a dedicated pool and customer-controlled security domain, so choose it when regulation or
    sovereignty demands single tenancy.
- q: Why are managed identities the preferred way for an app to read a secret from Key Vault?
  options:
  - They store the secret directly in the application source code
  - They disable RBAC so any app can read any secret
  - The application authenticates to Microsoft Entra ID with an identity Azure manages, so no credential
    is ever stored in code or config
  - They require you to embed a client secret in the app settings
  answer: 2
  why: A managed identity gives the app a Microsoft Entra identity whose credential Azure provisions and
    rotates automatically, so the app requests a token and reads the secret at runtime with no password
    in code or configuration. Combined with a least-privilege role like Key Vault Secrets User, this removes
    the bootstrapping secret that plaintext connection strings always reintroduce.
- q: In customer-managed key (CMK) encryption of Azure Storage or SQL TDE, what does envelope encryption mean?
  options:
  - The data is mailed on an encrypted disk
  - A data encryption key encrypts the data, and your Key Vault key (the key encryption key) wraps that
    data encryption key
  - Microsoft keeps a copy of your key in every region
  - The key and the data are stored in the same blob
  answer: 1
  why: With envelope encryption the service encrypts data with a symmetric data encryption key (DEK), then
    wraps that DEK with your key encryption key (KEK) held in Key Vault. The service only stores the wrapped
    DEK, so revoking or disabling the KEK renders the data unreadable, which is the power and the
    responsibility of CMK; you now own the availability and rotation of that key.
- q: Why does Azure RBAC for the data plane improve on legacy vault access policies?
  options:
  - Access policies are more granular than RBAC
  - RBAC provides a unified, role-based, least-privilege model managed alongside other Azure resources,
    with roles like Key Vault Secrets User and Crypto User scoped per vault or secret
  - RBAC removes the need for any permissions
  - Access policies integrate with Microsoft Entra ID but RBAC does not
  answer: 1
  why: The legacy access policy model grants broad permission sets per identity and is managed separately
    from the rest of Azure. Azure RBAC is Microsoft's recommended model, offering granular built-in roles
    (Key Vault Secrets User, Crypto User, Administrator) that you assign with least privilege at the vault
    or individual object scope, consistent with how you control every other Azure resource.
- q: In 3-4 sentences, explain why Key Vault is described as the "root of trust" for the storage and
    database protections built earlier in this module, and name one operational risk you accept when you
    move from Microsoft-managed keys to customer-managed keys.
  options: null
  answer: Key Vault holds the keys that encrypt the storage accounts, Azure SQL databases, and managed
    disks hardened earlier, so the confidentiality of all that data ultimately depends on the keys and
    access controls inside the vault, making it the single root of trust for platform encryption. If the
    vault is compromised or its keys are destroyed, the protected data is exposed or rendered permanently
    unreadable, which is why soft delete, purge protection, RBAC, and network isolation matter so much.
    When you move to customer-managed keys you accept responsibility for the key's availability and
    rotation, so an accidentally disabled, deleted, or expired key, or a vault that becomes unreachable,
    can take your storage and databases offline. That operational ownership is the trade-off for the
    control and revocability CMK provides.
  why: Key Vault is the root of trust because the keys that encrypt storage, SQL TDE, and disks live there,
    so its protection determines the security of everything downstream; the main CMK trade-off is that
    you now own key availability and rotation, and a lost or disabled key can make data unreadable.
resources:
- label: About Azure Key Vault
  url: https://learn.microsoft.com/en-us/azure/key-vault/general/overview
- label: Provide access to Key Vault keys, certificates, and secrets with Azure RBAC
  url: https://learn.microsoft.com/en-us/azure/key-vault/general/rbac-guide
- label: Customer-managed keys for Azure Storage encryption
  url: https://learn.microsoft.com/en-us/azure/storage/common/customer-managed-keys-overview
- label: Azure Key Vault soft-delete and purge protection
  url: https://learn.microsoft.com/en-us/azure/key-vault/general/soft-delete-overview
- label: Microsoft Defender for Key Vault
  url: https://learn.microsoft.com/en-us/azure/defender-for-cloud/defender-for-key-vault-introduction
---

## The Root of Trust for the Platform

Across this module you hardened **storage accounts**, **Azure SQL databases**, and the **network** around them. Strip away the configuration and every one of those protections comes down to one thing: a **key**. Azure Storage encrypts blobs with a key; Azure SQL **Transparent Data Encryption (TDE)** encrypts the database with a key; a managed disk is encrypted with a key. **Azure Key Vault** is where those keys, along with application **secrets** and **certificates**, live and are governed. That makes Key Vault the **root of trust** for the entire platform: if the vault is wrong, everything it protects is wrong. This lesson closes the module by tying the keys back to the resources they protect.

Key Vault manages three object types, and the distinction matters:

- **Secrets** — arbitrary protected strings: connection strings, API keys, passwords.
- **Keys** — cryptographic keys (RSA, EC) used for **wrap/unwrap, sign/verify**, never exported in the clear; these are what back customer-managed encryption.
- **Certificates** — X.509 certificates with lifecycle management, built on top of keys and secrets.

## Standard, Premium, and Managed HSM

Choose the protection level for your keys deliberately:

- **Standard** — keys are protected by software (still encrypted at rest in Microsoft's infrastructure). Fine for most secrets and certificates.
- **Premium** — adds **HSM-backed keys** protected by **FIPS 140-3 Level 3** validated HSMs (legacy keys were FIPS 140-2 Level 2) in a **multi-tenant** HSM pool. Use it when a key must never exist outside an HSM boundary, including most CMK scenarios.
- **Azure Key Vault Managed HSM** — a fully managed, **single-tenant** service backed by **FIPS 140-3 Level 3** validated HSMs, with a dedicated HSM pool and a customer-controlled security domain. Both Premium and Managed HSM reach FIPS 140-3 Level 3; choose Managed HSM when you need single tenancy / a dedicated cryptographic boundary, not a higher FIPS level.

The rule of thumb: **Standard** for secrets and certificates, **Premium** when CMK or compliance requires an HSM, **Managed HSM** when you need a dedicated, single-tenant cryptographic boundary.

## Access Model: Azure RBAC over Legacy Access Policies

Key Vault has two authorization models for the **data plane** (the operations that read secrets and use keys). The **legacy access policy** model grants coarse permission sets per identity and is managed separately from the rest of Azure. **Azure RBAC is the recommended model** and is what you should use for new vaults: it is granular, role-based, least-privilege, and managed consistently with every other Azure resource.

Assign the **narrowest** built-in data-plane role for the job:

- **Key Vault Secrets User** — read secret values. This is what an application's managed identity gets.
- **Key Vault Crypto User** — use keys to encrypt/decrypt, wrap/unwrap, sign/verify (but not manage them).
- **Key Vault Administrator** — full data-plane management; reserve for break-glass and platform engineers.

Switch the vault to RBAC and grant a role at the vault scope:

```bash
# Put the vault on the Azure RBAC authorization model
az keyvault update --name kv-platform-prod \
  --resource-group rg-platform \
  --enable-rbac-authorization true

# Grant an app's managed identity read-only access to secrets (least privilege)
az role assignment create \
  --assignee "<managed-identity-object-id>" \
  --role "Key Vault Secrets User" \
  --scope "/subscriptions/<sub>/resourceGroups/rg-platform/providers/Microsoft.KeyVault/vaults/kv-platform-prod"
```

Never hand an application **Administrator** when **Secrets User** will do. Least privilege at the vault is the difference between a leaked token reading one secret and an attacker owning every key you have.

## Eliminating Secrets from Code

In Module 5 the theme was automation without standing credentials. Key Vault is how that lands for applications. **Never store credentials in code or config.** Instead, give the workload a **managed identity** and let it fetch secrets at runtime.

- **System-assigned managed identity** — tied to the lifecycle of one resource (a VM, App Service, Function). Deleted with the resource. Use it for a 1:1 identity.
- **User-assigned managed identity** — a standalone identity you can attach to **many** resources. Use it when several workloads share an identity or you want the identity to outlive any single resource.

The app authenticates to **Microsoft Entra ID** with its managed identity, gets a token, and reads the secret. No password is ever stored. For App Service and Functions you do not even need code: use a **Key Vault reference** in app settings, and the platform resolves it at runtime:

```text
@Microsoft.KeyVault(SecretUri=https://kv-platform-prod.vault.azure.net/secrets/SqlConnectionString/)
```

The app sees a normal setting; the value is fetched from Key Vault under the resource's managed identity. The plaintext connection string never lives in your repo, your pipeline, or your configuration files.

## Protecting the Vault Itself

Because the vault is the root of trust, it gets its own defenses:

- **Soft delete** is **on by default** and cannot be disabled. Deleted vaults and objects are retained for a configurable period (7-90 days) so you can **recover from accidental deletion**.
- **Purge protection** goes further: during the retention window it **blocks permanent deletion even by an administrator**. Once enabled it cannot be turned off for the life of the vault. This is what stops a compromised admin or a rogue script from destroying the keys that encrypt your data. **For any vault holding CMK, purge protection is mandatory.**

```bash
az keyvault update --name kv-platform-prod \
  --resource-group rg-platform \
  --enable-purge-protection true
```

- **Network restriction** — set the firewall to **deny public access** and reach the vault over a **Private Endpoint**, so secrets never traverse the public internet. This is the same network discipline you applied to storage and SQL earlier in the module.
- **Diagnostic logging** — send **AuditEvent** logs to **Log Analytics / Microsoft Sentinel** so every secret read and key operation is recorded and huntable.

## Secret and Key Lifecycle: Versioning, Expiry, Rotation

Every object in Key Vault is **versioned**: updating a secret creates a new version while old versions remain addressable, so rotation never breaks a consumer mid-flight. Set **activation and expiry dates** on secrets and keys so stale credentials age out instead of living forever.

For keys, configure an **auto-rotation policy** so Key Vault generates a new key version on a schedule, and use **Event Grid near-expiry notifications** to drive rotation of secrets that Key Vault cannot rotate itself (for example, rotating a database password and writing the new value back). The goal is that no human is the rotation mechanism:

```bash
# Auto-rotate a key 30 days before expiry, with an 18-month lifetime
az keyvault key rotation-policy update \
  --vault-name kv-platform-prod --name cmk-storage \
  --value '{"lifetimeActions":[{"trigger":{"timeBeforeExpiry":"P30D"},"action":{"type":"Rotate"}}],"attributes":{"expiryTime":"P18M"}}'
```

## Customer-Managed Keys: Closing the Loop with Storage and SQL

This is where Key Vault connects back to Lessons 1 and 2. By default Azure encrypts storage, SQL, and disks with **Microsoft-managed keys** at no effort. **Customer-managed keys (CMK / BYOK)** let you supply and control the key instead, using **envelope encryption**: the service encrypts data with a **data encryption key (DEK)**, then **wraps** that DEK with your **key encryption key (KEK)** in Key Vault. The service stores only the wrapped DEK, so if you disable or revoke the KEK, the data becomes unreadable.

That revocability is the benefit. The cost is **ownership**: with CMK **you own the availability and rotation of the key**. An accidentally disabled, deleted, or expired key, or a vault made unreachable, can take your storage account or database offline. This is exactly why such a vault needs **soft delete and purge protection** and a managed-identity-based access path.

Point a storage account at a CMK (the storage account's managed identity needs **Key Vault Crypto Service Encryption User** on the key):

```bash
az storage account update \
  --name stplatformprod --resource-group rg-platform \
  --encryption-key-source Microsoft.Keyvault \
  --encryption-key-vault "https://kv-platform-prod.vault.azure.net/" \
  --encryption-key-name cmk-storage \
  --encryption-key-version ""   # empty = auto-track the latest key version on rotation
```

The same pattern applies to **Azure SQL TDE with a customer-managed key** (the TDE protector becomes your Key Vault key) and to **managed disks** via a **disk encryption set** that references the vault key. In every case Key Vault is the KEK and the platform resource is the consumer.

## Disk and Compute Encryption Options

For VMs and disks there are three distinct mechanisms; know which is which:

- **Server-side encryption (SSE) of managed disks** — the default. Azure encrypts disks at rest in the storage infrastructure with **platform-managed** or **customer-managed keys** (via a disk encryption set). Transparent to the guest OS.
- **Encryption at host** — encrypts the temp disk and host caches too; recommended for sensitive VMs, but must be explicitly enabled (not a default).
- **Azure Disk Encryption (ADE)** — in-guest volume encryption using **BitLocker** (Windows) or **DM-Crypt** (Linux), with the **encryption key stored in Key Vault**. Use it when you need OS-level volume encryption inside the guest.

And one line on the frontier: **Azure confidential computing** encrypts data **in use** by running the workload inside a hardware-based **trusted execution environment**, closing the last gap after at-rest and in-transit.

This Bicep snippet wires a disk encryption set to a Key Vault key so disks can use CMK:

```bicep
resource des 'Microsoft.Compute/diskEncryptionSets@2023-04-02' = {
  name: 'des-platform-prod'
  location: location
  identity: { type: 'SystemAssigned' }
  properties: {
    encryptionType: 'EncryptionAtRestWithCustomerKey'
    activeKey: {
      keyUrl: 'https://kv-platform-prod.vault.azure.net/keys/cmk-disk/<version>'
    }
  }
}
```

## Defender for Key Vault and Hunting Access

Finally, turn the vault into a **detection** surface. **Microsoft Defender for Key Vault** (a Defender for Cloud workload plan, introduced in Module 4) watches for **anomalous and suspicious access** patterns, unusual callers, spikes in secret reads, access from unfamiliar locations, and raises **alerts** that flow into **Sentinel** as potential **credential theft**. Combined with the AuditEvent logs you enabled, the SOC can both detect and investigate.

A simple hunt over the vault's diagnostic logs:

```kusto
// Unusual volume of secret reads per caller in the last 24h
AzureDiagnostics
| where ResourceType == "VAULTS"
| where OperationName == "SecretGet"
| summarize Reads = count(), Secrets = dcount(id_s) by CallerIPAddress, identity_claim_appid_g, bin(TimeGenerated, 1h)
| where Reads > 100
| sort by Reads desc
```

That closes Module 6 and SC-500 Domain 2. You secured storage, databases, and networking, and you have now seen that all of it hangs from one place: **Key Vault, the root of trust** whose keys encrypt the platform and whose access you govern with RBAC, isolate with private networking, protect with soft delete and purge protection, and monitor with Defender. Next, Module 7 brings the whole course together in the capstone.
