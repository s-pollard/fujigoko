# architecture

## design intent

Fujigoko is split into a small number of hosts with clear roles rather than allowing one machine to become the permanent home for every service.

```text
kawaguchi = media
motosu    = photos + backup storage
yamanaka  = general applications
saiko     = Proxmox lab / experimentation
shoji     = reserved / role undecided
```

The current deployment on `kawaguchi` is transitional. Non-media applications move to Yamanaka only if they remain useful.

## host roles

### kawaguchi — media

Primary role: media server and media-adjacent storage/services.

Verified hardware:

- UGREEN iDX6011 64GB AI NAS
- Intel Core Ultra 5 125H, 14 cores / 18 threads
- 64 GB memory
- Unraid 7.3.2
- 10 GbE uplink

Permanent workloads are the Plex/media automation stack, manga services, Uptime Kuma, and host-specific monitoring agents.

Primary storage responsibilities:

- bulk media
- downloads
- media application data

Kawaguchi is intentionally treated as relatively rebuildable. Most large movie and TV content can be reacquired; configuration and metadata matter more than backing up the entire media payload.

AdGuard Home is temporary on Kawaguchi and moves to the redundant Yamanaka/Motosu DNS design.

### motosu — photos and backup storage

Primary role: dedicated photo storage, Immich, and local backup target.

Verified hardware:

- UGREEN NASync DXP2800
- Intel N100, 4 cores / 4 threads
- 8 GB installed memory; about 7.5 GiB usable by the current OS
- 2 × 6 TB Seagate ST6000NM0024 drives
- 2.5 GbE onboard networking

Current platform:

- UGOS Pro / Debian-based system
- Linux RAID1 + Btrfs

Planned platform:

- TrueNAS SCALE
- 2-disk ZFS mirror using the existing HDDs initially
- ZFS snapshots for local rollback
- Restic/Backblaze B2 retained as the independent off-site layer

Permanent workloads:

- Immich server
- Immich PostgreSQL
- Immich Valkey/Redis
- Immich machine learning
- Tailscale
- AdGuard Home as one of two redundant LAN DNS resolvers

Motosu also becomes the local backup destination for important Yamanaka exports, database dumps, files, and configuration. It remains photo/storage-focused rather than becoming a general-purpose application host.

### yamanaka — general applications

Primary role: simple, always-on production application server.

Selected hardware and platform:

- Dell OptiPlex 3070 Small Form Factor
- Intel Core i5-9500, 6 cores / 6 threads
- Debian GNU/Linux 13 (trixie)
- Docker Engine + Docker Compose
- 16 GB DDR4-2666 installed; Dell documents 32 GB maximum
- Patriot P300 128 GB NVMe currently installed
- 500 GB NVMe ordered for application storage
- integrated Realtek RTL8111HSD-CG-class 1 GbE
- low-profile Intel X520-DA2 dual-port 10 GbE SFP+ adapter ordered
- Intel UHD Graphics 630; no discrete GPU requirement

Target workloads:

- Paperless-ngx
- Mealie
- Actual Budget
- HomeBox
- Linkwarden
- Stirling PDF
- Endurain
- Homepage
- Prometheus
- Grafana
- Loki
- AdGuard Home
- supporting PostgreSQL/Redis services

Yamanaka does not host game servers or general lab workloads.

### saiko — lab / experimentation

`saiko` is the former `bandai` system.

Current state:

- packed / offline
- Bazzite still installed
- Intel X520-DA2 ordered
- Proxmox conversion planned after unpacking and NIC verification

Known hardware:

- AMD Ryzen 9 3900X
- 32 GB DDR4
- EVGA GeForce RTX 3060 Ti FTW3 ULTRA GAMING 8 GB
- MSI MPG X570 GAMING EDGE WIFI
- WD Blue 500 GB SSD
- 4U rackmount chassis

Saiko is for OPNsense/Linux/Kubernetes/networking/game-server/GPU-passthrough experiments. It should not carry required production services and may remain powered off when unused.

### shoji — reserved

Shoji has no assigned role. Keep the name reserved until another major host is actually justified.

## network architecture

The current network uses the UDM-Pro as gateway and the USW-Aggregation as the main aggregation switch. The target design separates routing from UniFi management.

```text
current
internet -> UDM-Pro -> USW-Aggregation -> hosts

target
fiber handoff -> OPNsense -> switching -> hosts
```

Decisions:

- OPNsense is the target production router/firewall
- UDM-Pro leaves the routing role and is sold only after the replacement network is stable
- existing USW-Aggregation remains usable during the transition
- TP-Link Omada SX3016F is the main candidate for a future 16-port 10 GbE SFP+ core/aggregation switch; it is not yet deployed
- TP-Link Omada EAP775-Wall is the planned target AP
- exact addressing, VLAN IDs, reservations, and management URLs are intentionally excluded from this public repository
- if UniFi switches remain after the UDM-Pro is sold, a replacement UniFi Network management method must be established first
- Omada controller placement is optional/TBD; the AP can be deployed once the actual management approach is selected

## service placement rule

```text
media pipeline and Plex data      -> kawaguchi
manga services and manga data     -> kawaguchi
independent uptime watchdog       -> kawaguchi
Immich and photo data             -> motosu
photo archive storage             -> motosu
general personal applications     -> yamanaka
monitoring control plane          -> yamanaka
host-specific exporters/agents    -> monitored host
lab / disposable VMs              -> saiko
DNS                               -> redundant AdGuard on yamanaka + motosu
routing / firewall                -> OPNsense appliance
```

## monitoring architecture

```text
                yamanaka
        prometheus / grafana / loki
             /       |       \
     kawaguchi     motosu     saiko
      metrics      metrics    metrics

                kawaguchi
              uptime kuma
             /     |      \
       yamanaka  motosu    saiko
        uptime    uptime    uptime
```

Uptime Kuma remains outside Yamanaka so a Yamanaka failure does not remove every monitoring path.

## backup priorities

### high priority

- Motosu Immich library and database backups
- photo archive data
- Yamanaka databases and persistent application data
- irreplaceable documents and records

### medium priority

- Kawaguchi Unraid flash/configuration
- Kawaguchi application configuration and selected metadata
- Plex/media automation metadata
- AdGuard configuration

### low priority / replaceable

- movies and TV payloads
- downloads and caches
- machine-learning model cache
- Saiko lab VMs unless a specific experiment becomes worth preserving

## transition state

```text
current
kawaguchi -> media + transitional applications + temporary DNS
motosu    -> Immich; OS/storage rebuild planned
yamanaka  -> Debian installed; storage/NIC/application deployment in progress
saiko     -> packed/offline; Bazzite installed; Proxmox planned
network   -> UDM-Pro routing

target
kawaguchi -> media + manga + uptime monitoring
motosu    -> TrueNAS SCALE + photos + Immich + backups + AdGuard
yamanaka  -> Debian + applications + centralized monitoring + AdGuard
saiko     -> Proxmox lab
network   -> OPNsense routing + selected core/access switching
```

Migration order is migrate, verify, back up, then remove the old deployment.

## principles

1. Keep host roles obvious.
2. Prefer a small number of understandable systems over unnecessary clustering.
3. Use Docker Compose for Yamanaka unless a concrete need justifies something else.
4. Keep production and experimentation separate.
5. Document storage, dependencies, and recovery before adding automation.
6. Do not preserve experiments solely because they already exist.
7. Keep secrets, personal information, exact addressing, and unique external resource identifiers out of the public repository.
8. Treat the documentation as the source of truth for non-sensitive infrastructure design.
