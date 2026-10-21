# personal workstations

These personal PCs provide administration access to Fujigoko and Gusuku. Aso is the primary administration workstation and the most powerful non-server PC. Production services continue running when a workstation is offline.

| Host | Main use | Platform | CPU | Memory |
| --- | --- | --- | --- | --- |
| aso | Main desktop, gaming, photography, primary server administration | Arch Linux / KDE Plasma / Wayland | Ryzen 7 7800X3D, 8 cores / 16 threads | 32 GB Corsair DDR5, 2 × 16 GB, configured at 4800 MT/s |
| ontake | Main gaming laptop; alternative administration device | Bazzite 44 NVIDIA Open / KDE / Wayland | Core Ultra 9 285HX, 24 cores / 24 threads | 64 GB Micron DDR5, 2 × 32 GB, 6400 MT/s |
| norikura | Everyday portable use, browsing, off-site Tailscale tinkering | Arch Linux / COSMIC / Wayland | Core Ultra 7 165U, 12 cores / 14 threads | 32 GB Samsung soldered LPDDR5, configured at 6400 MT/s |
| azuma | Everyday portable use, browsing, off-site Tailscale tinkering | macOS 15.7.3 | Apple M2, 8 CPU cores / 10 GPU cores | 8 GB unified LPDDR5 |

## aso

- Gigabyte X670E AORUS XTREME motherboard
- AMD Radeon RX 7900 XTX
- Seagate FireCuda 520 500 GB NVMe: Arch Linux system, Btrfs
- Sabrent Rocket 4.0 2 TB NVMe: games
- WD_BLACK SN770 2 TB NVMe: photography
- Marvell/Aquantia AQC113C 10 GbE interface; observed link at 2.5 Gb/s
- separate Intel 82599-family 10 GbE interface
- Intel AX210-family Wi-Fi
- OpenSSH installed; Git, FreeRDP 3, Firefox, and Tailscale available
- Tailscale membership provides access to the existing tailnet; no gateway/exit-node role is assigned

## ontake

- MSI Raider 18 HX AI A2XWIG
- NVIDIA GeForce RTX 5080 Laptop GPU and Intel integrated graphics
- 18-inch 3840 × 2400 display, 120 Hz
- Phison 2 TB ESR02TBTLCA3-E1J-2MS and Samsung MZVL22T0HDLB-00BT7 2 TB NVMe SSDs
- both SSDs participate in the same Btrfs filesystem, labeled `bazzite`, approximately 3.72 TiB combined device capacity
- system and games share that filesystem; data/metadata allocation profiles are not yet recorded, so redundancy is not assumed
- Realtek RTL8125 2.5 GbE and Intel Wi-Fi 7
- SSH, Git, FreeRDP, Tailscale, WireGuard, OpenVPN, Podman, tmux, and Firefox available

## norikura

- Lenovo ThinkPad X1 Carbon Gen 12
- Intel integrated graphics
- 14-inch 1920 × 1200 display, 60 Hz
- SK hynix HFS001TEJ9X162N 1 TB NVMe, Btrfs
- Intel Wi-Fi
- SSH, Git, Tailscale, VS Code, and Firefox available

## azuma

- Apple MacBook Air, Mac14,15 / MQKX3LL/A
- Apple 512 GB SSD, APFS, FileVault enabled
- 2880 × 1864 Retina display
- Wi-Fi 6
- SSH, Git, Homebrew, Tailscale, screen, Ghostty, VS Code, Firefox, and Safari available

## backup and access boundary

Aso's photography images are backed up to Motosu. A whole-workstation backup is not established in this inventory.

Ontake, Norikura, and Azuma are not backed up. An old or accessible Time Machine backup detected on Azuma does not represent an active backup arrangement.

The laptops provide alternative administration devices if Aso is unavailable. Installed clients do not by themselves prove that every server login or remote-access path has been tested. Keep credentials, keys, exact addresses, and tailnet identifiers private.

Personal computers use Japanese mountain/volcano names. They remain personal clients rather than disposable Gusuku hosts. Detailed personal equipment notes are in [Home](https://github.com/s-pollard/home/tree/main/electronics/computers).
