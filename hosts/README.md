# hosts

Exact private IPs, MAC addresses, serial numbers, WAN details, and other sensitive operational identifiers are intentionally excluded from this public repository.

## kawaguchi

- role: media server / bulk media storage
- hardware: UGREEN iDX6011 64GB AI NAS
- platform: Unraid 7.3.2
- network: 10 GbE uplink
- cpu: Intel Core Ultra 5 125H
- cpu layout: 14 cores / 18 threads
- memory: 64 GB installed
- remote access: Tailscale and WireGuard
- target responsibilities: media stack, manga, bulk media storage, Uptime Kuma, host-specific monitoring

### storage summary

- six HDDs in the Unraid array
- two Samsung 970 EVO Plus 1 TB NVMe devices in the cache pool
- roughly 54 TB exposed through `/mnt/user` at inventory time
- main shares: `appdata`, `downloads`, `media`, `roms`, `domains`, `isos`, `system`
- legacy cleanup candidate: uppercase `Media` share

Kawaguchi remains on Unraid for the current generation.

## motosu

- role: photo NAS / backup storage / Immich host
- hardware: UGREEN NASync DXP2800
- cpu: Intel N100
- cpu layout: 4 cores / 4 threads
- memory: 8 GB installed; about 7.5 GiB usable by the current OS
- onboard network: 2.5 GbE
- current platform: UGOS Pro / Debian-based system
- planned platform: TrueNAS SCALE
- planned boot device: Patriot P300 128 GB NVMe
- storage: 2 × 6 TB Seagate ST6000NM0024 drives
- current array/filesystem: Linux RAID1 + Btrfs
- planned array/filesystem: 2-disk ZFS mirror
- remote access: Tailscale
- target responsibilities: Immich, phone photo sync, finished GFX photos, GFX RAW/archive storage, Yamanaka backup target, ZFS snapshots, Backblaze B2 backup, redundant AdGuard Home

The TrueNAS migration is gated on verified independent recovery copies of Immich. A full migration copy exists on a Samsung T7 external SSD, the Immich library was verified with SHA-256, and a PostgreSQL logical dump was created and validated.

## yamanaka

- role: always-on general application server
- status: base Debian deployment complete; hardware upgrades/application deployment in progress
- hardware: Dell OptiPlex 3070 Small Form Factor
- cpu: Intel Core i5-9500
- cpu layout: 6 cores / 6 threads
- platform: Debian GNU/Linux 13 (trixie)
- boot: UEFI
- deployment: Docker Engine + Docker Compose planned
- memory: 16 GB installed as 2 × 8 GB SK hynix HMA81GU6JJR8N-VK DDR4-2666 UDIMMs
- documented memory maximum: 32 GB across 2 DIMM slots
- memory policy: remain at 16 GB initially; upgrade only if measured usage justifies it
- current storage: Patriot P300 128 GB NVMe
- application storage: 500 GB NVMe ordered
- onboard network: Realtek RTL8111HSD-CG-family 1 GbE
- network upgrade: low-profile Intel X520-DA2 dual-port 10 GbE SFP+ adapter ordered
- GPU: Intel UHD Graphics 630; no discrete GPU required
- remote access: SSH
- target responsibilities: non-media self-hosted applications, centralized monitoring, redundant AdGuard Home

Important Yamanaka files, exports, database dumps, and configuration backups go to Motosu rather than depending on the Yamanaka system disk alone.

## saiko

- role: Proxmox lab / experimentation
- status: packed / offline; Proxmox conversion planned after unpacking
- hardware: existing 4U system
- cpu: AMD Ryzen 9 3900X
- memory: 32 GB DDR4
- gpu: EVGA GeForce RTX 3060 Ti FTW3 ULTRA GAMING 8 GB
- motherboard: MSI MPG X570 GAMING EDGE WIFI
- storage: WD Blue 500 GB SSD currently documented
- current platform: Bazzite
- target platform: Proxmox VE
- network upgrade: Intel X520-DA2 dual-port 10 GbE SFP+ adapter ordered
- target responsibilities: OPNsense labs, Linux VMs, Kubernetes/k3s experiments, networking labs, temporary services, GPU passthrough or game-server experiments

Saiko should not carry required production services and can remain powered off when not in use.

## shoji

- role: reserved
- status: undecided

Do not assign Shoji a permanent purpose until a real future role justifies another major host.

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

The appliance is documented by component because no reliable chassis/OEM model has been established. Do not invent a brand/model for the appliance itself.
