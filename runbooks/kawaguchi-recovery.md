# kawaguchi recovery

## purpose

Restore Kawaguchi as a media server after host, boot-device, cache, or configuration failure.

Kawaguchi is intentionally treated as more rebuildable than Motosu or Yamanaka. The priority is restoring configuration and service function, not immediately restoring every media file.

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
4. restore appdata/configuration
5. restore Docker services
6. verify media paths
7. verify media automation flow
8. reacquire replaceable content only as needed
```

## expected host state

Kawaguchi's permanent role is media and manga.

Expected retained services include:

```text
Plex
Sonarr
Radarr
SABnzbd
Bazarr
Seerr
Tautulli
Recyclarr
Unpackerr
Komga
Komf
Tachidesk
host-specific monitoring agent(s)
```

Non-media personal applications belong on Yamanaka once migration is complete.

## storage expectations

Primary paths:

```text
/mnt/user/media
/mnt/user/downloads
/mnt/user/appdata
```

Important media subpaths include:

```text
/mnt/user/media/movies
/mnt/user/media/tv
/mnt/user/media/music
/mnt/user/media/manga
```

Do not recreate the legacy uppercase `/mnt/user/Media` path unless a still-active dependency is verified.

## boot/config failure

If the Unraid boot device or configuration is lost:

1. obtain the most recent independent Unraid flash/config backup when one exists
2. recreate the Unraid boot device
3. restore configuration
4. verify disk assignments before starting the array
5. verify network configuration
6. start the array
7. confirm cache pool state
8. verify Docker and shares before enabling applications

If no usable flash backup exists, treat the current disk layout documentation and visible disk metadata as recovery aids rather than guessing assignments.

## cache/appdata failure

If the HDD media array is healthy but appdata/cache is lost:

1. preserve any readable cache data first
2. repair or replace the failed cache device/pool as appropriate
3. recreate the appdata location
4. restore media-service configuration from independent backup when available
5. recreate containers
6. verify bind mounts before starting applications

The bulk media should not need to be restored just because appdata was lost.

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

Movie and TV payloads are considered largely replaceable.

If media files are lost but automation configuration survives:

1. restore Sonarr/Radarr configuration first
2. verify indexers/download-client connectivity
3. verify root folders
4. let missing media be reacquired deliberately
5. avoid attempting to recover low-value replaceable files at the expense of configuration recovery

Treat manga separately if the content would be difficult to reacquire.

## completion criteria

Recovery is complete when:

- Unraid boots reliably
- expected disks and cache are online
- permanent media/manga containers are running
- Plex sees the expected libraries
- Sonarr/Radarr can import into the correct media paths
- SABnzbd can download to the expected path
- manga services can read the manga library
- no critical retained service depends on a removed legacy path
- the resulting state is reflected in the repository
