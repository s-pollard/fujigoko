# backups

Backup effort follows data value and rebuild cost rather than raw storage size.

The homelab has different recovery profiles:

```text
kawaguchi = mostly rebuildable media infrastructure
motosu    = irreplaceable photo library and future GFX archive
yamanaka  = irreplaceable application state
saiko     = mostly disposable lab state
```

## policy

A backup is only considered independent if loss of the source host or its primary storage does not also destroy the backup.

Application-generated backups stored on the same host are useful restore points, but they are not sufficient host-failure protection.

The preferred model is:

```text
source data
   |
   +--> local snapshot/application/database backup where useful
   |
   `--> independent backup destination
            |
            `--> off-site for irreplaceable data
```

Secrets, repository passwords, API keys, and backup credentials must not be committed to this public repository.

## motosu

Motosu has the strongest verified backup implementation because it stores the Immich photo library.

### current protected data

Restic currently backs up:

```text
/volume1/docker/immich/library
```

This includes the Immich media library and Immich-generated database backup files.

The live PostgreSQL directory:

```text
/volume1/docker/immich/postgres
```

is intentionally not copied directly by Restic. Immich creates database backups under the library path, and those backup files are included in the Restic repository.

### destination

```text
Backblaze B2
└── private bucket: sjp-immich
```

The Restic repository is encrypted before storage in B2.

### current schedule

```text
~01:00  Immich database backup
04:00   Restic backup to Backblaze B2
```

Root cron entry:

```cron
0 4 * * * /volume1/docker/restic/immich-backup.sh >> /volume1/docker/restic/backup.log 2>&1
```

### current retention

```text
7 daily
4 weekly
12 monthly
```

### restic files

```text
/volume1/docker/restic/restic.env
/volume1/docker/restic/password
/volume1/docker/restic/immich-backup.sh
/volume1/docker/restic/backup.log
```

The Restic repository password is required for recovery. Losing it makes the encrypted repository unusable.

### TrueNAS migration protection

Before wiping UGOS and rebuilding Motosu on TrueNAS SCALE:

1. create a fresh Immich database backup
2. stop Immich so the final copies represent a stable state
3. make an independent copy to a Samsung external SSD
4. make a second independent local copy to Kawaguchi
5. confirm the existing Backblaze B2 repository is current
6. verify both local copies before touching the source filesystem
7. keep the SSD and Kawaguchi copies untouched until the restored TrueNAS/Immich deployment is proven

The two local copies may be created in parallel after Immich has been stopped.

The goal before destructive migration work is effectively:

```text
motosu original
├── samsung external SSD copy
├── kawaguchi copy
└── backblaze B2 restic repository
```

### planned TrueNAS protection model

After the rebuild:

```text
single-drive failure
-> ZFS mirror

accidental deletion / unwanted changes
-> ZFS snapshots

host loss / theft / disaster
-> Restic + Backblaze B2
```

Local ZFS snapshots and Restic snapshots serve different purposes. The local snapshot tree does not need to be copied wholesale to B2; Restic will continue to provide its own deduplicated off-site history from the live datasets selected for backup.

The future GFX RAW/archive data on Motosu is also high-priority data and should be included in the off-site backup design once its dataset layout is finalized.

### verification commands

Recent backup log:

```bash
sudo tail -n 50 /volume1/docker/restic/backup.log
```

Search for backup failures:

```bash
sudo grep -E "snapshot|Fatal|error|ERROR" /volume1/docker/restic/backup.log | tail -n 20
```

List snapshots:

```bash
sudo docker run --rm \
  --env-file /volume1/docker/restic/restic.env \
  -v /volume1/docker/restic/password:/restic-password:ro \
  restic/restic \
  -p /restic-password snapshots
```

Manual backup:

```bash
sudo /volume1/docker/restic/immich-backup.sh
```

These paths/commands describe the current UGOS deployment and must be rewritten after the TrueNAS migration.

### recovery priority

Highest priority:

```text
1. original photo/media files
2. Immich database backup
3. future GFX RAW/archive files
4. configuration needed to recreate the stack
5. Tailscale state if convenient
```

Redis/Valkey state and the machine-learning model cache are rebuildable.

## kawaguchi

Kawaguchi currently has no verified independent backup system.

Several applications create local backup directories inside appdata, including Sonarr, Radarr, Bazarr, Tautulli, Mealie, and Tachidesk. These are stored on Kawaguchi itself and therefore do not protect against loss of the host or cache pool.

### protection goals

Kawaguchi is intentionally treated as relatively rebuildable. Most bulk movie and TV data can be reacquired through the existing Usenet workflow.

Priority should therefore be:

```text
medium
├── Unraid flash/configuration
├── appdata for retained media services
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
└── other easily reacquired payloads
```

The manga library should be considered separately from Usenet-reacquirable movie/TV media if any of it would be difficult to replace.

AdGuard Home is expected to leave Kawaguchi, so its long-term configuration backup belongs with whatever DNS design replaces the current deployment.

### current gap

Before Kawaguchi cleanup is considered complete, establish an independent backup for the configuration needed to rebuild the media stack.

The exact mechanism is intentionally undecided until the post-move layout is stable.

## yamanaka

Yamanaka does not exist yet, so no backup implementation is currently verified.

Its backup requirements are stricter than Kawaguchi because it will store personal application state.

### high-priority data

Expected important data includes:

```text
Paperless documents + metadata
Actual Budget data
HomeBox inventory
Mealie data
Linkwarden PostgreSQL + file storage
Endurain PostgreSQL + required application data
Grafana configuration worth preserving
Compose definitions and deployment documentation
```

Supporting caches such as Redis generally do not require direct backup when the parent application can recreate them.

### migration gate

A migrated application should not be permanently removed from Kawaguchi until its Yamanaka data has an independent backup.

For database-backed applications, prefer application-aware or database-native exports rather than copying live database files.

## saiko

Saiko is a Proxmox lab host and should not hold unique production data.

Most lab VMs are disposable. Back up only specific VM images/configuration that become valuable enough to justify preservation.

## backup classes

| class | examples | expectation |
| --- | --- | --- |
| irreplaceable | Immich photos, GFX archive, Paperless documents, budgets, personal databases | independent backup; off-site preferred |
| important configuration | Unraid config, Plex metadata, Arr configuration, Compose files | independent backup |
| convenient | dashboards, metrics history, selected lab VMs, caches | back up only if recovery value justifies it |
| replaceable | Usenet movie/TV payloads, downloads, ML cache, disposable lab VMs | normally recreate instead of backing up |

## verification

Backups are not complete merely because a scheduled job exists.

Periodic verification should include:

1. confirm recent successful runs
2. confirm new snapshots or archives are actually being created
3. confirm credentials and repository passwords are recoverable
4. perform a test restore of representative files
5. document any host-specific restore sequence in `runbooks/`

## known gaps

Current known gaps are:

- no verified independent Kawaguchi configuration/appdata backup
- Yamanaka backup design not selected yet
- no documented full restore test for Motosu from B2 yet
- TrueNAS/ZFS snapshot policy for Motosu not yet implemented
- GFX archive dataset/backup policy not yet finalized
- no common alerting for failed backup jobs yet

These should be resolved based on risk rather than by backing up every byte in the homelab.
