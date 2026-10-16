# hosts

## kawaguchi

- role: media server / bulk media storage
- hardware: UGREEN iDX6011 6-Bay AI NAS
- platform: Unraid 7.3.2
- ip: `192.168.1.220`
- network: 10 GbE active link to USW-Aggregation
- cpu: Intel Core Ultra 5 125H
- cpu layout: 14 cores / 18 logical CPUs
- memory: 64 GB installed; 62 GiB reported usable by Unraid
- remote access: Tailscale and WireGuard
- target responsibilities: media stack, manga, bulk media storage, Uptime Kuma, host-specific monitoring

### storage summary

- six HDDs in the Unraid array
- two Samsung 970 EVO Plus 1 TB NVMe devices in the cache pool
- `/mnt/user` provides roughly 54 TB total, with about 31 TB used at inventory time
- main shares: `appdata`, `downloads`, `media`, `roms`, `domains`, `isos`, `system`
- legacy candidate: uppercase `Media` share, currently only referenced by an unused Komf `/library` mount

Kawaguchi remains on Unraid for the current generation. A future custom successor may be considered if very large HDDs and higher-capacity hardware become economical, but no migration is currently planned.

## motosu

- role: photo NAS / Immich host
- hardware: UGREEN NASync DXP2800
- current platform: UGOS / Debian 12 base
- planned platform: TrueNAS SCALE
- ip: `192.168.1.169`
- network interface: Intel I226-V 2.5 GbE
- current physical link: 1 GbE to USW-Lite-8-PoE
- cpu: Intel N100
- cpu layout: 4 cores / 4 threads
- ram: 7.5 GiB
- storage: 2 × 6 TB Seagate ST6000NM0024 drives
- current array/filesystem: Linux RAID1 + Btrfs
- planned array/filesystem: 2-disk ZFS mirror
- current main volume: `/volume1`
- remote access: Tailscale
- target responsibilities: Immich, phone photo sync, finished GFX photos, GFX RAW/archive storage, ZFS snapshots, Backblaze B2 backup, redundant AdGuard Home

The TrueNAS migration will be performed only after independent copies of Immich exist and can be verified. The existing Restic/B2 repository remains the off-site recovery layer.

## yamanaka

- role: always-on general application server
- status: planned; hardware selection in progress
- target platform: Debian
- deployment: Docker Engine + Docker Compose
- memory target: 32 GB
- storage target: 1–2 TB NVMe
- networking: 2.5 GbE preferred; add-in NIC acceptable
- GPU: not required
- form factor: flexible; small/low-power preferred, but SFF is not a hard requirement
- target responsibilities: non-media self-hosted applications, centralized monitoring, redundant AdGuard Home

Yamanaka is intended to be simple production infrastructure rather than a virtualization or experimentation host. Hardware selection should prioritize low idle power, sufficient RAM, reliable NVMe storage, and reasonable expandability over a specific chassis class.

## saiko

- role: Proxmox lab / experimentation
- status: planned conversion from the machine formerly named `bandai`
- hardware: existing 4U system
- cpu: AMD Ryzen 9 3900X
- memory: 32 GB DDR4
- gpu: EVGA GeForce RTX 3060 Ti FTW3 Ultra 8 GB
- motherboard: MSI MPG X570 Gaming Edge WiFi
- storage: WD Blue 500 GB SSD currently documented
- target platform: Proxmox VE
- target responsibilities: OPNsense labs, Linux VMs, Kubernetes/k3s experiments, networking labs, temporary services, GPU passthrough or game-server experiments

Saiko should not carry required production services and can remain powered off when not in use.

## shoji

- role: reserved
- status: undecided

Do not assign Shoji a permanent purpose until an actual future Fujigoko role justifies another major host or platform.

## opnsense router appliance

Planned Miami production router/firewall, replacing the UDM-Pro routing role.

- cpu: Intel Core i5-8500
- memory: 8 GB DDR4
- storage: 128 GB SSD
- 10 GbE: dual SFP+ Intel X520 / 82599ES-class adapter
- 1 GbE: dual-port Intel I350 adapter
- onboard NIC: Intel I219-LM 1 GbE
- platform: OPNsense
- target role: primary router/firewall for the Miami network

The UDM-Pro will remain in the current pre-move network and be sold after the Miami network is migrated and stable.