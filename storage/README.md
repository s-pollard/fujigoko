# storage

Storage ownership, pools, shares, and application data locations. Physical devices are recorded in [hosts](../hosts/README.md); schedules, retention, and recovery evidence are in [backups](../backups/README.md).

## ownership

| Host | Primary data | Recovery value |
| --- | --- | --- |
| Kawaguchi | Bulk media, downloads, manga, media-service state | Movie/TV/download payloads largely reacquirable; configuration, metadata, and manga can have greater recovery value |
| Motosu | Immich/photo library, photo/archive storage, Yamanaka Restic repository, small service state | Irreplaceable photos and independent Yamanaka recovery copies |
| Yamanaka | Live non-media application state on local NVMe | Personal records, databases, identity/vault state, service configuration |

Gusuku storage is outside the Fujigoko production model.

## kawaguchi

Unraid owns the bulk-media array and cache pool; device counts/models are in [hosts](../hosts/README.md#kawaguchi).

| Share / data | Recorded path |
| --- | --- |
| Media | `/mnt/user/media` |
| Movies | `/mnt/user/media/movies` |
| TV | `/mnt/user/media/tv` |
| Music | `/mnt/user/media/music` |
| Manga | `/mnt/user/media/manga` |
| Downloads | `/mnt/user/downloads` |
| Application state | `/mnt/user/appdata` |

Other recorded production shares: `domains`, `isos`, and `system`.

Legacy shares such as uppercase `Media` and `roms` should be removed only after dependency checks. Do not recreate `/mnt/user/Media` during recovery unless a still-active dependency is verified. Manga remains on Kawaguchi; the [backup policy](../backups/README.md#kawaguchi) intentionally treats routine media automation as reconstructable.

## motosu

TrueNAS SCALE owns mirrored ZFS storage. The current documented mirror is healthy after a temporary spare replacement; replacement is planned maintenance, not an immediate fault response. Migration, Google Photos import, and mirror incident details are in [history](../history/motosu-storage-2026.md). Current drive models still need [confirmation](../history/documentation-review-2026-10-27.md#review-needed).

| Data / role | Recorded location / state |
| --- | --- |
| Immich/photo library | `/mnt/motosu/photos/immich`; deployed and restoration validated |
| Photo/archive storage | Motosu photo-storage role; additional deployed dataset names are not recorded here |
| Yamanaka Restic repository | Dedicated Motosu backup dataset; exact path not recorded here |
| Small service state | Motosu; exact paths not recorded here |

The earlier `photos` / `backups/yamanaka` sketch described storage roles, not a complete deployed dataset inventory. Add exact dataset names only after they exist.

ZFS mirroring provides single-drive fault tolerance, not an independent backup. Snapshot and encrypted off-site protection are documented in [Motosu backups](../backups/README.md#motosu).

### photo policy

Immich is the convenient photo-library layer. GFX RAW/original files should also have a normal filesystem/archive structure rather than making Immich the only organizational copy.

The GFX archive's final primary location, recovery classification, and backup policy are still undecided. The prior layout sketch is not proof of a deployed GFX dataset. Resolve these during the [move](../runbooks/move-checklist.md#7-gfx-archive).

### yamanaka backup storage

Motosu is the deployed independent local target for Yamanaka's encrypted Restic repository. Application exports/dumps are staged on Yamanaka before transfer. Protected scope, off-site intent, schedules, retention, and byte-for-byte restore evidence belong in [Yamanaka backups](../backups/README.md#yamanaka).

## yamanaka

Live application state remains on local NVMe; bulk media and photo storage do not belong here.

| Recorded location | Scope |
| --- | --- |
| `/srv/compose`, `/srv/data`, `/srv/docker` | Production application/configuration roots; per-service mount mappings are not recorded here |
| `/srv/backup-export` | Staged application-aware backup tree before Restic transfer |

The production layout is primarily under these paths; this is not an exhaustive per-application mount inventory. Do not create empty application directories over existing/restored data.

High-value state includes documents, budgets, inventories, saved links, activities, Grocy/TriliumNext data, Vaultwarden vault/signing material, Kept database/data/configuration, and Pocket ID identity state. The complete protected set and capture methods are maintained in [backups](../backups/README.md#yamanaka); application-specific restore steps are in [Yamanaka recovery](../runbooks/yamanaka-recovery.md).
