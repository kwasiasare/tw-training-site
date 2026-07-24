---
course: vdi-engineer
title: 'Autoscale and Cost Optimization: Scaling Plans, Start VM on Connect, and Hibernation'
month: 3
monthTitle: 'Azure Virtual Desktop Infrastructure: Plan, Deploy & Scale'
lesson: 5
summary: Session host compute is the biggest controllable cost in most AVD deployments. This lesson covers
  autoscale scaling plans for both pooled and personal host pools, Start VM on Connect, the generally
  available hibernation feature for personal host pools, drain mode as the manual control underneath all
  of this automation, an ongoing right-sizing discipline, and how Reserved Instances or Savings Plans
  combine with autoscale to build a real cost-per-user model.
objectives:
- Explain how autoscale scaling plans differ for pooled versus personal host pools
- Describe how Start VM on Connect reduces cost for infrequently used session hosts
- State the current (GA) status of hibernation for personal host pools and when to use it instead of full
  deallocation
- Use drain mode correctly as the manual control underneath autoscale and host refresh operations
- Build a simple cost-per-user model that combines right-sizing, autoscale, and Reserved Instances or
  Savings Plans
quiz:
- q: Why does depth-first load balancing pair naturally with an autoscale scaling plan for a pooled host
    pool?
  options:
  - Depth-first is required before autoscale can be enabled at all
  - Depth-first only works with personal host pools
  - Depth-first consolidates sessions onto fewer hosts by filling each one before starting another, which
    is exactly the condition that lets the scaling plan deallocate the remaining, now-empty hosts
  - Depth-first automatically enables hibernation
  answer: 2
  why: Depth-first fills one session host to its session limit before routing new sessions to the next
    host. That consolidation is what creates genuinely empty, idle hosts during ramp-down and off-peak
    periods — hosts an autoscale plan can then safely deallocate, which is the entire point of pairing
    the two.
- q: What does Start VM on Connect actually do?
  options:
  - It permanently keeps all session hosts running so connections are always instant
  - It replaces the need for an autoscale scaling plan entirely
  - It only applies to session hosts using ephemeral OS disks
  - It allows a session host to remain deallocated, incurring no compute cost, until a user attempts to
    connect, at which point the specific VM (personal) or an available VM (pooled) is automatically powered
    on for that session
  answer: 3
  why: 'Start VM on Connect is a reactive, on-demand power-on mechanism: the VM stays off (and free of
    compute charges) until a connection attempt triggers it to start. It complements, rather than replaces,
    a scheduled autoscale scaling plan — the plan handles predictable ramp patterns, and Start VM on Connect
    handles unplanned or infrequent connections outside those schedules.'
- q: What is the current status of hibernation support for personal host pool session hosts, and what
    does hibernation do differently from a full deallocation?
  options:
  - It is generally available; hibernation writes memory state to disk before powering down, so the next
    Start VM on Connect resumes closer to where the user left off, while still stopping compute billing
    during the hibernated period
  - It is still in private preview and unavailable to most customers; deallocation and hibernation are
    functionally identical
  - It is generally available but only for pooled host pools, never personal
  - It is generally available but provides no cost benefit compared to leaving the VM running
  answer: 0
  why: Hibernation for personal host pool session hosts is GA. Unlike a full deallocation, which discards
    in-memory state and forces a cold boot next time, hibernation preserves memory state to disk, giving
    users a faster, warmer resume on their next connection, while still avoiding compute charges during
    the hibernated period — combining a cost benefit with a better user experience than a cold start.
- q: An engineer needs to patch a single problem session host in a pooled host pool without disconnecting
    the three users currently signed into it. What's the correct first action?
  options:
  - Immediately deallocate the VM, which will gracefully migrate active sessions to another host
  - Put the host into drain mode so it stops accepting new sessions, then patch it once the existing sessions
    end naturally or during a scheduled maintenance window
  - Delete the session host from the host pool and recreate it
  - Disable the host pool's autoscale scaling plan entirely
  answer: 1
  why: Drain mode marks a host unavailable for new sessions while letting existing sessions continue uninterrupted
    — exactly the tool for patching or troubleshooting one host without disrupting users already connected
    to it. Deallocating or deleting the VM would forcibly end those active sessions, which is not what
    the scenario calls for.
