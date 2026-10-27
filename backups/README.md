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

- perform and document a representative restore from the encrypted B2 copy
- replace the temporary older mirror member with a better HDD and verify the resulting resilver/SMART/scrub state
- verify periodic SMART tests and failure alerting
- add monitoring independent of Yamanaka so a Yamanaka outage can still be detected

## kawaguchi

Kawaguchi is comparatively rebuildable. The backup priority is configuration and metadata, not the full media payload.

Higher-value items include:

- Unraid flash/configuration
- retained media-service appdata
- Plex metadata/configuration
- Sonarr/Radarr and related automation configuration
- useful manga application metadata

Movies, TV, downloads, caches, and other reacquirable payloads are normally low priority.

A verified independent Kawaguchi configuration/appdata backup remains a gap.

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
- AdGuard Home configuration
- Homepage, SearXNG, Stirling PDF, Prometheus, Alloy, Loki, Caddy, and other retained configuration
- signal-cli state
- Compose definitions and private environment/configuration required for recovery

Redis/Valkey cache data, Docker images, Docker sockets, raw live PostgreSQL database directories, disposable restore-test trees, Prometheus historical metrics, and Loki historical logs are intentionally excluded where recovery value does not justify them.

Database-backed services use database-native dumps or application-aware exports rather than copying live database directories.

### deployed schedule and retention

Yamanaka runs the production backup through a root-owned backup script and systemd timer.

- nightly Restic backup around 03:00 local time, with a small randomized delay
- weekly restore verification on Sunday around 05:00 local time, with a small randomized delay
- Restic retention: 14 daily, 8 weekly, and 6 monthly snapshots
- each backup run performs a Restic repository check after backup/retention processing
- Motosu performs the separate B2 cloud-sync step after the nightly local backup window

Exact addresses, credentials, repository passwords, bucket identifiers, and cloud-account details remain private.

### verified Yamanaka-to-Motosu recovery path

The production backup path was exercised end to end on 2026-10-26.

Verified:

- application-aware backup generation completed successfully
- Paperless exported 12 documents; the staged/restored Paperless export contained the expected export artifacts
- Linkwarden PostgreSQL custom-format dump is readable by `pg_restore`
- Endurain PostgreSQL custom-format dump is readable by `pg_restore`
- Restic stored the production staged backup on Motosu successfully
- the first production snapshot contained 2,157 files and about 867 MiB of logical backup data
- a later production snapshot was restored from Motosu to an isolated temporary path
- source and restored trees each contained 2,157 files
- recursive 1:1 comparison reported no differences
- the restored SHA-256 manifest validated successfully
- the restored Linkwarden and Endurain dumps passed archive validation
- automated verification completed successfully with exit status 0

This proves that the current staged production backup can be transferred to Motosu by Restic and restored byte-for-byte from the Motosu repository. It does not eliminate the need for periodic application-level restore testing as applications or backup formats change.

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
| irreplaceable | photos, documents, budgets, personal databases | independent backup; off-site preferred |
| important configuration | Unraid config, application config, Compose files, DNS config | independent backup |
| convenient | dashboards, metrics history | back up only if recovery value justifies it |
| replaceable | Usenet media, downloads, caches | recreate instead of backing up |

## verification

Periodically:

1. confirm recent successful backup jobs
2. confirm new snapshots/archives were actually created
3. confirm credentials and encryption material needed for recovery remain available in the private credential store
4. perform representative restores
5. update host-specific recovery runbooks with verified procedures

## known gaps

- a representative restore from the Motosu/B2 off-site copy is still required
- no verified independent Kawaguchi configuration/appdata backup
- GFX archive backup policy is not yet finalized
- common backup-failure alerting is not yet established
- monitoring independent of Yamanaka is not yet deployed
