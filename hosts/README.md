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

- role: photo NAS / backup storage / Immich host
- hardware: UGREEN NASync DXP2800
- current platform: UGOS / Debian 12 base
- planned platform: TrueNAS SCALE
- planned boot device: Patriot P300 128 GB NVMe
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
- target responsibilities: Immich, phone photo sync, finished GFX photos, GFX RAW/archive storage, Yamanaka backup target, ZFS snapshots, Backblaze B2 backup, redundant AdGuard Home

Motosu is the storage/recovery anchor for irreplaceable photo data and important Yamanaka application backups. The ZFS mirror protects against a single-disk failure, local snapshots provide rollback/version history, and selected Motosu datasets are backed up off-site to Backblaze B2.

The TrueNAS migration is gated on independent recovery copies of Immich. A full copy has been made to the Samsung T7 migration SSD, the Immich library was verified byte-for-byte with SHA-256, and a valid PostgreSQL logical dump was created. The existing Restic/B2 repository remains the off-site recovery layer until the TrueNAS deployment and replacement backup jobs are proven.

## yamanaka

- role: always-on general application server
- status: hardware selected; base Debian deployment complete; hardware upgrades/application deployment in progress
- hardware: Dell OptiPlex 3070 SFF
- cpu: Intel Core i5-9500
- cpu layout: 6 cores / 6 threads
- platform: Debian GNU/Linux 13 (trixie)
- kernel: 6.12.113+deb13-amd64 at initial inventory
- boot: UEFI
- deployment: Docker Engine + Docker Compose planned
- memory: 16 GB installed as 2 × 8 GB SK hynix HMA81GU6JJR8N-VK DDR4-2666 UDIMM
- memory capacity: 32 GB maximum across 2 DIMM slots
- memory upgrade policy: remain at 16 GB initially; move to 2 × 16 GB only if real application usage justifies it
- current storage: Patriot P300 128 GB NVMe
- application storage: 500 GB NVMe ordered
- onboard network: Realtek RTL8111/8168-family 1 GbE
- network upgrade: low-profile Intel X520-DA2 dual-port 10 GbE SFP+ adapter ordered
- GPU: Intel UHD Graphics 630; no discrete GPU required
- remote access: SSH working
- target responsibilities: non-media self-hosted applications, centralized monitoring, redundant AdGuard Home

Yamanaka is intended to be simple production infrastructure rather than a virtualization or experimentation host. Important files, application exports, database dumps, and configuration backups from Yamanaka should be copied to Motosu, which then provides mirrored local storage, snapshots, and the path to off-site B2 protection.

The selected OptiPlex is intentionally being deployed with 16 GB first rather than upgrading memory preemptively. Docker workloads should be deployed and observed before deciding whether the 32 GB maximum is necessary.

## saiko

- role: Proxmox lab / experimentation
- status: packed / offline; Proxmox conversion planned after unpacking
- hardware: existing 4U system
- cpu: AMD Ryzen 9 3900X
- memory: 32 GB DDR4
- gpu: EVGA GeForce RTX 3060 Ti FTW3 Ultra 8 GB
- motherboard: MSI MPG X570 Gaming Edge WiFi
- storage: WD Blue 500 GB SSD currently documented
- current platform: Bazzite
- target platform: Proxmox VE
- network upgrade: Intel X520-DA2 dual-port 10 GbE SFP+ adapter ordered
- target responsibilities: OPNsense labs, Linux VMs, Kubernetes/k3s experiments, networking labs, temporary services, GPU passthrough or game-server experiments

Saiko should not carry required production services and can remain powered off when not in use. After unpacking, install and verify the X520-DA2 before converting the system from Bazzite to Proxmox VE.

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
