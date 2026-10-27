# hosts

Current physical inventory. Exact addressing and sensitive identifiers stay in private operational notes under [SECURITY.md](../SECURITY.md).

| Host | Role | Platform | Recorded networking |
| --- | --- | --- | --- |
| [kawaguchi](#kawaguchi) | Media / bulk storage | Unraid 7.3.2 | 10 GbE uplink |
| [motosu](#motosu) | Photos / Immich / backup target | TrueNAS SCALE | 2.5 GbE onboard |
| [yamanaka](#yamanaka) | General applications / shared infrastructure | Debian GNU/Linux 13 | Onboard 1 GbE; 10 GbE upgrade acquired, installation pending |
| [shoji](#shoji) | Reserved | Unassigned | Not assigned |
| [OPNsense appliance](#opnsense-router-appliance) | Target router/firewall; hardware acquired | Target: OPNsense | Recorded interfaces below |

Service lists and dependencies are maintained in [services](../services/README.md); pools, shares, and data paths are in [storage](../storage/README.md).

## kawaguchi

- hardware: UGREEN iDX6011 64GB AI NAS
- cpu: Intel Core Ultra 5 125H
- memory: 64 GB
- disks: six HDDs in the Unraid array
- cache devices: two Samsung 970 EVO Plus 1 TB NVMe devices

Kawaguchi remains on Unraid for the current generation. It retains media/manga services and host-specific monitoring agents; the completed non-media migration and cleanup are recorded in [history](../history/yamanaka-migration-2026.md).

## motosu

- hardware: UGREEN NASync DXP2800
- cpu: Intel N100
- memory: 8 GB
- deployed drives: 2 × 6 TB Seagate ST6000NM0024 HDDs
- storage arrangement: mirrored ZFS

Both drives are confirmed deployed. Further upgrades are opportunistic; see [storage](../storage/README.md#motosu). The earlier mirror replacement is recorded in [history](../history/motosu-storage-2026.md#mirror-replacement).

Motosu is deployed on TrueNAS SCALE with validated Immich restoration. Current storage health is summarized in [storage](../storage/README.md#motosu); protection, alerting, and restore evidence are in [backups](../backups/README.md#motosu). Remaining storage and second-DNS work is tracked in the [move checklist](../runbooks/move-checklist.md).

## yamanaka

- status: deployed and carrying production non-media workloads
- hardware: Dell OptiPlex 3070 Small Form Factor
- cpu: Intel Core i5-9500, 6 cores / 6 threads
- platform: Debian GNU/Linux 13 (trixie)
- boot: UEFI
- memory: 16 GB DDR4-2666 installed
- documented memory maximum: 32 GB across 2 DIMM slots
- memory policy: upgrade only if measured usage justifies it
- storage: single Patriot P300 512 GB NVMe
- network upgrade: low-profile Intel X520-DA2 dual-port 10 GbE SFP+ adapter acquired; installation pending
- container platform: Docker Engine + Docker Compose

The documented production workload fits comfortably within 16 GB. See [services](../services/README.md#yamanaka) for the application/infrastructure inventory and [backups](../backups/README.md#yamanaka) for independent protection.

## shoji

- role: reserved
- status: undecided

Do not assign Shoji a permanent purpose until a real production requirement justifies another host.

## gusuku boundary

The physical system formerly documented here as `saiko` moved to the separate [`gusuku`](https://github.com/s-pollard/gusuku) learning/experimentation lab and is now `shuri`. Shuri hardware and lab state belong there. See [naming](../architecture/naming.md#major-hosts--fuji-five-lakes) for the reserved lake names and [architecture](../architecture/README.md) for the production boundary.

## OPNsense router appliance

Hardware acquired for the target production router/firewall. Deployment and UDM-Pro retirement are governed by the [network plan](../network/README.md#target-network).

Verified/recorded hardware:

- Intel Core i5-8500
- 8 GB DDR4
- 128 GB SSD
- dual-port Intel 82599ES/X520-family 10 GbE SFP+ adapter
- dual-port Intel I350-family 1 GbE adapter
- Intel I219-LM 1 GbE onboard interface
- target platform: OPNsense

No reliable chassis/OEM model has been established; use the recorded components rather than inventing a model.

## personal administration workstations

[Aso, Ontake, Norikura, and Azuma](workstations.md) are personal PCs used to administer both environments. Aso is the primary workstation; the laptops provide alternative access.
