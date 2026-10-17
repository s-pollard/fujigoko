# services

This file records service placement and dependencies without publishing private addresses, credentials, admin URLs, or other sensitive operational details.

## kawaguchi

### monitoring / infrastructure

- Prometheus
- Grafana
- cAdvisor
- Uptime Kuma
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

### manga / games

- Komga
- Komf
- Tachidesk
- RomM — planned retirement

### documents / utilities / personal

- Paperless-ngx
- Stirling PDF
- Linkwarden
- Mealie
- HomeBox
- Actual Budget
- Homepage

### fitness

- Endurain

### supporting services

- PostgreSQL for Linkwarden
- MariaDB for RomM
- Redis for Paperless
- PostgreSQL + Redis for Endurain

## verified kawaguchi dependencies

```text
sabnzbd -> download storage
sonarr  -> downloads + tv library
radarr  -> downloads + movie library
unpackerr -> completed downloads
bazarr  -> tv + movie libraries
plex    -> media library
komga / komf / tachidesk -> manga library
paperless -> document storage + redis
linkwarden -> postgres
romm -> mariadb
endurain -> postgres + redis
```

The exact internal ports, IPs, Docker network addresses, and management URLs are intentionally not published here.

## motosu

### Immich stack

- Immich server
- Immich PostgreSQL
- Immich Valkey/Redis
- Immich machine learning
- Tailscale

Critical persistence is the Immich library and PostgreSQL state. Redis/Valkey state and the machine-learning model cache are rebuildable.

Motosu is planned to move from UGOS to TrueNAS SCALE while keeping Immich and off-site recovery intact.

## yamanaka target

Retained non-media applications migrate from Kawaguchi to Yamanaka. Supporting databases/caches stay with the application they serve rather than becoming shared LAN infrastructure.

Planned/target services include:

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
- Nextcloud
- Vaultwarden

### Nextcloud

Nextcloud is the selected self-hosted general file-sync/collaboration platform. Live application state remains on Yamanaka; important files and recovery data are backed up independently to Motosu.

Immich remains the photo system and is not replaced by Nextcloud.

### Vaultwarden

Vaultwarden is planned as a security-sensitive service. This public repository records only that it is planned for Yamanaka and requires independent backup. Vault contents, synchronization design, account details, recovery material, administrative URLs, and other operational security details are deliberately kept out of the public repo.

## DNS target

The current single AdGuard Home instance on Kawaguchi is temporary.

Target placement:

```text
yamanaka -> adguard-home
motosu   -> adguard-home
```

Both instances should provide equivalent filtering policy so loss or maintenance of one host does not remove LAN DNS. Exact resolver addresses and synchronization details are private operational configuration.

## retirement / review

Current decisions:

```text
romm    -> delete
mariadb -> delete if romm is its only consumer
```

Existing appdata candidates to review before cleanup:

- TitleCardMaker
- Lidarr
- Kometa

Presence on disk does not prove an application is still active.
