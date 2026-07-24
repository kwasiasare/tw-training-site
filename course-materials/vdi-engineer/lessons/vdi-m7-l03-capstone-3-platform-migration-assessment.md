---
course: vdi-engineer
title: 'Capstone 3: Multi-Platform VDI Migration Assessment'
month: 7
monthTitle: Capstone Projects & Career Launch
lesson: 3
summary: 'Real EUC engineers are asked to make vendor-neutral recommendations, not just build one platform.
  In this capstone you assess a fictional 1,200-user logistics company running aging on-premises Citrix,
  and decide whether it should stay on Citrix DaaS, move fully to Azure Virtual Desktop, or split across
  platforms including Windows 365. You''ll reuse the weighted scoring matrix from Module 2''s platform-choice
  framework, sketch a TCO comparison, and produce a phased migration plan and a recommendation report
  — portfolio artifact #3, and the one that best proves you think like a platform-agnostic architect rather
  than a single-vendor specialist.'
objectives:
- Apply a weighted scoring matrix to compare competing VDI/DaaS platforms for a specific organization
- Reason about existing licensing investment, persistence mix, and peripheral needs as first-class migration
  criteria, not afterthoughts
- Sketch a directional TCO comparison across an on-prem refresh, a Citrix DaaS move, and an AVD/Windows
  365 split
- Design a phased migration plan that sequences the lowest-risk user population first
- Write a vendor-neutral recommendation report that a non-technical executive could act on
quiz:
- q: Solborne Logistics' 900 warehouse and dispatch staff use one kiosk-style app with almost no personalization.
    In the scoring matrix, which platform tends to score highest for this population specifically?
  options:
  - Windows 365 personal Cloud PCs, because persistence is the priority
  - Whichever platform has the most colorful marketing
  - Azure Virtual Desktop pooled multi-session, because it's built for exactly this high-density, low-persistence,
    cost-sensitive pattern
  - None of the platforms — this population should stay on physical desktops
  answer: 2
  why: 'Pooled multi-session is the design pattern built for high-volume, low-customization task workers:
    many users share fewer hosts, which drives down cost per user. Windows 365''s personal-only model
    is the wrong shape for this specific population, even though it may be the right choice elsewhere
    in the same organization.'
- q: Why does the scoring matrix include 'existing investment' as a weighted criterion rather than just
    picking the technically best platform?
  options:
  - Existing investment should always be ignored in a good technical assessment
  - It's a marketing requirement, not an engineering one
  - Existing investment only matters for on-premises data centers, not cloud licensing
  - A live Citrix ELA with 18 months remaining, and years of in-house Citrix Director/scripting expertise,
    are real switching costs and real assets that change which option is actually cheapest and lowest-risk,
    not just which is newest
  answer: 3
  why: A defensible platform recommendation accounts for sunk costs that still carry value (remaining
    license term, staff expertise) as real inputs to switching cost and risk, not just raw technical merit.
    Ignoring existing investment produces a recommendation that looks good on a whiteboard but is expensive
    or risky to actually execute.
- q: Why might the recommendation keep the 50-person GIS/route-optimization power-user group on Citrix
    DaaS with HDX 3D Pro rather than moving them to AVD in the first migration wave?
  options:
  - Their peripheral and protocol needs are the most demanding and least proven in the new environment,
    so it's lower-risk to migrate the largest, most standardized population first and revisit the specialized
    GPU cohort once the pattern is validated
  - GPU workloads cannot run on Azure at all
  - Citrix is always technically superior for every workload
  - Power users should never be migrated under any circumstances
  answer: 0
  why: Phased migration plans sequence the lowest-risk, most-standardized population first to build confidence
    and de-risk the overall project, and leave the smallest, most specialized, highest-peripheral-complexity
    group for a later phase where the migration pattern has already been proven — not because the target
    platform can't technically support GPU workloads.
- q: What is the primary purpose of a directional TCO sketch in a migration assessment like this one?
  options:
  - To produce an exact, guaranteed final invoice for the CFO
  - To compare the order of magnitude of costs across options (avoided hardware refresh, licensing overlap,
    fixed vs. variable cloud opex) so the recommendation is grounded in economics, not just technical
    preference
  - To replace the need for any architecture discussion entirely
  - To prove that on-premises is always the cheapest option
  answer: 1
  why: A TCO sketch at this stage is directional, not a committed quote — its job is to show the relative
    shape of costs (e.g., an avoided six-figure hardware refresh, existing Microsoft licensing that already
    covers AVD access rights, Windows 365's fixed per-user pricing vs. AVD's variable compute) so the
    recommendation is defensible on economics, not just architecture.
