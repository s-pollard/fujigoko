# kawaguchi recovery

## purpose

Restore Kawaguchi as a media server after host, boot-device, cache, or configuration failure.

Kawaguchi is intentionally treated as more rebuildable than Motosu or Yamanaka. The priority is restoring configuration and service function, not restoring bulk media.

## first checks

Determine whether the problem is:

- network only
- Unraid boot/configuration failure
- cache/appdata failure
- array/disk failure
- Docker-only failure
- complete host failure

Before changing storage configuration, record the current disk assignments and visible device serials if possible.

## recovery order

```text
1. restore network reachability
2. restore Unraid boot/config
3. bring array/cache online safely
4. restore protected appdata/configuration from Motosu Restic
5. restore Docker services
6. verify media paths
7. verify media automation flow
8. reacquire replaceable content only as needed
```

## recovery references

- [Host baseline](../hosts/README.md#kawaguchi)
- [Retained services and dependencies](../services/README.md#kawaguchi)
- [Shares and media paths](../storage/README.md#kawaguchi)
- [Deployed backup policy and verification](../backups/README.md#kawaguchi)

Kawaguchi's permanent role is media and manga plus host-specific monitoring agents. Non-media personal applications have migrated to Yamanaka. Do not recreate the legacy uppercase `/mnt/user/Media` path unless a still-active dependency is verified.

## deployed backup source

Kawaguchi has an encrypted Restic repository on a dedicated Motosu ZFS dataset. Transfer uses a dedicated restricted SFTP account over Tailscale. Motosu protects the dataset with local snapshots and a separate Backblaze B2 Cloud Sync target.

The protected backup set contains selected Unraid configuration and selected application state. Bulk media, manga, downloads, caches, generated metadata, transcodes, monitoring-agent state, and the Restic recovery credentials themselves are intentionally excluded.

The Restic repository password must be recovered from the private credential store; it is not stored inside the staged backup tree or public repository. The SSH key can be replaced if necessary by provisioning a new restricted key on Motosu.

## boot/config failure

If the Unraid boot device or configuration is lost:

1. obtain the latest verified Kawaguchi Restic snapshot from Motosu
2. recover the staged Unraid flash configuration from that snapshot
3. recreate the Unraid boot device
4. restore the protected configuration
5. verify disk assignments before starting the array
6. verify network configuration
7. start the array
8. confirm cache pool state
9. verify Docker and shares before enabling applications

The staged flash copy excludes the private Restic password/key directory by design. Restore those recovery credentials separately from the private credential store when needed.

## cache/appdata failure

If the HDD media array is healthy but appdata/cache is lost:

1. preserve any readable cache data first
2. repair or replace the failed cache device/pool as appropriate
3. recreate the appdata location
4. restore the selected protected application state from the latest Kawaguchi Restic snapshot
5. recreate containers
6. verify bind mounts before starting applications

The bulk media should not need to be restored just because appdata was lost.

Protected application state includes the Arr/download stack configuration, Seerr, Tautulli, Komga/Komf/Tachidesk configuration/state, Plex database/application state, and selected Jellyfin state. Generated Plex/Jellyfin metadata, caches, transcodes, and logs are intentionally omitted and can be rebuilt.

## backup verification reference

The production path was tested end to end on 2026-10-28 and again after reboot.

Recorded successful verification:

- about 10.097 GiB logical snapshot size
- 17,946 source and restored regular files
- Restic repository check with no errors
- isolated restore from Motosu
- restored SHA-256 manifest validation
- symlink-definition comparison without following transient runtime targets

Tachidesk/KCEF can create transient Chromium-style symlinks whose targets disappear after restart. Recovery verification therefore compares symlink definitions rather than following those targets.

## Docker recovery

Recreate only the services that belong on Kawaguchi.

Verify dependencies in this order:

```text
SABnzbd -> downloads
Sonarr/Radarr -> downloads + media
Bazarr -> TV/movies
Plex -> media
Komga/Komf/Tachidesk -> manga
```

Then verify:

- container starts
- application UI loads
- expected mounts exist
- permissions allow read/write where required
- application sees existing data
- no application is pointing at obsolete Yamanaka-era or legacy paths

## monitoring verification

After restoring Docker services, verify cAdvisor and smartctl-exporter from Prometheus on Yamanaka. For smartctl-exporter, check both target reachability and actual device metrics; a reachable exporter alone does not establish device access.

Use the [smartctl-exporter runbook](smartctl-exporter.md) for the privileged/root runtime configuration, device-access issue, recorded device coverage, and verification limits. SMART PASSED is not proof that a disk is problem-free.

## media flow verification

Use a small test item rather than a large download.

Expected flow:

```text
SABnzbd
  -> /mnt/user/downloads
  -> Sonarr or Radarr
  -> /mnt/user/media/tv or movies
  -> Plex
```

Confirm Unpackerr and Bazarr only after the basic acquisition/import flow works.

## array/media loss

Movies, TV, music, manga, downloads, and other media payloads are outside the Kawaguchi Restic backup scope.

If media files are lost but automation configuration survives:

1. restore Sonarr/Radarr and related configuration first
2. verify indexers/download-client connectivity
3. verify root folders
4. let replaceable media be reacquired deliberately
5. handle non-automated media, including manga, according to whatever source or reacquisition path is available; do not expect it in the Kawaguchi Restic repository
6. avoid attempting to recover low-value replaceable files at the expense of configuration recovery

## completion criteria

Recovery is complete when:

- Unraid boots reliably
- expected disks and cache are online
- protected application state has been restored where needed
- permanent media/manga containers are running
- Plex sees the expected libraries
- Sonarr/Radarr can import into the correct media paths
- SABnzbd can download to the expected path
- manga services can read whatever manga library is present
- no critical retained service depends on a removed legacy path
- the resulting state is reflected in the repository
