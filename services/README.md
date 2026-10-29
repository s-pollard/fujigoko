# services

Production service placement, purpose, dependencies, and authentication. Hardware is in [hosts](../hosts/README.md), data paths in [storage](../storage/README.md), and protected scope in [backups](../backups/README.md).

## kawaguchi

All services below are deployed. The non-media migration and retired services are recorded in [migration history](../history/yamanaka-migration-2026.md#retired-from-kawaguchi).

| Service | Purpose | Major dependency / data |
| --- | --- | --- |
| Plex | Media library | Media storage |
| Navidrome | Music streaming; Last.fm integration configured | Read-only music library; writable application database/settings; Symfonium Android client |
| Sonarr | TV automation | Downloads + TV library |
| Radarr | Movie automation | Downloads + movie library |
| SABnzbd | Downloads | Download storage |
| Bazarr | Media support | TV + movie libraries |
| Seerr, Tautulli, Recyclarr, Unpackerr | Media stack support | Further dependencies not recorded here |
| Komga, Komf, Tachidesk | Manga services | Manga library |
| cAdvisor | Host/container metrics | Scraped by Prometheus on Yamanaka |
| smartctl-exporter | SMART device metrics | Local block-device access; scraped by Prometheus on Yamanaka |

The smartctl exporter requires privileged mode and an explicit root runtime user. Its configuration, 2026-10-21 restoration evidence, and device-access troubleshooting are in the [smartctl runbook](../runbooks/smartctl-exporter.md).

### navidrome

Deployed on 2026-10-29 using the Unraid container template. Music is mounted read-only from `/mnt/user/media/music` to `/music`; application state is writable at `/mnt/user/appdata/navidrome`, mounted as `/data`. Local playback and private Caddy HTTPS access were verified. Last.fm API configuration and user authorization were completed; successful scrobble delivery has not yet been explicitly recorded. Track titles follow embedded metadata, which can differ from filenames.

### media dependencies

```text
internet
   |
sabnzbd
   |
download storage
   |
   +--> sonarr --> tv ------+
   |                        |
   +--> radarr --> movies --+--> plex
   |
   `--> unpackerr
```

[Storage paths](../storage/README.md#kawaguchi) and [recovery checks](../runbooks/kawaguchi-recovery.md#media-flow-verification) cover acquisition/import verification. Plex/Jellyfin artwork synchronization is configured.

## motosu

| Service / function | State | Purpose / major dependency |
| --- | --- | --- |
| Immich server | Deployed; restoration validated | Photo library, PostgreSQL, Valkey/Redis, machine learning |
| Immich PostgreSQL | Deployed | Photo-library database; logical/application recovery data is critical |
| Immich Valkey/Redis | Deployed | Application dependency; state is rebuildable |
| Immich machine learning | Deployed | Application dependency; model cache is rebuildable |
| TrueNAS storage/snapshots | Deployed | Photo/archive data and Yamanaka backup datasets |
| TrueNAS Cloud Sync | Immich and Yamanaka sync coverage confirmed; photo upload completed | Separate B2 buckets; see [scope and verification limits](../backups/README.md#off-site-copies) |
| AdGuard Home | Target, after relocation | Second DNS node; not deployed |

The restored Immich library is operating normally. See [Motosu history](../history/motosu-storage-2026.md) for the migration and mirror incident.

## yamanaka

Yamanaka hosts production non-media applications and their application-local database/cache dependencies. The stack has been reboot-tested with expected production containers returning automatically.

### applications

All listed applications are deployed. — means no supporting dependency is recorded here.

| Service | Purpose | Recorded supporting dependency |
| --- | --- | --- |
| Paperless-ngx | Documents and metadata | Private Redis |
| Mealie | Personal application | — |
| Actual Budget | Budget data | — |
| HomeBox | Inventory | — |
| Linkwarden | Saved links and archive data | PostgreSQL |
| Stirling PDF | PDF utilities | — |
| Endurain | Activities and history | PostgreSQL + Redis |
| Homepage | Convenience dashboard | — |
| SearXNG | Search | — |
| FreshRSS | Personal feed service | — |
| Grocy | Pantry/fridge/freezer inventory, quantities, expirations, barcodes | — |
| TriliumNext | Structured personal notes/wiki | — |
| Vaultwarden | Bitwarden-compatible password vault | SQLite |
| Kept | Locations, boxes, items, labels, moving workflows | PostgreSQL |

HomeBox remains deployed during Kept evaluation/import; it has not been retired.

### monitoring and infrastructure

All services below are deployed on Yamanaka.

| Service | Purpose / major dependency |
| --- | --- |
| Prometheus | Scrapes Kawaguchi cAdvisor and smartctl-exporter |
| Grafana | Monitoring/log exploration; Prometheus and Loki |
| Loki | Yamanaka Docker logs collected by Alloy |
| Grafana Alloy | Collects Yamanaka Docker logs into Loki |
| Uptime Kuma | Uptime monitoring; Signal notification bridge |
| signal-cli-rest-api | Uptime Kuma notifications and local Signal path for backup-failure alerts |
| AdGuard Home | Current DNS resolver and private application DNS |
| Caddy | Private HTTPS entry point across Yamanaka, Kawaguchi, and Motosu |
| Pocket ID | OIDC/passkey identity provider |
| Dockhand | Docker operations/management |

The accepted Uptime Kuma host dependency is documented in [architecture](../architecture/README.md#accepted-dependencies). Current/target DNS and ingress behavior are in [network](../network/README.md#dns).

## private application access

User-facing services across all three active hosts are reached through Caddy on Yamanaka. Kawaguchi application access and the Immich route have been verified from trusted clients.

| Private route destination | Host |
| --- | --- |
| Unraid management UI | Kawaguchi |
| TrueNAS management UI | Motosu |

See [network access policy](../network/README.md#private-application-access) for DNS, certificates, and the trusted LAN/Tailscale boundary. The application namespace and its DNS names remain private under [SECURITY.md](../SECURITY.md).

## authentication

Verified Pocket ID/OIDC integrations:

- FreshRSS
- Actual Budget
- Mealie
- Linkwarden
- Grafana
- Stirling PDF
- Paperless-ngx
- TriliumNext
- Kept

Navidrome currently uses application-local authentication for browser and Subsonic/OpenSubsonic clients. Pocket ID integration is not deployed; external authentication would require an authentication proxy and explicit client API handling.

Grocy retains application-local authentication rather than adding a separate authentication proxy solely for SSO.

Vaultwarden retains normal vault authentication and hardware-backed second-factor authentication. Pocket ID SSO was evaluated but is not enabled because the current identity claim reports email as unverified. The vault's email-verification requirement is intentionally not weakened. Secrets and recovery material remain private.

General authentication invariants are in [architecture](../architecture/README.md#private-access); client IDs, callback secrets, credentials, and recovery configuration follow [SECURITY.md](../SECURITY.md).

## deferred applications

| Application | Proposed host | State / reason |
| --- | --- | --- |
| Nextcloud | Yamanaka | Evaluated and deferred: no current file-sync/collaboration need |

Deferred does not mean rejected or required. Reconsider only when a concrete requirement appears. See [classification](classification.md) for lifecycle decisions and [service deployment](../runbooks/service-deployment.md) for future changes.
