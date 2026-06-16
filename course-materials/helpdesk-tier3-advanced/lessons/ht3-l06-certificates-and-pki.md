---
course: helpdesk-tier3-advanced
title: Certificates and PKI for endpoints
month: 3
monthTitle: Advanced Endpoint Security & Identity
lesson: 6
summary: Understand public key cryptography, X.509 certificates and PKI hierarchy, then deploy and troubleshoot
  device and user certificates on endpoints using AD CS auto-enrollment, Intune SCEP/PKCS profiles and
  certutil. You will tie certificates to real endpoint uses such as 802.1X, VPN and certificate-based
  authentication to Entra.
objectives:
- Explain asymmetric cryptography and the difference between signing and encryption
- Read the key X.509 fields of a certificate and describe what each asserts
- Describe a PKI hierarchy with an offline root and issuing CA, and how the chain of trust validates
- 'Trace the certificate lifecycle: enrollment, renewal, and revocation via CRL and OCSP'
- Deploy device and user certificates to endpoints using AD CS auto-enrollment and Intune SCEP/PKCS profiles
- Troubleshoot certificate problems on Windows endpoints using certutil and the certificate stores
video: ht3-l06-certificates-and-pki.mp4
quiz:
- q: A device presents a leaf certificate signed by an issuing CA, which is signed by an offline root
    CA. What must an endpoint validating this chain have in its trust store for validation to succeed?
  options:
  - The leaf certificate's private key
  - The root CA certificate installed as a trusted root anchor
  - The issuing CA's private key
  - A copy of every CRL ever published
  answer: 1
  why: Chain validation walks from the leaf up to a self-signed root that must be present and trusted
    in the LocalMachine\Root (trusted root) store. The intermediate is usually supplied in the chain or
    AIA; only the root must be pre-trusted as the anchor. Private keys are never distributed for validation.
- q: When a user digitally signs an email with S/MIME, which key performs the signing and which verifies
    it?
  options:
  - Sign with the recipient's public key; verify with the recipient's private key
  - Sign with the sender's private key; verify with the sender's public key
  - Sign with a shared symmetric key on both ends
  - Sign with the CA's private key; verify with the sender's private key
  answer: 1
  why: 'Signing proves origin and integrity, so the sender signs with their own private key and anyone
    verifies with the sender''s public key from the certificate. Encryption is the reverse: you encrypt
    to the recipient''s public key. Mixing these up is the classic PKI exam trap.'
- q: An issuing CA is compromised on a Tuesday. Which mechanism lets relying parties learn that previously
    valid certificates should no longer be trusted, in near real time?
  options:
  - Auto-enrollment
  - A certificate template
  - OCSP (Online Certificate Status Protocol)
  - Key archival
  answer: 2
  why: OCSP gives a real-time per-certificate status response and is lighter than downloading a full CRL.
    The CRL is the periodically published revocation list; OCSP is the live lookup. Auto-enrollment, templates
    and key archival have nothing to do with revocation distribution.
- q: You are deploying a device certificate to unmanaged-by-domain Windows endpoints via Intune so the
    private key never leaves the device. Which profile type is the correct choice?
  options:
  - SCEP certificate profile with an NDES connector
  - A trusted root certificate profile
  - A PKCS imported certificate profile
  - A Wi-Fi profile alone
  answer: 0
  why: SCEP has the device generate its own key pair locally and only sends a CSR, so the private key
    never leaves the endpoint, which is ideal for device authentication. PKCS imported certs are generated
    centrally (key escrowed) and suit user S/MIME scenarios where the same key must be reused. A trusted
    root profile only distributes the anchor.
- q: Name the certutil command that displays the certificates currently in a named Windows certificate
    store, and state which store holds a machine's own identity certificates.
  answer: certutil -store (for example, certutil -store My for the personal/identity store, or certutil
    -store -enterprise NTAuth). A machine's own identity certificates live in the LocalMachine\My (Personal)
    store; trusted roots live in LocalMachine\Root.
  why: certutil -store enumerates a store and prints each certificate's subject, serial, thumbprint and
    whether the private key is present. Knowing My versus Root, and machine versus user scope, is fundamental
    to triaging endpoint certificate issues.
- q: In one sentence, explain why a root CA is typically kept offline while an issuing (subordinate) CA
    stays online.
  answer: The root CA's private key is the ultimate trust anchor, so it is kept offline (powered off or
    air-gapped) to protect it from compromise, while the online issuing CA does the day-to-day signing
    and can be revoked and replaced by the root if it is ever breached.
  why: If the root key is stolen the entire PKI collapses and cannot be cheaply recovered, so it signs
    only the issuing CA(s) and then goes offline; a compromised issuing CA, by contrast, can be revoked
    by the root and reissued, containing the blast radius.
resources:
- label: Microsoft Learn — Active Directory Certificate Services (AD CS) overview
  url: https://learn.microsoft.com/en-us/windows-server/identity/ad-cs/active-directory-certificate-services-overview
