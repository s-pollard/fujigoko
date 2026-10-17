# network

This document intentionally omits exact private addressing, VLAN IDs, MAC addresses, WAN details, management URLs, and other sensitive operational identifiers.

## current physical topology

```text
internet
  |
current ISP handoff
  |
udm-pro
  |
usw-aggregation
  |-- u7 pro
  |-- kawaguchi
  `-- usw-lite-8-poe
       |-- motosu
       `-- doorbell lite
```

The U7 Pro is the currently active AP. Other owned UniFi APs are offline during the move/rebuild period.

## current hardware

### gateway / controller

- Ubiquiti UniFi Dream Machine Pro (UDM-Pro)
  - current production gateway
  - current UniFi Network controller
  - leaves the routing role after the replacement network is proven
  - planned for eventual sale

### switching

- Ubiquiti UniFi Switch Aggregation (USW-Aggregation)
  - 8 × 10 GbE SFP+ ports
  - current production aggregation switch
- Ubiquiti UniFi Switch Lite 8 PoE (USW-Lite-8-PoE)
  - 8 × 1 GbE ports
  - 4 PoE+ ports
  - 52 W shared PoE budget

### wireless inventory

- Ubiquiti UniFi U7 Pro — active; 2.5 GbE PoE+ uplink
- Ubiquiti UniFi U6 Enterprise — owned, currently offline
- Ubiquiti UniFi U6 Lite — owned, currently offline
- Ubiquiti UniFi AC Pro — owned, currently offline

The U7 Pro should not be documented as a 10 GbE AP. Ubiquiti specifies a 2.5 GbE RJ45 uplink.

## target network

```text
fiber handoff
     |
  OPNsense
     |
core / aggregation
     |
  hosts + access switching + APs
```

### router / firewall

The target OPNsense appliance uses:

- Intel Core i5-8500
- 8 GB DDR4
- 128 GB SSD
- dual-port Intel 82599ES/X520-family 10 GbE SFP+
- dual-port Intel I350-family 1 GbE
- Intel I219-LM onboard 1 GbE

No reliable OEM/chassis model is currently documented, so the appliance should be described by its verified components rather than assigned an invented brand/model.

### core-switch candidate

- **TP-Link Omada SX3016F**
  - main candidate; not yet purchased/deployed
  - 16 × 10 GbE SFP+ slots
  - 320 Gbps switching capacity
  - redundant internal power supplies

The SX3016F is a TP-Link Omada switch, not a Mellanox model.

### target wireless

- **TP-Link Omada EAP775-Wall**
  - planned target AP
  - Wi-Fi 7 tri-band wall-plate AP
  - 2 × 2.5 GbE ports, including the PoE input/uplink
  - additional 1 GbE access ports

Final AP placement and management/controller choice will be decided during deployment.

## management-plane dependency

Selling the UDM-Pro removes the current UniFi Network controller. If the USW-Aggregation or other UniFi devices remain in service, establish a replacement UniFi Network management method before the UDM-Pro is removed.

The Omada EAP775-Wall can be managed through an Omada controller or an appropriate standalone workflow; final controller placement is not yet selected.

## network policy

The current design separates trusted clients, IoT, and server/lab workloads. The important policy intent is retained here without publishing exact VLAN IDs or subnets:

```text
trusted -> IoT        allowed as needed
IoT -> trusted        blocked by default
IoT -> internet       allowed

trusted -> servers    allowed as needed
servers -> trusted    blocked by default for new connections
servers -> internet   allowed as needed
```

Exact VLAN IDs, subnets, reservations, and interface assignments belong in private operational documentation.

## DNS

Current state:

- AdGuard Home runs temporarily on Kawaguchi
- clients receive that resolver through DHCP
- Quad9 DNS-over-HTTPS is the current upstream design
- this is a single-resolver dependency

Target state:

```text
lan clients
  |-- DNS --> yamanaka / AdGuard Home
  `-- DNS --> motosu / AdGuard Home
```

Both resolver instances should remain on separate physical hosts and share equivalent policy/configuration. Exact resolver addresses and synchronization details are intentionally not published here.

## power

Owned/current power hardware:

- APC Smart-UPS SMT2200RM2U
  - 2200 VA-class 2U Smart-UPS
  - do not assume receptacle compatibility at the new site; verify the actual unit nameplate/input plug before deployment
- CyberPower BN1050M
  - existing smaller UPS

Preferred server-UPS candidate:

- CyberPower CP1500PFCRM2U
  - 1500 VA / 1000 W
  - 2U rackmount
  - pure sine wave / line-interactive
  - NEMA 5-15P input
  - USB management available
  - NUT integration should be verified during deployment rather than assumed from model name alone

Power strategy:

- Saiko is not required to be UPS-backed
- Yamanaka and Motosu should perform graceful shutdown on sustained battery operation
- networking should use a separate long-runtime UPS path if practical
- final load/runtime thresholds are documented only after the actual UPS topology is built and measured

## public-repo boundary

Do not add any of the following to this file:

- WAN/public IPs
- private IP assignments or DHCP reservations
- MAC addresses or device serial numbers
- VPN endpoints/keys
- management passwords or tokens
- exact physical address/location details
