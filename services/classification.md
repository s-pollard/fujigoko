# service classification

Services are classified by function, intended production placement, and persistence value.

```text
kawaguchi = media + manga + host-specific monitoring agent
motosu    = photos + Immich + backup storage + redundant DNS target
yamanaka  = non-media applications + centralized monitoring/logging + DNS + private application access
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
- smartctl-exporter

Manga remains on Kawaguchi. Movie/TV payloads are largely reacquirable; configuration and metadata have higher backup value than the bulk media.

Kawaguchi migration cleanup is complete. Retired non-media containers, unused Docker images/volumes, and obsolete appdata have been removed.

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

Motosu is now on TrueNAS SCALE. Immich application/database restoration is complete and validated.

## personal applications — yamanaka

The retained application migration from Kawaguchi is complete:

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
| SearXNG | deployed | low |
| FreshRSS | deployed | medium |

Supporting PostgreSQL/Redis services stay with their parent application and remain private to the relevant Compose network unless external access is actually required.

## monitoring / infrastructure

| service | placement | status | backup priority |
| --- | --- | --- | --- |
| Prometheus | yamanaka | deployed | medium |
| Grafana | yamanaka | deployed | medium-high |
| Loki | yamanaka | deployed | low-medium |
| Grafana Alloy | yamanaka | deployed | low |
| Uptime Kuma | yamanaka | deployed | low-medium |
| signal-cli-rest-api | yamanaka | deployed | low |
| Dockhand | yamanaka | deployed | low-medium |
| Caddy | yamanaka | deployed | medium |
| Pocket ID | yamanaka | deployed | high |
| cAdvisor/exporters | monitored host | deployed where needed | low |
| smartctl-exporter | kawaguchi | deployed | low |
| AdGuard Home | yamanaka | deployed | medium |
| AdGuard Home | motosu | target | medium |

Prometheus on Yamanaka continues to scrape Kawaguchi cAdvisor and smartctl-exporter. Alloy collects Yamanaka Docker logs into Loki. Uptime Kuma remains on Yamanaka rather than on an independent host, so a total Yamanaka outage also removes that monitoring path.

Caddy, AdGuard Home, and Pocket ID now form the private application-access layer on Yamanaka. Private HTTPS is intended for trusted LAN and Tailscale clients. Pocket ID OIDC has been verified with FreshRSS, Actual Budget, Mealie, Linkwarden, Grafana, Stirling PDF, and Paperless-ngx. Exact hostnames, client IDs, secrets, callback URLs, and other operational identity-provider configuration do not belong in this public repository.

## planned additions

- Grocy — Yamanaka; household food inventory, expiration, quantity, and barcode tracking alongside Mealie
- TriliumNext — Yamanaka; structured personal notes, backlinks, and synchronized/offline-capable note access
- Nextcloud — Yamanaka; general file sync/collaboration if retained after testing
- Vaultwarden — Yamanaka; security-sensitive service with operational details kept private

Planned does not mean required. Remove ideas that are no longer useful rather than carrying them indefinitely.

## retired / removed

The following Kawaguchi services or appdata have been retired and removed:

- RomM
- MariaDB used by RomM
- old shared Redis state
- stopped copies of migrated non-media services
- TitleCardMaker
- Lidarr
- Kometa
- Listenarr

Presence in old notes or backups should not be interpreted as active production placement.

## migration rule

Preferred procedure for future migrations:

```text
1. identify persistence and dependencies
2. create an independent backup/export
3. deploy on the destination host
4. restore/copy persistence
5. verify application behavior
6. verify dependencies
7. establish independent backup coverage
8. observe with the previous copy stopped but intact when practical
9. remove the old copy after successful cutover
```

The Yamanaka service cutover, reboot verification, and Kawaguchi cleanup are complete. Independent Yamanaka-to-Motosu backup coverage was deferred because no new valuable production data had yet been added after migration; establishing that backup is now a high-priority operational follow-up.
