# vdi-engineer — Course Plan (TW-135)

Planned 2026-07-24 (Fable). Scope confirmed by owner: hybrid of (a) cert-aligned Azure Virtual Desktop depth mapped to AZ-140 and (b) vendor-neutral VDI survey (Citrix DaaS, Omnissa Horizon, Windows 365). Target learner: IT pro upskilling into VDI — assumes basic Windows admin + some Azure; depth bar = cloud-security-engineer course.

Videos and study packs are DEFERRED to a follow-up ticket (do not author `video` fields in decks).

## Verified 2026 cert anchors (do not contradict these)

- **AZ-140** — Microsoft Certified: Azure Virtual Desktop Specialty. ACTIVE in 2026. Domains: Plan & implement AVD infrastructure (40–45%), Plan & implement identity & security (15–20%), Plan & implement user environments & apps (20–25%), Monitor & maintain AVD infrastructure (10–15%). Modules 3–6 map 1:1 to these domains.
- **Citrix** (Cloud Software Group): associate cert = **CCA-V** (Citrix Certified Associate – Virtualization); Citrix-Cloud/DaaS credential = **CC-VAD-CC**.
- **Omnissa** (former VMware EUC, spun out under Broadcom era): current admin cert = **OCA-H** (Omnissa Certified Administrator – Horizon). Legacy VMware **VCP-DTM is no longer issued** (existing ones honored). Never present VCP-DTM as the current path.
- Windows 365 has no dedicated cert; it appears inside MD-102/Intune-adjacent content and this course's platform coverage.

## Module & lesson outline (7 modules / 34 lessons)

Deck file naming: `vdi-m<module>-l<NN>-<kebab-slug>.json`, e.g. `vdi-m1-l01-what-is-vdi-and-euc.json`.

