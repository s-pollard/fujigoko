# network

This document intentionally omits exact private addressing, VLAN IDs, MAC addresses, WAN details, management URLs, and other sensitive operational identifiers.

## current production topology

```text
internet
  |
Bluepeak ONT
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

### ISP handoff

- Bluepeak ONT
  - current fiber handoff to the production gateway
  - remains the ISP-side handoff when routing moves from the UDM-Pro to OPNsense

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
AT&T 620 ONT
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

Preferred AP power option:

- **TP-Link Omada POE370S** — preferred injector; purchase/deployment not confirmed
- 802.3af/at/bt Type 3, up to 60 W, with multi-gigabit/10 GbE data support
- preferred over the used MokerLink 10GINJ65W considered during equipment review
- verify the selected SFP+-to-copper module supports the AP's negotiated Ethernet speed; injector data capability does not change the AP uplink speed

The EAP775-Wall remains the target; the seller's EAP773 bundle does not replace it. The SX3016F remains the main core-switch candidate; the eight-port SX3008F was considered but is not a confirmed purchase.

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

- AdGuard Home runs on Yamanaka
- Yamanaka also serves private/split DNS for the internal application namespace
- a wildcard private rewrite sends application names to the Yamanaka reverse-proxy entry point
- exact resolver addresses and application hostnames remain private operational configuration

Target:

```text
lan clients
  |-- DNS --> yamanaka / AdGuard Home
  `-- DNS --> motosu / AdGuard Home
```

Both instances should provide equivalent filtering and private application-DNS policy while remaining on separate physical hosts. Exact resolver addresses and synchronization details are private operational configuration.

## private application access

User-facing Yamanaka applications now use a private HTTPS front door:

```text
trusted LAN / Tailscale client
          |
      private DNS
          |
        Caddy
          |
   Yamanaka applications
```

Policy:

- private application names are intended to resolve only through trusted network paths
- direct public-internet exposure is not part of the design
- trusted LAN and Tailscale access are both acceptable
- Caddy terminates HTTPS and reverse-proxies user-facing applications
- certificate issuance uses DNS-01 validation so inbound public HTTP exposure is unnecessary
- Pocket ID provides OIDC/passkey identity for applications where native SSO is useful
- services without a meaningful login requirement do not need an added authentication layer solely for uniformity
- direct container ports should be treated as implementation details and reduced where practical over time, but this is not required for the current trusted-LAN model

Do not publish the private application namespace, callback URLs, identity-provider client identifiers, API tokens, or reverse-proxy credentials in this repository.

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

Do not add WAN/public IPs, exact private IP assignments, DHCP reservations, MAC addresses, serial numbers, VPN keys/endpoints, management credentials, application hostnames, SSO client identifiers, callback URLs, or personal location details.
