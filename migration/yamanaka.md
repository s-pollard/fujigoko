# yamanaka migration plan

## goal

Move non-media self-hosted applications off `kawaguchi` and onto `yamanaka` without disrupting the media stack.

The final role split is:

```text
kawaguchi = media + independent uptime watchdog
motosu    = photos
yamanaka  = non-media applications + centralized monitoring
saiko     = Proxmox lab / experimentation
shoji     = reserved / role undecided
```

Yamanaka will not host game servers or lab workloads.

The migration order is always:

```text
inventory -> back up -> deploy -> restore -> verify -> cut over -> observe -> clean up
```

Do not remove a working Kawaguchi deployment until its Yamanaka replacement has been verified.

## current yamanaka state

Hardware selection is complete.

```text
hardware        Dell OptiPlex 3070 SFF
cpu             Intel Core i5-9500, 6C/6T
os              Debian GNU/Linux 13 (trixie)
boot            UEFI
memory          16 GB DDR4-2666, 2 x 8 GB
memory maximum  32 GB, 2 x 16 GB
current nvme    Patriot P300 128 GB
new nvme        500 GB ordered
onboard nic     Realtek 1 GbE
new nic         Intel X520-DA2 dual-port 10 GbE SFP+, low-profile, ordered
remote access   SSH working
```

The previous assumption that Yamanaka required 32 GB before deployment is retired. Start with the installed 16 GB and use actual Docker workload, memory pressure, and swap behavior to decide whether the 2 × 16 GB upgrade is justified.

The 500 GB NVMe will be the local application-storage device. Live databases, Redis, application state, and monitoring data remain local to Yamanaka; Motosu is the independent backup target.

## scope

### stays on kawaguchi

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
- Kawaguchi-specific monitoring agents

Manga remains part of the Kawaguchi media role. AdGuard Home does not remain on Kawaguchi in the target state.

### stays on motosu

- Immich server
- Immich PostgreSQL
- Immich Valkey/Redis
- Immich machine learning
- Tailscale

Motosu is handled as a separate UGOS-to-TrueNAS migration project.

### moves to yamanaka

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
- supporting databases and caches required by those applications
- AdGuard Home as one of the two redundant LAN DNS resolvers

### delete instead of migrate

- RomM
- MariaDB if verification confirms RomM is its only remaining consumer

### review during cleanup

- `TitleCardMaker`
- `lidarr`
- `kometa`

Remove these only after confirming that no active service depends on them.

## phase 0 — hardware selection — complete

The production host is the OptiPlex 3070 SFF described above. Hardware shopping is no longer a migration prerequisite.

Remaining physical work:

1. install and verify the ordered 500 GB NVMe
2. install and verify the ordered X520-DA2
3. confirm stable networking and storage
4. leave the existing 16 GB RAM in place unless measured workload justifies 32 GB

## phase 1 — prepare yamanaka — in progress

Completed:

- Debian 13 installed
- hostname set to `yamanaka`
- UEFI boot verified
- SSH working
- sudo working
- basic hardware inventory completed

Remaining:

1. install the 500 GB NVMe and establish the final application-data filesystem/layout
2. install the X520-DA2 and configure the production network connection
3. configure a fixed/reserved production address after the network layout is finalized
4. install Docker Engine and Docker Compose plugin
5. create the application-data directory structure
6. configure normal update/time/administration policy
7. confirm Yamanaka can reach required Internet services and trusted LAN hosts
8. configure the Yamanaka-to-Motosu backup path before irreplaceable application state is cut over

Recommended directory pattern:

```text
/srv/
├── compose/
│   ├── paperless/
│   ├── mealie/
│   ├── actual-budget/
│   ├── homebox/
│   ├── linkwarden/
│   ├── stirling-pdf/
│   ├── endurain/
│   ├── homepage/
│   └── monitoring/
└── data/
    ├── paperless/
    ├── mealie/
    ├── actual-budget/
    ├── homebox/
    ├── linkwarden/
    ├── endurain/
    ├── homepage/
    ├── prometheus/
    ├── grafana/
    └── loki/
```

The exact path can change during installation. Compose definitions and persistent data must have predictable documented locations.

## phase 2 — capture kawaguchi source state

For every service being moved, record:

- image and tag
- container name
- environment variables, excluding secrets from the public repository
- exposed ports
- bind mounts and Docker volumes
- Docker networks
- restart policy
- dependencies
- database connection settings
- current application version
- current data size

Create an independent copy of relevant persistent data before changing the service. Application-generated backups stored only inside Kawaguchi appdata are not independent backups.

## phase 3 — create yamanaka compose stacks

Use Docker Compose as the normal deployment method. Prefer one Compose project per application or tightly coupled stack. Databases and caches stay with the application that uses them.

