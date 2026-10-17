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

Never commit credentials, repository passwords, API keys, cloud bucket names, account identifiers, or other backup secrets to this public repository.

## motosu

Motosu is now on TrueNAS SCALE and remains the highest-priority backup/storage host.

Current verified migration protection includes:

- an external migration copy of the Immich data
- SHA-256 verification of the copied Immich library before the rebuild
- a PostgreSQL custom-format logical dump created before the source stack was retired
- an existing encrypted Backblaze B2 / Restic off-site repository
- the Immich library copied onto the rebuilt TrueNAS system

The rebuilt Immich database/application restore is still being completed and validated. Keep migration recovery copies until the restored stack has been proven.

### protection model

```text
single-drive failure
-> mirrored ZFS storage

accidental deletion / unwanted changes
-> ZFS snapshots

host loss / theft / disaster
-> Backblaze B2
```

The ZFS mirror is fault tolerance, not an independent backup.

Selected high-value Motosu data should include the Immich library/database recovery data, photo archives, and Yamanaka backup datasets.

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
3. confirm credentials needed for recovery remain available in the private credential store
4. perform representative restores
5. update host-specific recovery runbooks with verified procedures

## known gaps

- Immich restore on rebuilt Motosu is not yet fully validated
- final Motosu snapshot retention is not yet documented
- Yamanaka-to-Motosu backup jobs/retention are not yet finalized
- no verified independent Kawaguchi configuration/appdata backup
- no documented full Motosu restore test from B2 yet
- GFX archive backup policy is not yet finalized
- common backup-failure alerting is not yet established
