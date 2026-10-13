# architecture

## design intent

Fujigoko is being split into a small number of hosts with clear roles rather than letting one machine become the permanent home for every service.

The target model is:

```text
kawaguchi = media
motosu    = photos
yamanaka  = general applications
```

The current deployment on `kawaguchi` is transitional. It still runs a number of non-media applications that are being tested and may move to Yamanaka if they remain useful.

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

Manga remains part of the Kawaguchi media role.

Primary storage responsibilities:

- `/mnt/user/media`
- `/mnt/user/downloads`
- media-related application data

Kawaguchi is intentionally treated as relatively easy to rebuild. Most of the large movie and TV library originates from Usenet and can be reacquired. The priority is preserving enough configuration and metadata to restore the media stack without treating the media payload itself as irreplaceable.

Kawaguchi should not become the permanent host for unrelated personal applications just because it has spare compute capacity.

### motosu — photos

Primary role: dedicated photo storage and Immich host.

Hardware:

- UGREEN NASync DXP2800
- Intel N100
- 7.5 GiB usable memory
- 2 × 6 TB Seagate drives
- Linux RAID1
- Btrfs

Permanent workloads:

- Immich server
- Immich PostgreSQL
- Immich Valkey/Redis
- Immich machine learning
- Tailscale

Important persistent paths:

```text
/volume1/docker/immich/library
/volume1/docker/immich/postgres
/volume1/docker/tailscale/state
```

Motosu should remain focused on the photo library rather than becoming a second general-purpose Docker host.

### yamanaka — general applications

Primary role: small, quiet, low-power 24/7 application server.

Yamanaka will take over non-media self-hosted applications from Kawaguchi.

Desired characteristics:

- physically small
- low idle power
- quiet
- 32 GB RAM target
- NVMe application storage
- at least 2.5 GbE preferred
- no discrete GPU requirement
- Linux server OS
- Docker Compose

Candidate workloads currently running on Kawaguchi that may move here:

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
- supporting PostgreSQL, Redis, and similar service dependencies

RomM is currently expected to be deleted rather than migrated.

Yamanaka will not host game servers. Game-server hosting remains a separate role from the always-on general application host.

Only applications that prove useful should be migrated. Experimental containers can be removed instead of preserved indefinitely.

## bandai

`bandai` is the current legacy game/TV-gaming host and is presently offline and packed for the move.

Known hardware:

- AMD Ryzen 9 3900X
- 32 GB DDR4
- EVGA GeForce RTX 3060 Ti FTW3 Ultra 8 GB
- MSI MPG X570 Gaming Edge WiFi
- WD Blue 500 GB SSD
- 4U rackmount chassis

Historically it ran Bazzite and also hosted Palworld and Valheim through Podman and a WireGuard/VPS relay.

Bandai is powerful enough to host the application workload, but its large 4U form factor and desktop-class hardware conflict with the desired low-power, compact always-on role. The current plan is to use a separate low-power host named Yamanaka for general applications.

Bandai does not need to remain part of the permanent Fujigoko naming scheme.

## service placement rule

Services should stay near the data and role they primarily depend on.

```text
media pipeline and Plex data      -> kawaguchi
manga services and manga data     -> kawaguchi
Immich and photo data             -> motosu
general personal applications     -> yamanaka
monitoring control plane          -> yamanaka
host-specific exporters/agents    -> monitored host
game servers                      -> not yamanaka
```

Examples:

- Sonarr and Radarr stay on Kawaguchi because they manage media stored there.
- Komga, Komf, and Tachidesk stay on Kawaguchi because manga remains part of the media role.
- Immich stays on Motosu because its library and database are stored there.
- Paperless, Actual Budget, Linkwarden, HomeBox, and similar personal applications should move to Yamanaka if retained.
- Prometheus and Grafana should eventually live on Yamanaka while lightweight exporters can remain on the machines being monitored.

## backup priorities

Backup effort should follow data value rather than raw size.

### high priority

- Motosu Immich library
- Motosu Immich PostgreSQL data
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
- other data that can be recreated or reacquired

Kawaguchi currently has local application-generated backups for several services but no verified independent backup system. Because the host is mostly a Usenet-backed media system, recovery should prioritize configuration over bulk media backup.

## current transition state

```text
                         current

kawaguchi
├── media workloads                permanent
├── monitoring                     transitional
├── personal applications         transitional
└── supporting databases          transitional

motosu
└── immich stack                   permanent

bandai
└── offline / packed               legacy


                         target

kawaguchi
└── media + manga

motosu
└── photos

yamanaka
└── general applications + monitoring
```

Kawaguchi cleanup is deferred until either the Miami rebuild or Yamanaka deployment. The migration order is migrate, verify, back up, then remove the old deployment.

## principles

1. Keep host roles obvious.
2. Prefer a small number of understandable systems over unnecessary clustering or orchestration.
3. Use Docker Compose for general application deployment unless a concrete requirement justifies something more complex.
4. Document services, storage, dependencies, and recovery paths before adding automation.
5. Do not preserve experimental services solely because they already exist.
6. Treat the documentation as the source of truth for the infrastructure map.
