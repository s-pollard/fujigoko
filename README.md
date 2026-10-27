# /fujigoko/

Fujigoko is the production environment within **/pleblab/**. The separate [`gusuku`](https://github.com/s-pollard/gusuku) environment is for experimentation and learning. Required home services must not depend on gusuku.

Keep host roles clear, document deployed state, and preserve recoverability. Add complexity only when it solves a production problem.

## core hosts

| Host | Platform | Role |
| --- | --- | --- |
| kawaguchi | Unraid | Media, manga, bulk storage, host monitoring agents |
| motosu | TrueNAS SCALE | Photos, Immich, local backup target |
| yamanaka | Debian | General applications, monitoring/logging, DNS, private HTTPS and identity |
| shoji | Unassigned | Reserved |

See [host hardware](hosts/README.md), [administration workstations](hosts/workstations.md), and [naming](architecture/naming.md) for hardware, access, and reserved names.

Private application access uses `plebworks.com` from trusted LAN and Tailscale clients. See [DNS and ingress](network/README.md#private-application-access).

## documentation

| Document | Purpose |
| --- | --- |
| [architecture](architecture/README.md) | Production boundaries, placement rules, accepted dependencies |
| [naming](architecture/naming.md) | Naming conventions and reserved names |
| [hosts](hosts/README.md) | Physical hardware, platforms, host roles |
| [workstations](hosts/workstations.md) | Personal PCs and administration access |
| [services](services/README.md) | Service inventory, dependencies, authentication |
| [classification](services/classification.md) | Placement and lifecycle decisions |
| [network](network/README.md) / [topology](network/topology.md) | Equipment, plans, DNS, ingress, recorded connections |
| [storage](storage/README.md) | Pools, shares, data paths, ownership |
| [backups](backups/README.md) | Scope, schedules, retention, verified recovery and gaps |
| [runbooks](runbooks/README.md) | Recovery, deployment, troubleshooting, move procedures |
| [history](history/README.md) | Migrations, incidents, completed changes |
| [security](SECURITY.md) | Public repository information policy |

## current status

No required pre-move infrastructure project is currently outstanding.

- Yamanaka-to-Motosu Restic backups are deployed and restore-verified; Signal and TrueNAS email failure alerts are tested. See [backup evidence and limits](backups/README.md).
- Kawaguchi media automation is intentionally rebuildable. Plex/Jellyfin artwork synchronization is configured.
- Motosu's mirror is healthy; replacement HDDs are an opportunistic purchase. Obsolete Kawaguchi shares are low-priority housekeeping.
- Network replacement, redundant DNS, B2 restore testing, and GFX policy are deferred to the [move checklist](runbooks/move-checklist.md).

The [documentation review](history/documentation-review-2026-10-27.md#review-needed) records conflicting policy wording and facts that still need confirmation.
