# motosu storage record

Recorded from the existing documentation during the 2026-10-27 review; individual event dates were not recorded.

## TrueNAS and Immich migration

- TrueNAS SCALE was installed and the Motosu pool and photo/Immich dataset were created.
- The Immich library was copied to the rebuilt system and verified during migration.
- Immich application/database restoration was completed and validated.
- The subsequent Google Photos import was completed successfully; the restored library was operating normally.

Historical migration recovery material may be retained or retired according to recovery value. It is no longer the primary protection model; see [backups](../backups/README.md#motosu).

## mirror replacement

One HDD failed after the rebuild. It was replaced temporarily with the best available older spare. The resilver completed successfully, redundancy was restored, and the documented current mirror is healthy.

Replacing the temporary member with a better drive remains planned maintenance rather than an immediate fault response. The current member models need confirmation; see the [documentation review](documentation-review-2026-10-27.md#review-needed).

Current storage ownership is in [storage](../storage/README.md#motosu); replacement and validation work is in the [move checklist](../runbooks/move-checklist.md#6-motosu-storage-work).
