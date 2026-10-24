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
- B2 transfer uses client-side remote encryption; recovery secrets are kept outside this public repository
- the current B2 photo upload has completed

Historical migration recovery material can be retained or retired according to recovery value now that the TrueNAS/Immich migration has been validated; it is no longer the primary protection model.

### protection model

```text
single-drive failure
-> mirrored ZFS storage

accidental deletion / unwanted changes
-> ZFS snapshots

host loss / theft / disaster
-> encrypted Backblaze B2 copy
```

The ZFS mirror is fault tolerance, not an independent backup.

Selected high-value Motosu data should include the Immich/photo library, photo archives, and Yamanaka backup datasets.

### motosu follow-up

- perform and document a representative restore from the encrypted B2 copy
- replace the temporary older mirror member with a better HDD and verify the resulting resilver/SMART/scrub state
- verify periodic SMART tests and failure alerting
- implement Yamanaka-to-Motosu backup jobs and retention
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

Yamanaka is the production application host. Important live application data remains local for normal operation, with independent recovery copies going to Motosu.

Establishing Yamanaka-to-Motosu backup coverage is now a high-priority operational task. The retained services were migrated to Yamanaka before that off-host backup path was established because no new valuable production data had yet been added after migration. That deferred backup setup should not be treated as the normal procedure for future migrations.

High-priority examples include:

- Paperless documents and metadata
- Actual Budget data
- HomeBox inventory
- Mealie data
- Linkwarden data
- Endurain data
- Uptime Kuma configuration
- security-sensitive application state if deployed
- important file-sync data if deployed
- Compose definitions and service configuration

Use database-native dumps or application-aware exports for database-backed services rather than copying live database directories.

For future migrations involving valuable production data, verify the destination service and establish an independent backup before retiring the previous production copy when practical.

### Paperless restore validation

An application export was restored and tested on Yamanaka in an isolated environment using the pinned Paperless-ngx 3.3.3 image. This validates recovery of this export, not a complete off-host backup process.

Verified:

- all 12 documents restored; downloaded originals match export and database SHA-256 checksums
- normal container startup with a separate Redis instance, healthy database/Celery/index, and no unapplied migrations
- search index contains exactly the restored document IDs; content searches and a negative query work
- previews, thumbnails, password authentication, and browser document-list/detail/PDF rendering
- data, search, authentication, and download checks survive a container stop/start and Redis restart
- test containers had no host port bindings; external network and production Paperless/Redis access were blocked
- manual sanity check reported no issues
- temporary containers, networks, credentials, and sessions were removed; production and the source export were unchanged

No archive versions exist in this export; only originals and thumbnails are expected. Classifier/sanity-status warnings reflected missing task history, not damaged data. Classifier training, new-document consumption/OCR, archive generation, larger datasets, clean-host recovery, and recovery from Motosu remain untested. Browser password entry and the Download button were not exercised directly; password login and downloads were verified separately over HTTP.

The export contains user password hashes and must be stored privately. Compose configuration, environment values, and the application secret key require a separate private backup.

### Yamanaka-to-Motosu setup status

The Yamanaka backup destination on Motosu has **not been set up**. The verified Paperless export remains only on Yamanaka; no Motosu transfer, schedule, retention job, or failure monitoring has been implemented for it.

Next work:

1. choose/create the destination dataset and restricted backup access on Motosu
2. establish the transfer method and private handling of application configuration/secrets
3. add application-aware backups for Paperless and the other retained Yamanaka services
4. configure scheduling, retention, and failure monitoring
5. verify checksums and perform an isolated restore from the Motosu copy
6. verify the destination is included in the intended off-site protection

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

- encrypted B2 upload is complete, but a representative Motosu restore test is still required
- Yamanaka-to-Motosu backup destination/access, transfer jobs, scheduling, retention, and monitoring are not yet set up; this is high priority
- no verified independent Kawaguchi configuration/appdata backup
- GFX archive backup policy is not yet finalized
- common backup-failure alerting is not yet established
