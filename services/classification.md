# service classification

Services are classified by function, current placement, intended placement, and persistence value.

```text
kawaguchi = media + independent uptime watchdog
motosu    = photos + backup storage + redundant DNS
yamanaka  = non-media applications + centralized monitoring
saiko     = Proxmox lab / experimentation
shoji     = reserved / role undecided
```

Yamanaka does not host game servers. Saiko does not host required production services.

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

Manga remains on Kawaguchi. Movie/TV payloads are largely reacquirable; configuration and metadata have higher backup value than the bulk media itself.

## photos / storage — motosu

Permanent:

- Immich server
- Immich PostgreSQL
- Immich Valkey/Redis
- Immich machine learning
- Tailscale
- one AdGuard Home instance

Motosu also becomes the independent local backup target for important Yamanaka exports, database dumps, files, and configuration.

High-value persistence includes the Immich library, database backups, photo archive, and selected Yamanaka recovery data. Redis/Valkey state and ML caches are rebuildable.

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

Supporting PostgreSQL/Redis services move with their parent applications and remain private to the relevant Compose network unless an external client actually requires access.

## monitoring / infrastructure

| service | target | status | backup priority |
| --- | --- | --- | --- |
| Prometheus | yamanaka | transitional | medium |
| Grafana | yamanaka | transitional | medium-high |
| Loki | yamanaka | planned | low-medium |
| Uptime Kuma | kawaguchi | permanent watchdog | low-medium |
| cAdvisor | monitored host | permanent agent | low |
| AdGuard Home | yamanaka + motosu | planned redundant pair | medium |

Uptime Kuma remains outside Yamanaka so a Yamanaka failure does not remove every monitoring path.

Exact resolver addresses, scrape addresses, internal ports, management URLs, and credentials are private operational details and are intentionally excluded from this public repository.

## planned additions

- Nextcloud — Yamanaka; general file sync/collaboration
- Vaultwarden — Yamanaka; security-sensitive service, with operational details kept private

## planned removal / review

```text
romm    -> delete
mariadb -> delete if romm is its only consumer
```

Review before cleanup:

- TitleCardMaker
- Lidarr
- Kometa

## lab / experimentation

Saiko is the former Bandai machine and becomes the Proxmox lab host.

Expected experiments include:

- OPNsense VMs
- Linux VMs
- Kubernetes/k3s
- networking labs
- temporary game servers/services
- GPU passthrough

Kubernetes is an experiment, not a production migration plan. Shoji remains unassigned.

## maybe / under consideration

- Grafana Alloy
- Scrutiny
- Dozzle
- OpenSpeedTest
- NUT / PeaNUT
- Rackula
- Paperless AI / Paperless-GPT
- container update notifier

## migration rule

For each service moving from Kawaguchi to Yamanaka:

```text
1. identify persistent data and dependencies
2. back up application/database state
3. deploy on yamanaka
4. restore/copy persistence
5. verify behavior
6. verify dependencies
7. establish independent backup to motosu
8. leave the kawaguchi copy intact during observation
9. remove the old copy only after successful cutover
```
