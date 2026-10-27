# motosu recovery

## purpose

Restore Motosu and the Immich/photo storage after host, application, or storage failure.

Motosu contains irreplaceable photo data and serves as a backup target, so preservation takes precedence over fast service restoration.

Secrets, cloud bucket names, encryption material, exact network addresses, and other sensitive operational details are intentionally excluded from this public runbook.

## recovery references

- [Host baseline](../hosts/README.md#motosu) — TrueNAS SCALE and physical inventory
- [Storage](../storage/README.md#motosu) — mirror state and deployed Immich path
- [Backups](../backups/README.md#motosu) — snapshots, encrypted B2 copy, alerting, verification limits
- [Migration and mirror history](../history/motosu-storage-2026.md)

The TrueNAS/Immich migration is complete and validated. Both mirror members are accepted as deployed; verify current pool health before acting on historical incident notes.

## first checks

Determine whether the problem is:

- network only
- TrueNAS host/boot failure
- Immich application failure
- PostgreSQL/database failure
- one-disk ZFS mirror degradation
- pool/dataset problem
- accidental deletion/corruption
- complete host/storage loss

Do not initialize, format, destroy, or recreate the pool until existing data has been evaluated and a restore path is understood.

## recovery order

```text
1. preserve readable source data
2. restore host/network access
3. restore/import ZFS pool and datasets
4. verify photo/Immich files
5. restore Immich database
6. restore/redeploy Immich application stack
7. verify users/photos/albums/search
8. restore backup jobs and remote access
9. verify snapshots and off-site backup
```

## data classes

High-value:

- Immich library
- validated PostgreSQL logical/application backups
- photo/archive datasets
- Yamanaka backup datasets
- backup configuration and private encryption material needed to reach the independent off-site copy

Rebuildable:

- Redis/Valkey state
- Immich machine-learning model cache
- application containers/images

## degraded ZFS mirror

If one HDD fails but the pool remains available:

1. confirm the pool is degraded and identify the failed physical disk
2. record the healthy member and current pool state
3. avoid unrelated heavy writes until replacement is ready
4. replace the failed disk using TrueNAS/ZFS procedures
5. allow the resilver to complete
6. verify pool health and scrub status
7. open representative Immich/photo files
8. run/verify a fresh independent backup after the pool is healthy

The mirror provides fault tolerance, not an independent backup.

## application-only failure

If the pool/datasets are healthy but Immich is broken:

1. avoid changing the photo library unnecessarily
2. inspect Immich/PostgreSQL application logs
3. verify the expected dataset is mounted and readable
4. verify PostgreSQL health and version compatibility
5. preserve existing persistent data before destructive application changes
6. redeploy/recreate application components only after the data path and database recovery plan are clear

The [Immich service inventory](../services/README.md#motosu) records the server, PostgreSQL, Valkey/Redis, and machine-learning components.

Do not assume a database dump from an older PostgreSQL/Immich deployment can be restored blindly into a newer schema. Validate the version-appropriate restore path first.

## accidental deletion or unwanted changes

If the affected data is covered by a usable ZFS snapshot:

1. identify the affected dataset and time window
2. inspect the snapshot before rollback
3. prefer restoring selected files to a temporary location when possible
4. use a full dataset rollback only when the blast radius is understood
5. verify Immich/database consistency afterward

Use the [deployed snapshot schedule and retention](../backups/README.md#deployed-schedule-and-retention) to identify available recovery points; verify the actual snapshots before relying on them.

## restore from Backblaze B2

Use the off-site path when local data is unavailable or cannot be trusted.

Current B2 protection is a TrueNAS Cloud Sync copy with client-side remote encryption, not the former Restic repository workflow.

Prerequisites:

- B2 application credentials from the private credential store
- TrueNAS/rclone remote-encryption password and salt from the private credential store
- sufficient temporary/local storage

Restore to a temporary dataset/path first. Configure the B2 credential and the same remote-encryption values in TrueNAS, create a pull/restore task for a representative subset, and verify that restored files open correctly before attempting a full production restore.

A representative encrypted B2 restore test is still a follow-up item and should be documented here once verified.

### database recovery

Use a validated logical/application backup and the Immich version-appropriate database restore process. Do not treat a copied live PostgreSQL data directory as the primary recovery method.

## complete host loss

If Motosu must be rebuilt or replaced:

1. install TrueNAS SCALE on replacement boot media
2. restore/import healthy pool storage if available, otherwise create replacement mirrored storage
3. recreate required datasets
4. restore photo/Immich files from the best independent source
5. restore PostgreSQL from a validated logical/application backup
6. redeploy Immich
7. verify permissions/ownership and application access
8. verify users, albums, representative old/recent assets, metadata, and search
9. recreate Yamanaka backup targets and remote access as needed
10. re-establish snapshots and encrypted off-site backup

## follow-up

Use the [move checklist](move-checklist.md) for conditional drive upgrades and the representative encrypted B2 restore test. Verify periodic SMART testing and alerting.

The previous requests to deploy Yamanaka backups and add independent monitoring were stale. Use the [deployed backup record](../backups/README.md#verified-yamanaka-to-motosu-recovery-path) and [accepted monitoring boundary](../architecture/README.md#accepted-dependencies); the earlier instructions are retained in the [review history](../history/documentation-review-2026-10-27.md#confirmed-state).

## completion criteria

Recovery is complete when:

- the ZFS pool is healthy/redundant or a documented degraded state is understood
- required datasets are mounted and readable
- Immich starts successfully
- expected users can log in
- representative old and recent photos open correctly
- albums/metadata/database-backed features work
- Yamanaka backup storage is available if required
- scheduled snapshots/backups are active
- a representative restore or fresh off-site backup has been verified
