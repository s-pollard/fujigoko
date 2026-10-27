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
- [runbooks](runbooks/README.md) — recovery and move procedures
- [move checklist](runbooks/move-checklist.md) — work intentionally deferred until relocation

## Current status

No required pre-move infrastructure project is currently outstanding.

Completed or intentionally settled:

- Yamanaka-to-Motosu Restic backups are deployed and restore-verified
- Yamanaka backup and verification failures send Signal alerts
- Motosu/TrueNAS alerts are configured to send email, covering Cloud Sync failures independently of Yamanaka
- Kawaguchi media automation state is intentionally treated as rebuildable rather than requiring a full independent backup
- Plex/Jellyfin artwork synchronization is configured
- the current Motosu mirror is healthy; replacement HDDs are an opportunistic purchase rather than an immediate fault response

Low-priority housekeeping such as removal of obsolete Kawaguchi shares can be done when convenient.

## Deferred until the move

The following work is intentionally deferred rather than considered an active gap:

1. deploy and validate the OPNsense-based network and new wireless/core network hardware
2. deploy the second AdGuard Home instance on Motosu and verify redundant DNS
3. perform a representative restore from the B2 off-site copy
4. decide the final GFX archive storage/backup policy
5. install replacement Motosu HDDs if suitable drives have been acquired by then
6. perform full post-move service, network, backup, and alert validation
7. retire/sell the UDM-Pro only after the replacement network is proven stable

See the [move checklist](runbooks/move-checklist.md) for execution order.
