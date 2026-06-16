---
course: helpdesk-tier3-advanced
title: Building reusable automation modules with error handling
month: 2
monthTitle: 'Automation: PowerShell & Microsoft Graph at Scale'
lesson: 6
summary: Package your scripts into a proper PowerShell module with a manifest, controlled exports, robust
  error handling, structured logging, and Pester tests.
objectives:
- Structure a script module (.psm1) and manifest (.psd1) the right way
- Control which functions are public versus internal with Export-ModuleMember
- Build robust error handling with try/catch/finally and custom error records
- Add structured logging and verbose output that callers can toggle
- Add retry with exponential backoff as a reusable helper
- Write a basic Pester test to protect a function's behaviour
video: ht2-l06-reusable-modules-error-handling.mp4
quiz:
- q: What is the role of the module manifest (.psd1)?
  options:
  - It declares metadata, version, dependencies, and what the module exports
  - It contains the function code
  - It stores credentials
  - It is optional and ignored by PowerShell
  answer: 0
  why: The .psd1 manifest declares the module's version, author, required modules, and the functions/cmdlets
    it exports, while the .psm1 holds the actual code.
- q: How do you keep a helper function internal to a module so callers cannot use it directly?
  options:
  - Name it with a lowercase letter
  - Put it in a comment
  - Prefix it with an underscore
  - Do not list it in FunctionsToExport / Export-ModuleMember
  answer: 3
  why: Only functions you explicitly export (via Export-ModuleMember or FunctionsToExport in the manifest)
    are public; everything else stays private to the module scope.
- q: What is the advantage of throwing a custom error record with a meaningful category and target?
  options:
  - It runs faster
  - It hides the error
  - Callers can catch specific error types and get actionable context for diagnostics
  - It disables -ErrorAction
  answer: 2
  why: A well-formed ErrorRecord (message, category, target object) lets callers branch on the failure
    type and gives operators the context they need, rather than a generic opaque failure.
- q: In a retry-with-backoff helper, why increase the wait time after each failed attempt?
  options:
  - To make the script slower on purpose
  - To avoid hammering a struggling or throttling service and give it time to recover
  - Because PowerShell requires it
  - To use more memory
  answer: 1
  why: Exponential backoff spaces out retries so you stop pounding a service that is rate-limiting or
    temporarily down, which is both more polite and more likely to succeed.
- q: Name the testing framework you would use to write automated tests for your PowerShell module.
  answer: Pester — the de facto PowerShell testing framework, using Describe/It blocks and Should assertions
    to test functions and mock dependencies.
  why: Pester lets you assert behaviour and mock Graph calls so you can test logic without touching a
    live tenant, which is essential for reliable, refactorable modules.
- q: In one sentence, why prefer Write-Verbose and a logging function over Write-Host inside a module?
  answer: Write-Host writes straight to the host and cannot be captured or toggled, whereas Write-Verbose
    and a logging function let callers control detail and redirect or persist logs.
  why: Modules are consumed by other scripts and runbooks, so output must be controllable and capturable
    rather than hard-printed to a screen that may not exist.
resources:
- label: Microsoft Learn — How to write a PowerShell script module
  url: https://learn.microsoft.com/en-us/powershell/scripting/developer/module/how-to-write-a-powershell-script-module
- label: Microsoft Learn — How to write a PowerShell module manifest
  url: https://learn.microsoft.com/en-us/powershell/scripting/developer/module/how-to-write-a-powershell-module-manifest
- label: Microsoft Learn — Everything about exceptions (try/catch)
  url: https://learn.microsoft.com/en-us/powershell/scripting/learn/deep-dives/everything-about-exceptions
- label: Pester — Documentation
  url: https://pester.dev/docs/quick-start
---

## From scripts to a module

Once you have more than a handful of functions, copy-pasting them between scripts becomes a liability. A **PowerShell module** packages related functions so others can `Import-Module` them and call your work like built-in cmdlets. A script module is two files: a **`.psm1`** holding the code, and a **`.psd1`** **manifest** declaring metadata, version, dependencies, and exports.

