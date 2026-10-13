# yamanaka migration plan

## goal

Move non-media self-hosted applications off `kawaguchi` and onto `yamanaka` without disrupting the media stack.

The final role split is:

```text
kawaguchi = media
motosu    = photos
yamanaka  = non-media applications + monitoring
```

Yamanaka will not host game servers.

Kawaguchi cleanup is intentionally deferred until either the Miami rebuild or the Yamanaka migration. The migration order is always:

```text
inventory -> back up -> deploy -> restore -> verify -> cut over -> observe -> clean up
```

Do not remove a working Kawaguchi deployment until its Yamanaka replacement has been verified.

## scope

### stays on kawaguchi

Media and manga services remain on Kawaguchi:

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
- cAdvisor or other Kawaguchi-specific monitoring agents

Kawaguchi bulk media is considered largely replaceable because most of it can be reacquired from Usenet. Backups should favor configuration and metadata rather than the movie and TV payloads themselves.

### stays on motosu

- Immich server
- Immich PostgreSQL
- Immich Valkey/Redis
- Immich machine learning
- Tailscale

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
- supporting databases and caches required by those applications

### delete instead of migrate

- RomM
- MariaDB if verification confirms RomM is its only remaining consumer

### review during cleanup

The following existing appdata directories should be reviewed rather than automatically migrated:

- `TitleCardMaker`
- `lidarr`
- `kometa`

If they are no longer in use, remove them only after confirming that no active service depends on them.

## phase 0 — hardware selection

Hardware selection is handled separately.

The migration should not begin until Yamanaka is physically available and stable enough to become an always-on host.

Minimum deployment assumptions currently are:

- Linux server OS
- Docker Engine with Docker Compose
- persistent NVMe storage
- enough RAM for the application stack and databases
- wired Ethernet
- static or reserved LAN address

Do not hard-code hardware-specific assumptions into service definitions unless the selected machine requires them.

## phase 1 — prepare yamanaka

Before moving any application:

1. Install the selected Linux server OS.
2. Set hostname to `yamanaka`.
3. Configure updates, time synchronization, SSH, and basic administration.
4. Install Docker Engine and the Docker Compose plugin.
5. Configure a fixed/reserved network address.
6. Create the application-data directory structure.
7. Configure remote administration.
8. Confirm Yamanaka can reach required Internet services and can be reached from the trusted LAN.
9. Decide the final backup destination before important personal data is migrated.

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
    └── grafana/
```

The exact path can change during installation. The important rule is that Compose definitions and persistent data have predictable locations and are documented.

## phase 2 — capture the kawaguchi source state

Before the first migration, preserve enough information to recreate the current deployment.

For each service being moved, record:

- image and image tag
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

Create an independent copy of the relevant persistent data before changing the service.

Do not treat the existing application-generated backup folders inside Kawaguchi appdata as independent backups because they are stored on the same host.

## phase 3 — create yamanaka compose stacks

Use Docker Compose as the normal deployment method.

Prefer one Compose project per application or tightly coupled application stack. Databases and caches should live with the application that uses them.

Examples:

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
└── grafana
```

Where practical, use Docker-internal DNS names for application-to-database communication instead of sending traffic back through Yamanaka's LAN address and published database ports.

Databases such as PostgreSQL, MariaDB, and Redis should not be published to the LAN unless an actual external client requires it.

## phase 4 — migration waves

Move applications in small groups. Complete and verify one wave before starting the next.

### wave 1 — low-risk utilities

Move first:

- Stirling PDF
- Homepage

Reason:

- little unique state
- easy to recreate
- useful for validating the Yamanaka Docker, networking, storage, and Compose conventions

Success criteria:

- containers survive a Yamanaka reboot
- application URLs work
- persistent settings survive container recreation

### wave 2 — simple stateful applications

Move:

- Mealie
- Actual Budget
- HomeBox

For each application:

1. Stop writes on the Kawaguchi instance.
2. Make an independent backup/export.
3. Copy its persistent data to Yamanaka.
4. Start the Yamanaka stack.
5. Verify login, settings, and representative data.
6. Keep the Kawaguchi copy stopped but intact during the observation period.

These applications contain personal data and should have a working Yamanaka backup process before the old Kawaguchi copy is removed.

### wave 3 — database-backed personal applications

Move Linkwarden, Paperless, and Endurain individually rather than simultaneously.

#### linkwarden

Current verified dependency:

```text
linkwarden -> postgresql17-linkwarden
```

Current deployment reaches PostgreSQL through Kawaguchi's LAN address and published port `5432`.

Target design:

```text
linkwarden -> postgres
```

on a private Docker network within its Yamanaka Compose project.

Migration requirements:

