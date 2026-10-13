# backups

Backup effort follows data value and rebuild cost rather than raw storage size.

The homelab has three different recovery profiles:

```text
kawaguchi = mostly rebuildable media infrastructure
motosu    = irreplaceable photo library

yamanaka  = irreplaceable application state
```

## policy

A backup is only considered independent if loss of the source host or its primary storage does not also destroy the backup.

Application-generated backups stored on the same host are useful restore points, but they are not sufficient host-failure protection.

The preferred model is:

```text
source data
   |
   +--> local application/database backup where useful
   |
   `--> independent backup destination
            |
            `--> off-site for irreplaceable data
```

Secrets, repository passwords, API keys, and backup credentials must not be committed to this public repository.

## motosu

Motosu has the strongest verified backup implementation because it stores the Immich photo library.

### protected data

Restic backs up:

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

### schedule

```text
~01:00  Immich database backup
04:00   Restic backup to Backblaze B2
```

Root cron entry:

```cron
0 4 * * * /volume1/docker/restic/immich-backup.sh >> /volume1/docker/restic/backup.log 2>&1
```

### retention

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

### recovery priority

Highest priority:

```text
1. photo/media library
2. Immich database backup
3. configuration needed to recreate the stack
4. Tailscale state if convenient
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
└── manga application metadata where useful

low / normally not backed up
├── movies
├── TV
├── downloads
├── caches
└── other easily reacquired payloads
```

The manga library should be considered separately from Usenet-reacquirable movie/TV media if any of it would be difficult to replace.

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

## backup classes

| class | examples | expectation |
| --- | --- | --- |
| irreplaceable | Immich photos, Paperless documents, budgets, personal databases | independent backup; off-site preferred |
| important configuration | Unraid config, Plex metadata, Arr configuration, Compose files | independent backup |
| convenient | dashboards, metrics history, caches | back up only if recovery value justifies it |
| replaceable | Usenet movie/TV payloads, downloads, ML cache | normally recreate instead of backing up |

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
- no common alerting for failed backup jobs yet

These should be resolved based on risk rather than by backing up every byte in the homelab.