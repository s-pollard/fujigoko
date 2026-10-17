# services

This file records production service placement and dependencies without publishing private addresses, credentials, admin URLs, or other sensitive operational details.

## kawaguchi

### monitoring / infrastructure

- Prometheus — transitional
- Grafana — transitional
- cAdvisor / host monitoring
- Uptime Kuma — permanent independent watchdog
- AdGuard Home — temporary placement only

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

### non-media applications awaiting migration/review

- Paperless-ngx
- Stirling PDF
- Linkwarden
- Mealie
- HomeBox
- Actual Budget
- Homepage
- Endurain

### retirement

- RomM — planned removal
- MariaDB — remove if RomM is its only consumer

Known dependency examples:

```text
sabnzbd -> download storage
sonarr  -> downloads + tv library
radarr  -> downloads + movie library
bazarr  -> tv + movie libraries
plex    -> media library
komga / komf / tachidesk -> manga library
paperless -> document storage + redis
linkwarden -> postgres
endurain -> postgres + redis
```

## motosu

Motosu is now a TrueNAS SCALE host.

Target/permanent service classes:

- Immich server
- Immich PostgreSQL
- Immich Valkey/Redis
- Immich machine learning
- storage/snapshot services provided by TrueNAS
- one AdGuard Home instance

The Immich library has been copied onto the rebuilt TrueNAS system. Final database/application restoration is still being completed and validated, so do not yet describe the Immich migration as finished.

Critical persistence is the Immich library, database recovery data, photo/archive data, and Yamanaka backup datasets. Redis/Valkey state and machine-learning caches are rebuildable.

## yamanaka

Retained non-media applications migrate from Kawaguchi to Yamanaka. Supporting databases/caches stay with the application they serve rather than becoming shared LAN infrastructure.

Target services:

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
- one AdGuard Home instance

Potential additions under evaluation:

- Nextcloud
- Vaultwarden

These remain optional until actually deployed and found useful.

## DNS target

Current:

```text
kawaguchi -> temporary single AdGuard Home
```

Target:

```text
yamanaka -> adguard-home
motosu   -> adguard-home
```

Both instances should provide equivalent filtering policy on separate physical hosts. Exact resolver addresses and synchronization details stay in private operational configuration.

## cleanup candidates

Review before removal:

- TitleCardMaker
- Lidarr
- Kometa
- obsolete appdata, Docker networks, mounts, and legacy shares

Presence on disk does not prove a service is active.

## lab boundary

Disposable services, VMs, Kubernetes experiments, game servers, and other learning workloads belong in the separate gusuku lab. Fujigoko production services must not depend on them.
