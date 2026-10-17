# network

This document intentionally omits exact private addressing, VLAN IDs, MAC addresses, WAN details, management URLs, and other sensitive operational identifiers.

## current production topology

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

The U7 Pro is the currently active AP. Other owned UniFi APs may remain offline during the move/rebuild period.

## current hardware

### gateway / controller

- Ubiquiti UniFi Dream Machine Pro
  - current production gateway
  - current UniFi Network controller
  - leaves the routing role after the replacement network is proven
  - planned for eventual sale

### switching

- Ubiquiti UniFi Switch Aggregation (USW-Aggregation)
  - 8 × 10 GbE SFP+ ports
  - current production aggregation switch
- Ubiquiti UniFi Switch Lite 8 PoE
  - current access/PoE switching

### wireless inventory

- Ubiquiti UniFi U7 Pro — current active AP; 2.5 GbE-capable uplink
- Ubiquiti UniFi U6 Enterprise — owned
- Ubiquiti UniFi U6 Lite — owned
- Ubiquiti UniFi AC Pro — owned

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

The target OPNsense appliance has the following verified/recorded components:

- Intel Core i5-8500
- 8 GB DDR4
- 128 GB SSD
- dual-port Intel 82599ES/X520-family 10 GbE SFP+
- dual-port Intel I350-family 1 GbE
- Intel I219-LM onboard 1 GbE

No reliable OEM/chassis model is documented, so do not invent one.

### core-switch candidate

- **TP-Link Omada SX3016F**
  - main candidate; not yet purchased/deployed
  - 16 × 10 GbE SFP+ slots
  - redundant internal power supplies

### target wireless

- **TP-Link Omada EAP775-Wall**
  - planned target AP
  - Wi-Fi 7 wall-plate AP
  - 2.5 GbE-capable uplink/access connectivity

Final AP placement and controller/management method are deployment decisions.

## management-plane dependency

Selling the UDM-Pro removes the current UniFi Network controller. If UniFi switches remain in service, establish a replacement UniFi management method before removing the UDM-Pro.

## segmentation policy

The design separates trusted clients, IoT, and server workloads. Exact VLAN IDs and subnets remain private.

```text
trusted -> IoT        allowed as needed
IoT -> trusted        blocked by default
IoT -> internet       allowed

trusted -> servers    allowed as needed
servers -> trusted    blocked by default for new connections
servers -> internet   allowed as needed
```

Experimental gusuku networking is separate from this production design and must not become a required dependency for Fujigoko.

## DNS

Current:

- AdGuard Home runs temporarily on Kawaguchi
- this is a single-resolver dependency

Target:

```text
lan clients
  |-- DNS --> yamanaka / AdGuard Home
  `-- DNS --> motosu / AdGuard Home
```

Both instances should provide equivalent policy while remaining on separate physical hosts. Exact resolver addresses and synchronization details are private operational configuration.

## power

Owned/current power hardware includes an APC Smart-UPS SMT2200RM2U and a CyberPower BN1050M.

Preferred server-UPS candidate:

- CyberPower CP1500PFCRM2U
- 1500 VA / 1000 W
- 2U rackmount
- pure sine wave / line-interactive
- USB management

Production power goals:

- Yamanaka and Motosu should gracefully shut down on sustained battery operation
- networking should use a separate long-runtime UPS path if practical
- final runtime thresholds should be based on the actual deployed loads
- verify receptacle/input-plug compatibility before deployment

Lab/gusuku UPS decisions are intentionally outside this production-network document.

## public-repo boundary

Do not add WAN/public IPs, exact private IP assignments, DHCP reservations, MAC addresses, serial numbers, VPN keys/endpoints, management credentials, or personal location details.
