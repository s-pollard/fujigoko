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

### retired / stopped rollback copies

The former Kawaguchi copies of migrated non-media services are stopped. Their appdata may remain temporarily for rollback until independent Yamanaka backups are verified.

RomM and its MariaDB dependency are also stopped pending final data/appdata cleanup.

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

The Immich library has been copied onto the rebuilt TrueNAS system. Final database/application restoration is still being completed and validated, so do not yet describe the Immich migration as finished.

Critical persistence is the Immich library, database recovery data, photo/archive data, and Yamanaka backup datasets. Redis/Valkey state and machine-learning caches are rebuildable.

## yamanaka

Yamanaka now hosts the retained non-media production services migrated from Kawaguchi. Supporting databases/caches stay with the application they serve rather than becoming shared LAN infrastructure.

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

### monitoring / logging

- Prometheus
- Grafana
- Loki
- Grafana Alloy
- Uptime Kuma

Prometheus continues to scrape cAdvisor on Kawaguchi for host/container metrics. Alloy collects Yamanaka Docker logs into Loki for Grafana exploration.

### infrastructure

- AdGuard Home
- signal-cli-rest-api for Uptime Kuma notifications

The Yamanaka stack has been reboot-tested successfully and all expected containers return automatically.

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

## cleanup candidates

Review before removal:

- old stopped Kawaguchi copies of migrated services after Yamanaka backups are verified
- RomM and MariaDB appdata
- old shared Redis appdata
- TitleCardMaker
- Lidarr
- Kometa
- obsolete Docker networks, mounts, and legacy shares

Presence on disk does not prove a service is active.

## lab boundary

Disposable services, VMs, Kubernetes experiments, game servers, and other learning workloads belong in the separate gusuku lab. Fujigoko production services must not depend on them.
