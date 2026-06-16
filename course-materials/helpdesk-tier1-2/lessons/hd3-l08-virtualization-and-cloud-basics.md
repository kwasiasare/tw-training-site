---
course: helpdesk-tier1-2
title: Virtualization and cloud basics
month: 3
monthTitle: Windows, OS Support & Security (A+ Core 2)
lesson: 8
summary: Understand what virtual machines are and why technicians use them, run a VM with Hyper-V, and
  learn the core cloud service and deployment models you will meet on the helpdesk.
objectives:
- Explain what a hypervisor and a virtual machine are
- Tell type 1 (bare-metal) from type 2 (hosted) hypervisors
- Create and manage a Hyper-V virtual machine from PowerShell
- 'Describe the cloud service models: IaaS, PaaS and SaaS'
- Tell public, private and hybrid cloud deployment models apart
- Recognise common support scenarios involving VMs and cloud apps
video: hd3-l08-virtualization-and-cloud-basics.mp4
quiz:
- q: What is a hypervisor?
  options:
  - A faster type of hard drive
  - Software that creates and runs virtual machines
  - A cloud billing dashboard
  - A type of network cable
  answer: 1
  why: A hypervisor is the software layer that creates, runs and manages virtual machines by sharing the
    physical hardware among them.
- q: Which is a type 1 (bare-metal) hypervisor?
  options:
  - VirtualBox running on your laptop
  - Microsoft Hyper-V on a server
  - A web browser tab
  - Notepad
  answer: 1
  why: Type 1 hypervisors such as Hyper-V or ESXi run directly on the hardware, while type 2 hypervisors
    like VirtualBox run as an application on top of an existing operating system.
- q: A company uses Microsoft 365 — email and Office in the browser with nothing to install or patch on
    the server side. Which cloud model is that?
  options:
  - IaaS
  - PaaS
  - SaaS
  - On-premises
  answer: 2
  why: Software as a Service delivers ready-to-use applications over the internet, with the provider managing
    everything underneath; the customer just uses the app.
- q: Which PowerShell command lists the virtual machines on a Hyper-V host?
  options:
  - Get-VM
  - Get-Process
  - Get-Service
  - Get-ChildItem
  answer: 0
  why: Get-VM returns the virtual machines and their state on a Hyper-V host; the others list processes,
    services, or files.
- q: In one sentence, explain the difference between IaaS and PaaS.
  answer: IaaS gives you raw virtual machines, storage and networking that you manage yourself, while
    PaaS gives you a managed platform to run your code without managing the underlying servers.
  why: IaaS hands you the infrastructure (you patch the OS); PaaS abstracts the servers away so you only
    deal with your application, trading control for convenience.
- q: Why might an organisation choose a hybrid cloud over a purely public cloud?
  answer: To keep sensitive or regulated data and some workloads on their own private infrastructure while
    still using public cloud for scale, bursting, or cheaper general workloads.
  why: Hybrid combines private control for sensitive systems with public-cloud flexibility and scale,
    which is why regulated industries often adopt it.
resources:
- label: Microsoft Learn — Introduction to Hyper-V on Windows
  url: https://learn.microsoft.com/en-us/virtualization/hyper-v-on-windows/about/
- label: Microsoft Learn — Hyper-V PowerShell module reference
  url: https://learn.microsoft.com/en-us/powershell/module/hyper-v/
- label: Microsoft Learn — What is cloud computing?
  url: https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/strategy/cloud-computing-terms
- label: CompTIA — A+ certification
  url: https://www.comptia.org/certifications/a
---

## What virtualization actually means

**Virtualization** lets one physical computer pretend to be many. A **virtual machine (VM)** is a complete computer — its own OS, disk, and network — running as software inside another machine. The thing that makes this possible is the **hypervisor**, the software layer that shares the real hardware (CPU, RAM, disk) among several VMs and keeps them isolated from each other.

For a helpdesk technician this is everyday gold: you can test a risky fix, run an old application, or reproduce a user's problem on a throwaway VM without touching a production machine.

## Type 1 vs type 2 hypervisors

There are two kinds. A **type 1 (bare-metal)** hypervisor runs directly on the hardware with no host OS underneath — think **Hyper-V** on a server or VMware **ESXi**. A **type 2 (hosted)** hypervisor runs as an application on top of your existing OS — think **VirtualBox** or VMware Workstation on your laptop. Type 1 is for servers and performance; type 2 is for convenience on a desktop.

## Running a VM with Hyper-V

Windows includes **Hyper-V** (a type 1 hypervisor) on Pro and Enterprise editions. Manage it with PowerShell:

```powershell
# See what VMs exist and their state
Get-VM

# Create a new VM with 4 GB RAM and a new virtual disk
New-VM -Name "Test-Win11" -MemoryStartupBytes 4GB -NewVHDPath "C:\VMs\test.vhdx" -NewVHDSizeBytes 60GB

# Start it
Start-VM -Name "Test-Win11"
```

Sample output:

```powershell
Name        State   CPUUsage(%)   MemoryAssigned(M)   Uptime
----        -----   -----------   -----------------   ------
Test-Win11  Running 1             4096                00:00:42
```

## The cloud: someone else's computer, on demand

The **cloud** is computing you rent over the internet instead of owning. The three classic **service models** describe how much the provider manages for you:

- **IaaS** (Infrastructure as a Service): you rent raw VMs, storage and networking, and you manage the OS and apps. Example: an Azure or AWS virtual machine.
- **PaaS** (Platform as a Service): you deploy your code onto a managed platform and never touch the servers.
- **SaaS** (Software as a Service): you just use a finished app in the browser. Example: Microsoft 365 or Gmail.

A quick way to spin up cloud infrastructure with the Azure CLI:

```bash
# Log in, then create a resource group and a small VM
az login
az group create --name demo-rg --location uksouth
az vm create --resource-group demo-rg --name demo-vm --image Ubuntu2204 --size Standard_B1s
```

## Deployment models

Where the cloud lives matters too. **Public cloud** is shared infrastructure run by a provider (Azure, AWS). **Private cloud** is dedicated infrastructure for one organisation. **Hybrid cloud** mixes both — keeping sensitive data private while using public cloud for scale. Regulated industries often choose hybrid for exactly this reason.

## Your task

If you have Windows Pro/Enterprise, enable Hyper-V, then use `Get-VM` to list any existing VMs and `New-VM` to create one (you can delete it afterwards with `Remove-VM`). If Hyper-V is not available, install VirtualBox and create a small Linux VM instead. Then write a short note classifying three real services you use — for example a hosted email service, a rented server, and a code-hosting platform — into IaaS, PaaS or SaaS, and explain your reasoning for each.
