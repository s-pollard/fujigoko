# backups

Backup effort follows data value and rebuild cost rather than raw storage size.

```text
kawaguchi = mostly rebuildable media infrastructure
motosu    = irreplaceable photo library + backup storage
yamanaka  = irreplaceable application state
saiko     = mostly disposable lab state
```

## policy

A backup is independent only if loss of the source host or its primary storage does not also destroy the backup.

Application-generated backups stored on the same host are useful restore points but are not sufficient host-failure protection.

Secrets, repository passwords, API keys, cloud bucket names, account identifiers, and backup credentials must not be committed to this public repository.

## motosu

Motosu currently has the strongest verified backup implementation because it stores the Immich library and will become the local backup target for Yamanaka.

### current protected data

Restic currently backs up the Immich library, including Immich-generated database backup files.

The live PostgreSQL data directory is not copied directly by Restic. Recovery relies on application/database-aware backups rather than treating a live database directory as a normal file copy.

### destination

- Backblaze B2
- private bucket
- encrypted Restic repository

The exact bucket name, endpoint credentials, and repository password are intentionally excluded from this public repository.

### current schedule / retention

Current policy:

```text
Immich database backup -> before cloud backup
Restic cloud backup     -> daily
```

Retention:

```text
7 daily
4 weekly
12 monthly
```

The exact local credential-file locations are private operational details. Public documentation should describe the recovery method without publishing where secrets are stored.

### TrueNAS migration protection

Before rebuilding Motosu on TrueNAS SCALE:

1. create and validate a PostgreSQL logical dump
2. stop Immich for the final stable filesystem copy
3. copy the relevant Motosu application data to the Samsung T7 migration SSD
4. verify the copy with rsync/checksums
5. keep the existing B2 repository as the off-site recovery layer
6. leave the migration SSD untouched until the rebuilt stack is restored and proven

Current migration protection therefore consists of:

```text
motosu source
├── verified Samsung T7 migration copy
└── encrypted Backblaze B2 Restic repository
```

### planned TrueNAS protection model

```text
single-drive failure
-> ZFS mirror

accidental deletion / unwanted changes
-> ZFS snapshots

host loss / theft / disaster
-> Backblaze B2
```

The mirror is fault tolerance, not an independent backup.

Planned dataset roles:

```text
photos / immich
photos / gfx archive
backups / yamanaka
small service state
```

Dataset names can change during implementation; exact mount paths and permissions should be documented only where they are useful and not security-sensitive.

## kawaguchi

Kawaguchi currently has no verified independent backup system.

Priority:

```text
medium
├── Unraid flash/configuration
├── retained media-service appdata
├── Plex metadata/configuration
├── Sonarr/Radarr configuration
├── request/subtitle/statistics configuration
├── Uptime Kuma configuration
└── manga application metadata where useful

low / normally not backed up
├── movies
├── TV
├── downloads
├── caches
└── easily reacquired payloads
```

The goal is to preserve enough configuration to rebuild the media stack without trying to back up every replaceable media byte.

## yamanaka

Yamanaka is the Dell OptiPlex 3070 SFF production application host. Debian is installed; application migration and independent backup implementation are still in progress.

High-priority data includes:

- Paperless documents and metadata
- Actual Budget data
- HomeBox inventory
- Mealie data
- Linkwarden database/file data
- Endurain database/application data
- Vaultwarden persistent data and recovery material
- important Nextcloud user files and recovery data
- Compose definitions and service configuration

Target flow:

```text
yamanaka live data on local NVMe
├── native database/application backup where appropriate
└── independent copy to motosu
    ├── ZFS mirror
    ├── ZFS snapshots
    └── selected off-site B2 protection
```

For database-backed services, use database-native dumps or application-aware backups rather than copying live database directories.

A migrated application should not be permanently removed from Kawaguchi until its Yamanaka instance is verified and an independent backup exists on Motosu.

## saiko

Saiko is a lab host and should not hold unique production data. Back up only specific VM images/configuration that become valuable enough to preserve.

## backup classes

| class | examples | expectation |
| --- | --- | --- |
| irreplaceable | photos, photo archive, Paperless docs, budgets, password-vault state, personal databases | independent backup; off-site preferred |
| important configuration | Unraid config, Plex/Arr config, Compose files, DNS config | independent backup |
| convenient | dashboards, metrics history, selected lab VMs | back up only if recovery value justifies it |
| replaceable | Usenet media payloads, downloads, caches, disposable lab VMs | recreate instead of backing up |

## verification

Backups are not complete merely because a scheduled job exists.

Periodic verification should include:

1. confirm recent successful runs
2. confirm new snapshots/archives are actually created
3. confirm credentials and repository passwords are recoverable from the private credential store
4. perform representative test restores
5. document host-specific restore order in `runbooks/`

## known gaps

- no verified independent Kawaguchi configuration/appdata backup
- Yamanaka-to-Motosu backup implementation and retention not finalized
- no documented full Motosu restore test from B2 yet
- TrueNAS/ZFS snapshot policy not yet implemented
- photo-archive dataset/backup policy not finalized
- no common alerting for failed backup jobs yet
