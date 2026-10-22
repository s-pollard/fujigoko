# architecture

## design intent

Fujigoko is the production homelab. Host roles should remain obvious, production services should not depend on the experimental gusuku lab, and storage/recovery design should follow the value of the data rather than the size of the system.

```text
kawaguchi = media + manga + host-specific monitoring agent
motosu    = photos + Immich + backup storage
yamanaka  = general applications + centralized monitoring/logging + DNS
shoji     = reserved / unassigned
```

The physical machine formerly documented here as `saiko` moved to the separate gusuku lab and is now `shuri`.

## kawaguchi — media

Primary role: media server and media-adjacent storage/services.

- UGREEN iDX6011 64GB AI NAS
- Intel Core Ultra 5 125H
- 64 GB memory
- Unraid 7.3.2
- 10 GbE uplink

Permanent workload classes:

- Plex and media automation
- manga services
- bulk media/download storage
- cAdvisor and smartctl-exporter / host-specific monitoring agents

Kawaguchi is intentionally relatively rebuildable. Configuration and metadata are more important to protect than reacquirable movie/TV payloads.

## motosu — photos and backup storage

Primary role: photo storage, Immich, and local backup target.

- UGREEN NASync DXP2800
- Intel N100
- 8 GB memory
- TrueNAS SCALE
- 2 × 6 TB Seagate ST6000NM0024 HDDs
- mirrored ZFS storage
- 2.5 GbE onboard networking

Current migration state:

- TrueNAS SCALE is installed
- the photo/Immich dataset exists under the Motosu pool
- the Immich library was copied to the rebuilt system and verified during migration
- Immich application/database restoration is complete and validated

Target permanent workloads:

- Immich
- photo/archive storage
- Yamanaka backup datasets
- ZFS snapshots
- Backblaze B2 off-site protection for selected high-value data
- one AdGuard Home instance as the second DNS node

Motosu remains storage/photo focused rather than becoming a general application host.

## yamanaka — general applications

Primary role: simple, always-on production application server.

- Dell OptiPlex 3070 SFF
- Intel Core i5-9500
- Debian GNU/Linux 13
- 16 GB DDR4 installed; upgrade only if measured usage justifies it
- Patriot P300 512 GB NVMe
- Intel X520-DA2 10 GbE upgrade planned/ordered

Current workload classes:

- retained non-media personal applications
- Prometheus / Grafana / Loki / Alloy
- Uptime Kuma and Signal notification bridge
- one AdGuard Home instance
- application-local PostgreSQL/Redis dependencies

The migrated workload has substantial CPU and memory headroom on the current hardware. Yamanaka does not host game servers or disposable lab workloads.

## shoji — reserved

Shoji has no assigned role. Keep the name reserved until another production host is justified.

## network architecture

```text
current
internet -> UDM-Pro -> USW-Aggregation -> hosts

target
fiber handoff -> OPNsense -> switching -> hosts
```

Decisions:

- OPNsense is the target production router/firewall
- UDM-Pro leaves the routing role only after replacement routing is proven
- USW-Aggregation can remain during transition
- TP-Link Omada SX3016F is the main future core/aggregation-switch candidate
- TP-Link Omada EAP775-Wall is the planned target AP
- exact addressing, VLAN IDs, reservations, and management URLs stay out of this public repository

## service placement

```text
media / manga                    -> kawaguchi
host-specific monitoring agent   -> monitored host
Immich / photos / backup storage -> motosu
general personal applications   -> yamanaka
central monitoring/logging       -> yamanaka
uptime monitoring                -> yamanaka
DNS                              -> yamanaka + motosu target pair
routing / firewall               -> OPNsense appliance
experimentation                  -> gusuku, not fujigoko
```

Uptime Kuma currently runs on Yamanaka, so a total Yamanaka host failure also removes that monitoring path. This is accepted current state rather than an independent-watchdog design.

## backup priorities

High priority:

- Immich library and database recovery data
- photo archive data
- Yamanaka application data/databases
- irreplaceable documents and records

Medium priority:

- Kawaguchi Unraid configuration
- retained application configuration and metadata
- DNS/monitoring configuration

Low priority / replaceable:

- movie/TV payloads
- downloads and caches
- transient metrics/history where rebuilding is acceptable

## principles

1. Keep production and experimentation separate.
2. Keep host roles obvious.
3. Prefer understandable systems over unnecessary clustering.
4. Keep application databases local to the host that runs them; back them up independently.
5. Document storage, dependencies, and recovery before adding automation.
6. Remove retired experiments instead of preserving them by inertia.
7. Keep secrets, exact addressing, personal information, and unique external identifiers out of the public repository.
8. Treat deployed state—not old migration assumptions—as the source of truth.