- export/back up PostgreSQL
- verify whether Linkwarden has any persistent files or uploads outside PostgreSQL before cutover
- restore database on Yamanaka
- update database connection to the internal Compose service name
- verify saved links, users, and application settings

#### paperless-ngx

Current verified persistent paths include:

```text
/mnt/user/appdata/paperless-ngx/data
/mnt/user/media/paperless/consume
/mnt/user/media/paperless/export
/mnt/user/media/paperless/media
```

Current Paperless Redis traffic goes to Kawaguchi's LAN address on `6379`.

Target design:

```text
paperless-ngx
├── persistent application/document data on yamanaka
└── redis on the private paperless compose network
```

Migration requirements:

- identify every Paperless persistent path and copy it to Yamanaka
- preserve the document/media library
- deploy Redis as a local supporting service
- update the Redis URL to the internal service name
- verify document counts, search, OCR, tags, correspondents, and file access

Paperless data is high-priority backup data after migration.

#### endurain

Current stack already has a useful logical boundary:

```text
endurain-app
├── endurain-postgres
└── redis
```

Migration requirements:

- back up Endurain PostgreSQL
- copy persistent backend data/logs that are required
- deploy the entire stack together on Yamanaka
- restore PostgreSQL
- keep PostgreSQL and Redis private to the Compose network
- verify users, activities, settings, and representative historical data

### wave 4 — monitoring

Move:

- Prometheus
- Grafana

Keep host-local agents where they belong. For example, cAdvisor can remain on Kawaguchi while Prometheus and Grafana run on Yamanaka.

Migration requirements:

- copy Grafana persistent data or export the dashboards/configuration that matter
- decide whether historical Prometheus metrics are worth preserving
- update Prometheus scrape targets for the post-move network
- verify Kawaguchi and Yamanaka metrics
- later add Motosu metrics only if useful

Historical metrics are less important than recreating the monitoring configuration cleanly.

## phase 5 — romm retirement

RomM should be removed rather than migrated.

Before deletion:

1. Confirm no emulator/ROM data needs to be retained.
2. Confirm no other service uses the MariaDB container.
3. Confirm no other active service uses `/mnt/user/roms`.
4. Stop RomM.
5. Leave it stopped for a short observation period.
6. Remove the RomM container and associated application data.
7. Remove MariaDB only after confirming it has no other consumers.
8. Remove the ROM share later if nothing else uses it and its contents are unwanted.

## phase 6 — cutover conventions

For each migrated application:

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

Avoid running two writable copies of the same database-backed application against duplicated data.

## phase 7 — backup yamanaka

Yamanaka will contain more irreplaceable state than Kawaguchi, so its backup requirements are stricter.

High-priority Yamanaka data includes:

- Paperless documents and metadata
- Actual Budget data
- HomeBox inventory
- Linkwarden PostgreSQL data and any file storage
- Mealie data
- Endurain PostgreSQL and required application data
- important Grafana configuration
- Compose definitions and deployment documentation

The final backup mechanism will be selected after Yamanaka hardware and storage are finalized.

At minimum, Yamanaka should have an independent backup outside its own system disk before the corresponding Kawaguchi copies are permanently deleted.

## phase 8 — kawaguchi cleanup

Only clean Kawaguchi after migrations are proven.

Cleanup scope:

- remove successfully migrated non-media containers
- remove their obsolete appdata only after backup and verification
- remove retired RomM and its MariaDB dependency
- review `TitleCardMaker`, `lidarr`, and `kometa`
- remove unused Docker networks such as `homelable` and Docker `wg0` only after confirming they remain unused
- remove the uppercase `/mnt/user/Media` share after removing the obsolete Komf `/library` mount and confirming nothing else uses it
- leave manga services and `/mnt/user/media/manga` on Kawaguchi
- retain only monitoring agents that specifically need to run on Kawaguchi

The desired end state is that looking at Kawaguchi's Docker list immediately makes sense as a media server.

## final target

```text
kawaguchi
├── plex
├── media acquisition / automation
├── subtitles / requests / statistics
├── manga services
└── local monitoring agent

motosu
└── immich stack

yamanaka
├── paperless
├── mealie
├── actual budget
├── homebox
├── linkwarden + postgres
├── stirling pdf
├── endurain + postgres + redis
├── homepage
├── prometheus
├── grafana
└── future non-media self-hosted applications
```

Game servers are outside Yamanaka's role.

## completion criteria

The migration is complete when:

- every retained non-media application runs from Yamanaka
- important Yamanaka application data has an independent backup
- no retained application on Yamanaka depends on an old Kawaguchi database or appdata path
- Kawaguchi contains only media/manga workloads and host-specific agents
- Motosu remains dedicated to Immich/photos
- RomM is retired
- obsolete Kawaguchi containers, networks, mounts, and appdata have been cleaned up
- the Fujigoko documentation reflects the deployed state rather than the transitional state
