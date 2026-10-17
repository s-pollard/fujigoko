# storage

This document describes where Fujigoko data lives, what each host is responsible for, and which data is considered replaceable versus important to preserve.

The storage model follows the host-role split:

```text
kawaguchi = bulk media + media application state
motosu    = photo library + Immich + GFX archive + backup storage
yamanaka  = personal application state
saiko     = disposable/experimental VM storage
```

## kawaguchi

Kawaguchi is the bulk-storage host and media server.

### array

- platform: Unraid
- six HDDs in the main array
- approximately 54 TB available through `/mnt/user` at inventory time
- approximately 31 TB used at inventory time

Observed disk sizes:

- 2 × 8 TB-class drives
- 2 × 12 TB-class drives
- 2 × 10 TB-class drives

The bulk array primarily exists for media that can be reacquired if necessary.

### cache

- 2 × Samsung 970 EVO Plus 1 TB NVMe
- ZFS cache pool
- approximately 1.7 TB usable at inventory time

Application state and other high-I/O data currently live on the cache pool through normal Unraid share placement.

An additional approximately 119 GB YSO NVMe is installed. Its current purpose has not been established and should not be assigned a role in documentation until verified.

### shares

Current known shares:

```text
/mnt/user/appdata
/mnt/user/domains
/mnt/user/downloads
/mnt/user/isos
/mnt/user/media
/mnt/user/roms
/mnt/user/system
```

There is also a legacy uppercase share:

```text
/mnt/user/Media
```

It is currently only known to be referenced by an obsolete Komf `/library` mount and is a cleanup candidate after that dependency is removed and verified.

### media layout

Primary production data lives under:

```text
/mnt/user/media/
├── movies
├── tv
├── manga
├── music
├── Photos
└── paperless
```

Approximate observed usage at inventory time:

- movies: ~18 TB
- TV: ~12 TB
- music: ~1 TB
- manga: ~140 GB
- Photos: ~40 GB

Paperless currently also stores data below `/mnt/user/media/paperless`, but that data is intended to move to Yamanaka with the application.

### downloads

```text
/mnt/user/downloads/
├── complete
└── incomplete-downloads
```

This data is temporary and replaceable.

### storage criticality

Kawaguchi is intentionally treated as relatively rebuildable.

Most movie and TV data originates from Usenet and does not justify full off-site backup at its current scale.

Higher-value Kawaguchi data is configuration and metadata rather than bulk media:

```text
higher value
├── unraid flash/configuration
├── /mnt/user/appdata
├── plex metadata/configuration
└── media automation configuration

replaceable
├── movies
├── tv
├── downloads
└── caches
```

Manga remains on Kawaguchi as part of the permanent media role.

## motosu

Motosu is the dedicated photo-storage and backup-storage host.

### current physical storage

- 2 × Seagate ST6000NM0024 6 TB drives
- Linux md RAID1
- LVM
- Btrfs
- main volume: `/volume1`
- approximately 5.5 TB usable
- approximately 298 GB used at inventory time

Unlike Kawaguchi media, Motosu contains irreplaceable photo data and should be treated as high-priority storage.

### planned TrueNAS storage

Motosu will be rebuilt on TrueNAS SCALE, booting from a Patriot P300 128 GB NVMe.

Initial target storage:

```text
2 × 6 TB HDD
└── ZFS mirror
    └── ~6 TB-class usable capacity
```

The mirror provides single-disk fault tolerance. ZFS snapshots provide local rollback/versioning, while Backblaze B2 remains the independent off-site backup layer for selected high-value datasets.

Future capacity upgrades can replace the two mirror members one at a time with larger drives, allowing the mirror to expand after both members have been replaced and resilvered.

### planned dataset roles

Exact names can change during the TrueNAS build, but Motosu should separate data by purpose rather than mixing everything into one dataset:

```text
motosu pool
├── photos
│   ├── immich
│   └── gfx-archive
├── backups
│   └── yamanaka
└── service-state
    └── adguard / other small persistent configuration
```

Separate datasets allow snapshots, retention, permissions, and B2 policies to be tuned independently.

### photo roles

Motosu will hold two related but distinct photo workloads:

```text
Immich
├── phone photos
├── family phone sync
└── finished/exported GFX photos

GFX archive
├── RAW/original files
├── sidecars / edit metadata
├── edited masters as needed
└── normal filesystem storage independent of Immich
```

The GFX archive design will be finalized only after the TrueNAS migration is complete and these are verified:

1. Immich runs correctly on the rebuilt Motosu.
2. Phone sync works normally.
3. ZFS snapshots work as intended.
4. B2 backups and recovery are confirmed.

Immich should remain a convenient photo library rather than the only copy or organizational structure for GFX RAW files.

### yamanaka backup role

Motosu is the independent local backup destination for important Yamanaka data.

Expected Yamanaka backup content includes:

```text
application exports
native database dumps
important user/filesystem data
compose definitions
service configuration
other non-rebuildable application state
```

Yamanaka keeps live application data on local NVMe for normal operation. Motosu stores backup copies on the mirrored ZFS pool, snapshots those backup datasets, and selected high-value backup data is then included in the Motosu-to-B2 off-site policy.

```text
yamanaka live data
└── motosu backup dataset
    ├── ZFS mirror
    ├── ZFS snapshots
    └── Backblaze B2
```

The ZFS mirror is fault tolerance, not an independent backup by itself.

### current Immich persistence

Current critical paths before the TrueNAS migration:

```text
/volume1/docker/immich/library
/volume1/docker/immich/postgres
```

Important but secondary:

```text
/volume1/docker/tailscale/state
```

Rebuildable:

```text
immich redis / valkey state
immich machine-learning model cache
```

The Immich library and database backups must remain independently recoverable throughout the TrueNAS migration.

A full migration copy currently exists on a Samsung T7 external SSD. The copied Immich library has been verified byte-for-byte with SHA-256, and a PostgreSQL custom-format logical dump was created and validated before the source stack was stopped.

## yamanaka

Yamanaka is the selected Dell OptiPlex 3070 SFF production application host.

Current storage state:

- Patriot P300 128 GB NVMe installed during initial Debian deployment
- 500 GB NVMe ordered for the production application-storage role

The 500 GB NVMe will hold live non-media application state, databases, Redis/cache state where required, and the Prometheus/Grafana/Loki monitoring stack. Live PostgreSQL or Redis directories should not be placed on SMB/NFS storage.

Planned logical layout:

```text
/srv/
├── compose/
└── data/
```

Expected high-value data includes:

- Paperless documents and metadata
- Actual Budget data
- HomeBox inventory
- Linkwarden PostgreSQL data and file storage
- Mealie data
- Endurain PostgreSQL and required application state
- Grafana configuration
- Compose definitions and service configuration

Yamanaka data must have an independent backup on Motosu before the corresponding Kawaguchi copy is permanently removed. Database-backed applications should use native dumps or application-aware exports for backup rather than direct copies of live database directories.

The 500 GB local device is considered sufficient for the planned application role because bulk media and photo storage remain on Kawaguchi and Motosu respectively.

## saiko

Saiko is an experimentation host rather than a primary storage host.

Proxmox VM disks and lab state are generally considered disposable unless a particular experiment becomes worth preserving. Important production data should not depend on Saiko storage.

## storage ownership

```text
kawaguchi
├── bulk media
├── downloads
├── manga
└── media-service state

motosu
├── phone / Immich photo library
├── Immich database/state
├── GFX archive
└── Yamanaka backup copies

yamanaka
└── live non-media application state on local NVMe

saiko
└── lab / experimental VM storage
```

Services should remain close to the storage they primarily operate on. This is why media automation stays on Kawaguchi, photos remain on Motosu, and general personal applications move to Yamanaka. Backup copies are deliberately separated from Yamanaka onto Motosu so a Yamanaka host/storage failure does not destroy the recovery copy.

## future documentation

Update this document when:

- Motosu has been rebuilt on TrueNAS SCALE
- ZFS datasets and snapshot policies are finalized
- the GFX archive layout is selected
- the ordered Yamanaka 500 GB NVMe is installed and its final filesystem/mount layout is established
- Yamanaka-to-Motosu backup jobs and retention are finalized
- Motosu-to-B2 dataset selection and retention are finalized
- Kawaguchi is cleaned after the migration
- the legacy uppercase `Media` share is removed
- the `roms` share is retired
- disk layout or pool configuration changes