- q: Why does the recommendation put persistent analyst desktops on Windows 365 rather than a persistent
    AVD host pool?
  options:
  - AVD cannot support persistent desktops
  - Windows 365 is always cheaper than AVD for every workload
  - Windows 365's fixed per-user, per-month pricing and simpler, SaaS-style management fit a population
    needing predictable, always-available personal desktops better than owning and autoscaling personal
    AVD hosts would
  - Persistent desktops are being eliminated in this migration entirely
  answer: 2
  why: AVD can absolutely run personal, persistent host pools — but Windows 365's SaaS model trades some
    flexibility for simpler management and predictable fixed pricing, which is a good fit for a population
    that needs reliable, always-there personal desktops without a team having to own the underlying host
    pool and autoscale logic themselves.
- q: In three to five sentences, explain why this capstone's recommendation is a hybrid across three platforms
    rather than a single winner-take-all platform choice, and why that is a more credible answer than
    picking one platform for the whole company.
  answer: 'Solborne Logistics has three populations with genuinely different needs: high-density task
    workers, persistent knowledge workers, and a small GPU-dependent specialist group, and no single platform
    is the best fit for all three at once. A hybrid recommendation — AVD pooled for warehouse staff, Windows
    365 for persistent analysts, and Citrix DaaS retained short-term for the GPU cohort — matches infrastructure
    to workload the same way the host-pool design in Capstone 1 did, rather than forcing a one-size-fits-all
    answer for cost or simplicity''s sake. It''s also more credible to a real hiring manager or client,
    because it shows the engineer weighed trade-offs per population instead of defaulting to whichever
    platform they personally know best. A forced single-platform answer would either overpay for GPU-capable
    infrastructure for task workers, or under-serve the GPU cohort''s peripheral and protocol needs —
    both real risks a mixed recommendation avoids.'
  why: A strong answer explicitly connects the hybrid recommendation to the three distinct personas' needs,
    echoes the 'match infrastructure to workload' principle from earlier in the course, and explains why
    forcing a single-platform answer would create real downside for at least one population.
resources:
- label: Citrix DaaS overview
  url: https://docs.citrix.com/en-us/citrix-daas/overview.html
- label: Omnissa Horizon product documentation
  url: https://docs.omnissa.com/category/Horizon
- label: Windows 365 documentation
  url: https://learn.microsoft.com/en-us/windows-365/
- label: Understand and estimate costs for Azure Virtual Desktop
  url: https://learn.microsoft.com/en-us/azure/virtual-desktop/understand-estimate-costs
video: vdi-m7-l03-capstone-3-platform-migration-assessment.mp4
---

## The Case Study

Solborne Logistics runs 1,200 users across three distribution hubs on an aging on-premises Citrix Virtual Apps and Desktops estate. The hardware is out of warranty and due for refresh in nine months — that deadline is what's forcing the decision, not enthusiasm for change. Three populations: 900 warehouse and dispatch staff on pooled, kiosk-style desktops running a single warehouse management app; 250 route-planning analysts and customer service staff on persistent desktops running Office and a line-of-business transportation management system; and 50 GIS and route-optimization power users running GPU-accelerated modeling software. Solborne has 18 months left on a Citrix enterprise license agreement and deep in-house Citrix Director and scripting expertise. Leadership wants a recommendation: stay on Citrix but move to Citrix DaaS on Azure, replatform fully to Azure Virtual Desktop, or split the estate across platforms.

This is the vendor-neutral capstone. There is no "correct" platform in the abstract — there's only the platform (or mix of platforms) that best fits Solborne's specific populations, existing investment, and constraints.

## The Scoring Matrix

Reuse the decision framework from Module 2's platform-choice lesson: score each option against the same weighted criteria used there — **existing investment**, **cloud strategy alignment**, **persistent vs. pooled mix fit**, **protocol/peripheral needs**, **budget model** (fixed opex vs. variable), and **compliance/sovereignty**. Assign each criterion a weight from 1 to 5 based on how much it matters to Solborne specifically, score each platform option 1 to 5 against each criterion, multiply, and sum.

