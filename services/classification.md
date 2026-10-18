# service classification

Services are classified by function, intended production placement, and persistence value.

```text
kawaguchi = media + manga + host-specific monitoring agent
motosu    = photos + Immich + backup storage + redundant DNS target
yamanaka  = non-media applications + centralized monitoring/logging + DNS
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
- cAdvisor

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
- one AdGuard Home instance as the second DNS node

Motosu is now on TrueNAS SCALE. The Immich library has been copied to the rebuilt system; final application/database restoration is still being validated.

## personal applications — yamanaka

The retained application migration from Kawaguchi is complete at the service level:

| service | status | backup priority |
| --- | --- | --- |
| Paperless-ngx | deployed | high |
| Mealie | deployed | high |
| Actual Budget | deployed | high |
| HomeBox | deployed | high |
| Linkwarden | deployed | high |
| Endurain | deployed | high |
| Stirling PDF | deployed | low |
| Homepage | deployed | medium |

Supporting PostgreSQL/Redis services stay with their parent application and remain private to the relevant Compose network unless external access is actually required.

Old Kawaguchi copies remain stopped only as temporary rollback material until independent backups are verified.

## monitoring / infrastructure

| service | placement | status | backup priority |
| --- | --- | --- | --- |
| Prometheus | yamanaka | deployed | medium |
| Grafana | yamanaka | deployed | medium-high |
| Loki | yamanaka | deployed | low-medium |
| Grafana Alloy | yamanaka | deployed | low |
| Uptime Kuma | yamanaka | deployed | low-medium |
| signal-cli-rest-api | yamanaka | deployed | low |
| cAdvisor/exporters | monitored host | deployed where needed | low |
| AdGuard Home | yamanaka | deployed | medium |
| AdGuard Home | motosu | target | medium |

Prometheus on Yamanaka continues to scrape Kawaguchi cAdvisor. Alloy collects Yamanaka Docker logs into Loki. Uptime Kuma currently runs on Yamanaka rather than on an independent host, so a total Yamanaka outage also removes that monitoring path.

## planned additions

- Nextcloud — Yamanaka; general file sync/collaboration if retained after testing
- Vaultwarden — Yamanaka; security-sensitive service with operational details kept private

Planned does not mean required. Remove ideas that are no longer useful rather than carrying them indefinitely.

## retirement / cleanup

```text
romm    -> stopped; delete after confirming no data needs retention
mariadb -> stopped with romm; delete if no retained dependency exists
```

Also review before cleanup:

- old shared Redis appdata
- stopped Kawaguchi copies of migrated services
- TitleCardMaker
- Lidarr
- Kometa

## migration rule

For each retained service moved from Kawaguchi to Yamanaka:

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

The service cutover and reboot verification are complete. Independent Yamanaka backup coverage remains the gating item before permanent deletion of old Kawaguchi state.
