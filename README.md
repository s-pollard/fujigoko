# fujigoko

Fujigoko is my production homelab.

The design is intentionally simple: keep host roles clear, document deployed state, preserve recoverability, and add complexity only when it solves a real production problem.

Experimental and career-learning infrastructure belongs in the separate [`gusuku`](https://github.com/s-pollard/gusuku) lab. Fujigoko must not depend on gusuku for required home services.

## Core hosts

- **kawaguchi** — Unraid media server, manga, bulk media storage, and independent uptime monitoring
- **motosu** — TrueNAS SCALE photo/Immich host and backup target
- **yamanaka** — Debian general-application server; deployment and migration in progress
- **shoji** — reserved; no assigned role

The physical system formerly documented as **saiko** is no longer part of Fujigoko. It moved to gusuku and is now **shuri**.

## Network direction

- current gateway: UDM-Pro
- target gateway/firewall: dedicated OPNsense appliance
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
- [naming](architecture/naming.md) — naming conventions
- [hosts](hosts/README.md) — hardware and platform inventory
- [network](network/README.md) — current and target network design
- [topology](network/topology.md) — physical/logical topology
- [services](services/README.md) — service inventory and dependencies
- [service classification](services/classification.md) — placement and lifecycle decisions
- [storage](storage/README.md) — storage ownership and data criticality
- [backups](backups/README.md) — backup policy, verified state, and gaps
- [Yamanaka migration](migration/yamanaka.md) — non-media workload migration plan
- [runbooks](runbooks/README.md) — recovery procedures

## Current priorities

1. Finish restoring and validating Immich on the rebuilt TrueNAS Motosu.
2. Finish Yamanaka hardware/application deployment and migrate retained non-media workloads from Kawaguchi.
3. Establish Yamanaka-to-Motosu backups before deleting migrated Kawaguchi state.
4. Move DNS from the temporary Kawaguchi instance to redundant AdGuard Home on Yamanaka and Motosu.
5. Rebuild the post-move network around OPNsense; keep the SX3016F as the main core-switch candidate until purchased and verified.
6. Finalize the UPS/power plan after verifying real outlet/receptacle compatibility.
7. Preserve independent recovery for irreplaceable data before optimizing convenience services.