- label: Microsoft Learn — certutil command reference
  url: https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/certutil
- label: Microsoft Learn — Use SCEP certificate profiles with Microsoft Intune
  url: https://learn.microsoft.com/en-us/mem/intune/protect/certificates-scep-configure
- label: Microsoft Learn — Certificate-based authentication in Microsoft Entra ID
  url: https://learn.microsoft.com/en-us/entra/identity/authentication/concept-certificate-based-authentication
---

## Public key cryptography in two minutes

Everything in PKI rests on **asymmetric cryptography**: a mathematically linked **key pair**. The **private key** is secret and never leaves the holder; the **public key** is freely shared. The two operations matter for endpoints:

- **Signing** proves origin and integrity. You sign with your **private** key; anyone verifies with your **public** key.
- **Encryption** for confidentiality is the reverse. You encrypt to the recipient's **public** key; only their **private** key decrypts.

Getting that direction right is the single most useful thing to internalise.

## What a certificate actually is

A **digital certificate** is a public key plus identity claims, all **signed by a Certificate Authority (CA)**. The format is **X.509**. The fields you will read constantly:

- **Subject** — who the cert identifies (a user, a device, a server FQDN).
- **Issuer** — the CA that signed it.
- **Validity** — not-before and not-after dates.
- **Public key** and **signature algorithm**.
- **Subject Alternative Name (SAN)** — the real identity for TLS and 802.1X.
- **Enhanced Key Usage (EKU)** — what it is allowed to do (Client Authentication, Server Authentication, Code Signing, Secure Email).

## PKI hierarchy and the chain of trust

A production **PKI** is tiered. An **offline root CA** signs one or more **issuing (subordinate) CAs**, then is powered off to protect the ultimate trust anchor. The online **issuing CA** does the everyday signing. An endpoint trusts a leaf certificate only if it can build a chain up to a **root it already trusts** in `LocalMachine\Root`.

```text
Root CA (offline, self-signed)        <- in Trusted Root store
   |  signs
Issuing CA (online, in NTAuth/CA store)
   |  signs
Device / User leaf certificate        <- in LocalMachine\My
```

Validate a chain from a Windows endpoint:

```powershell
# Verify the full chain, revocation and trust path of a cert file
certutil -verify -urlfetch device.cer

# Inspect a CSR before submitting it to the CA
certutil -dump request.req
```

## Lifecycle: enroll, renew, revoke

Certificates are born from a **Certificate Signing Request (CSR)** — the endpoint generates a key pair, keeps the private key, and sends only the public key and subject to the CA. The CA issues against a **template**, the endpoint installs the cert, and **auto-enrollment** in AD CS renews it before expiry. When a cert must be killed early it is **revoked**; relying parties learn this from a periodically published **CRL** or a live **OCSP** lookup.

```text
Key pair generated on device
  -> CSR (public key + subject) sent to CA
  -> CA validates against template, signs, issues
  -> Cert installed in LocalMachine\My (private key stays put)
  -> Auto-enrollment renews before not-after
  -> If compromised: revoke -> appears on CRL / OCSP
```

## Getting certs onto endpoints

Domain-joined devices use **AD CS auto-enrollment** driven by certificate **templates** and Group Policy. For Intune-managed or cloud devices you choose between two profile types: a **SCEP** profile (the device generates its own key, sends a **CSR** via the NDES connector, so the private key never leaves the endpoint — ideal for device auth) or a **PKCS** profile (the key is generated centrally and imported, suited to user **S/MIME** where the same key is reused). A separate **trusted root** profile distributes the anchor. These certs then power **802.1X/Wi-Fi**, **VPN**, **TLS**, **code signing**, **S/MIME**, and **certificate-based authentication to Entra**.

## Troubleshooting with certutil

When authentication fails, certutil is your scalpel. List a store, dump a cert, check the CA-side picture:

```text
certutil -store My                 :: machine identity certs + key presence
certutil -store -user My           :: the user store instead
certutil -store -enterprise NTAuth :: CAs trusted for Entra/AD logon
certutil -dump device.cer          :: decode all X.509 fields
certutil -verify -urlfetch x.cer   :: build chain, fetch CRL/OCSP, report errors
```

The golden questions: is the private key present, does the chain reach a trusted root, has it been revoked, and is the right EKU on it.

## Your task

In a test tenant, deploy a **device certificate** to one managed Windows endpoint using an Intune **SCEP** profile (with its trusted-root and SCEP profiles), then prove it works for **certificate-based authentication**. On the endpoint, run `certutil -store My` and `certutil -verify -urlfetch` against the issued cert, and capture: the Subject, SAN, EKU, the full chain to the root, whether the private key is present, and the revocation check result. Then deliberately revoke the certificate at the CA, force a CRL/OCSP refresh, and document how the endpoint's behaviour changes and what certutil now reports.
