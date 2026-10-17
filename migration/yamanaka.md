# yamanaka migration plan

## goal

Move retained non-media self-hosted applications off `kawaguchi` and onto `yamanaka` without disrupting the media stack.

Final production role split:

```text
kawaguchi = media + manga + independent uptime watchdog
motosu    = photos + Immich + backup storage + redundant DNS
yamanaka  = non-media applications + centralized monitoring + redundant DNS
shoji     = reserved / unassigned
```

Experimental/lab workloads belong in gusuku, not Yamanaka.

Migration order:

```text
inventory -> back up -> deploy -> restore -> verify -> cut over -> observe -> clean up
```

Do not remove a working Kawaguchi deployment until the Yamanaka replacement and its independent backup are verified.

## current yamanaka state

```text
hardware        Dell OptiPlex 3070 SFF
cpu             Intel Core i5-9500, 6C/6T
os              Debian GNU/Linux 13 (trixie)
memory          16 GB DDR4-2666
memory maximum  32 GB
boot nvme       Patriot P300 128 GB
app nvme        500 GB device planned/ordered
network         onboard 1 GbE; Intel X520-DA2 upgrade planned/ordered
remote access   SSH working
```

The prior assumption that Yamanaka required 32 GB before deployment is retired. Upgrade memory only if measured workload justifies it.

Motosu is already rebuilt on TrueNAS SCALE and is the intended independent backup target. Its Immich restore is still being validated, so Yamanaka backup jobs should be finalized against the stable TrueNAS dataset layout rather than old UGOS paths.

## stays on kawaguchi

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

Manga remains part of the Kawaguchi media role. AdGuard Home is temporary there.

## stays on motosu

- Immich stack
- photo/archive storage
- Yamanaka backup datasets
- TrueNAS/ZFS snapshot functionality
- selected B2 backup jobs
- one AdGuard Home instance in the target state

## moves to yamanaka

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
- application-local PostgreSQL/Redis dependencies
- one AdGuard Home instance

## delete instead of migrate

- RomM
- MariaDB if RomM is its only remaining consumer

Review before cleanup:

- TitleCardMaker
- Lidarr
- Kometa

## phase 1 — finish yamanaka platform

Completed:

- Debian 13 installed
- hostname/UEFI/basic administration verified
- SSH working
- hardware inventory completed

Remaining:

1. install/verify final application NVMe
2. install/verify Intel X520-DA2
3. configure stable production networking
4. install Docker Engine and Docker Compose
5. establish predictable Compose/data paths
6. configure normal update/time/administration policy
7. establish Yamanaka-to-Motosu backup flow before high-value cutovers

Recommended logical pattern:

```text
/srv/
├── compose/
└── data/
```

The exact directory tree may evolve, but Compose definitions and persistent data should remain predictable and documented.

## phase 2 — capture kawaguchi source state

For every service being moved, record privately as appropriate:

- image/tag
- container name
- environment variables
- exposed ports
- bind mounts/volumes
- Docker networks
- restart policy
- dependencies
- application version
- persistent-data size

Do not put secrets in this public repo.

Create an independent backup/export before changing each service. A backup stored only inside Kawaguchi appdata is not independent.

## phase 3 — deploy compose stacks

Use Docker Compose as the normal deployment method. Prefer one project per application or tightly coupled stack.

Examples:

```text
linkwarden -> app + postgres
paperless  -> app + redis
endurain   -> app + postgres + redis
monitoring -> prometheus + grafana + loki
```

Keep databases/caches on private Compose networks unless an external client actually requires access.

## phase 4 — migration waves

### wave 1 — low-risk utilities

- Stirling PDF
- Homepage

Use these to validate Docker, networking, storage, reboot behavior, and Compose conventions.

### wave 2 — simpler stateful apps

- Mealie
- Actual Budget
- HomeBox

For each: stop writes, export/back up, copy persistence, start on Yamanaka, verify representative data, and keep the Kawaguchi copy stopped but intact during observation.

### wave 3 — database-backed apps

- Linkwarden
- Paperless-ngx
- Endurain

Use native database dumps/application-aware exports. Verify users, representative historical data, file storage, search/indexing where relevant, and all dependent services before cutover.

### wave 4 — monitoring and DNS

Deploy/move:

- Prometheus
- Grafana
- Loki
- AdGuard Home

Keep Uptime Kuma on Kawaguchi so Yamanaka failure does not remove every monitoring path.

Target monitoring relationship:

```text
                yamanaka
        prometheus / grafana / loki
             /               \
     kawaguchi               motosu
      metrics                 metrics

                kawaguchi
              uptime kuma
             /          \
        yamanaka       motosu
         uptime         uptime
```

## phase 5 — romm retirement

Before deletion:

1. confirm no ROM/emulator data needs retention
2. confirm no other service uses MariaDB
3. confirm no other active service uses the ROM share
4. stop RomM and observe briefly
5. remove RomM/appdata
6. remove MariaDB only if unused
7. remove the ROM share later if nothing depends on it

## cutover convention

For every migrated application:

```text
1. stop writes on kawaguchi
2. take final backup/export
3. sync persistent data
4. start on yamanaka
5. verify locally
6. update normal client access/DNS/bookmarks as needed
7. verify from normal clients
8. keep kawaguchi copy stopped but intact
9. observe
10. remove old copy only when confident
```

Never run two writable copies of the same database-backed service against duplicated state.

## backup requirement

Important Yamanaka state must have an independent backup on Motosu before old Kawaguchi state is permanently deleted.

Use database-native dumps or application-aware exports. Do not treat direct copies of live PostgreSQL/Redis directories as the primary backup method.

## completion criteria

The migration is complete when:

- every retained non-media application runs from Yamanaka
- important Yamanaka data has an independent Motosu backup
- no retained Yamanaka app depends on old Kawaguchi state
- Kawaguchi is reduced to media/manga, Uptime Kuma, and host-specific agents
- redundant AdGuard Home runs on Yamanaka and Motosu
- RomM is retired
- obsolete Kawaguchi containers, networks, mounts, and appdata are cleaned up
- the repository describes deployed state rather than obsolete transition assumptions
