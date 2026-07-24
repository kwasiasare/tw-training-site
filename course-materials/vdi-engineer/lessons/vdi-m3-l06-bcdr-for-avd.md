---
course: vdi-engineer
title: 'BCDR for AVD: Availability Zones, Backup Strategy, and Host Pool DR Patterns'
month: 3
monthTitle: 'Azure Virtual Desktop Infrastructure: Plan, Deploy & Scale'
lesson: 6
summary: This closing lesson of Module 3 answers what business continuity and disaster recovery actually
  mean for a fleet of mostly-disposable session hosts. You'll learn how availability zones protect the
  compute layer, the precise rule for what to back up versus what to rebuild from a golden image, how
  Azure Files redundancy tiers protect FSLogix profile storage, and how to choose between active-active
  and active-passive host pool DR patterns based on recovery time objectives.
objectives:
- Explain how availability zones and availability sets protect session hosts differently, for both pooled
  and personal host pools
- Apply the 'back up what you can't rebuild' rule to decide what in an AVD environment actually needs
  backup
- Choose the appropriate Azure Files redundancy tier (ZRS, GRS, GZRS) for FSLogix profile storage based
  on the failure scenario being protected against
- Compare active-active and active-passive host pool DR patterns and select one based on recovery time
  objective and cost
quiz:
- q: Why does deploying pooled host pool session hosts across multiple availability zones improve resilience?
  options:
  - It automatically backs up user profile data
  - It eliminates the need for an autoscale scaling plan
  - It converts pooled host pools into personal host pools automatically
  - It spreads session hosts across physically separate datacenters with independent power and networking,
    so a single zone outage only removes a fraction of total capacity rather than the whole pool
  answer: 3
  why: Availability zones are physically separate datacenters within a region with independent power,
    cooling, and networking. Spreading a pooled host pool's session hosts across multiple zones means
    a zone-level failure only removes the capacity in that zone, not the entire pool — the remaining zones
    (helped by autoscale) can absorb the load.
- q: According to the BCDR mental model in this lesson, which of the following should NOT be backed up
    at the VM level?
  options:
  - A non-persistent pooled session host VM, since it's entirely reproducible from the golden image and
    holds no user data locally
  - The FSLogix profile storage account/file share
  - The Azure Compute Gallery holding your golden image versions
  - Your Bicep/Terraform infrastructure-as-code definitions
  answer: 0
  why: The rule is 'don't back up what you can rebuild.' A non-persistent pooled session host holds no
    meaningful state of its own — user data lives in FSLogix profiles on Azure Files, and the OS/app state
    is entirely reproducible from the golden image — so VM-level backup of it wastes cost and time for
    no recovery benefit. The profile storage, the image gallery, and the IaC definitions are the things
    that actually need protecting.
- q: An organization's DR plan only needs to survive a single availability zone outage within the primary
    region, not a full regional outage. Which Azure Files redundancy tier is the appropriate baseline
    for FSLogix profile storage?
  options:
  - Locally redundant storage (LRS)
  - Zone-redundant storage (ZRS)
  - Geo-redundant storage (GRS) only, without ZRS
  - No redundancy is needed since FSLogix data is disposable
  answer: 1
  why: Zone-redundant storage (ZRS) replicates the Azure Files share synchronously across three availability
    zones in the region, which is exactly the protection needed against a single zone outage. Geo-redundant
    storage protects against a full regional failure, which is a different (and here, out of scope) requirement;
    locally redundant storage offers no zone protection at all.
- q: What is the key trade-off between an active-passive and an active-active host pool DR pattern?
  options:
  - Active-passive has a faster recovery time but is more expensive to run day to day
  - There is no cost difference between the two patterns
  - Active-active has near-zero recovery time but costs more because it runs production compute continuously
    in multiple regions; active-passive is cheaper day to day but has a real recovery time to stand up
    the secondary environment
  - Active-passive cannot use golden images or Azure Compute Gallery replication
  answer: 2
  why: Active-active runs host pools concurrently in multiple regions, so a regional failure is absorbed
    by the other region with minimal disruption, but at the cost of running duplicate production compute
    continuously. Active-passive only provisions the secondary region during a DR event (from IaC templates
    and a replicated golden image), which is cheaper but introduces a real recovery time that must be
    tested and documented rather than assumed.
