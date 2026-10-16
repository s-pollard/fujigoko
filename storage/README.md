# storage

This document describes where Fujigoko data lives, what each host is responsible for, and which data is considered replaceable versus important to preserve.

The storage model follows the host-role split:

```text
kawaguchi = bulk media + media application state
motosu    = photo library + Immich + GFX archive
yamanaka  = personal application state (planned)
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

Motosu is the dedicated photo-storage host.

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

Motosu will be rebuilt on TrueNAS SCALE.

Initial target storage:

```text
2 × 6 TB HDD
└── ZFS mirror
    └── ~6 TB-class usable capacity
```

The mirror provides single-disk fault tolerance. ZFS snapshots provide local rollback/versioning, while Restic to Backblaze B2 remains the independent off-site backup layer.

Future capacity upgrades can replace the two mirror members one at a time with larger drives, allowing the mirror to expand after both members have been replaced and resilvered.

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
4. Restic/B2 backups and recovery are confirmed.

Immich should remain a convenient photo library rather than the only copy or organizational structure for GFX RAW files.

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

## yamanaka

Yamanaka will hold persistent state for non-media self-hosted applications.

The target host is a small SFF system running Debian with Docker Compose and NVMe application storage.

The planned logical layout is:

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

Yamanaka data should have an independent backup before the corresponding Kawaguchi copy is permanently removed.

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
└── GFX archive

yamanaka
└── non-media application state

saiko
└── lab / experimental VM storage
```

Services should remain close to the storage they primarily operate on. This is why media automation stays on Kawaguchi, photos remain on Motosu, and general personal applications move to Yamanaka.

## future documentation

Update this document when:

- Motosu has been rebuilt on TrueNAS SCALE
- ZFS datasets and snapshot policies are finalized
- the GFX archive layout is selected
- Yamanaka hardware and storage are selected
- Kawaguchi is cleaned after the migration
- the legacy uppercase `Media` share is removed
- the `roms` share is retired
- disk layout or pool configuration changes
- backup destinations and retention policies are finalized
