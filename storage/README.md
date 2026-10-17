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
- data drives: 2 × 6 TB Seagate ST6000NM0024
- primary storage: mirrored ZFS pool

The TrueNAS rebuild has occurred. Current migration state:

- the pool is created
- the photo/Immich dataset exists under `/mnt/motosu/photos/immich`
- the Immich library was copied onto the rebuilt system
- the final Immich database/application restore is still being completed and validated

The library migration copy transferred roughly 315 GB of data. The prior external migration copy and logical PostgreSQL dump remain recovery assets until the rebuilt Immich stack is proven.

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

ZFS mirror redundancy protects against a single-drive failure; it is not an independent backup. Snapshots provide local rollback, while Backblaze B2 provides the intended off-site layer for selected high-value data.

### photo policy

Immich is the convenient photo-library layer. GFX RAW/original files should also have a normal filesystem/archive structure rather than making Immich the only organizational copy.

### yamanaka backup role

Motosu is the independent local backup target for important Yamanaka data, including:

- application exports
- native database dumps
- important files
- Compose definitions
- service configuration

Database-backed services should use native dumps or application-aware exports rather than copies of live database directories.

## yamanaka

Yamanaka stores live non-media application state on local NVMe.

Expected high-value data includes Paperless documents/metadata, Actual Budget data, HomeBox inventory, Linkwarden data, Mealie data, Endurain state, monitoring configuration, and Compose/service configuration.

Bulk media and photo storage do not belong on Yamanaka.

Before removing a migrated service from Kawaguchi, verify the Yamanaka deployment and an independent Motosu backup.

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
├── Immich recovery data
└── Yamanaka backup copies

yamanaka
└── live non-media application state
```

Experimental/lab storage belongs in gusuku and is intentionally not part of the Fujigoko production-storage model.
