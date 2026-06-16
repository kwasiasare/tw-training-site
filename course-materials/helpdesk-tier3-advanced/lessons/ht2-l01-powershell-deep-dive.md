---
course: helpdesk-tier3-advanced
title: PowerShell deep dive for administrators
month: 2
monthTitle: 'Automation: PowerShell & Microsoft Graph at Scale'
lesson: 1
summary: Move beyond one-line commands and learn the object pipeline, parameters, and error model that
  make PowerShell a real automation language for endpoint operations.
objectives:
- Explain how PowerShell passes .NET objects through the pipeline rather than text
- Write functions with param blocks, typed parameters, and pipeline binding
- Use the streams and ErrorAction to control terminating vs non-terminating errors
- Filter and shape data efficiently with Where-Object, Select-Object and calculated properties
- Choose PowerShell 7 over Windows PowerShell 5.1 and understand the practical differences
- Discover and read help for any cmdlet without leaving the console
video: ht2-l01-powershell-deep-dive.mp4
quiz:
- q: What flows down the PowerShell pipeline between commands?
  options:
  - .NET objects with typed properties and methods
  - Plain text lines
  - JSON strings only
  - Byte streams
  answer: 0
  why: Unlike traditional shells that pipe text, PowerShell passes rich .NET objects, so downstream commands
    can access properties and methods directly without parsing.
- q: Which parameter forces a non-terminating error to become a terminating one so a try/catch can handle
    it?
  options:
  - -ErrorVariable
  - -WarningAction
  - -ErrorAction Stop
  - -Verbose
  answer: 2
  why: Most cmdlet errors are non-terminating and bypass catch blocks; -ErrorAction Stop promotes them
    to terminating errors that try/catch can trap.
- q: In a function, which attribute lets a parameter accept values straight from the pipeline?
  options:
  - '[Parameter(Mandatory)]'
  - '[Parameter(ValueFromPipeline)]'
  - '[ValidateSet()]'
  - '[CmdletBinding()]'
  answer: 1
  why: ValueFromPipeline binds incoming pipeline objects to that parameter, typically processed inside
    a process{} block for one-at-a-time handling.
- q: Why prefer PowerShell 7 over Windows PowerShell 5.1 for new automation?
  options:
  - It is the only version that supports modules
  - It cannot run old scripts so it is safer
  - It removes the need for execution policy
  - It is cross-platform, actively developed, and ships newer language and performance features
  answer: 3
  why: PowerShell 7 (built on .NET) is cross-platform and the version that receives new features and fixes;
    5.1 is in maintenance only and stays for legacy compatibility.
- q: Name the cmdlet you would run to see the syntax, parameters, and examples for any command.
  answer: Get-Help (for example Get-Help Get-Process -Examples), and Get-Command / Get-Member to discover
    commands and object members.
  why: Get-Help is the built-in documentation engine; pairing it with Get-Member to inspect object properties
    is the fastest way to learn an unfamiliar cmdlet.
- q: In one sentence, why is filtering with Where-Object early in a pipeline better than collecting everything
    first?
  answer: Filtering early reduces the number of objects flowing downstream, which lowers memory use and
    speeds up the whole pipeline, especially against large device fleets.
  why: Streaming and filtering as close to the source as possible avoids materialising huge collections
    and is the core habit behind scalable scripts.
resources:
- label: Microsoft Learn — PowerShell documentation
  url: https://learn.microsoft.com/en-us/powershell/
- label: Microsoft Learn — Understanding the PowerShell pipeline
  url: https://learn.microsoft.com/en-us/powershell/scripting/learn/ps101/04-pipelines
- label: Microsoft Learn — about_Functions_Advanced_Parameters
  url: https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_functions_advanced_parameters
- label: Microsoft Learn — Migrating from Windows PowerShell 5.1 to PowerShell 7
  url: https://learn.microsoft.com/en-us/powershell/scripting/whats-new/migrating-from-windows-powershell-51-to-powershell-7
---

## PowerShell is an object pipeline, not a text shell

If you came from Bash or `cmd`, the biggest mental shift is this: PowerShell pipes **.NET objects**, not text. When you run `Get-Process | Where-Object CPU -gt 100`, each process is a full object with properties and methods. You never parse columns by position or count spaces — you ask for the property you want.

```powershell
Get-Process |
    Where-Object { $_.CPU -gt 100 } |
    Sort-Object CPU -Descending |
    Select-Object Name, Id, CPU -First 5
```

The two cmdlets you will lean on forever are **Get-Command** (find things) and **Get-Member** (see what an object actually contains). When you do not know what is on an object, pipe it to `Get-Member`.

## Functions, param blocks, and pipeline binding

Real automation lives in **functions**, not loose one-liners. A function with `[CmdletBinding()]` and a typed `param` block behaves like a built-in cmdlet — it gets `-Verbose`, `-ErrorAction`, and parameter validation for free.

```powershell
function Get-StaleDevice {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory, ValueFromPipeline)]
        [string]$DeviceName,

        [ValidateRange(1, 365)]
        [int]$StaleAfterDays = 90
    )
    process {
        Write-Verbose "Checking $DeviceName against $StaleAfterDays day window"
        # ... logic per device ...
        [pscustomobject]@{ Device = $DeviceName; StaleAfterDays = $StaleAfterDays }
    }
}
```

The `process{}` block runs once per pipeline object, so the function streams. `ValidateRange` and `ValidateSet` reject bad input before your logic ever runs.

## The error model: terminating vs non-terminating

Most cmdlets emit **non-terminating** errors that print red text but keep going — and crucially, they **slip past `try/catch`**. To trap them you must promote them with **`-ErrorAction Stop`**.

```powershell
try {
    Get-Item 'C:\does-not-exist.txt' -ErrorAction Stop
}
catch {
    Write-Warning "Handled: $($_.Exception.Message)"
}
finally {
    Write-Verbose 'Cleanup runs no matter what'
}
```

PowerShell also has **streams**: success (1), error (2), warning (3), verbose (4), and information (6). Use `Write-Verbose` and `Write-Warning` instead of `Write-Host` so callers can switch detail on and off.

## Shaping data without melting your machine

Against a fleet of thousands of devices, *where* you filter matters. Filter as close to the source as possible so fewer objects travel down the pipeline.

```powershell
Get-ChildItem C:\Logs -Recurse -Filter *.log |
    Where-Object Length -gt 10MB |
    Select-Object FullName,
        @{ Name = 'SizeMB'; Expression = { [math]::Round($_.Length / 1MB, 1) } }
```

The `@{ Name=...; Expression=... }` syntax is a **calculated property** — it lets you rename and transform columns inline.

## PowerShell 7 vs Windows PowerShell 5.1

**Windows PowerShell 5.1** ships in the box and is in maintenance only. **PowerShell 7** is cross-platform, built on modern .NET, faster, and gets all new features — including the Microsoft Graph SDK improvements you will use this month. Install it side by side; it runs as `pwsh`.

```powershell
$PSVersionTable.PSVersion   # confirm which engine you are in
```

## Your task

Write an advanced function `Get-LargeProfile` that accepts computer profile paths from the pipeline, has a `[CmdletBinding()]` block, a mandatory `ValueFromPipeline` path parameter and a validated `-MinSizeMB` threshold (default 5000), uses a `process{}` block, emits a `[pscustomobject]` per oversized profile with a calculated `SizeGB`, and wraps its disk access in a `try/catch` with `-ErrorAction Stop`. Run it with `-Verbose` and confirm the verbose stream appears.
