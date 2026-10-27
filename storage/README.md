# storage

This document records storage ownership and recovery value. It intentionally avoids exact private addresses, credentials, serial numbers, and other sensitive identifiers.

```text
kawaguchi = bulk media + media-service state
motosu    = photos + Immich + backup storage
yamanaka  = live non-media application state
```

## kawaguchi

Kawaguchi is the bulk-media host.

- platform: Unraid
- six HDDs in the main array
- two Samsung 970 EVO Plus 1 TB NVMe devices in the cache pool
- bulk movie/TV/download data is largely reacquirable
- configuration, metadata, manga state, and retained application state have higher recovery value than media payloads

Known production shares include appdata, downloads, media, domains, isos, and system. Legacy shares such as uppercase `Media` and `roms` should be removed only after dependency checks during cleanup.

Manga remains on Kawaguchi.

## motosu

Motosu is the dedicated photo/backup-storage host.

- platform: TrueNAS SCALE
- hardware: UGREEN NASync DXP2800
- data drives: 2 × 6 TB Seagate ST6000NM0024-class HDDs in mirrored ZFS storage
- Immich/photo data: `/mnt/motosu/photos/immich`

The TrueNAS and Immich migration is complete and validated. The photo library is operational on the rebuilt system, and subsequent Google Photos import work has been completed successfully.

One mirror member failed after the rebuild and was replaced temporarily with the best available older spare. The resilver completed successfully and redundancy was restored. Replacing that temporary member with a better drive remains planned maintenance rather than an immediate fault response.

### storage roles

```text
motosu
├── photos
│   ├── immich
│   └── gfx/archive data
├── backups
│   └── yamanaka
└── small service state
```

Exact dataset names beyond those already deployed should be documented only after they exist.

ZFS mirror redundancy protects against a single-drive failure; it is not an independent backup. Current local snapshot policy is daily with 30-day retention for photos and 14-day retention for backups. Selected high-value data is also protected off-site in Backblaze B2 through TrueNAS Cloud Sync with client-side remote encryption.

### photo policy

Immich is the convenient photo-library layer. GFX RAW/original files should also have a normal filesystem/archive structure rather than making Immich the only organizational copy.

### yamanaka backup role

Motosu is the deployed independent local backup target for important Yamanaka data.

The production flow is:

```text
Yamanaka application-aware exports/dumps
-> staged backup tree
-> encrypted Restic repository on Motosu
-> Motosu snapshots/local protection
-> scheduled TrueNAS Cloud Sync to Backblaze B2
```

The Yamanaka Restic policy keeps 14 daily, 8 weekly, and 6 monthly snapshots. Nightly backup and weekly restore verification are deployed, and the current backup tree has been restored byte-for-byte from Motosu successfully.

Protected state includes application exports, native database dumps, important persistent files, Compose definitions, and service configuration. PostgreSQL-backed services use native dumps; Vaultwarden's SQLite database is captured with SQLite's online backup mechanism rather than by blindly copying a live database.

A representative recovery originating from the B2 off-site copy remains intentionally deferred until the move.

## yamanaka

Yamanaka stores live non-media application state on local NVMe.

High-value state includes:

- Paperless documents and metadata
- Actual Budget data
- HomeBox inventory
- Linkwarden database/application state
- Mealie data
- Endurain database/application state
- Grocy data
- TriliumNext data
- Vaultwarden vault state and signing material
- Pocket ID identity state
- FreshRSS and Uptime Kuma state
- Grafana dashboards/configuration
- AdGuard, Caddy, monitoring, Compose, and other important service configuration

Bulk media and photo storage do not belong on Yamanaka.

Independent Yamanaka-to-Motosu backup coverage is deployed and restore-verified. For future migrations or new stateful applications, establish independent backup coverage and a representative recovery test before treating the new state as safely protected.

## ownership summary

```text
kawaguchi
├── bulk media
├── downloads
├── manga
└── media-service state

motosu
├── Immich/photo library
├── photo archive
├── encrypted off-site protection
└── Yamanaka Restic repository

yamanaka
└── live non-media application state
```

Experimental/lab storage belongs in gusuku and is intentionally not part of the Fujigoko production-storage model.
