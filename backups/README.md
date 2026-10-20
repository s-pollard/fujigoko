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
- Uptime Kuma configuration
- useful manga application metadata

Movies, TV, downloads, caches, and other reacquirable payloads are normally low priority.

A verified independent Kawaguchi configuration/appdata backup remains a gap.

## yamanaka

Yamanaka is the production application host. Important live application data remains local for normal operation, with independent recovery copies going to Motosu.

High-priority examples include:

- Paperless documents and metadata
- Actual Budget data
- HomeBox inventory
- Mealie data
- Linkwarden data
- Endurain data
- security-sensitive application state if deployed
- important file-sync data if deployed
- Compose definitions and service configuration

Use database-native dumps or application-aware exports for database-backed services rather than copying live database directories.

A migrated application should not be permanently removed from Kawaguchi until the Yamanaka instance is verified and an independent Motosu backup exists.

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
- Yamanaka-to-Motosu backup jobs/retention are not yet finalized
- no verified independent Kawaguchi configuration/appdata backup
- GFX archive backup policy is not yet finalized
- common backup-failure alerting is not yet established
