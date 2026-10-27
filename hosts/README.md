# hosts

Exact private IPs, MAC addresses, serial numbers, WAN details, and other sensitive operational identifiers are intentionally excluded from this public repository.

## kawaguchi

- role: media server / bulk media storage
- hardware: UGREEN iDX6011 64GB AI NAS
- platform: Unraid 7.3.2
- cpu: Intel Core Ultra 5 125H
- memory: 64 GB
- network: 10 GbE uplink
- current responsibilities: Plex/media automation, manga, bulk media storage, and host-specific monitoring via cAdvisor and the smartctl-exporter

Storage summary:

- six HDDs in the Unraid array
- two Samsung 970 EVO Plus 1 TB NVMe devices in the cache pool
- main shares include appdata, downloads, media, domains, isos, and system

Kawaguchi remains on Unraid for the current generation. The non-media migration cleanup is complete: retired containers were removed, unused images and volumes were pruned, and obsolete appdata for migrated/retired services was deleted. Kawaguchi now retains only the active media/manga stack plus cAdvisor and the smartctl-exporter.

## motosu

- role: photo NAS / Immich host / local backup target
- hardware: UGREEN NASync DXP2800
- cpu: Intel N100
- memory: 8 GB
- network: 2.5 GbE onboard
- platform: TrueNAS SCALE
- storage: mirrored ZFS storage on 2 × 6 TB Seagate ST6000NM0024 HDDs
- current responsibilities: Immich, photo/archive storage, snapshots, encrypted Backblaze B2 off-site backup, and future Yamanaka backup storage

Current state:

- TrueNAS SCALE migration is complete
- the Motosu pool and photo/Immich dataset are deployed
- Immich application/database restoration is complete and validated
- the restored photo library and subsequent Google Photos import are working normally
- the mirror was resilvered successfully after one HDD failed; the temporary replacement is an older spare and should be replaced with a better drive later
- selected photo data is uploading/backed up to Backblaze B2 using TrueNAS Cloud Sync with client-side remote encryption
- local snapshot policy is daily with 30-day retention for photos and 14-day retention for backups

Remaining Motosu work is tracked as operational follow-up rather than migration work:

- replace the temporary older mirror member with a better HDD, resilver, then verify SMART/scrub health
- verify periodic SMART testing and alerting
- perform and document a representative encrypted B2 restore test
- implement Yamanaka-to-Motosu backup jobs and retention
- add monitoring independent of Yamanaka so a Yamanaka outage can still be detected

Do not describe Motosu as still awaiting or validating the TrueNAS/Immich migration.

## yamanaka

- role: always-on general application server
- status: deployed and carrying production non-media workloads
- hardware: Dell OptiPlex 3070 Small Form Factor
- cpu: Intel Core i5-9500, 6 cores / 6 threads
- platform: Debian GNU/Linux 13 (trixie)
- memory: 16 GB DDR4-2666 installed
- documented memory maximum: 32 GB across 2 DIMM slots
- memory policy: upgrade only if measured usage justifies it
- storage: Patriot P300 512 GB NVMe
- network: onboard 1 GbE; low-profile Intel X520-DA2 dual-port 10 GbE SFP+ adapter planned/ordered
- container platform: Docker Engine + Docker Compose
- current responsibilities: retained non-media applications, FreshRSS, centralized monitoring/logging, Uptime Kuma, Signal notification bridge, AdGuard Home, private HTTPS/reverse proxying with Caddy, Pocket ID OIDC/passkey identity, SearXNG, and Dockhand

The deployed workload fits comfortably within the current 16 GB memory configuration. Important Yamanaka files, exports, database dumps, Pocket ID state, and configuration backups should be copied independently to Motosu.

## shoji

- role: reserved
- status: undecided

Do not assign Shoji a permanent purpose until a real production requirement justifies another host.

## gusuku boundary

The physical system formerly documented in Fujigoko as `saiko` has moved to the separate [`gusuku`](https://github.com/s-pollard/gusuku) learning/experimentation lab and is now `shuri`.

Do not duplicate Shuri hardware or lab-state documentation here. Fujigoko should only document the boundary: production services must not depend on gusuku.

## OPNsense router appliance

Target production router/firewall, replacing the UDM-Pro routing role.

Verified/recorded hardware:

- Intel Core i5-8500
- 8 GB DDR4
- 128 GB SSD
- dual-port Intel 82599ES/X520-family 10 GbE SFP+ adapter
- dual-port Intel I350-family 1 GbE adapter
- Intel I219-LM 1 GbE onboard interface
- target platform: OPNsense

No reliable chassis/OEM model has been established, so document the appliance by verified components rather than inventing a model.

## personal administration workstations

[Aso, Ontake, Norikura, and Azuma](workstations.md) are personal PCs used to administer both environments. Aso is the primary workstation and most powerful non-server PC; the laptops provide alternative access.
