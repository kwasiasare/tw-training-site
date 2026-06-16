---
course: helpdesk-tier3-advanced
title: Intune proactive remediations
month: 2
monthTitle: 'Automation: PowerShell & Microsoft Graph at Scale'
lesson: 4
summary: 'Build self-healing endpoints with Intune proactive remediations: a detection script that finds
  a problem and a remediation script that fixes it, deployed and reported at fleet scale.'
objectives:
- Explain the detection-plus-remediation script pair model and its exit-code contract
- Write a detection script that exits 1 only when remediation is needed
- Write a matching remediation script that fixes the issue idempotently
- Understand the SYSTEM vs user context and 64-bit execution settings
- Interpret detection and remediation status output in the Intune reports
- Deploy a remediation to a device group and read pre/post remediation results
video: ht2-l04-intune-proactive-remediations.mp4
quiz:
- q: In a proactive remediation, what does an exit code of 1 from the detection script mean?
  options:
  - The script failed to run
  - Everything is healthy, do nothing
  - An issue was detected, so the remediation script should run
  - Reboot the device
  answer: 2
  why: By contract, detection exit 0 means compliant (no action), and exit 1 means an issue was detected
    and triggers the remediation script on that device.
- q: Why must a remediation script be idempotent?
  options:
  - So it runs faster
  - So running it repeatedly on already-fixed devices causes no harm and produces the same end state
  - Because Intune only runs it once ever
  - So it can run without PowerShell
  answer: 1
  why: Remediations run on a schedule, so re-running on an already-healthy device must be safe and produce
    the same correct state without side effects or errors.
- q: By default, in which security context does a proactive remediation run?
  options:
  - The local SYSTEM account, unless you choose to run it in the user context
  - The signed-in user only
  - A domain admin account you supply
  - Anonymous
  answer: 0
  why: Remediations run as SYSTEM by default; you can opt to run them in the logged-on user's context,
    which matters for HKCU registry keys and per-user settings.
- q: What should detection write to standard output to make Intune reporting useful?
  options:
  - Nothing, output is ignored
  - The entire script source
  - A binary blob
  - A short single-line status string via Write-Output describing the finding
  answer: 3
  why: The last line written to stdout is surfaced as the pre/post-remediation output in Intune reports,
    so a concise status string makes triage and reporting far easier.
- q: Name the setting you must enable when a remediation needs to read 64-bit registry or program paths.
  answer: Run script in 64-bit PowerShell (set to Yes); otherwise the script runs in 32-bit and may be
    redirected to WOW6432Node or miss 64-bit paths.
  why: By default scripts can run 32-bit; enabling 64-bit execution prevents registry/file-system redirection
    from hiding the real 64-bit state on modern Windows.
- q: In one sentence, why split logic into separate detection and remediation scripts rather than one
    script that fixes everything?
  answer: Detection-only runs let you measure how widespread an issue is and report on it without changing
    devices, and only the affected machines incur the remediation, which is safer and observable.
  why: The pair model gives you a reporting/measurement phase and a controlled fix phase, so you can pilot,
    quantify impact, and avoid touching healthy devices.
resources:
- label: Microsoft Learn — Remediations (proactive remediations) in Intune
  url: https://learn.microsoft.com/en-us/mem/intune/fundamentals/remediations
- label: Microsoft Learn — Manage Intune remediations with Microsoft Graph
  url: https://learn.microsoft.com/en-us/graph/api/resources/intune-devices-devicehealthscript
- label: Microsoft Learn — PowerShell scripts and remediations for Windows
  url: https://learn.microsoft.com/en-us/mem/intune/apps/intune-management-extension
- label: Microsoft Learn — about_Automatic_Variables (LASTEXITCODE / exit)
  url: https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_automatic_variables
---

## Self-healing endpoints, by design

A **proactive remediation** (now called a **remediation** in Intune) is a pair of PowerShell scripts that run on a schedule via the **Intune Management Extension**: a **detection** script that decides whether a problem exists, and a **remediation** script that fixes it. The two scripts communicate through a strict **exit-code contract**.

- Detection **exit 0** = healthy, do nothing.
- Detection **exit 1** = problem found, run the remediation.

This pair model lets you first *measure* how widespread an issue is across the fleet before you ever change a device.

## Writing the detection script

Detection should be fast, read-only, and decisive. Output a short status string (it appears in the Intune report), then exit with the right code.

```powershell
# Detect: is the Windows Time service running and automatic?
$svc = Get-Service -Name 'W32Time' -ErrorAction SilentlyContinue

if ($svc -and $svc.Status -eq 'Running' -and $svc.StartType -eq 'Automatic') {
    Write-Output 'W32Time healthy: running and automatic'
    exit 0
}
else {
    Write-Output 'W32Time not running or not automatic'
    exit 1
}
```

The **last line on stdout** becomes the *pre-remediation output* in reporting, so make it human-readable.

## Writing the remediation script

Remediation must be **idempotent** — running it on an already-fixed device must be harmless and produce the same end state. Always wrap changes in `try/catch` and exit non-zero on failure so Intune records the failure.

```powershell
try {
    Set-Service -Name 'W32Time' -StartupType Automatic -ErrorAction Stop
    Start-Service -Name 'W32Time' -ErrorAction Stop
    Write-Output 'W32Time set to Automatic and started'
    exit 0
}
catch {
    Write-Output "Remediation failed: $($_.Exception.Message)"
    exit 1
}
```

Because this runs on a schedule, re-running on a healthy device simply re-asserts the desired state with no harm.

## Context and bitness matter

Two settings change behaviour. **Run this script using the logged-on credentials** controls whether the script runs as the user (needed for `HKCU` and per-user settings) or as **SYSTEM** (the default, for machine-wide changes). **Run script in 64-bit PowerShell** should be **Yes** whenever you touch 64-bit registry hives or program paths — otherwise the script runs 32-bit and gets redirected to `WOW6432Node`, hiding the real state.

## Deploying and reading results

You assign a remediation to a **device or user group** with a schedule (once, hourly, or daily). Intune then shows, per device, the detection status and remediation status. You can also manage remediations through Graph as `deviceHealthScript` resources.

```powershell
Connect-MgGraph -Scopes 'DeviceManagementConfiguration.Read.All'

# List your remediation (device health) scripts via Graph
Invoke-MgGraphRequest -Method GET `
    -Uri 'https://graph.microsoft.com/beta/deviceManagement/deviceHealthScripts' |
    Select-Object -ExpandProperty value |
    Select-Object displayName, id
```

Start with **detection only** (a remediation that just reports) to size the problem, then add the fix and pilot it on a small ring.

## Your task

Build a complete remediation pair for a real issue: a stale DNS cache or a disabled firewall profile (your choice). The **detection** script must read-only check the condition, write a clear single-line status, and exit 0 or 1 correctly. The **remediation** script must fix it **idempotently**, wrap changes in `try/catch`, and exit 0 on success and 1 on failure. State which context (SYSTEM or user) and bitness it needs and why. Finally, use `Invoke-MgGraphRequest` to list the `deviceHealthScripts` in your tenant.
