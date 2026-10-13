# service classification

Services are classified by function, current placement, intended placement, and how important their persistent data is.

The target host model is:

```text
kawaguchi = media
motosu    = photos
yamanaka  = non-media applications + monitoring
```

Yamanaka is not intended to host game servers.

## media

These services directly manage, acquire, index, subtitle, serve, or monitor media stored on Kawaguchi. They should remain on Kawaguchi.

| service | current host | target host | status | backup priority |
| --- | --- | --- | --- | --- |
| Plex | kawaguchi | kawaguchi | permanent | medium |
| Sonarr | kawaguchi | kawaguchi | permanent | medium |
| Radarr | kawaguchi | kawaguchi | permanent | medium |
| SABnzbd | kawaguchi | kawaguchi | permanent | low-medium |
| Bazarr | kawaguchi | kawaguchi | permanent | medium |
| Seerr | kawaguchi | kawaguchi | permanent | medium |
| Tautulli | kawaguchi | kawaguchi | permanent | medium |
| Recyclarr | kawaguchi | kawaguchi | permanent | low-medium |
| Unpackerr | kawaguchi | kawaguchi | permanent | low |
| Komga | kawaguchi | kawaguchi | permanent | medium |
| Komf | kawaguchi | kawaguchi | permanent | low-medium |
| Tachidesk | kawaguchi | kawaguchi | permanent | medium |

Primary data dependencies:

```text
/mnt/user/media
/mnt/user/downloads
```

Manga remains on Kawaguchi along with the rest of the media stack.

Kawaguchi is intentionally treated as a relatively easy-to-rebuild media host. Most of its large data set comes from Usenet and can be reacquired. Configuration and metadata are useful to preserve, but the media payload itself is not a high-priority backup target.

## photos

The Immich stack stays together on Motosu because its primary library and database live there.

| service | current host | target host | status | backup priority |
| --- | --- | --- | --- | --- |
| Immich server | motosu | motosu | permanent | high |
| Immich PostgreSQL | motosu | motosu | permanent | high |
| Immich Valkey/Redis | motosu | motosu | permanent | low |
| Immich machine learning | motosu | motosu | permanent | low |
| Tailscale | motosu | motosu | permanent | medium |

Critical persistence:

```text
/volume1/docker/immich/library
/volume1/docker/immich/postgres
```

The machine-learning model cache and Redis state are rebuildable.

## personal applications

These are non-media applications currently running on Kawaguchi while being evaluated. Services that remain useful should move to Yamanaka.

| service | current host | target host | status | backup priority |
| --- | --- | --- | --- | --- |
| Paperless-ngx | kawaguchi | yamanaka | transitional | high |
| Mealie | kawaguchi | yamanaka | transitional | high |
| Actual Budget | kawaguchi | yamanaka | transitional | high |
| HomeBox | kawaguchi | yamanaka | transitional | high |
| Linkwarden | kawaguchi | yamanaka | transitional | high |
| Endurain | kawaguchi | yamanaka | transitional | high |

These services should not remain on Kawaguchi solely because spare compute capacity is available there.

## utilities

These are useful general-purpose tools rather than core media or photo services.

| service | current host | target host | status | backup priority |
| --- | --- | --- | --- | --- |
| Stirling PDF | kawaguchi | yamanaka | transitional | low |
| Homepage | kawaguchi | yamanaka | transitional | medium |

Utility services with little or no unique state can be recreated instead of heavily backed up.

## monitoring and infrastructure

The monitoring control plane should move to Yamanaka. Lightweight host-specific agents can remain on the systems they monitor.

| service | current host | target host | status | backup priority |
| --- | --- | --- | --- | --- |
| Prometheus | kawaguchi | yamanaka | transitional | medium |
| Grafana | kawaguchi | yamanaka | transitional | medium-high |
| cAdvisor | kawaguchi | kawaguchi | permanent host agent | low |

Future exporters or agents should remain near the host they monitor, while dashboards, metrics storage, and monitoring coordination live on Yamanaka.

## supporting services

Databases and caches belong with the application that depends on them rather than being treated as independent infrastructure.

| service | current host | target host | parent application | backup priority |
| --- | --- | --- | --- | --- |
| postgresql17-linkwarden | kawaguchi | yamanaka | Linkwarden | high |
| Redis | kawaguchi | yamanaka | Paperless-ngx | low-medium |
| endurain-postgres | kawaguchi | yamanaka | Endurain | high |
| endurain Redis | kawaguchi | yamanaka | Endurain | low |

MariaDB currently exists primarily for RomM. If RomM is removed, the MariaDB deployment should be reviewed and removed if nothing else depends on it.

Database backups should follow the importance of the parent application's data.

## planned removal / review before migration

A container should not automatically move to Yamanaka just because it currently exists on Kawaguchi.

Before migration, each non-media service should be classified as one of:

```text
keep     -> migrate to yamanaka
replace  -> deploy preferred replacement on yamanaka
delete   -> remove after confirming nothing depends on it
```

Current decisions:

```text
romm -> delete
```

RomM will probably be removed rather than migrated because emulation is not a significant enough use case to justify keeping the service.

Known appdata directories that should be reviewed before cleanup include:

```text
TitleCardMaker
lidarr
kometa
```

Their presence does not prove they are still actively used.

## game servers

Yamanaka will not host game servers.

Game-server hosting should remain separate from the always-on general application role. Bandai historically hosted Palworld and Valheim, but that does not make game-server hosting part of Yamanaka's target workload.

## migration rule

For every service moving from Kawaguchi to Yamanaka:

```text
1. identify persistent data and dependencies
2. back up the application and database
3. deploy on yamanaka
4. restore or copy persistent data
5. verify application behavior
6. verify dependent services and URLs
7. leave the kawaguchi copy intact until verification is complete
8. remove the old container and data only after successful cutover
```

Kawaguchi cleanup is intentionally deferred until either the Miami rebuild or Yamanaka deployment.