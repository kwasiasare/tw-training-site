---
course: vdi-engineer
title: 'Image and Host Lifecycle: Patching, Versioning, and Rolling Updates'
month: 6
monthTitle: Monitoring, Operations & Troubleshooting
lesson: 2
summary: Keeping session hosts patched at scale is a lifecycle problem, not a per-VM chore. This lesson
  covers the two competing patching philosophies — patch the running host versus rebuild from a versioned
  golden image — and lands firmly on why Microsoft designs AVD around the second. You'll walk through
  Azure Compute Gallery image versioning cadence, the session host update feature's batch-based drain-and-replace
  mechanics, and the Scheduled Agent Updates feature that governs when the AVD agent itself updates. You'll
  finish knowing how a rolling update actually behaves in production, including the gotchas that catch
  teams off guard the first time they run one.
objectives:
- Compare golden-image patching against in-place per-host patching and state when each is appropriate
- Describe Azure Compute Gallery image definitions and versions, and propose a sane versioning cadence
- Explain the session host update process end to end, including batching, the initial test host, and drain
  mode's role
- Configure Scheduled Agent Updates maintenance windows for the AVD agent, side-by-side stack, and Geneva
  Monitoring agent
- Identify the operational gotchas that most often break a rolling session host update
quiz:
- q: Which approach does Microsoft recommend for keeping AVD session hosts current over time?
  options:
  - Patch each running VM individually, forever, with no image strategy
  - Manage updates in the core source image and replace hosts from it, rather than patching each host
    repeatedly
  - There is no recommended pattern; either approach is equally supported
  - Only ever use Windows Update directly on each host and ignore Azure Compute Gallery
  answer: 1
  why: Microsoft Learn describes session host update as aligning 'with the recommendation of managing
    updates within the core source image, rather than distributing and installing updates to each session
    host individually on an ongoing repeated schedule.'
- q: During a session host update, what happens to a targeted session host immediately before it's removed
    from the host pool and its VM is deleted?
  options:
  - It's force-restarted instantly, dropping any active sessions without warning
  - It's deleted while still actively accepting new connections
  - It's placed into drain mode so it stops accepting new sessions while existing ones finish, then removed
    once empty
  - Nothing changes about its session-acceptance state before deletion
  answer: 2
  why: The documented process places selected hosts into drain mode and sends a sign-out notification
    before removing them from the host pool; the original VMs are deleted only after the replacement hosts
    have joined and drain mode is disabled on the new ones.
- q: What does the 'batch' size control during a session host update?
  options:
  - The total number of session hosts that will ever exist in the pool
  - How many users are allowed to be signed in during the entire update
  - The retention period for Log Analytics ingestion
  - The maximum number of session hosts unavailable/updating at the same time, after the single initial
    test host completes
  answer: 3
  why: Session host update first updates a single 'initial' host to validate the process, then updates
    the remaining hosts in batches of the configured size, so only that many hosts are unavailable at
    once.
- q: Is Scheduled Agent Updates enabled by default on a host pool, and how do you turn it on for a brand-new
    host pool?
  options:
  - It's disabled by default, and it can only be configured on an existing host pool — not at host pool
    creation time
  - It's enabled by default with one maintenance window automatically chosen
  - It's enabled by default but can be fully disabled only via PowerShell
  - It's mandatory and cannot be disabled once a host pool exists
  answer: 0
  why: Scheduled Agent Updates is disabled by default (meaning the agent can update anytime via the flighting
    service), and Microsoft Learn is explicit that you can only configure this feature for existing host
    pools — you can't enable it when you create a new one.
- q: If an agent component update fails inside its configured maintenance window, how many total attempts
    will the broker make before forcing the install?
  options:
  - One attempt only, then it waits for the next maintenance window
  - Up to four attempts, after which the broker force-installs the update
  - Two attempts
  - Ten attempts across ten separate windows
  answer: 1
  why: Microsoft Learn states the broker attempts to update agent components during each maintenance window
    up to four times; after the fourth try it installs the update by force, and critical security updates
    can be force-installed outside this retry logic entirely.
