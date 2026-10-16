# architecture

## design intent

Fujigoko is being split into a small number of hosts with clear roles rather than letting one machine become the permanent home for every service.

The target model is:

```text
kawaguchi = media
motosu    = photos
yamanaka  = general applications
saiko     = Proxmox lab / experimentation
shoji     = reserved / role undecided
```

The current deployment on `kawaguchi` is transitional. It still runs a number of non-media applications that will move to Yamanaka if retained.

## host roles

### kawaguchi — media

Primary role: media server and media-adjacent storage/services.

Hardware:

- UGREEN iDX6011 64 GB 6-Bay AI NAS
- Intel Core Ultra 5 125H
- 64 GB installed memory
- Unraid 7.3.2
- 10 GbE uplink

Intended permanent workloads:

- Plex
- Sonarr
- Radarr
- SABnzbd
- Bazarr
- Seerr
- Tautulli
- Recyclarr
- Unpackerr
- Komga
- Komf
- Tachidesk
- Uptime Kuma
- cAdvisor / host-specific monitoring agents

Manga remains part of the Kawaguchi media role.

Primary storage responsibilities:

- `/mnt/user/media`
- `/mnt/user/downloads`
- media-related application data

Kawaguchi is intentionally treated as relatively easy to rebuild. Most of the large movie and TV library originates from Usenet and can be reacquired. The priority is preserving enough configuration and metadata to restore the media stack without treating the media payload itself as irreplaceable.

Kawaguchi should not become the permanent host for unrelated personal applications just because it has spare compute capacity.

AdGuard Home currently runs on Kawaguchi but is not part of its target role. DNS will move off Kawaguchi; final placement and redundancy are still to be designed.

### motosu — photos

Primary role: dedicated photo storage and Immich host.

Current hardware:

- UGREEN NASync DXP2800
- Intel N100
- 7.5 GiB usable memory
- 2 × 6 TB Seagate drives
- current UGOS / Debian-based platform
- current Linux RAID1 + Btrfs storage

Planned platform:

- TrueNAS SCALE
- 2-disk ZFS mirror using the existing 6 TB drives initially
- ZFS snapshots for local rollback
- Restic backup to Backblaze B2 retained as the independent off-site backup

Permanent workloads:

- Immich server
- Immich PostgreSQL
- Immich Valkey/Redis
- Immich machine learning
- Tailscale

Motosu will also become the home of the GFX photo archive once the TrueNAS migration, Immich phone sync, ZFS snapshots, and B2 backup are verified. Immich itself is intended primarily for phone photos and finished/exported GFX photos; the main GFX RAW archive will remain normal files on Motosu storage rather than being treated as an Immich-only library.

Motosu should remain focused on photos rather than becoming a general-purpose application host.

### yamanaka — general applications

Primary role: simple, always-on production application server.

Yamanaka will take over non-media self-hosted applications from Kawaguchi.

Target characteristics:

- SFF business PC
- Debian
- Docker Engine + Docker Compose
- 32 GB RAM target
- 1–2 TB NVMe application storage
- at least 2.5 GbE preferred
- no discrete GPU requirement

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
- supporting PostgreSQL, Redis, and similar service dependencies

Yamanaka itself should expose host/container metrics so the central monitoring stack can monitor its own host.

Yamanaka will not host game servers. Only applications that prove useful should be migrated. Experimental containers can be removed instead of preserved indefinitely.

### saiko — lab / experimentation

`saiko` is the server formerly known as `bandai`.

Known hardware:

- AMD Ryzen 9 3900X
- 32 GB DDR4
- EVGA GeForce RTX 3060 Ti FTW3 Ultra 8 GB
- MSI MPG X570 Gaming Edge WiFi
- WD Blue 500 GB SSD
- 4U rackmount chassis

Planned platform:

- Proxmox VE

Intended use:

- OPNsense test VMs
- Linux test VMs
- Kubernetes / k3s experiments
- networking labs
- temporary game-server or service experiments
- GPU passthrough experiments if useful

