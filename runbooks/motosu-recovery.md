# motosu recovery

## purpose

Restore Motosu and the Immich photo library after host or storage failure.

Motosu contains irreplaceable photo data, so preservation takes precedence over fast service restoration.

Secrets, cloud bucket names, credential-file locations, exact network addresses, and other sensitive operational details are intentionally excluded from this public runbook.

## first checks

Determine whether the problem is:

- network only
- OS/platform failure
- application/container failure
- one-disk mirror degradation
- full storage failure
- application/database corruption
- complete host loss

Do not initialize, format, or recreate storage until the existing data has been evaluated and a restore path is understood.

## recovery order

```text
1. preserve readable source data
2. restore host/network access
3. restore storage availability
4. restore Immich media library
5. restore Immich database
6. restore application stack
7. verify users/photos/search
8. restore remote access
9. verify backup jobs
```

## current pre-TrueNAS state

The current deployment uses UGOS Pro / Debian-based storage with Linux RAID1 and Btrfs.

Critical data:

- Immich library
- Immich PostgreSQL state / validated logical backup
- Restic backup configuration

Rebuildable data:

- machine-learning model cache
- Redis/Valkey cache/state

## degraded mirror

If one of the two HDDs fails but storage remains readable:

1. identify the failed physical disk
2. record the healthy disk and current array/pool state
3. avoid unnecessary writes until replacement is ready
4. replace the failed disk
5. rebuild/resilver using the active platform's normal recovery process
6. verify filesystem/pool health
7. confirm representative Immich files are readable
8. run a fresh independent backup after storage is healthy

A mirror provides availability, not an independent backup.

## application-only failure

If storage is intact but Immich is broken:

1. avoid modifying the photo library unnecessarily
2. inspect application logs
3. verify the database is available
4. verify persistent storage mounts/datasets
5. recreate application containers/apps from known configuration if required
6. preserve existing persistent data

Expected logical stack:

```text
immich server
immich postgres
immich redis/valkey
immich machine learning
```

## restore from Backblaze B2

Use this path when local Immich data is unavailable or cannot be trusted.

Prerequisites:

- B2 application credentials from the private credential store
- Restic repository password
- Restic repository identifier from private operational documentation
- enough local storage for the restore

The off-site repository contains the Immich library and application-generated database backups. It does not rely on blindly copying a live PostgreSQL directory.

### inspect snapshots

Use the locally documented Restic environment and password file to list snapshots. Do not commit the real credential paths or repository identifier here.

Example pattern:

```bash
restic -r <repository> snapshots
```

### restore to a temporary path first

Do not restore directly over uncertain or partially recovered source data.

```bash
restic -r <repository> restore <snapshot> --target <temporary-restore-path>
```

Inspect the restored data before moving it into the final Immich library location.

### database recovery

Use a validated application/database backup and follow the Immich version-appropriate restore process at recovery time.

Do not hard-code a database restore command here because the supported Immich/PostgreSQL restore process may change between releases.

## complete host loss

If Motosu itself is replaced:

1. prepare redundant replacement storage
2. install the intended platform
3. recreate the Immich stack
4. restore the library from the independent backup
5. restore the database from a validated backup
6. verify ownership/permissions
7. start Immich
8. verify users, albums, assets, metadata, and search
9. recreate remote access if required
10. re-establish automated off-site backup

## TrueNAS target state

After the planned TrueNAS SCALE rebuild, update this runbook for:

- ZFS pool/dataset names
- snapshot policy
- application deployment method
- replacement Restic/B2 job
- Yamanaka backup datasets

Keep exact addresses, credentials, cloud resource identifiers, and other sensitive details in private operational documentation rather than this public repository.

## completion criteria

Recovery is complete when:

- storage is healthy and redundant again
- Immich starts successfully
- expected users can log in
- representative old and recent photos open correctly
- albums/metadata are present
- database-backed features work
- remote access works if required
- scheduled independent backup is active
- a fresh off-site snapshot has been verified