- q: Why should Reserved Instances or Savings Plans typically be purchased to cover baseline capacity
    rather than full fleet capacity in an autoscaled AVD environment?
  options:
  - Because Reserved Instances cannot be applied to session host VMs at all
  - Because Savings Plans and autoscale are mutually exclusive and cannot be used together
  - Because autoscale is specifically designed to scale burst/peak capacity up and down, and committing
    a reservation to capacity that isn't always running defeats the purpose of the commitment discount
  - Because baseline capacity is always billed at a lower rate automatically
  answer: 2
  why: Reserved Instances and Savings Plans discount the price of compute you commit to running continuously.
    Applying that commitment to the minimum, always-on baseline capacity makes sense; applying it to burst
    capacity that autoscale deliberately turns on and off wastes the commitment, since you'd be paying
    for a reservation on hours the VM isn't even running.
- q: In two to four sentences, describe how to build a cost-per-user model for an AVD environment and
    explain why it's a better steering metric than total monthly session host spend alone.
  answer: 'Build the model by taking total monthly session host compute cost (after any Reserved Instance
    or Savings Plan discounts are applied) and dividing it by the number of active monthly users on that
    host pool or environment, then tracking that ratio over time as you tune autoscale, right-size VM
    SKUs, and adjust commitment coverage. It''s a better steering metric than raw spend alone because
    it normalizes for growth: a host pool whose total bill went up because it now serves more users can
    still show an improving (falling) cost-per-user trend, which is the actual signal that your optimization
    work — not just your headcount — is paying off, whereas total spend alone conflates the two.'
  why: Total compute spend is a poor optimization signal on its own because it moves with both efficiency
    and growth at the same time; normalizing to cost-per-user isolates whether your autoscale, right-sizing,
    and commitment strategy are genuinely working.
resources:
- label: Create and assign an autoscale scaling plan for Azure Virtual Desktop
  url: https://learn.microsoft.com/en-us/azure/virtual-desktop/autoscale-create-assign-scaling-plan
- label: Configure Start VM on Connect for Azure Virtual Desktop
  url: https://learn.microsoft.com/en-us/azure/virtual-desktop/start-virtual-machine-connect
- label: Azure Virtual Desktop autoscale FAQ
  url: https://learn.microsoft.com/en-us/azure/virtual-desktop/autoscale-faq
- label: Autoscale scaling plans and example scenarios
  url: https://learn.microsoft.com/en-us/azure/virtual-desktop/autoscale-scenarios
- label: Reservations for Azure Virtual Machines
  url: https://learn.microsoft.com/en-us/azure/cost-management-billing/reservations/save-compute-costs-reservations
---

## Why This Is Where the Money Is

Session host compute is usually the single largest recurring line item in an AVD deployment, and it's also the line item you have the most control over. This lesson covers the tools that turn "VMs running 24/7 whether anyone's using them or not" into a cost profile that actually tracks real usage: autoscale scaling plans, Start VM on Connect, hibernation for personal hosts, drain mode, right-sizing, and the commercial levers (Reserved Instances and Savings Plans) layered on top.

## Autoscale Scaling Plans

An **autoscale scaling plan** is an Azure Virtual Desktop resource that automatically starts, stops, or hibernates session hosts on a schedule and in response to load, instead of requiring an admin (or a separate runbook) to manage capacity by hand. Scaling plans support both host pool types, but the mechanics differ:

- **Pooled scaling plans** define **ramp-up**, **peak**, **ramp-down**, and **off-peak** phases across the day, each with its own load-balancing algorithm and capacity thresholds (for example, minimum percentage of hosts running, or a target number of sessions per host before starting another one). During ramp-down, the plan can force logoffs after a warning, and during off-peak it can scale down to a minimum number of hosts — this is where **depth-first** load balancing (Lesson 1) pairs naturally with autoscale, since consolidating sessions onto fewer hosts is exactly what lets the plan deallocate the rest.
- **Personal scaling plans** work differently because each user owns a specific VM: instead of load-balancing across a pool, the plan defines schedules for when a user's assigned VM should start, and what should happen to it when the user disconnects or logs off during different times of day — deallocate, or (where enabled) **hibernate**.

You can assign one scaling plan to multiple host pools if their schedules and capacity needs line up, or build separate plans for pools with genuinely different usage patterns (a follow-the-sun global pool looks nothing like a single-region 9-to-5 pool).

## Start VM on Connect