```
EndpointOps/
  EndpointOps.psd1   # manifest: version, author, RequiredModules, FunctionsToExport
  EndpointOps.psm1   # dot-sources functions, then Export-ModuleMember
```

Generate the manifest with `New-ModuleManifest` and never hand-edit a GUID.

```powershell
New-ModuleManifest -Path .\EndpointOps\EndpointOps.psd1 `
    -RootModule 'EndpointOps.psm1' -ModuleVersion '1.0.0' `
    -RequiredModules 'Microsoft.Graph.Authentication' `
    -FunctionsToExport @('Get-StaleDevice','Invoke-DeviceSyncBulk')
```

## Public vs internal functions

Not everything should be callable from outside. Only the functions you **export** are public; the rest stay private to the module scope and act as internal helpers. Control this with `FunctionsToExport` in the manifest, or `Export-ModuleMember` in the `.psm1`.

```powershell
# inside EndpointOps.psm1
Export-ModuleMember -Function 'Get-StaleDevice','Invoke-DeviceSyncBulk'
# Write-Log and Invoke-WithRetry stay internal — not exported
```

## Error handling that helps the next person

Generic failures waste hours. Throw **meaningful error records** so callers can catch a specific type and get context. Use `try/catch/finally`, and re-throw with detail rather than swallowing errors.

```powershell
function Get-DeviceOrThrow {
    [CmdletBinding()]
    param([Parameter(Mandatory)][string]$DeviceName)
    try {
        $d = Get-MgDeviceManagementManagedDevice -All `
            -Filter "deviceName eq '$DeviceName'" -ErrorAction Stop
        if (-not $d) {
            throw [System.Management.Automation.ItemNotFoundException] "No device named $DeviceName"
        }
        $d
    }
    catch {
        Write-Error -Message "Get-DeviceOrThrow failed for '$DeviceName': $($_.Exception.Message)" `
            -Category ObjectNotFound -TargetObject $DeviceName
    }
}
```

## Logging and retry as reusable helpers

Give your module an internal **logging** function and a **retry-with-backoff** helper that every public function can use.

```powershell
function Write-Log {
    param([string]$Message, [ValidateSet('INFO','WARN','ERROR')][string]$Level = 'INFO')
    Write-Verbose "[$([datetime]::UtcNow.ToString('s'))] [$Level] $Message"
}

function Invoke-WithRetry {
    param([scriptblock]$Action, [int]$MaxRetries = 5)
    for ($i = 1; $i -le $MaxRetries; $i++) {
        try { return & $Action }
        catch {
            if ($i -eq $MaxRetries) { throw }
            $delay = [math]::Pow(2, $i)   # exponential backoff: 2,4,8...
            Write-Log "Attempt $i failed, retrying in $delay s" WARN
            Start-Sleep -Seconds $delay
        }
    }
}
```

Now a public function wraps a flaky Graph call in `Invoke-WithRetry { ... }` and gets resilience for free.

## Test it with Pester

A module you cannot test, you cannot safely change. **Pester** lets you assert behaviour and **mock** Graph so tests never touch a live tenant.

```powershell
Describe 'Get-DeviceOrThrow' {
    It 'errors when no device is found' {
        Mock Get-MgDeviceManagementManagedDevice { @() }
        { Get-DeviceOrThrow -DeviceName 'NOPE' -ErrorAction Stop } | Should -Throw
    }
}
```

## Your task

Turn at least two functions from earlier lessons into a real module `EndpointOps`: create the folder, generate the manifest with `New-ModuleManifest`, and export only the public functions while keeping `Write-Log` and `Invoke-WithRetry` internal. Wrap one Graph call in `Invoke-WithRetry` with exponential backoff. Add structured logging via `Write-Log`. Finally, write one Pester `Describe/It` test that mocks the Graph cmdlet and asserts your function throws when no device is found.
