# hosts

## kawaguchi

- role: primary homelab server
- platform: Unraid 7.3.2
- ip: `192.168.1.220`
- network: 10 GbE active link to USW-Aggregation
- cpu: Intel Core Ultra 5 125H
- cpu layout: 14 cores / 18 logical CPUs
- ram: 62 GiB
- remote access: Tailscale and WireGuard
- primary responsibilities: Docker services, media stack, monitoring, document/personal apps, bulk media storage

### storage summary

- six HDDs in the Unraid array
- two Samsung 970 EVO Plus 1 TB NVMe devices in the cache pool
- `/mnt/user` provides roughly 54 TB total, with about 31 TB used at inventory time
- main shares: `appdata`, `downloads`, `media`, `roms`, `domains`, `isos`, `system`
- legacy candidate: uppercase `Media` share, currently only referenced by an unused Komf `/library` mount

## motosu

- role: Immich NAS
- hardware: UGREEN NASync DXP2800
- platform: UGOS / Debian 12 base
- ip: `192.168.1.169`
- network interface: Intel I226-V 2.5 GbE
- current physical link: 1 GbE to USW-Lite-8-PoE
- cpu: Intel N100
- cpu layout: 4 cores / 4 threads
- ram: 7.5 GiB
- storage: 2 × 6 TB Seagate ST6000NM0024 drives
- array: Linux RAID1
- filesystem: Btrfs
- main volume: `/volume1`
- remote access: Tailscale
- primary responsibility: Immich photo library and related Docker services