- q: In two to four sentences, explain why FSLogix profile storage and the Azure Compute Gallery deserve
    more BCDR attention than most individual session host VMs in an AVD environment.
  answer: Most session host VMs, especially in pooled host pools, are deliberately stateless and can be
    rebuilt from the golden image in minutes, so they don't hold anything unique that needs protecting
    on their own. FSLogix profile storage is different because it holds the actual user data, application
    settings, and profile state that users would lose permanently if the storage were damaged or unavailable,
    and the Azure Compute Gallery is different because it holds the versioned golden images that every
    session host in the fleet depends on to be rebuilt in the first place — if the gallery were lost,
    you couldn't reconstruct the fleet even though the individual VMs themselves were never meant to be
    backed up. Protecting these two things with the right redundancy and backup strategy is what actually
    makes the 'rebuild, don't back up' approach to session hosts safe.
  why: 'This is the core BCDR insight for AVD: the stateless VM design only works as a cost and operations
    strategy if the small set of genuinely stateful, non-reproducible assets underneath it — profile storage
    and the golden image gallery — are protected with real rigor.'
resources:
- label: Business continuity and disaster recovery for Azure Virtual Desktop (Cloud Adoption Framework)
  url: https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/scenarios/azure-virtual-desktop/eslz-business-continuity-and-disaster-recovery
- label: Azure Virtual Desktop disaster recovery concepts
  url: https://learn.microsoft.com/en-us/azure/virtual-desktop/disaster-recovery-concepts
- label: Multiregion BCDR for Azure Virtual Desktop (Azure Architecture Center)
  url: https://learn.microsoft.com/en-us/azure/architecture/example-scenario/azure-virtual-desktop/azure-virtual-desktop-multi-region-bcdr
- label: Business continuity and disaster recovery options for FSLogix
  url: https://learn.microsoft.com/en-us/fslogix/concepts-container-recovery-business-continuity
- label: Azure Virtual Machines availability zones documentation
  url: https://learn.microsoft.com/en-us/azure/reliability/availability-zones-overview
video: vdi-m3-l06-bcdr-for-avd.mp4
---

## What "BCDR" Actually Means for a Stateless Fleet

Business continuity and disaster recovery for AVD looks different from BCDR for a traditional application, because most of your session hosts are deliberately **stateless** — you can rebuild a pooled, non-persistent host from the golden image in minutes. The real BCDR question for AVD is: what are the pieces that *aren't* disposable, and how do you protect *those*? This lesson closes out Module 3 by answering that precisely: availability zones for the compute layer, what actually needs backing up, Azure Files redundancy for FSLogix profiles, and the two host pool DR patterns you choose between.

## Availability Zones for Session Hosts

Azure Virtual Desktop doesn't have a single AVD-specific "enable DR" toggle — its resilience for the session host layer is built from standard Azure compute resiliency primitives applied deliberately:

- **Availability zones** spread session hosts across physically separate datacenters within a region, each with independent power, cooling, and networking, protecting against a zone-level outage. For a pooled host pool, deploying session hosts across two or three zones (rather than one) means a single zone failure only takes out a fraction of your capacity — combined with autoscale, the remaining zones can absorb the load, especially if you're not running at 100% utilization even during peak.
- **Availability sets** (grouping VMs across fault and update domains within a single datacenter) are the older, single-datacenter alternative — useful when zone support isn't available in a region, but they don't protect against a full datacenter/zone outage the way availability zones do.
- For **personal host pools**, zone placement is still worth doing, but remember each user's VM is a single instance — zone redundancy protects against the *zone* going down, not against that individual VM having a problem, so it's a complement to, not a substitute for, the backup strategy below.

## What to Back Up (and What Not To)

The single most important BCDR mental model for AVD: **don't back up what you can rebuild, back up what you can't.**

