# network

Network equipment, DNS, ingress, segmentation, and planned changes. Recorded physical links belong in [topology](topology.md). Exact addressing, VLAN IDs, MAC addresses, WAN details, and sensitive management configuration stay private; see [SECURITY.md](../SECURITY.md) and the [public-repo boundary](#public-repo-boundary).

## current hardware

| Component | Hardware | State / capability |
| --- | --- | --- |
| ISP handoff | Bluepeak ONT | Current fiber handoff; model unknown |
| Gateway/controller | Ubiquiti UniFi Dream Machine Pro | Current gateway and UniFi Network controller; eventual sale after replacement is proven |
| Aggregation | Ubiquiti UniFi Switch Aggregation (USW-Aggregation) | Current; 8 × 10 GbE SFP+ ports |
| Access/PoE | Ubiquiti UniFi Switch Lite 8 PoE | Current access/PoE switching |
| Active AP | Ubiquiti UniFi U7 Pro | Current; 2.5 GbE-capable uplink |
| Other APs | Ubiquiti UniFi U6 Enterprise, U6 Lite, AC Pro | Owned; may remain offline during move/rebuild |

See the [current topology](topology.md#current-topology) for recorded connections, including Yamanaka through USW-Lite-8-PoE and USW-Aggregation.

## target network

The [target topology](topology.md#target-topology) replaces UDM-Pro routing with a dedicated OPNsense appliance. USW-Aggregation can remain during transition. Do not retire/sell the UDM-Pro until replacement routing and required management functions are stable.

### ISP handoff

After relocation, the ISP will be AT&T. The plan is to request the 620 ONT; that model is requested target state, not confirmed supplied hardware.

### router / firewall

OPNsense is the target platform; appliance hardware is acquired. Verified/recorded components and the unknown chassis/OEM model are documented in [hosts](../hosts/README.md#opnsense-router-appliance).

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

| From | To | Policy |
| --- | --- | --- |
| Trusted | IoT | Allowed as needed |
| IoT | Trusted | Blocked by default |
| IoT | Internet | Allowed |
| Trusted | Servers | Allowed as needed |
| Servers | Trusted | New connections blocked by default |
| Servers | Internet | Allowed as needed |

Gusuku networking is separate and must not become a required Fujigoko dependency.

## dns

| State | Resolver placement | Behavior |
| --- | --- | --- |
| Current | AdGuard Home on Yamanaka | Filtering and private/split DNS; wildcard application rewrite to Caddy on Yamanaka |
| Target, after relocation | AdGuard Home on Yamanaka and Motosu | Equivalent filtering and private application-DNS policy on separate physical hosts |

The Motosu resolver is not yet deployed. Exact resolver addresses and synchronization details remain private operational configuration. Deployment and failover testing are in the [move checklist](../runbooks/move-checklist.md#3-redundant-dns).

## private application access

Trusted LAN and Tailscale clients use private application DNS names. Private DNS sends those names to Caddy on Yamanaka, which reverse-proxies user-facing services on Yamanaka, Kawaguchi, and Motosu. The namespace and DNS names remain in private operational configuration.

- Private application names are intended to resolve only through trusted network paths.
- Direct public-internet exposure is not part of the design.
- Caddy terminates HTTPS and uses DNS-01 certificate validation, so inbound public HTTP exposure is unnecessary.
- Provider tokens and reverse-proxy credentials remain in private runtime configuration.
- Pocket ID supplies OIDC/passkey identity where native integration is useful; [authentication policy](../architecture/README.md#private-access) and [verified integrations](../services/README.md#authentication) are maintained separately.
- Direct container ports are implementation details and should be reduced where practical over time; this is not required for the current trusted-LAN model.

Management UI destinations and access verification are recorded in [services](../services/README.md#private-application-access).

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
- final runtime thresholds should be based on actual deployed loads
- verify receptacle/input-plug compatibility before deployment

Lab/gusuku UPS decisions are outside this production-network document.

## public-repo boundary

Do not publish the private application namespace or application/management DNS names. Keep WAN/public IPs, exact private IP assignments, DHCP reservations, MAC addresses, serial numbers, VPN keys/endpoints, credentials, SSO client identifiers, callback URLs, and personal location details private under [SECURITY.md](../SECURITY.md).
