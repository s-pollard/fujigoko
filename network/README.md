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

### switching

- **TP-Link Omada SX3008F**
  - selected aggregation switch: 8 × 10 GbE SFP+ slots
  - not yet purchased, received, or deployed
  - existing USW-Aggregation can remain during transition
- **TP-Link Omada SG3218XP-M2 V2**
  - ordered on 2026-10-29; delivery and deployment pending
  - 16 × 2.5 GbE RJ45 ports and 2 × 10 GbE SFP+ slots
  - 4 × PoE++ ports and 12 × PoE+ ports; 240 W shared PoE budget
  - selected access switch for wired household devices and the wireless AP

This replaces the earlier SX3016F candidate and SG3210XHP-M2 eight-port access-switch option. Connect aggregation and access switching over a 10 GbE SFP+ link; final cabling and port assignments remain deployment decisions.

### target wireless

- **TP-Link Omada EAP775-Wall**
  - ordered on 2026-10-29; delivery and deployment pending
  - Wi-Fi 7 wall-plate AP
  - 2.5 GbE uplink
  - planned power: a PoE++ port on the SG3218XP-M2 V2, supporting the AP's downstream PoE functionality
  - no separate PoE injector required for this design

The previously considered POE370S injector is no longer part of the selected design. Final AP placement and controller/management method are deployment decisions.

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
| Current | AdGuard Home on Yamanaka | Filtering and private/split DNS; wildcard application rewrite to Caddy on Yamanaka; global DNS for Tailscale clients |
| Target, after relocation | AdGuard Home on Yamanaka and Motosu | Equivalent filtering and private application-DNS policy on separate physical hosts |

AdGuard Home on Yamanaka runs on a Docker macvlan network. Because the host cannot directly reach macvlan-attached containers through the parent interface, Yamanaka has a persistent host-side macvlan shim and host route for resolver reachability. This path is required for Yamanaka-originated and Tailscale-routed DNS traffic to reach AdGuard. Exact resolver and shim addresses remain private operational configuration.

Yamanaka's LAN address used as the private application-DNS target must remain stable. The current host networking therefore uses persistent static addressing rather than relying on a changing DHCP lease. Exact addresses remain private operational configuration. When changing resolver or interface settings, verify the host address before and after reloading the network client; an address change breaks the wildcard application-DNS path even when AdGuard and Caddy themselves are healthy.

Tailscale uses AdGuard Home as the global DNS resolver, so connected clients use the same filtering policy as trusted LAN clients. Private application DNS remains available through the same resolver path. Yamanaka advertises the trusted LAN subnet into Tailscale for private-service reachability.

The Motosu resolver is not yet deployed. Exact resolver addresses and synchronization details remain private operational configuration. Deployment and failover testing are in the [move checklist](../runbooks/move-checklist.md#3-redundant-dns).

### Caddy container DNS recovery

On 2026-10-29, Caddy's embedded Docker resolver returned SERVFAIL for the ACME directory hostname. Its generated resolver configuration reported no external nameservers, while host resolution and direct container queries to a public resolver succeeded. Explicit external DNS servers were added to the private Caddy Compose service, then only Caddy was recreated. Container DNS resolution recovered and the new Navidrome HTTPS route was verified. Preserve the service-level DNS configuration during recovery; successful Caddy configuration validation alone does not prove certificate issuance works.

Caddy's configuration is bind-mounted into the container. Editing the host Caddyfile with a tool that replaces the file inode can leave the running container attached to the old mounted file even though the host path shows the new content. After changing a bind-mounted Caddyfile, verify the file from inside the running container before relying on `caddy reload`; if host and container content differ, restart or recreate Caddy so the bind mount is re-established, then validate the active route.

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