- q: A colleague suggests just RDP'ing into each of 40 pooled session hosts every month to run Windows
    Update by hand. Explain why this doesn't scale, and name the AVD-native alternative that solves the
    problem.
  answer: 'Manually patching each host doesn''t scale because it''s slow and error-prone, it produces
    configuration drift (some hosts patched, some not, or patched at slightly different times), it doesn''t
    help when you also need to change VM size, disk type, security type, or other configuration, and it
    leaves no consistent audit trail. The AVD-native alternative is session host update, a host pool feature
    built on a session host configuration: it rolls out an updated image (from Azure Compute Gallery,
    a managed image, or Marketplace) by draining, replacing, and rejoining session hosts in controlled
    batches, testing on one initial host first, so every host in the pool ends up standardized on the
    same image rather than patched piecemeal.'
  why: This restates the documented rationale for session host update — managing updates in the source
    image instead of distributing them host by host — plus the batch/drain/replace mechanics covered in
    this lesson.
resources:
- label: Session host update (AVD)
  url: https://learn.microsoft.com/en-us/azure/virtual-desktop/session-host-update
- label: Azure Virtual Desktop Scheduled Agent Updates
  url: https://learn.microsoft.com/en-us/azure/virtual-desktop/scheduled-agent-updates
- label: Drain session hosts for maintenance
  url: https://learn.microsoft.com/en-us/azure/virtual-desktop/drain-mode
- label: Azure Compute Gallery overview
  url: https://learn.microsoft.com/en-us/azure/virtual-machines/azure-compute-gallery
- label: Windows Update for Business overview
  url: https://learn.microsoft.com/en-us/windows/deployment/update/waas-manage-updates-wufb
video: vdi-m6-l02-image-and-host-lifecycle.mp4
---

## Two Philosophies, One Winner

There are two ways to keep a fleet of session hosts current: patch each running VM in place, forever, or treat the image as the source of truth and periodically replace hosts wholesale from an updated version of it. Traditional server admins default to the first because it's what you'd do with a handful of physical servers. It falls apart at AVD scale: forty hosts patched over forty separate maintenance windows drift out of sync with each other, some picking up a driver update before others, some silently failing a patch and nobody noticing until a user hits it. Microsoft's own guidance for AVD is explicit — manage updates in the core source image, and replace hosts from it, rather than distributing and installing updates to each host individually on a repeated schedule. This lesson is about making that pattern real: Azure Compute Gallery versioning, the session host update feature that performs the replacement, and Scheduled Agent Updates for the one component that still updates in place — the AVD agent itself.

## Azure Compute Gallery Versioning Cadence

Your golden image build (Module 3) produces a VM you generalize and capture into an **Azure Compute Gallery image definition**. Each subsequent build produces a new **image version** under that definition — a immutable, numbered snapshot (e.g., `1.0.0`, `1.1.0`, `1.2.0`) you can replicate to the regions your session hosts live in. A workable cadence for most estates: rebuild monthly aligned to Patch Tuesday, plus an out-of-band rebuild for anything security-critical. Keep a **test ring** — a small pilot host pool that gets the new version first — before you push it to production pools with session host update. Never patch a live golden image VM and recapture it without going through this staged flow; an unvalidated image pushed straight to production is how a bad driver or a broken FSLogix hook takes down every session host in a pool at once.

## Session Host Update: The Mechanics

