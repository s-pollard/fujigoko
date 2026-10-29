# backups

Backup effort follows data value and rebuild cost rather than raw storage size.

## protection summary

| Source / data | Destination / protection | Recorded state and limit |
| --- | --- | --- |
| Motosu photos | Local ZFS snapshots | Deployed; same-host protection, not an independent backup |
| Motosu backup datasets | Local ZFS snapshots | Deployed; same-host protection |
| Immich/photo data on Motosu | Encrypted TrueNAS Cloud Sync to a dedicated B2 bucket | Sync coverage confirmed; photo upload completed; representative B2 restore deferred |
| Yamanaka application-aware staged tree | Encrypted Restic repository on Motosu | Deployed and byte-for-byte restore-verified on 2026-10-26/27 |
| Yamanaka Restic repository on Motosu | TrueNAS Cloud Sync to a separate dedicated B2 bucket | Sync coverage confirmed; latest upload completion and off-site recovery still need verification |
| Kawaguchi selected Unraid/appdata state | Encrypted Restic repository on Motosu | Deployed and restore-verified on 2026-10-28/29; bulk media and manga intentionally excluded |
| Kawaguchi Restic repository on Motosu | TrueNAS Cloud Sync to a dedicated B2 target | Configured; representative off-site recovery still needs verification |
| Personal workstations | See [workstation scope](#workstations) | Aso photography to Motosu; no whole-PC protection established |

Schedules and retention are in the [schedule table](#deployed-schedule-and-retention).

## policy

A backup is independent only if loss of the source host or its primary storage does not also destroy the backup.

Application-generated backups stored only on the source host are useful restore points but are not sufficient host-failure protection.

Never commit credentials, repository passwords, API keys, cloud bucket names, account identifiers, encryption passwords/salts, or other backup secrets to this public repository.

## motosu

Motosu is on TrueNAS SCALE and remains the highest-priority backup/storage host.

Current protection and recorded verification:

- mirrored ZFS storage for single-drive fault tolerance
- daily ZFS snapshots for photos and backups; retention is in the [schedule table](#deployed-schedule-and-retention)
- restored and validated Immich application/database/library
- Backblaze B2 off-site backup configured through TrueNAS Cloud Sync
- B2 transfer uses encrypted backup content and private credentials kept outside this public repository
- the current B2 photo upload has completed
- the Yamanaka Restic repository on Motosu syncs to its own B2 bucket, separate from the Immich bucket
- the Kawaguchi Restic repository on Motosu has its own Cloud Sync target, separate from Yamanaka and Immich
- TrueNAS email alerting is configured and tested so Cloud Sync failures do not depend on Yamanaka being available

Migration recovery material and the temporary mirror replacement are documented in [Motosu history](../history/motosu-storage-2026.md).

### off-site copies

The protected sets sync from Motosu through TrueNAS Cloud Sync using separate B2 targets:

| Source on Motosu | Destination |
| --- | --- |
| Immich/photo data | Dedicated Immich bucket |
| Yamanaka Restic repository | Dedicated Yamanaka bucket |
| Kawaguchi Restic repository | Dedicated Kawaguchi target |

Bucket identifiers and credentials remain private. The latest Yamanaka upload completion is not recorded, the Kawaguchi Cloud Sync path is configured but representative B2 recovery is not yet recorded, and representative off-site recovery remains a move-time test. The earlier completed photo upload and local Restic restores do not establish off-site recovery for the Restic repositories.

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

Off-site scope includes Immich/photo data, Yamanaka backups, and the Kawaguchi Restic repository. The GFX archive's final location and protection policy remain deferred until the move.

### motosu follow-up

- perform and document a representative restore from the encrypted B2 copy during the move
- consider drive upgrades when a suitable deal appears; the [current mirror is deployed and healthy](../storage/README.md#motosu)
- after any drive replacement, verify resilver, SMART, scrub, and alert state

The target second AdGuard Home instance has medium-priority configuration; it is not deployed. The accepted monitoring dependency is documented in [architecture](../architecture/README.md#accepted-dependencies).

## kawaguchi

Kawaguchi remains comparatively rebuildable. Bulk media, downloads, caches, generated media metadata, and manga are intentionally outside independent backup scope; the goal is fast host/service recovery rather than preserving the entire media server byte-for-byte.

The deployed backup flow is:

```text
selected Unraid configuration and application state on Kawaguchi
-> staged backup tree
-> encrypted Restic repository on a dedicated Motosu ZFS dataset over SSH/SFTP via Tailscale
-> Motosu local snapshots
-> scheduled TrueNAS Cloud Sync to Backblaze B2
```

Kawaguchi uses a dedicated restricted Restic account/key on Motosu and a repository password kept outside the public repository. Restic is installed persistently from the Unraid flash configuration into the runtime filesystem at array startup. Backup and verification are run through Unraid User Scripts.

### protected scope

Protected material is deliberately selective:

- Unraid `/boot/config`, excluding the private Restic credential/key directory
- Radarr, Sonarr, Prowlarr, SABnzbd, Bazarr, Seerr, Tautulli, Komga, Komf, Tachidesk, Unpackerr, and Recyclarr application state
- Navidrome application state, captured with the container stopped and restarted only if it was running
- Plex database/application state under `Plug-in Support` plus small top-level configuration files
- Jellyfin configuration, core data/database state, plugins, users, and ASP.NET key state

Intentionally excluded:

- movies, TV, music, manga, and downloads
- Plex transcodes, cache, generated media, generated metadata, and drivers
- Jellyfin cache, generated metadata, transcodes, and logs
- cAdvisor and smartctl-exporter persistent state
- Restic repository password and private SSH key from the staged flash copy

The retained application state is backed up to reduce rebuild time even though the underlying media automation stack remains reconstructable.

### verified Kawaguchi-to-Motosu recovery path

The first production backup and restore verification completed successfully on 2026-10-28.

Verified:

- selected configuration/appdata was staged successfully with stateful containers stopped briefly for consistent copies
- the encrypted Restic repository was initialized on a dedicated Motosu ZFS dataset
- transport works through the dedicated restricted SFTP account over Tailscale
- the first production snapshot represented about 10.097 GiB of logical backup data
- Restic repository checking reported no errors
- the latest production snapshot restored successfully to an isolated temporary path
- source and restored trees each contained 17,946 regular files
- the restored SHA-256 manifest validated successfully
- symlink definitions matched without following transient KCEF/Chromium runtime targets
- restore verification was repeated successfully after reboot, confirming Restic runtime persistence and recovery access

The restore verifier intentionally validates regular-file counts, the captured SHA-256 manifest, and symlink definitions instead of recursively following live symlink targets. Tachidesk/KCEF creates transient Chromium-style symlinks whose targets may not exist after the application restarts; following those links produced false verification failures even though the Restic snapshot itself was intact.

Navidrome was added to the production backup on 2026-10-29. The expanded snapshot contained 22,983 regular files and 10.585 GiB of logical data. Repository checking reported no errors; restoration to an isolated temporary path reproduced all 22,983 files, the SHA-256 manifest passed, and symlink definitions matched. This verifies recovery of the staged files; launching Navidrome from restored state has not been tested. Music files remain excluded.

### deployed schedule and retention

Kawaguchi uses Unraid User Scripts; Yamanaka uses systemd timers.

| Job / dataset | Schedule | Retention / behavior |
| --- | --- | --- |
| Yamanaka Restic backup | Nightly around 03:00 local time, small randomized delay | 14 daily, 8 weekly, 6 monthly snapshots; repository check after backup/retention processing |
| Yamanaka restore verification | Sunday around 05:00 local time, small randomized delay | Latest production snapshot restored to an isolated path; SHA-256 manifest, recursive 1:1 source comparison, restored database archive validation |
| Kawaguchi Restic backup | Nightly through Unraid User Scripts, after the Yamanaka backup window | 14 daily, 8 weekly, 6 monthly snapshots; repository check after backup/retention processing |
| Kawaguchi restore verification | Weekly through Unraid User Scripts | Latest production snapshot restored to an isolated path; regular-file count, SHA-256 manifest, and symlink-definition validation |
| Motosu photo snapshots | Daily | 30 days |
| Motosu backup snapshots | Daily | 14 days |
| Motosu B2 Cloud Sync | After the nightly local backup window | Separate cloud-sync tasks; exact times and remote retention are not recorded here |

Failures of the Yamanaka backup and verification services trigger Signal alerts through the local Signal service. TrueNAS alerting independently sends email for Motosu-side/Cloud Sync failures.

Exact addresses, phone numbers, credentials, repository passwords, bucket identifiers, and cloud-account details remain private.

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

Nextcloud is deferred; backup priority is not applicable. Kawaguchi's selected configuration/appdata now has independent Restic protection, while bulk media and manga remain intentionally outside backup scope.

Redis/Valkey cache data, Docker images, Docker sockets, raw live PostgreSQL database directories, disposable restore-test trees, Prometheus historical metrics, and Loki historical logs are intentionally excluded where recovery value does not justify them.

Database-backed services use database-native dumps, SQLite-aware snapshots, or application-aware exports rather than copying live database directories blindly.

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
- Motosu drive upgrades are opportunistic; the current pair is deployed and healthy

Backup-failure alerting is deployed and tested on Yamanaka and Motosu. Kawaguchi backup/verify scheduling is deployed through Unraid User Scripts; separate Kawaguchi failure alerting is not recorded here. See the [move checklist](../runbooks/move-checklist.md) for execution order and the [documentation review](../history/documentation-review-2026-10-27.md#review-needed) for remaining decisions and verification work.
