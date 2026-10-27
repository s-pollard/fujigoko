# backups

Backup effort follows data value and rebuild cost rather than raw storage size.

## protection summary

| Source / data | Destination / protection | Recorded state and limit |
| --- | --- | --- |
| Motosu photos | Local ZFS snapshots | Deployed; same-host protection, not an independent backup |
| Motosu backup datasets | Local ZFS snapshots | Deployed; same-host protection |
| Selected Motosu high-value data | Encrypted TrueNAS Cloud Sync to Backblaze B2 | Configured; photo upload completed; representative B2 restore deferred |
| Yamanaka application-aware staged tree | Encrypted Restic repository on Motosu | Deployed and byte-for-byte restore-verified on 2026-10-26/27 |
| Motosu Yamanaka repository | Intended B2 Cloud Sync path | Confirm selection/completion and off-site recovery during the move; local verification does not prove this copy |
| Kawaguchi media automation | Rebuild/reconstruct | Full independent Arr-stack backup intentionally not required |
| Personal workstations | See [workstation scope](#workstations) | Aso photography to Motosu; no whole-PC protection established |

Schedules and retention are in the [schedule table](#deployed-schedule-and-retention).

## policy

A backup is independent only if loss of the source host or its primary storage does not also destroy the backup.

Application-generated backups stored only on the source host are useful restore points but are not sufficient host-failure protection.

Never commit credentials, repository passwords, API keys, cloud bucket names, account identifiers, encryption passwords/salts, or other backup secrets to this public repository.

## motosu

Motosu is on TrueNAS SCALE and remains the highest-priority backup/storage host.

Current verified protection includes:

- mirrored ZFS storage for single-drive fault tolerance
- daily ZFS snapshots for photos and backups; retention is in the [schedule table](#deployed-schedule-and-retention)
- restored and validated Immich application/database/library
- Backblaze B2 off-site backup configured through TrueNAS Cloud Sync
- B2 transfer uses encrypted backup content and private credentials kept outside this public repository
- the current B2 photo upload has completed
- a dedicated Yamanaka Restic repository is stored on Motosu and included in the intended B2 off-site path
- TrueNAS email alerting is configured and tested so Cloud Sync failures do not depend on Yamanaka being available

Migration recovery material and the temporary mirror replacement are documented in [Motosu history](../history/motosu-storage-2026.md).

### protection model

```text
single-drive failure
-> mirrored ZFS storage

accidental deletion / unwanted changes
-> ZFS snapshots / Restic snapshot history

host loss / theft / disaster
-> encrypted Backblaze B2 copy
```

The ZFS mirror is fault tolerance, not an independent backup.

Selected high-value Motosu data should include the Immich/photo library, photo archives, and Yamanaka backup datasets.

### motosu follow-up

- perform and document a representative restore from the encrypted B2 copy during the move
- replace the current mirror drives when a suitable deal is available; the present mirror is healthy and replacement is not urgent
- after any drive replacement, verify resilver, SMART, scrub, and alert state

The target second AdGuard Home instance has medium-priority configuration; it is not deployed. The accepted monitoring dependency is documented in [architecture](../architecture/README.md#accepted-dependencies).

## kawaguchi

Kawaguchi is comparatively rebuildable, and its media automation state is intentionally treated as disposable/reconstructable.

No full independent backup of the Arr stack or other routine media automation state is required. If Kawaguchi or its Unraid installation fails catastrophically, the intended response is to rebuild or migrate the media services rather than preserve the existing Unraid installation exactly.

Movies, TV, downloads, caches, and associated automation state are therefore outside the high-value backup scope unless that policy changes later.

Recorded recovery priorities: Unraid/retained application configuration and metadata are medium priority; cAdvisor/exporters and smartctl-exporter are low priority. These rankings do not establish an independent backup or override the rebuild policy.

## yamanaka

Yamanaka is the production application host. Important live application data remains local for normal operation, with independent recovery copies stored on Motosu in a dedicated Restic repository.

The deployed backup flow is:

```text
application-aware exports/dumps on Yamanaka
-> staged backup tree
-> Restic repository on Motosu over SSH/SFTP
-> Motosu local protection
-> scheduled TrueNAS Cloud Sync to Backblaze B2
```

The Restic repository is encrypted with recovery material kept outside this public repository. Yamanaka uses a dedicated restricted account/key for the Motosu repository rather than general administrative access.

### service priorities

Recorded recovery priorities and protected material. Service placement and lifecycle are maintained in [services](../services/README.md).

| Service / state | Protected material | Priority |
| --- | --- | --- |
| Paperless-ngx | Documents/metadata via application exporter | High |
| Actual Budget | Persistent budget data | High |
| HomeBox | Inventory state | High |
| Mealie | Persistent data | High |
| Linkwarden | PostgreSQL custom-format dump + application/archive data | High |
| Endurain | PostgreSQL custom-format dump + backend/application data | High |
| Grocy | Persistent configuration/data; consistent-copy workflow | High |
| TriliumNext | Persistent data; consistent-copy workflow | High |
| Vaultwarden | SQLite online backup, validated before staging; signing key and other required persistent state | Critical |
| Kept | PostgreSQL custom-format dump + persistent data and recovery-critical configuration volumes | High |
| Pocket ID | Identity state and private deployment configuration | High |
| FreshRSS | Persistent state | Medium |
| Grafana | State, configuration, dashboards | Medium-high |
| Uptime Kuma | Persistent state | Low-medium |
| Dockhand | Persistent state | Low-medium |
| AdGuard Home | Configuration | Medium |
| Homepage | Configuration | Medium |
| SearXNG | Configuration | Low |
| Stirling PDF | Configuration | Low |
| Prometheus | Configuration, not historical metrics | Medium |
| Loki | Configuration, not historical logs | Low-medium |
| Grafana Alloy | Configuration | Low |
| Caddy | Configuration | Medium |
| signal-cli-rest-api | Signal-cli state | Low |
| Compose / private deployment configuration | Definitions, environment/configuration required for recovery | Not separately ranked |

Nextcloud is deferred; backup priority is not applicable. Kawaguchi's configuration/metadata can have greater recovery value than bulk media, but its [rebuild policy](#kawaguchi) does not require a full independent media-automation backup. Independent flash/config and manga backup availability is [not established by these docs](../history/documentation-review-2026-10-27.md#review-needed).

Redis/Valkey cache data, Docker images, Docker sockets, raw live PostgreSQL database directories, disposable restore-test trees, Prometheus historical metrics, and Loki historical logs are intentionally excluded where recovery value does not justify them.

Database-backed services use database-native dumps, SQLite-aware snapshots, or application-aware exports rather than copying live database directories blindly.

### deployed schedule and retention

Yamanaka runs the production backup through a root-owned backup script and systemd timer.

| Job / dataset | Schedule | Retention / behavior |
| --- | --- | --- |
| Yamanaka Restic backup | Nightly around 03:00 local time, small randomized delay | 14 daily, 8 weekly, 6 monthly snapshots; repository check after backup/retention processing |
| Yamanaka restore verification | Sunday around 05:00 local time, small randomized delay | Latest production snapshot restored to an isolated path; SHA-256 manifest, recursive 1:1 source comparison, restored database archive validation |
| Motosu photo snapshots | Daily | 30 days |
| Motosu backup snapshots | Daily | 14 days |
| Motosu B2 Cloud Sync | After the nightly local backup window | Separate cloud-sync step; exact time and remote retention not recorded here |

Failures of the Yamanaka backup and verification services trigger Signal alerts through the local Signal service. TrueNAS alerting independently sends email for Motosu-side/Cloud Sync failures.

Exact addresses, phone numbers, credentials, repository passwords, bucket identifiers, and cloud-account details remain private.

### verified Yamanaka-to-Motosu recovery path

The production backup path was exercised end to end on 2026-10-26 and re-verified after adding Grocy, TriliumNext, Vaultwarden, and Kept on 2026-10-27.

Verified:

- application-aware backup generation completed successfully
- Paperless exported 12 documents; the staged/restored Paperless export contained the expected export artifacts
- Linkwarden PostgreSQL custom-format dump is readable by `pg_restore`
- Endurain PostgreSQL custom-format dump is readable by `pg_restore`
- Grocy state is captured through a consistent-copy workflow
- TriliumNext state is captured through a consistent-copy workflow
- Vaultwarden's SQLite database is backed up with SQLite's online `.backup` mechanism and the resulting database passes `PRAGMA integrity_check`
- Kept PostgreSQL is captured in native custom dump format and validated with `pg_restore`; Kept's persistent data and configuration volumes are included in the staged tree
- an isolated Vaultwarden restore test successfully launched the application from the backed-up database and signing key before production backup integration
- Restic stored the expanded production staged backup on Motosu successfully
- the latest verified production snapshot contained 5,345 files and about 988 MiB of logical backup data
- Restic repository checking reported no errors
- the latest snapshot was restored from Motosu to an isolated temporary path
- source and restored trees each contained 5,345 files
- recursive 1:1 comparison reported no differences
- the restored SHA-256 manifest validated successfully
- the restored Linkwarden, Endurain, and Kept dumps passed archive validation
- automated verification completed successfully

This proves that the current staged production backup, including Grocy, TriliumNext, Vaultwarden, and Kept, can be transferred to Motosu by Restic and restored byte-for-byte from the Motosu repository. It does not eliminate the need for periodic application-level restore testing as applications or backup formats change.

### Vaultwarden restore validation

Vaultwarden received an additional application-level restore test before being treated as a production password store.

Verified:

- a SQLite online backup was created from the live database
- the backup passed `PRAGMA integrity_check`
- expected Vaultwarden schema tables were present
- the backed-up database and signing key were copied into an isolated temporary data directory
- a separate Vaultwarden container launched successfully from that restored data on a temporary port
- the disposable restore container and temporary restore tree were removed afterward

Vaultwarden credentials, master-password material, recovery codes, OIDC secrets, and other sensitive authentication material are never committed to this repository.

### Paperless restore validation

An application export was restored and tested on Yamanaka in an isolated environment using the pinned Paperless-ngx 3.3.3 image. This validates recovery of this export as well as the later byte-for-byte Restic recovery of the staged export from Motosu.

Verified:

- all 12 documents restored; downloaded originals match export and database SHA-256 checksums
- normal container startup with a separate Redis instance, healthy database/Celery/index, and no unapplied migrations
- search index contains exactly the restored document IDs; content searches and a negative query work
- previews, thumbnails, password authentication, and browser document-list/detail/PDF rendering
- data, search, authentication, and download checks survive a container stop/start and Redis restart
- test containers had no host port bindings; external network and production Paperless/Redis access were blocked
- manual sanity check reported no issues
- temporary containers, networks, credentials, and sessions were removed; production and the source export were unchanged

No archive versions exist in this export; only originals and thumbnails are expected. Classifier/sanity-status warnings reflected missing task history, not damaged data. Classifier training, new-document consumption/OCR, archive generation, larger datasets, and full clean-host recovery remain untested. Browser password entry and the Download button were not exercised directly; password login and downloads were verified separately over HTTP.

The export contains user password hashes and must be stored privately. Compose configuration, environment values, and the application secret key are protected separately in the private backup set.

## workstations

Aso's photography images are backed up to Motosu. A whole-workstation backup is not established in this inventory.

Ontake, Norikura, and Azuma are not backed up. An old or accessible Time Machine backup detected on Azuma does not represent an active backup arrangement. Workstation hardware and access limitations are in [workstations](../hosts/workstations.md).

## backup classes

| class | examples | expectation |
| --- | --- | --- |
| irreplaceable | photos, documents, budgets, personal databases, password-vault state | independent backup; off-site preferred |
| important configuration | application config, Compose files, DNS config | independent backup when recovery value justifies it |
| convenient | dashboards, metrics history, media automation state | back up only if recovery value justifies it |
| replaceable | Usenet media, downloads, caches | recreate instead of backing up |

## verification

Periodically:

1. confirm recent successful backup jobs
2. confirm new snapshots/archives were actually created
3. confirm credentials and encryption material needed for recovery remain available in the private credential store
4. perform representative restores
5. update host-specific recovery runbooks with verified procedures

## deferred / remaining work

- representative recovery from the B2 off-site copy is intentionally deferred until the move
- GFX archive backup policy is intentionally deferred until the move
- Motosu drive replacement is waiting for a suitable deal on two HDDs; the current mirror is healthy

Backup-failure alerting is deployed and tested on both Yamanaka and Motosu. See the [move checklist](../runbooks/move-checklist.md) for execution order and the [documentation review](../history/documentation-review-2026-10-27.md#review-needed) for unresolved off-site scope and follow-up wording.