**Session host update** operates on a host pool that uses a **session host configuration** (Microsoft's newer host-pool-management approach). It doesn't patch VMs — it deallocates or deletes the existing ones and creates new VMs from your updated configuration: image, VM size, disk type, security type (Standard, Trusted Launch, or Confidential), domain-join credentials, Intune enrollment, local admin credentials, and an optional custom PowerShell script.

The process runs in a specific order:

1. You choose a **batch size** — the maximum number of hosts unavailable at once. The update always starts by targeting a single **initial** host first, to prove the end-to-end process works before touching the rest of the pool. This is a deliberate blast-radius control: if your new image is broken, you find out with one host down, not all of them.
2. Existing users on a targeted host get a notification, then after a configured wait the host is placed into **drain mode** and removed from the pool. If it's Active Directory-joined, the **computer account is not deleted** — it becomes temporarily orphaned.
3. A new VM is created with the updated configuration. Its Azure resource name follows the pattern `SessionHostName-DateTime` (e.g., `VM1-0` becomes `VM1-0-2023-04-15T17-16-07`), but the **OS hostname stays the same**, so it inherits the orphaned AD computer object and existing Group Policy targeting continues to apply.
4. The new host joins the pool, drain mode is disabled, and it starts accepting connections. Only after that does the original VM get deleted.

Only one update can run per host pool at a time (though different pools can update concurrently), and the existing power state and drain mode of hosts is honored — you can even run an update against a fully deallocated pool to save cost during the process.

## Gotchas That Catch Teams the First Time

A few things the documentation calls out as **known issues** that will bite you if you skip them:

- **Disable autoscale before updating.** If a scaling plan is active during a session host update, the update can fail with a runtime error. Turn autoscale off, run the update, turn it back on.
- **Azure Virtual Desktop Insights doesn't self-heal.** The Azure Monitor Agent is *not* automatically reinstalled on the new hosts after an update. If you rely on Insights (Lesson 1), either enforce AMA via Azure Policy or you'll silently lose monitoring coverage on every host that gets replaced.
- **Manual customizations don't survive.** Anything hand-installed on a session host outside the image — a registry tweak, a certificate, a one-off file — disappears when that host is replaced. Bake it into the image, apply it via Intune/GPO, or add it to the custom configuration PowerShell script.
- **Test on a pilot pool first.** Because the new VM reuses the old hostname and AD computer object, there are subtle domain and GPO-targeting effects worth validating outside production.
- **Progress reporting is chunky, not smooth.** In a 10-host pool, progress shows 0% while the initial host updates, then jumps to 10% once it completes — don't assume a stall.

## Scheduled Agent Updates: The One Thing Still Updated In Place

While session host update refreshes the OS and configuration, the **AVD agent, its side-by-side stack, and the Geneva Monitoring agent** update independently and in place on the running host — this is what **Scheduled Agent Updates** controls. It's a host-pool-level setting, **disabled by default**, meaning without it the agent can update at any time via Microsoft's flighting service. Enabling it gives you up to **two maintenance windows**, each **two hours long**, in either a single time zone for the whole pool or each host's local time zone. Within a window, the broker retries a failed component update **up to four times**, then force-installs it; a **critical security update bypasses this schedule entirely** and installs immediately regardless of window. Note this doesn't apply to the *initial* agent install on a new VM — that always happens on VM creation, window or not.

## Windows Update on the Hosts Themselves

Separate from both mechanisms above, the Windows OS on your session hosts (and on Windows 365 Cloud PCs) still needs conventional Windows updates for the OS and Microsoft 365 Apps. Most estates manage this the same way they manage any Intune-enrolled Windows fleet: **Windows Update for Business** policies through Intune, layered with deferral rings so you're not deploying an untested cumulative update to production the day it ships. For pooled, non-persistent hosts, many teams deliberately keep Windows Update rings conservative or even minimal on the running hosts and let the *image* absorb most patching — reinforcing the same golden-image-first philosophy this whole lesson is built around.

## What You'd Actually Do

Build a monthly image cadence with a pilot ring; use session host update with a sensible batch size (small enough to protect capacity, large enough to finish overnight) and always let the single initial host validate first; disable autoscale for the update window and confirm AMA re-enrollment afterward; turn on Scheduled Agent Updates with two off-hours maintenance windows so agent updates never surprise you mid-shift; and keep OS-level Windows Update policy conservative on running hosts because the image, not the host, is where you actually manage change.
