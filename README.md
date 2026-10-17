# fujigoko

Fujigoko is my homelab.

The design is intentionally simple: document what exists first, keep host roles clear, and add automation or complexity only when it solves a real problem.

## Core hosts

- **kawaguchi** — media server and Unraid host
- **motosu** — photo NAS / Immich host; planned migration to TrueNAS SCALE with a two-disk ZFS mirror
- **yamanaka** — Dell OptiPlex 3070 SFF general application server; Debian 13 installed, hardware upgrades/deployment in progress
- **saiko** — packed/offline Proxmox lab / experimentation host; formerly `bandai`
- **shoji** — reserved; role undecided

## Network direction

- current gateway: UDM-Pro
- target gateway/firewall: dedicated OPNsense appliance
- UDM-Pro: retire from routing and sell after the replacement network is stable
- current aggregation: USW-Aggregation
- future core-switch main candidate: TP-Link Omada SX3016F
- target wireless AP: TP-Link Omada EAP775-Wall
- permanent DNS target: redundant AdGuard Home on Yamanaka + Motosu

## Public repository policy

This repository is intentionally safe to publish. Do not commit:

- passwords, API keys, tokens, private keys, recovery codes, or `.env` files containing secrets
- public/WAN IP addresses, VPN endpoints, MAC addresses, serial numbers, or account identifiers
- exact private addressing, DHCP reservations, VLAN IDs, or management URLs
- cloud bucket names or other unique external resource identifiers
- personal location details

Exact addressing, credentials, and other sensitive operational details belong in private/local documentation outside this repository.

## Repository structure

```text
.
├── README.md
├── SECURITY.md
├── architecture/
│   ├── README.md
│   └── naming.md
├── hosts/
│   └── README.md
├── network/
│   ├── README.md
│   └── topology.md
├── services/
│   ├── README.md
│   └── classification.md
├── storage/
│   └── README.md
├── backups/
│   └── README.md
├── migration/
│   └── yamanaka.md
└── runbooks/
    ├── README.md
    ├── kawaguchi-recovery.md
    ├── motosu-recovery.md
    ├── yamanaka-recovery.md
    └── network-recovery.md
```

## Documentation

- [architecture](architecture/README.md) — design intent, host roles, placement rules, network direction, and backup priorities
- [naming](architecture/naming.md) — Japan-based naming conventions for hosts and infrastructure
- [hosts](hosts/README.md) — host hardware, platform, and storage summary
- [network](network/README.md) — current network state and target design
- [topology](network/topology.md) — current and target physical/logical topology and service flows
- [services](services/README.md) — current service inventory and dependencies
- [service classification](services/classification.md) — permanent, transitional, planned, and retirement decisions
- [storage](storage/README.md) — arrays, pools, shares, persistent data, and storage criticality
- [backups](backups/README.md) — verified backup state, priorities, retention, and known gaps
- [Yamanaka migration](migration/yamanaka.md) — migration plan for non-media workloads
- [runbooks](runbooks/README.md) — operational recovery procedures for hosts and network infrastructure

## Current priorities

1. Keep an accurate inventory of hosts, services, storage, backups, and network dependencies.
2. Rebuild the post-move network around OPNsense; the TP-Link Omada SX3016F remains the main core-switch candidate until purchased and verified.
3. Rebuild Motosu on TrueNAS SCALE while preserving and verifying Immich and Backblaze B2 recovery.
4. Finish Yamanaka hardware upgrades, deploy its Docker application stack, and migrate retained non-media containers off Kawaguchi.
5. Unpack Saiko, verify its ordered Intel X520-DA2, then convert it from Bazzite to an on-demand Proxmox lab.
6. Move DNS from the temporary single AdGuard instance on Kawaguchi to redundant AdGuard Home instances on Yamanaka and Motosu.
7. Establish the replacement UPS/power-protection plan and verify actual receptacle compatibility before deployment.
8. Make irreplaceable data independently recoverable before optimizing convenience services.
9. Add automation or orchestration only where it improves maintenance, repeatability, recovery, or useful experimentation.