Saiko is not intended to host required production services. It may remain powered off when not in use so experiments can be broken or rebuilt without affecting normal Fujigoko operation.

### shoji — reserved

Shoji has no decided role. Keep the name reserved until a future major Fujigoko host or platform has a clear purpose.

Kubernetes is currently a Saiko lab experiment, not a planned production architecture. Shoji should not be assigned to Kubernetes or any other role until that role is actually justified.

## service placement rule

Services should stay near the data and role they primarily depend on.

```text
media pipeline and Plex data      -> kawaguchi
manga services and manga data     -> kawaguchi
independent uptime watchdog       -> kawaguchi
Immich and photo data             -> motosu
GFX RAW/archive storage           -> motosu
general personal applications     -> yamanaka
monitoring control plane          -> yamanaka
host-specific exporters/agents    -> monitored host
lab / disposable VMs              -> saiko
network infrastructure            -> place for availability, not convenience
DNS                               -> not kawaguchi in target state
```

Examples:

- Sonarr and Radarr stay on Kawaguchi because they manage media stored there.
- Komga, Komf, and Tachidesk stay on Kawaguchi because manga remains part of the media role.
- Immich stays on Motosu because its library and database are stored there.
- Paperless, Actual Budget, Linkwarden, HomeBox, and similar personal applications move to Yamanaka.
- Prometheus, Grafana, and Loki live on Yamanaka while lightweight exporters/agents remain on the machines being monitored.
- Uptime Kuma stays on Kawaguchi as an independent watchdog so monitoring is not entirely dependent on Yamanaka.
- AdGuard Home leaves Kawaguchi; its replacement/final placement should prioritize DNS availability and redundancy.

## monitoring architecture

```text
                yamanaka
        prometheus / grafana / loki
             /       |       \
            /        |        \
     kawaguchi     motosu     saiko
      metrics      metrics    metrics


                kawaguchi
              uptime kuma
             /     |      \
            /      |       \
       yamanaka  motosu    saiko
        uptime    uptime    uptime
```

Optional external monitoring can be added later if detection of a complete homelab or Internet outage becomes useful.

## backup priorities

Backup effort should follow data value rather than raw size.

### high priority

- Motosu Immich library and database backups
- Motosu GFX archive once established
- Yamanaka databases and persistent application data
- irreplaceable personal documents and records

### medium priority

- Kawaguchi Unraid flash/configuration
- Kawaguchi application configuration and selected metadata
- Plex metadata and configuration
- media automation configuration

### low priority / replaceable

- movies
- TV library
- downloads
- caches
- machine-learning model cache
- Saiko lab VMs unless a specific experiment becomes worth preserving
- other data that can be recreated or reacquired

Kawaguchi currently has local application-generated backups for several services but no verified independent backup system. Because the host is mostly a Usenet-backed media system, recovery should prioritize configuration over bulk media backup.

## current transition state

```text
                         current

kawaguchi
├── media workloads                permanent
├── monitoring                     mixed permanent/transitional
├── adguard home                   temporary placement
├── personal applications         transitional
└── supporting databases          transitional

motosu
└── immich stack                   permanent; OS/storage rebuild planned

bandai
└── offline / packed               becoming saiko


                         target

kawaguchi
└── media + manga + uptime kuma + host monitoring

motosu
└── truenas scale + photos + immich + gfx archive

yamanaka
└── debian + general applications + centralized monitoring

saiko
└── proxmox lab / experimentation

shoji
└── reserved
```

Kawaguchi cleanup is deferred until either the Miami rebuild or Yamanaka deployment. The migration order is migrate, verify, back up, then remove the old deployment.

## principles

1. Keep host roles obvious.
2. Prefer a small number of understandable systems over unnecessary clustering or orchestration.
3. Use Docker Compose for Yamanaka unless a concrete requirement justifies something more complex.
4. Keep production and experimentation separate: Yamanaka is production; Saiko is the lab.
5. Document services, storage, dependencies, and recovery paths before adding automation.
6. Do not preserve experimental services solely because they already exist.
7. Treat the documentation as the source of truth for the infrastructure map.
