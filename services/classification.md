# service classification

Services are classified by function, intended production placement, and persistence value.

```text
kawaguchi = media + manga + independent uptime watchdog
motosu    = photos + Immich + backup storage + redundant DNS
yamanaka  = non-media applications + centralized monitoring + redundant DNS
shoji     = reserved / unassigned
```

Experimental infrastructure belongs in gusuku, not Fujigoko.

## media — kawaguchi

Permanent:

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

Manga remains on Kawaguchi. Movie/TV payloads are largely reacquirable; configuration and metadata have higher backup value than the bulk media.

## photos / storage — motosu

Permanent/target:

- Immich server
- Immich PostgreSQL
- Immich Valkey/Redis
- Immich machine learning
- photo/archive storage
- Yamanaka backup datasets
- ZFS snapshots
- selected Backblaze B2 protection
- one AdGuard Home instance

Motosu is now on TrueNAS SCALE. The Immich library has been copied to the rebuilt system; final application/database restoration is still being validated.

## personal applications — kawaguchi to yamanaka

Retained applications migrate to Yamanaka:

| service | status | backup priority |
| --- | --- | --- |
| Paperless-ngx | transitional | high |
| Mealie | transitional | high |
| Actual Budget | transitional | high |
| HomeBox | transitional | high |
| Linkwarden | transitional | high |
| Endurain | transitional | high |
| Stirling PDF | transitional | low |
| Homepage | transitional | medium |

Supporting PostgreSQL/Redis services move with their parent application and remain private to the relevant Compose network unless external access is actually required.

## monitoring / infrastructure

| service | target | status | backup priority |
| --- | --- | --- | --- |
| Prometheus | yamanaka | transitional | medium |
| Grafana | yamanaka | transitional | medium-high |
| Loki | yamanaka | planned | low-medium |
| Uptime Kuma | kawaguchi | permanent watchdog | low-medium |
| cAdvisor/exporters | monitored host | permanent agents | low |
| AdGuard Home | yamanaka + motosu | planned redundant pair | medium |

Uptime Kuma remains outside Yamanaka so a Yamanaka failure does not remove every monitoring path.

## planned additions

- Nextcloud — Yamanaka; general file sync/collaboration if retained after testing
- Vaultwarden — Yamanaka; security-sensitive service with operational details kept private

Planned does not mean required. Remove ideas that are no longer useful rather than carrying them indefinitely.

## planned removal / review

```text
romm    -> delete
mariadb -> delete if romm is its only consumer
```

Review before cleanup:

- TitleCardMaker
- Lidarr
- Kometa

## migration rule

For each retained service moving from Kawaguchi to Yamanaka:

```text
1. identify persistence and dependencies
2. create an independent backup/export
3. deploy on yamanaka
4. restore/copy persistence
5. verify application behavior
6. verify dependencies
7. establish backup to motosu
8. observe with the kawaguchi copy stopped but intact
9. remove the old copy only after successful cutover
```
