# motosu recovery

## purpose

Restore Motosu and the Immich photo library after host or storage failure.

Motosu contains irreplaceable personal photos, so data preservation takes precedence over fast service restoration.

## first checks

Determine whether the problem is:

- network only
- UGOS / OS failure
- Docker failure
- one-disk RAID1 degradation
- full storage failure
- application/database corruption
- complete host loss

Do not initialize, format, or recreate the RAID unless existing data has been evaluated and a restore path is understood.

## recovery order

```text
1. preserve readable source data
2. restore host/network access
3. restore RAID/filesystem availability
4. restore Immich media library
5. restore Immich database
6. restore Docker stack
7. verify users/photos/search
8. restore remote access
```

## expected storage

Primary volume:

```text
/volume1
```

Critical Immich paths:

```text
/volume1/docker/immich/library
/volume1/docker/immich/postgres
```

Restic configuration:

```text
/volume1/docker/restic/restic.env
/volume1/docker/restic/password
/volume1/docker/restic/immich-backup.sh
```

The machine-learning model cache and Redis/Valkey state are rebuildable.

## degraded RAID1

If one of the two 6 TB disks fails but the array remains readable:

1. confirm which physical disk failed
2. record the healthy disk identity and current array state
3. avoid unnecessary writes until replacement is ready
4. replace the failed disk
5. rebuild the mirror using the platform's normal RAID recovery process
6. verify Btrfs/filesystem health afterward
7. confirm Immich files are readable
8. run a fresh backup after the array is healthy

A RAID1 mirror is availability protection, not a substitute for the B2 backup.

## application-only failure

If storage is intact but Immich is broken:

1. do not modify the photo library unnecessarily
2. inspect the Immich containers and logs
3. verify `immich_default` networking
4. verify PostgreSQL is available
5. verify the library bind mount points to `/volume1/docker/immich/library`
6. recreate containers from known configuration if needed
7. preserve existing persistent paths

Expected stack:

```text
immich_server
immich_postgres
immich_redis
immich_machine_learning
```

## restore from Backblaze B2

Use this path when local Immich library data is unavailable or cannot be trusted.

Prerequisites:

- B2 application credentials
- Restic repository password
- access to the `sjp-immich` repository
- enough local storage for the restore

The repository contains the Immich library and Immich-generated database backups. It does not directly back up the live PostgreSQL data directory.

### inspect snapshots

```bash
sudo docker run --rm \
  --env-file /volume1/docker/restic/restic.env \
  -v /volume1/docker/restic/password:/restic-password:ro \
  restic/restic \
  -p /restic-password snapshots
```

Choose a known-good snapshot before restoring.

### restore to a temporary path first

Do not restore directly over uncertain or partially recovered source data.

Example target:

```text
/volume1/restore/immich
```

Restore the selected snapshot there, inspect it, and only then place data into the final Immich library path.

### database recovery

Use the Immich-generated database backup contained under the restored library backup rather than copying old live PostgreSQL files into a new database blindly.

Follow the Immich version-appropriate database restore procedure at recovery time.

The repository intentionally does not hard-code a database restore command because the exact Immich/PostgreSQL restore process may change between releases.

## complete host loss

If Motosu itself is replaced:

1. prepare replacement storage with suitable redundancy
2. install the host OS and Docker
3. recreate the Immich stack
4. restore the library from Restic/B2
5. restore the Immich database from an included database backup
6. verify ownership and permissions
7. start Immich
8. verify users, albums, assets, metadata, and search
9. recreate Tailscale if needed
10. re-establish the automated Restic backup job

## backup verification after recovery

Confirm:

```bash
sudo crontab -l
sudo tail -n 50 /volume1/docker/restic/backup.log
```

Then perform a manual backup:

```bash
sudo /volume1/docker/restic/immich-backup.sh
```

Verify a new Restic snapshot appears.

## completion criteria

Recovery is complete when:

- storage is healthy and redundant again
- Immich starts successfully
- expected users can log in
- representative old and recent photos open correctly
- albums/metadata are present
- database-backed features work
- remote access works if required
- scheduled Restic backup is active
- a fresh successful B2 snapshot has been verified
