# fujigoko

Fujigoko is my homelab.

The design is intentionally simple: document what exists first, keep host roles clear, and add automation or complexity only when it solves a real problem.

## Core hosts

- **kawaguchi** — media server and Unraid host
- **motosu** — Immich / photo NAS
- **yamanaka** — planned low-power general application server

## Repository structure

```text
.
├── README.md
├── architecture/
│   └── README.md
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

- [architecture](architecture/README.md) — design intent, host roles, placement rules, and backup priorities
- [hosts](hosts/README.md) — host hardware, platform, addressing, and storage summary
- [network](network/README.md) — UniFi inventory, ports, VLANs, and network state
- [topology](network/topology.md) — physical/logical topology and service flows
- [services](services/README.md) — current service inventory and dependencies
- [service classification](services/classification.md) — permanent, transitional, and retirement decisions
- [storage](storage/README.md) — arrays, pools, shares, persistent data, and storage criticality
- [backups](backups/README.md) — verified backup state, priorities, retention, and known gaps
- [Yamanaka migration](migration/yamanaka.md) — migration plan for non-media workloads
- [runbooks](runbooks/README.md) — operational recovery procedures for hosts and network infrastructure

## Current priorities

1. Keep an accurate inventory of hosts, services, storage, backups, and network dependencies.
2. Separate media, photo, and general application workloads by host role.
3. Build the infrastructure map from documented state rather than memory.
4. Complete the Yamanaka migration before cleaning transitional services from Kawaguchi.
5. Make irreplaceable data independently recoverable before optimizing convenience services.
6. Add automation only where it improves maintenance, repeatability, or recovery.