| Criterion | Weight | Citrix DaaS (Azure) | Pure AVD | AVD + Windows 365 split |
|---|---|---|---|---|
| Existing investment (ELA, staff skill) | 5 | 5 | 2 | 3 |
| Cloud strategy alignment | 4 | 3 | 5 | 5 |
| Persistent/pooled mix fit | 5 | 4 | 3 | 5 |
| Protocol/peripheral needs (GIS/GPU) | 4 | 5 | 3 | 4 |
| Budget model fit | 3 | 3 | 3 | 5 |
| Compliance/sovereignty | 3 | 4 | 4 | 4 |
| **Weighted total** | | **98** | **78** | **103** |

The mixed option comes out ahead — not because any single platform "wins," but because it lets each population land on the platform actually shaped for it.

## The Recommendation

**Migrate the 900 pooled warehouse and dispatch users to Azure Virtual Desktop** first. This population is the largest, the most standardized, and the lowest-risk to move — a single kiosk app on pooled multi-session hosts, and Solborne already owns the Microsoft licensing that covers AVD access rights. **Move the 250 persistent analysts to Windows 365.** Their need is a predictable, always-available personal desktop, and Windows 365's fixed per-user pricing and SaaS-simple management fit that better than owning and autoscaling a persistent AVD host pool would. **Keep the 50 GIS/GPU power users on Citrix DaaS on Azure for now**, preserving HDX 3D Pro's mature protocol handling for demanding peripherals, and revisit whether AVD's NV-series GPU SKUs and vGPU licensing are a clean fit once the rest of the migration has proven the pattern.

## The TCO Sketch

This is directional, not a committed quote — its job is to ground the recommendation in economics. Three shapes of cost matter here: the **avoided hardware refresh** (a six-figure on-premises spend that disappears entirely if the pooled and persistent populations move to cloud platforms before the nine-month deadline); the **licensing overlap**, since Solborne's existing Microsoft 365 E3/E5 entitlements already cover AVD user access rights, reducing incremental licensing cost for that piece; and the **fixed-vs-variable opex trade-off**, where Windows 365's flat per-user, per-month price is easier to forecast for the persistent population than AVD's variable compute cost would be, while AVD's variable pricing is actually the better fit for the pooled population because autoscale lets that cost track real usage down to near-zero overnight.

## The Migration Phasing Plan

**Phase 0 — Pilot.** One hub, roughly 50 pooled users and 10 persistent users, to validate the FSLogix profile experience, network path, and user acceptance before committing further.

**Phase 1 — Pooled rollout.** Move the remaining warehouse and dispatch population across all three hubs to AVD, in waves by hub, so any issue is contained to one site at a time.

**Phase 2 — Persistent rollout.** Move the analyst population to Windows 365, coordinated with device refresh where it overlaps.

**Phase 3 — Reassess the GPU cohort.** Once Phases 1 and 2 are stable, revisit whether the power-user group should move to AVD GPU SKUs or remain on Citrix DaaS long-term.

**Phase 4 — Decommission.** Retire the on-premises Citrix hardware once the ELA term and hardware lease both allow it, avoiding early-termination costs.

## The Deliverable

Package this as a recommendation report or short deck: executive summary, the scoring matrix table, the TCO sketch, the phased plan, and a brief risk register (the two most obvious risks here are GPU peripheral compatibility during Phase 3, and user resistance to losing a persistent desktop feel during the Phase 1 pooled migration). Write it for a non-technical executive audience — the technical justification lives in the appendix, but the front page should be a clear, confident recommendation they can act on.

## Why a Scoring Matrix Beats a Gut Call

It would be faster to just recommend "move everything to AVD" or "stay on Citrix" from experience and skip the matrix entirely. Resist that instinct, both in this capstone and in a real job. A weighted scoring matrix does two things a gut call can't: it forces you to name the criteria that actually matter to *this* organization before you know which answer they point to, which guards against picking a platform first and rationalizing it afterward; and it gives a skeptical executive, or a skeptical interviewer, something concrete to push back on and debate, rather than just your word. If a stakeholder disagrees with the recommendation, the matrix gives you a productive conversation — "you think peripheral needs should be weighted higher than budget model, let's talk about why" — instead of a standoff. That's the difference between an opinion and an assessment, and it's exactly the kind of structured reasoning a hiring manager is listening for when they ask how you'd make a platform recommendation in an interview.
