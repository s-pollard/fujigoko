# hosts

Exact private IPs, MAC addresses, serial numbers, WAN details, and other sensitive operational identifiers are intentionally excluded from this public repository.

## kawaguchi

- role: media server / bulk media storage
- hardware: UGREEN iDX6011 64GB AI NAS
- platform: Unraid 7.3.2
- cpu: Intel Core Ultra 5 125H
- memory: 64 GB
- network: 10 GbE uplink
- target responsibilities: Plex/media automation, manga, bulk media storage, Uptime Kuma, host-specific monitoring

Storage summary:

- six HDDs in the Unraid array
- two Samsung 970 EVO Plus 1 TB NVMe devices in the cache pool
- main shares include appdata, downloads, media, domains, isos, system, and legacy/cleanup candidates

Kawaguchi remains on Unraid for the current generation.

## motosu

- role: photo NAS / Immich host / local backup target
- hardware: UGREEN NASync DXP2800
- cpu: Intel N100
- memory: 8 GB
- network: 2.5 GbE onboard
- platform: TrueNAS SCALE
- storage: 2 × 6 TB Seagate ST6000NM0024 HDDs in mirrored ZFS storage
- target responsibilities: Immich, photo/archive storage, Yamanaka backups, snapshots, selected B2 backup, redundant AdGuard Home

Current restore state:

- TrueNAS SCALE is installed
- the Motosu pool and photo/Immich dataset are created
- the Immich library has been copied onto the rebuilt system
- application/database restoration is still being completed and validated

Do not describe Motosu as still awaiting the TrueNAS migration.

## yamanaka

- role: always-on general application server
- status: base Debian deployment complete; hardware/application deployment in progress
- hardware: Dell OptiPlex 3070 Small Form Factor
- cpu: Intel Core i5-9500
- platform: Debian GNU/Linux 13 (trixie)
- memory: 16 GB DDR4-2666 installed
- documented memory maximum: 32 GB across 2 DIMM slots
- memory policy: upgrade only if measured usage justifies it
- current/boot NVMe: Patriot P300 128 GB
- application NVMe: 500 GB device planned/ordered for production application storage
- network upgrade: low-profile Intel X520-DA2 dual-port 10 GbE SFP+ adapter planned/ordered
- target responsibilities: retained non-media applications, centralized monitoring, redundant AdGuard Home

Important Yamanaka files, exports, database dumps, and configuration backups should be copied independently to Motosu.

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