```text
linkwarden/
├── linkwarden
└── postgres

paperless/
├── paperless-ngx
└── redis

endurain/
├── endurain-app
├── postgres
└── redis

monitoring/
├── prometheus
├── grafana
└── loki
```

Use Docker-internal DNS names for application-to-database communication. PostgreSQL, MariaDB, and Redis should not be published to the LAN unless an external client actually requires it.

## phase 4 — migration waves

### wave 1 — low-risk utilities

Move first:

- Stirling PDF
- Homepage

Use these to validate Docker, networking, storage, Compose conventions, reboot behavior, and persistence.

### wave 2 — simple stateful applications

Move:

- Mealie
- Actual Budget
- HomeBox

For each application: stop writes on Kawaguchi, create an independent backup/export, copy persistent data, start the Yamanaka stack, verify representative data, and keep the old copy stopped but intact during observation.

### wave 3 — database-backed personal applications

Move individually:

- Linkwarden
- Paperless-ngx
- Endurain

#### linkwarden

Current dependency:

```text
linkwarden -> postgresql17-linkwarden
```

Target:

```text
linkwarden -> postgres
```

on a private Compose network. Export PostgreSQL, identify any file storage outside the database, restore on Yamanaka, and verify users and saved links.

#### paperless-ngx

Current persistent paths include:

```text
/mnt/user/appdata/paperless-ngx/data
/mnt/user/media/paperless/consume
/mnt/user/media/paperless/export
/mnt/user/media/paperless/media
```

Copy all required Paperless state and document/media data to Yamanaka, deploy Redis locally to the Compose stack, and verify document counts, search, OCR, tags, correspondents, and file access.

Paperless is high-priority backup data after migration.

#### endurain

Move the application, PostgreSQL, Redis, and required persistent files as one logical stack. Restore PostgreSQL and verify users, activities, settings, and representative historical data.

### wave 4 — monitoring and DNS

Deploy/move:

- Prometheus
- Grafana
- Loki
- AdGuard Home

Keep host-local agents on the monitored hosts. Uptime Kuma remains on Kawaguchi so the independent availability check is outside Yamanaka's failure domain.

Target monitoring design:

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

AdGuard Home runs on both Yamanaka and Motosu in the final design.

Historical Prometheus data is lower priority than clean monitoring configuration and working scrape targets.

## phase 5 — romm retirement

Before deletion:

1. confirm no emulator/ROM data needs retention
2. confirm no other service uses MariaDB
3. confirm no other active service uses `/mnt/user/roms`
4. stop RomM
5. leave it stopped for a short observation period
6. remove RomM and associated application data
7. remove MariaDB only after confirming no other consumers
8. remove the ROM share later if nothing else uses it

## phase 6 — cutover convention

For every migrated application:

```text
1. stop writes on kawaguchi
2. take final backup/export
3. sync final persistent data
4. start on yamanaka
5. verify locally
6. update bookmark/DNS/reverse-proxy entry if applicable
7. verify from normal client devices
8. keep kawaguchi copy stopped but intact
9. observe
10. remove kawaguchi copy only when confident
```

Never run two writable copies of the same database-backed application against duplicated state.

## phase 7 — backup yamanaka

Important Yamanaka data includes:

- Paperless documents and metadata
- Actual Budget data
- HomeBox inventory
- Linkwarden PostgreSQL data and file storage
- Mealie data
- Endurain PostgreSQL and required application data
- important Grafana configuration
- Compose definitions and deployment documentation

Live application state stays on the local 500 GB NVMe. Independent backups go to Motosu, where the backup dataset receives ZFS mirror protection, snapshots, and selected B2 off-site protection.

Use database-native dumps or application-aware exports for database-backed services rather than copying live database directories.

## phase 8 — kawaguchi cleanup

Only clean Kawaguchi after migrations are proven.

- remove successfully migrated non-media containers
- remove obsolete appdata only after backup and verification
- remove retired RomM and its MariaDB dependency
- review `TitleCardMaker`, `lidarr`, and `kometa`
- remove unused Docker networks only after confirming they remain unused
- remove uppercase `/mnt/user/Media` only after removing the obsolete Komf `/library` mount and confirming nothing else uses it
- leave manga services and `/mnt/user/media/manga` on Kawaguchi
- retain Uptime Kuma and Kawaguchi-specific monitoring agents
- remove AdGuard Home from Kawaguchi only after Yamanaka + Motosu DNS is working

## completion criteria

The migration is complete when:

- every retained non-media application runs from Yamanaka
- important Yamanaka application data has an independent backup on Motosu
- no retained Yamanaka application depends on old Kawaguchi database or appdata paths
- Kawaguchi contains only media/manga workloads, Uptime Kuma, and host-specific agents
- redundant AdGuard Home runs on Yamanaka and Motosu
- RomM is retired
- obsolete Kawaguchi containers, networks, mounts, and appdata are cleaned up
- the repository reflects the deployed state rather than the transitional state