### M1 — VDI & EUC Foundations (5 lessons)
1. `what-is-vdi-and-euc` — VDI vs session-based/RDS vs app virtualization vs DaaS; brief history (Citrix WinFrame → Terminal Services → today's cloud DaaS; eras only, no trivia); why VDI in 2026: hybrid work, security/data-egress control, contractors/BYOD, regulated industries, GPU/AI workstations.
2. `vdi-architecture-building-blocks` — the universal parts: control plane/broker, gateway/access layer, session hosts, golden images, profile layer, connection flow (user → broker → gateway → host); agent-based vs agentless registration.
3. `display-protocols-explained` — RDP (+ Shortpath/UDP), Citrix HDX/ICA, Omnissa Blast Extreme, PCoIP (legacy); TCP vs UDP transports, codecs (H.264/AVC, HEVC), latency/bandwidth budgets, what breaks UX and why.
4. `persistent-vs-nonpersistent-and-profiles` — pooled vs personal/dedicated; why non-persistent needs profile tooling; concept survey: FSLogix, Citrix Profile Management, Omnissa DEM; folder redirection vs container-based profiles.
5. `vdi-economics-licensing-and-sizing` — cost drivers (compute, storage, egress, licensing); Windows licensing for VDI (per-user entitlements via M365/Windows E3+), Citrix/Omnissa subscription models; density & sizing basics (vCPU:user ratios, RAM, IOPS); on-prem vs cloud TCO framing.

### M2 — The 2026 VDI Platform Landscape (5 lessons)
1. `azure-virtual-desktop-and-windows-365` — AVD (PaaS, you own session hosts, pooled multi-session Win 10/11 Enterprise multi-session) vs Windows 365 Cloud PC (SaaS, fixed-price per-user, personal only); when each wins; Windows 365 Link/Boot/Switch/Frontline at a high level.
2. `citrix-daas-overview` — Citrix DaaS architecture: Citrix Cloud control plane, Cloud Connectors, resource locations, Workspace/StoreFront, Delivery Groups, MCS provisioning, Director; where Citrix still wins (protocol maturity, peripherals, on-prem estates); CCA-V path.
3. `omnissa-horizon-overview` — Horizon 8: Connection Server, Unified Access Gateway, Instant Clones, App Volumes, DEM; Horizon Cloud next-gen; the VMware→Omnissa transition and what it means for customers; OCA-H path.
4. `gpu-workloads-and-other-players` — GPU VDI: use cases (CAD, media, AI/ML dev), Azure NV-series, NVIDIA vGPU licensing concepts; other players surveyed briefly: Amazon WorkSpaces (Family), Dizzion/Frame (**fact-check flag**: Frame left Nutanix — verify current ownership/name before writing), Kasm, Apache Guacamole (open source).
5. `choosing-a-platform` — decision framework: existing investments, cloud strategy, persistent vs pooled mix, protocol/peripheral needs, budget model (opex fixed vs variable), compliance/sovereignty; produce a scoring matrix learners reuse in the M7 capstone.

### M3 — AVD Infrastructure: Plan, Deploy & Scale (6 lessons) — AZ-140 Domain 1 (40–45%)
1. `avd-architecture-and-planning` — AVD service architecture: Microsoft-managed control plane (broker, gateway, web), customer-owned session hosts; reverse connect (no inbound ports); host pools, app groups (Desktop/RemoteApp), workspaces; personal vs pooled; validation vs production pools; service limits worth knowing.
2. `avd-networking` — VNet design for AVD, required outbound URLs/service tags, RDP Shortpath (managed networks + public networks/STUN/TURN), Private Link for AVD, bandwidth planning per workload type, hybrid connectivity (VPN/ER).
3. `session-hosts-and-golden-images` — VM sizing by workload class, OS choices (Win 11 Enterprise multi-session), golden image build, Azure Compute Gallery versioning, Azure Image Builder / custom image templates, Trusted Launch, ephemeral vs managed disks.
4. `deploying-host-pools` — portal deployment walkthrough; infrastructure-as-code with Bicep (primary) + note Terraform azurerm; host pool registration keys/tokens; Azure Virtual Desktop Insights workbook enablement at deploy time; session host update options (**fact-check flag**: verify current state of the session host update/configuration feature naming).
5. `autoscale-and-cost-optimization` — Autoscale scaling plans (pooled + personal), Start VM on Connect, hibernation for personal hosts (**fact-check flag**: verify GA status), drain mode, right-sizing, Reserved Instances/Savings Plans, cost per user math.
6. `bcdr-for-avd` — availability zones for session hosts, backup strategy (what to back up: images, FSLogix profiles, not stateless pooled hosts), Azure Files redundancy/failover for profiles, active-active vs active-passive host pool DR patterns.

### M4 — Identity & Security for Virtual Desktops (4 lessons) — AZ-140 Domain 2 (15–20%)
1. `identity-for-avd` — identity sources: Entra ID join vs Microsoft Entra hybrid join vs Entra Domain Services; Entra-joined + FSLogix with Entra Kerberos for Azure Files; licensing prerequisites; single sign-on with Entra SSO.
2. `access-control-and-conditional-access` — AVD-specific RBAC roles (Desktop Virtualization *), app group assignment, Conditional Access targeting AVD (cloud apps: Azure Virtual Desktop / Windows Cloud Login), MFA, session frequency, device filters.
3. `securing-session-hosts` — Intune management of multi-session (supported scenarios), security baselines, Microsoft Defender for Endpoint on session hosts, screen capture protection, watermarking, RDP device/clipboard redirection lockdown, Azure Firewall for egress.
4. `zero-trust-across-vdi-platforms` — vendor-neutral security lesson: Citrix App Protection & UAG hardening equivalents, per-platform gateway posture, session recording, the Zero Trust mapping for EUC (identity, endpoint, session, data); ties to broader Zero Trust framing used elsewhere on this site.

### M5 — User Environments & App Delivery (5 lessons) — AZ-140 Domain 3 (20–25%)
1. `fslogix-deep-dive` — profile containers vs ODFC, VHDLocations vs Cloud Cache, storage options (Azure Files + Entra Kerberos, Azure NetApp Files), sizing/performance, exclusions, common failure modes (locked VHDX, 0x0000004c etc. — verify exact codes), per-user vs per-machine install.
2. `app-delivery-and-app-attach` — **App attach** (current) vs legacy MSIX app attach (**fact-check flag**: verify current naming/GA state and differences); MSIX packaging basics, RemoteApp publishing, comparison: Citrix App Layering / Omnissa App Volumes.
3. `teams-multimedia-and-peripherals` — Teams on AVD (media optimization / SlimCore — **fact-check flag**: verify current architecture name), multimedia redirection, camera/audio redirection, printing (Universal Print), scanners/USB, what to test before go-live.
4. `user-environment-management` — GPO vs Intune policy for session hosts, Start menu/taskbar management, Citrix WEM and Omnissa DEM as category comparisons, language/regional settings, shortpath between "image bloat" vs "policy at login" trade-offs.
5. `windows-365-administration` — provisioning policies, network options (Microsoft-hosted vs ANC), Intune-first management, restore points, resize, Windows 365 Boot/Switch/Frontline modes, when a customer should be on W365 instead of AVD (revisits M2 decision framework with admin depth).

### M6 — Monitoring, Operations & Troubleshooting (4 lessons) — AZ-140 Domain 4 (10–15%)
1. `avd-monitoring-and-insights` — Azure Virtual Desktop Insights (workbooks), required diagnostic settings, Log Analytics tables (WVD* — verify exact table names: WVDConnections, WVDErrors, etc.), starter KQL queries (connection failures, round-trip time, session duration), alerting.
2. `image-and-host-lifecycle` — patching strategy for golden images vs in-place, image versioning cadence, host pool rolling updates, drain + replace patterns, scheduled agent updates, Windows Update on Cloud PCs.
3. `troubleshooting-vdi` — a triage methodology on the connection chain (client → feed → auth → gateway → host → profile → in-session UX); the classic failure buckets with tools per bucket; FSLogix triage; comparisons: Citrix Director / Horizon Helpdesk equivalents; when to open which support path.
4. `day-2-operations-and-dex` — capacity management, cost reviews, user-experience metrics and DEX (digital employee experience) tooling category (Omnissa Intelligence, Nexthink, ControlUp as category examples), runbooks/on-call for VDI, SLOs for session availability and logon time.

### M7 — Capstone Projects & Career Launch (5 lessons)
1. `capstone-1-design-an-avd-environment` — case study org (given requirements: 600 users, 3 personas, compliance constraint); learner produces an architecture design doc (host pool topology, identity, networking, FSLogix, autoscale, BCDR) — portfolio artifact #1; includes a worked reference solution.
2. `capstone-2-build-and-document` — hands-on build of a scaled-down version in a trial/dev subscription: Bicep deploy, FSLogix on Azure Files, autoscale plan, Insights enabled; document with screenshots into a portfolio README — portfolio artifact #2; include cost-teardown warning and cleanup steps.
3. `capstone-3-platform-migration-assessment` — vendor-neutral capstone: assess a fictional Citrix on-prem estate for migration (stay on Citrix DaaS vs move to AVD vs W365 mix), using the M2 scoring matrix + TCO sketch; deliverable is a recommendation deck/report — portfolio artifact #3.
4. `az-140-and-cert-roadmap` — AZ-140 logistics (format, measured skills, how domains map to Modules 3–6 of this course), study/practice plan, then the multi-platform roadmap: CCA-V, OCA-H, and adjacent certs (MD-102) — with the 2026 cert facts from the header of this file.
5. `resume-linkedin-and-interviews` — translating the three capstone artifacts into resume bullets, EUC-engineer LinkedIn positioning, common VDI interview questions (with strong answers): "walk me through the connection flow", "profile bloat", "how do you size a host pool", "AVD vs W365"; 2026 job-market notes for EUC roles.

## Deck-authoring spec (for implementing agents)

- Format: match `course-materials/cloud-security-engineer/decks/cse-m1-l01-*.json` EXACTLY in shape: keys `slug, title, month, monthTitle, lesson, summary, objectives, quiz, resources, body_markdown, slides`. **Omit the `video` key entirely** (videos deferred).
- `month` = module number (1–7); `monthTitle` = module title from course.json verbatim; `lesson` = lesson number within the module.
- `objectives`: 4–6 outcome-verb objectives.
- `quiz`: 5–6 questions; mostly 4-option MCQ (`answer` = 0-based index, `why` explains); include exactly ONE short-answer question per lesson (string `answer` = model answer, plus `why`) — mirroring the cse pattern.
- `resources`: 3–5 items with REAL urls — Microsoft Learn for AVD/W365; Citrix docs (docs.citrix.com), Omnissa docs/Tech Zone for their platforms. No invented URLs: if unsure of a deep link, link the product's docs landing page.
- `body_markdown`: the actual lesson, ~900–1500 words, teaching prose with ## sections, tables where they clarify, concrete commands/portal paths where applicable (PowerShell `Az.DesktopVirtualization`, Bicep snippets in M3). Write for a practitioner: every lesson should answer "what would I actually do".
- `slides`: 8–12 slides; first is `{type:"title", title, sub, narration}`, rest `{type:"content", title, bullets[3-5], narration}`. Narration = spoken-style paragraph (it becomes TTS later), no markdown in narration.
- Tone/quality bar: same as cloud-security-engineer course. Bake in the three specialist reviewer perspectives from the start: professor (pedagogy: each lesson builds on prior, objectives testable), industry peer (2026 real-world accuracy, real tools/JD language), cert examiner (AZ-140 domain coverage where mapped).
- Accuracy rules: prefer current product names (Microsoft Entra ID not Azure AD; Omnissa not VMware; app attach naming per fact-check). Anything marked **fact-check flag** above must be verified against vendor docs during authoring or flagged as `TODO-FACTCHECK` in a comment field for the review pass. Do not fabricate version numbers, prices, or exam question counts.

## Pipeline (after decks authored)

1. `python convert_decks_to_md.py vdi-engineer`
2. `python add_course_to_consts.py vdi-engineer`
3. `python build_catalog.py` — then ASSERT `vdi-engineer` present in `api/src/shared/catalog.generated.json` (known silent-drop gotcha; re-run if missing).
4. `python build_lesson_index.py` — assert vdi lessons present in `api/src/shared/lessons.generated.json`.
5. Site build (`npm --prefix site run build` or repo-standard command) + API tests (`api/test`).
6. Peer review (7-reviewer) + adversarial fact-check gate → fixes → scoped commit to dev (only `course-materials/vdi-engineer`, `site/src/consts.ts`, the two generated JSONs).