- **Golden images**: your Azure Compute Gallery image versions *are* your backup for session host state — as long as the gallery and its replication are intact, you can redeploy an entire pooled host pool's worth of session hosts from a known-good version. Protect the gallery itself with geo-redundant storage and cross-region replication rather than trying to "back up" individual stateless VMs.
- **Non-persistent pooled session hosts**: do not back these up as VMs. There is nothing on them worth restoring — user data doesn't live there (it's in FSLogix profiles on Azure Files), and the OS/app state is entirely reproducible from the golden image. Backing up disposable VMs wastes storage spend and backup-window time for zero recovery benefit.
- **Personal host pool session hosts**: these *can* hold meaningful local state beyond the golden image, since users may install their own apps or save files locally. If your organization allows that, personal host pool VMs are reasonable candidates for **Azure Backup** on the VM level, unlike pooled hosts.
- **FSLogix profile containers**: this is the data that actually matters to users day to day — their profile, app settings, and (depending on configuration) redirected data. Protect the **storage account/file share** holding these containers with Azure Backup for Azure Files (or NetApp Files snapshots, if that's your storage choice), not with per-session-host backup.
- **Configuration as code**: your Bicep/Terraform templates, Azure Image Builder definitions, and autoscale scaling plan definitions are themselves a form of backup — since they're what you'd use to rebuild the entire environment from scratch in a new region if it came to that. Keep them in source control with the same rigor as any other production infrastructure code.

## Azure Files Redundancy for FSLogix Profiles

Because FSLogix profile containers are the thing that actually needs protecting, the storage layer underneath them deserves the most redundancy attention:

- **Zone-redundant storage (ZRS)** replicates the Azure Files share synchronously across three availability zones in the region, so a zone outage doesn't take profile storage down with it — this is the recommended baseline for FSLogix storage accounts backing a production pool, since AVD session hosts across multiple zones need the profile store itself to survive a single zone failure too.
- **Geo-redundant storage (GRS)**, or geo-zone-redundant storage (GZRS) combining both, extends protection to a full **region** failure, replicating asynchronously to a paired region — the right choice when your DR plan includes failing over to session hosts in a second region entirely, not just surviving a zone event in the primary region.
- Regardless of the redundancy tier, **Azure Backup for Azure Files** gives you point-in-time recoverability for the profile share itself — protecting against corruption or accidental deletion of profile data, which storage redundancy alone doesn't address (redundancy protects against infrastructure failure, not against a bad write replicating everywhere instantly).

## Active-Active vs. Active-Passive Host Pool DR Patterns

When your DR requirement extends beyond a single region — a full regional outage, not just a zone event — you choose between two host pool patterns:

- **Active-passive**: host pools and session hosts exist in a primary region only during normal operations. In a DR event, you deploy (or activate previously deployed-but-empty) host pools, application groups, and workspaces in the secondary region from your Bicep/Terraform templates and golden image (already replicated there via Azure Compute Gallery), point FSLogix at the geo-replicated profile storage, and redirect users to the secondary region's workspace. This is cheaper day-to-day since you're not running duplicate compute, but it has a real **recovery time** — the time to stand up the secondary environment — that you need to test and document, not assume.
- **Active-active**: host pools run concurrently in two (or more) regions, with users assigned or load-balanced across both under normal conditions. A regional failure simply means the other region absorbs the affected users, often via workspace/feed configuration or Global Traffic Manager-style routing at the client level. This gives near-zero recovery time but costs meaningfully more, since you're running production compute in both regions continuously rather than only provisioning the second region when you need it.

The right choice depends on your **recovery time objective (RTO)**: if the business can tolerate the time it takes to stand up a secondary environment from code and geo-replicated storage, active-passive is more cost-effective. If any downtime beyond a failover blip is unacceptable, active-active is the only pattern that delivers that, at a real ongoing cost.

## Bringing Module 3 Together

Across this module you've gone from the architectural model (Lesson 1), through networking (Lesson 2), images and sizing (Lesson 3), deployment automation (Lesson 4), and cost optimization (Lesson 5), to this lesson's resilience story. The common thread is worth stating explicitly: AVD's design leans hard on treating session hosts as **disposable, rebuildable compute** driven from **code and versioned images**, with the durable, precious state concentrated in a much smaller set of things — FSLogix profile storage, your image and IaC definitions, and identity — that get protected deliberately and specifically. That's the mental model AZ-140 Domain 1 is testing, and it's the mental model that will keep you from over-engineering backup for VMs that were never meant to be permanent in the first place.
