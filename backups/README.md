# backups

Backup effort follows data value and rebuild cost rather than raw storage size.

```text
kawaguchi = mostly rebuildable media infrastructure
motosu    = irreplaceable photo data + backup storage
yamanaka  = irreplaceable application state
```

## policy

A backup is independent only if loss of the source host or its primary storage does not also destroy the backup.

Application-generated backups stored only on the source host are useful restore points but are not sufficient host-failure protection.

Never commit credentials, repository passwords, API keys, cloud bucket names, account identifiers, encryption passwords/salts, or other backup secrets to this public repository.

## motosu

Motosu is on TrueNAS SCALE and remains the highest-priority backup/storage host.

Current verified protection includes:

- mirrored ZFS storage for single-drive fault tolerance
- daily ZFS snapshots for photos with 30-day retention
- daily ZFS snapshots for backups with 14-day retention
- restored and validated Immich application/database/library
- Backblaze B2 off-site backup configured through TrueNAS Cloud Sync
- B2 transfer uses encrypted backup content and private credentials kept outside this public repository
- the current B2 photo upload has completed
- a dedicated Yamanaka Restic repository is stored on Motosu and included in the intended B2 off-site path
- TrueNAS email alerting is configured and tested so Cloud Sync failures do not depend on Yamanaka being available

Historical migration recovery material can be retained or retired according to recovery value now that the TrueNAS/Immich migration has been validated; it is no longer the primary protection model.

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

A separate external monitor for Yamanaka is not currently required. Loss of normal access to Yamanaka is sufficient operational indication for the present home-use requirements.

## kawaguchi

Kawaguchi is comparatively rebuildable, and its media automation state is intentionally treated as disposable/reconstructable.

No full independent backup of the Arr stack or other routine media automation state is required. If Kawaguchi or its Unraid installation fails catastrophically, the intended response is to rebuild or migrate the media services rather than preserve the existing Unraid installation exactly.

Movies, TV, downloads, caches, and associated automation state are therefore outside the high-value backup scope unless that policy changes later.

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

High-priority protected state includes:

- Paperless documents and metadata through the Paperless exporter
- Actual Budget data
- HomeBox inventory
- Mealie data
- Linkwarden PostgreSQL dump and application data
- Endurain PostgreSQL dump and application data
- Uptime Kuma state
- FreshRSS state
- Pocket ID state and private deployment configuration
- Grafana state
- Grocy persistent configuration/data
- TriliumNext persistent data
- Vaultwarden persistent data, with the SQLite database captured using SQLite's online backup mechanism and validated before staging
- AdGuard Home configuration
- Homepage, SearXNG, Stirling PDF, Prometheus, Alloy, Loki, Caddy, and other retained configuration
- signal-cli state
- Compose definitions and private environment/configuration required for recovery

Redis/Valkey cache data, Docker images, Docker sockets, raw live PostgreSQL database directories, disposable restore-test trees, Prometheus historical metrics, and Loki historical logs are intentionally excluded where recovery value does not justify them.

Database-backed services use database-native dumps, SQLite-aware snapshots, or application-aware exports rather than copying live database directories blindly.

### deployed schedule and retention

Yamanaka runs the production backup through a root-owned backup script and systemd timer.

- nightly Restic backup around 03:00 local time, with a small randomized delay
- weekly restore verification on Sunday around 05:00 local time, with a small randomized delay
- Restic retention: 14 daily, 8 weekly, and 6 monthly snapshots
- each backup run performs a Restic repository check after backup/retention processing
- Motosu performs the separate B2 cloud-sync step after the nightly local backup window
- failures of the Yamanaka backup and verification services trigger Signal alerts through the local Signal service
- TrueNAS system alerting independently sends email for Motosu-side/Cloud Sync failures

Exact addresses, phone numbers, credentials, repository passwords, bucket identifiers, and cloud-account details remain private.

### verified Yamanaka-to-Motosu recovery path

The production backup path was exercised end to end on 2026-10-26 and re-verified after adding Grocy, TriliumNext, and Vaultwarden on 2026-10-27.

Verified:

- application-aware backup generation completed successfully
- Paperless exported 12 documents; the staged/restored Paperless export contained the expected export artifacts
- Linkwarden PostgreSQL custom-format dump is readable by `pg_restore`
- Endurain PostgreSQL custom-format dump is readable by `pg_restore`
- Grocy state is captured through a consistent-copy workflow
- TriliumNext state is captured through a consistent-copy workflow
- Vaultwarden's SQLite database is backed up with SQLite's online `.backup` mechanism and the resulting database passes `PRAGMA integrity_check`
- an isolated Vaultwarden restore test successfully launched the application from the backed-up database and signing key before production backup integration
- Restic stored the expanded production staged backup on Motosu successfully
- the post-expansion production snapshot contained 2,301 files and about 873 MiB of logical backup data
- Restic repository checking reported no errors
- the latest snapshot was restored from Motosu to an isolated temporary path
- source and restored trees each contained 2,301 files
- recursive 1:1 comparison reported no differences
- the restored SHA-256 manifest validated successfully
- the restored Linkwarden and Endurain dumps passed archive validation
- automated verification completed successfully

This proves that the current staged production backup, including Grocy, TriliumNext, and Vaultwarden, can be transferred to Motosu by Restic and restored byte-for-byte from the Motosu repository. It does not eliminate the need for periodic application-level restore testing as applications or backup formats change.

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

Backup-failure alerting is deployed and tested on both Yamanaka and Motosu. A separate independent Yamanaka uptime monitor is not currently required.
