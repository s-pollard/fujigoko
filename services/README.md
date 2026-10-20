# services

This file records production service placement and dependencies without publishing private addresses, credentials, admin URLs, or other sensitive operational details.

## kawaguchi

### monitoring / infrastructure

- cAdvisor / host monitoring agent

### media

- Plex
- Sonarr
- Radarr
- SABnzbd
- Bazarr
- Seerr
- Tautulli
- Recyclarr
- Unpackerr

### manga

- Komga
- Komf
- Tachidesk

The former Kawaguchi copies of migrated non-media services have been removed. RomM, its MariaDB dependency, and other retired appdata have also been removed. Kawaguchi now contains only the active media/manga stack plus cAdvisor.

Known dependency examples:

```text
sabnzbd -> download storage
sonarr  -> downloads + tv library
radarr  -> downloads + movie library
bazarr  -> tv + movie libraries
plex    -> media library
komga / komf / tachidesk -> manga library
```

## motosu

Motosu is now a TrueNAS SCALE host.

Target/permanent service classes:

- Immich server
- Immich PostgreSQL
- Immich Valkey/Redis
- Immich machine learning
- storage/snapshot services provided by TrueNAS
- one AdGuard Home instance as the second DNS node

The Immich application/database restoration is complete and validated. The restored photo library is operating normally.

Critical persistence is the Immich library, database recovery data, photo/archive data, and Yamanaka backup datasets. Redis/Valkey state and machine-learning caches are rebuildable.

## yamanaka

Yamanaka hosts the retained non-media production services migrated from Kawaguchi. Supporting databases/caches stay with the application they serve rather than becoming shared LAN infrastructure.

Current services:

### applications

- Paperless-ngx + private Redis
- Mealie
- Actual Budget
- HomeBox
- Linkwarden + PostgreSQL
- Stirling PDF
- Endurain + PostgreSQL + Redis
- Homepage
- SearXNG

### monitoring / logging

- Prometheus
- Grafana
- Loki
- Grafana Alloy
- Uptime Kuma

Prometheus continues to scrape cAdvisor on Kawaguchi for host/container metrics. Alloy collects Yamanaka Docker logs into Loki for Grafana exploration.

### infrastructure / operations

- AdGuard Home
- signal-cli-rest-api for Uptime Kuma notifications
- Dockhand for Docker operations/management

The Yamanaka stack has been reboot-tested successfully and expected production containers return automatically.

Potential additions under evaluation:

- Nextcloud
- Vaultwarden

These remain optional until actually deployed and found useful.

## DNS target

Current deployed state:

```text
yamanaka -> adguard-home
```

Target redundant state:

```text
yamanaka -> adguard-home
motosu   -> adguard-home
```

Both instances should provide equivalent filtering policy on separate physical hosts. Exact resolver addresses and synchronization details stay in private operational configuration.

## completed cleanup

Kawaguchi cleanup completed on 2026-10-20:

- migrated non-media containers removed
- RomM and MariaDB removed
- obsolete stopped containers removed
- dangling Docker volumes removed
- unused Docker images pruned
- retired appdata removed
- TitleCardMaker, Kometa, Lidarr, and Listenarr appdata removed

The resulting Docker state was 14 active containers, 14 active images, no local Docker volumes, and no reclaimable Docker image/container space.

## lab boundary

Disposable services, VMs, Kubernetes experiments, game servers, and other learning workloads belong in the separate gusuku lab. Fujigoko production services must not depend on them.