**Start VM on Connect** lets a session host stay deallocated — costing nothing in compute — until a user actually tries to connect, at which point AVD automatically powers on the specific VM (for personal pools) or an available VM in the pool (for pooled pools) just in time for the session to begin. This is what makes a personal host pool genuinely cost-efficient for users who don't need their desktop every single day: the VM only runs when someone is using it, rather than sitting powered on and billing around the clock waiting for a connection that might not come until next week. Start VM on Connect is a host pool-level setting (`startVMOnConnect` in the resource model you saw in the deployment lesson) and works alongside, not instead of, an autoscale scaling plan — the scaling plan handles proactive schedule-driven scaling, while Start VM on Connect handles the reactive "someone just showed up" case outside those schedules.

## Hibernation for Personal Host Pools

**Hibernation** support for AVD session hosts in personal host pools is **generally available**: rather than fully deallocating a VM on disconnect or logoff (which discards RAM state and means the next session starts from a cold boot), hibernation writes memory state to disk and powers the VM down, so the next Start VM on Connect resumes the user's session much closer to where they left off — open applications and all — while still stopping compute billing during the hibernated period. You can enable hibernation when you deploy personal host pool session hosts (portal, PowerShell, CLI, ARM/Bicep, or the underlying APIs), and a personal scaling plan can choose hibernation specifically as the scaling action to take after a user disconnects or logs off for a configurable idle period — combining the cost benefit of powering down with a faster, warmer resume than a cold start. Hibernation requires the VM size and OS configuration to support it (not every SKU does), so factor hibernation support into your sizing decision from Lesson 3 if this is part of your cost strategy.

## Drain Mode

**Drain mode** marks a session host as unavailable for *new* sessions while allowing existing sessions to continue uninterrupted. It's the manual control you reach for outside of autoscale's automated ramp-down behavior: putting a host into maintenance for patching, safely retiring a host as part of the classic replace pattern from the previous lesson, or troubleshooting a single problem host without disrupting the users already connected to it. Drain mode is a per-session-host setting (`Update-AzWvdSessionHost` with the `-AllowNewSession $false` parameter, in PowerShell terms) and is a building block both autoscale and your own scripted host-refresh process rely on.

## Right-Sizing: The Ongoing Discipline

Sizing isn't a one-time decision made in Lesson 3 and forgotten. Right-sizing is an ongoing practice:

- Review **Azure Virtual Desktop Insights** (wired in during deployment, per the previous lesson) for actual CPU, memory, and session-count patterns per host pool, and compare against the sessions-per-host target you originally sized for.
- Watch for pools that are consistently over-provisioned (low utilization even at peak) or under-provisioned (users complaining, hosts pegged at high CPU well before the ramp-down window).
- Revisit VM SKU choice periodically — Azure regularly introduces newer VM generations with better price-performance, and a SKU that was the best choice eighteen months ago may not be today.

## Reserved Instances, Savings Plans, and Cost-Per-User Math

Autoscale reduces *how much you run*; **Reserved Instances** and **Azure Savings Plans for compute** reduce the *price per hour* of whatever you do run, in exchange for a one- or three-year commitment. The two aren't mutually exclusive, and the practical strategy is usually:

- Use **Reserved Instances** (or a **Savings Plan**, which is more flexible across VM families and sizes but with a slightly lower discount than a matched Reserved Instance) to cover your **baseline** capacity — the minimum number of session hosts running even during off-peak hours, which autoscale won't scale below.
- Leave **burst/peak** capacity on-demand, since that's exactly the capacity autoscale is scaling up and down, and committing to a reservation for capacity that isn't always running defeats the purpose.
- Build a simple **cost-per-user** model as your steering metric: total monthly session host compute cost (post-discount) divided by active monthly users. This number, tracked over time, tells you whether right-sizing, autoscale tuning, and reservations are actually working, in a way that raw VM spend alone doesn't — a pool that costs more in absolute terms but serves proportionally more users can still have a *better* cost-per-user trend.

## Putting the Levers Together

A cost-optimized AVD environment combines all of these: autoscale scaling plans handle the daily rhythm of ramp-up and ramp-down, Start VM on Connect and hibernation cover the "not on a predictable schedule" cases for personal pools, drain mode gives you a manual override for maintenance and refresh, right-sizing keeps the underlying SKU choice honest over time, and Reserved Instances or Savings Plans buy down the price of whatever baseline capacity autoscale never turns off. None of these levers work in isolation — the discipline is reviewing them together, on a recurring cadence, against real usage data from Insights.
