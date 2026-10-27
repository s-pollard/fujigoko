# /fujigoko/

Fujigoko is the production environment within **/pleblab/**, the overall homelab.

```text
/pleblab/
├── fujigoko  -> production
└── gusuku    -> experimentation / learning
```

The design is intentionally simple: keep host roles clear, document deployed state, preserve recoverability, and add complexity only when it solves a real production problem.

Experimental and career-learning infrastructure belongs in the separate [`gusuku`](https://github.com/s-pollard/gusuku) environment under /pleblab/. Fujigoko must not depend on gusuku for required home services.

## Core hosts

- **kawaguchi** — Unraid media server, manga, bulk media storage, and host-specific monitoring agent
- **motosu** — TrueNAS SCALE photo/Immich host and backup target
- **yamanaka** — Debian general-application server hosting retained non-media services, monitoring/logging, Uptime Kuma, AdGuard Home, Caddy, and Pocket ID
- **shoji** — reserved; no assigned role

The physical system formerly documented as **saiko** is no longer part of Fujigoko. It moved to gusuku and is now **shuri**.

## Administration workstations

**Aso** is the primary personal desktop and administration workstation. **Ontake**, **Norikura**, and **Azuma** provide alternative laptop access. See [workstation inventory](hosts/workstations.md) for hardware, roles, and backup scope.

## Private application access

`plebworks.com` is the private application namespace for Fujigoko. Trusted LAN and Tailscale clients use `*.plebworks.com`; private DNS directs those names to Caddy on Yamanaka, which reverse-proxies user-facing services hosted on Yamanaka, Kawaguchi, and Motosu.

The namespace is for private access and is not intended to expose Fujigoko applications directly to the public internet.

## Network direction

- current gateway: UDM-Pro
- target gateway/firewall: dedicated OPNsense appliance; hardware acquired
- current aggregation: USW-Aggregation
- future core-switch main candidate: TP-Link Omada SX3016F
- target wireless AP: TP-Link Omada EAP775-Wall
- target DNS: redundant AdGuard Home on Yamanaka and Motosu

The UDM-Pro can be sold after replacement routing and any required UniFi management are stable.

## Public repository policy

This repository is intended to be safe to publish. Do not commit credentials, secrets, public/WAN addressing, exact private addressing, MAC addresses, serial numbers, account identifiers, cloud resource identifiers, management URLs, or personal location details.

See [`SECURITY.md`](SECURITY.md) for the full policy.

## Documentation

- [architecture](architecture/README.md) — production roles and placement rules
- [naming](architecture/naming.md) — /pleblab/ and Fujigoko naming conventions
- [hosts](hosts/README.md) — hardware and platform inventory
- [network](network/README.md) — current and target network design
- [topology](network/topology.md) — physical/logical topology
- [services](services/README.md) — service inventory and dependencies
- [service classification](services/classification.md) — placement and lifecycle decisions
- [storage](storage/README.md) — storage ownership and data criticality
- [backups](backups/README.md) — backup policy, verified state, and gaps
- [Yamanaka migration history](history/yamanaka-migration-2026.md) — archived record of the completed service migration and cleanup
- [runbooks](runbooks/README.md) — recovery procedures

## Current priorities

1. Deploy the second AdGuard Home instance on Motosu to complete redundant DNS.
2. Deploy and validate the OPNsense-based network; keep the SX3016F as the main core-switch candidate until purchased and verified.
3. Complete remaining Motosu protection work: representative B2 restore testing, replacement of the temporary older mirror member, and SMART/scrub alert verification.
4. Establish an independent Kawaguchi configuration/appdata backup.
5. Remove the legacy Kawaguchi shares (uppercase `Media` and `roms`) after dependency checks confirm nothing still uses them.
6. Add monitoring independent of Yamanaka and common backup-failure alerting.

Yamanaka-to-Motosu Restic backups are deployed and restore-verified. Immich restoration and Kawaguchi container/appdata cleanup are complete. See [backups](backups/README.md) for the verified backup design, [services](services/README.md) for current placement, and [Yamanaka migration history](history/yamanaka-migration-2026.md) for the completed migration record.
