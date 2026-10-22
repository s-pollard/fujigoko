# network recovery

## purpose

Restore basic Fujigoko network connectivity after gateway, switch, DNS, VLAN, or addressing failure.

Exact IPs, VLAN IDs, MACs, WAN details, and management URLs are intentionally kept out of this public runbook.

## current core path

```text
internet
  |
current ISP handoff
  |
udm-pro
  |
usw-aggregation
  |-- kawaguchi
  |-- u7 pro
  `-- usw-lite-8-poe
       |-- motosu
       `-- doorbell lite
```

## target core path

```text
fiber handoff
  |
opnsense
  |
core / aggregation switching
  |-- kawaguchi
  |-- motosu
  |-- yamanaka
  `-- access / AP switching
```

The TP-Link Omada SX3016F is the main future core-switch candidate, not deployed hardware. The UDM-Pro remains relevant only until the replacement routing design is proven.

## recovery order

```text
1. restore gateway + trusted LAN
2. restore switching uplinks
3. restore one known-good wired/admin path or AP
4. restore core host connectivity
5. restore DNS
6. restore VLAN/firewall policy
7. restore IoT and optional devices
8. verify Internet and inter-segment behavior
```

## gateway failure

### current UDM-Pro

1. verify power and physical WAN/LAN links
2. verify the UDM-Pro boots and is reachable locally
3. restore a known-good UniFi configuration if required and available
4. verify trusted LAN DHCP/routing
5. verify Kawaguchi and Motosu are reachable
6. restore segmentation only after basic LAN function is stable

### target OPNsense

1. verify appliance power and WAN/LAN links
2. verify the fiber handoff path is up
3. use a known-good management/LAN interface if normal switching is suspect
4. verify OPNsense boots and interface assignments match private operational documentation
5. restore the latest known-good OPNsense configuration backup if necessary
6. restore trusted LAN DHCP/routing first
7. verify Kawaguchi, Motosu, and Yamanaka connectivity
8. restore DNS and then segmentation/firewall policy

Do not troubleshoot every downstream device before confirming the gateway itself works.

## switching failure

### USW-Aggregation

If the current aggregation switch fails, restore a temporary trusted-LAN path for critical hosts before reproducing the final topology. A temporary lower-speed connection is acceptable during recovery.

### future SX3016F

The **TP-Link Omada SX3016F** is only a candidate today. Add actual port assignments and recovery steps after purchase/deployment.

### USW-Lite-8-PoE

If the current access switch fails, prioritize restoring Motosu connectivity before lower-priority accessories.

## management-plane recovery

If the UDM-Pro is sold while UniFi switches remain, the replacement UniFi Network controller/management method must already exist and be documented privately.

The Omada EAP775-Wall management approach is selected independently. Do not make AP management a prerequisite for restoring basic wired routing.

## DNS recovery

### current

Yamanaka hosts the single AdGuard Home resolver.

If it fails:

1. confirm Yamanaka itself is reachable
2. confirm the AdGuard service is running
3. if necessary, temporarily point DHCP/clients at a trusted external resolver
4. repair AdGuard
5. return clients to the intended design

### target

Target DNS uses AdGuard Home on both Yamanaka and Motosu.

If one resolver fails, verify clients continue using the other before changing infrastructure. Restore the failed instance without taking down the surviving resolver.

## segmentation recovery

The intended policy is:

```text
trusted -> IoT        allowed as needed
IoT -> trusted        blocked by default
IoT -> internet       allowed

trusted -> servers    allowed as needed
servers -> trusted    blocked by default for new connections
servers -> internet   allowed as needed
```

Exact VLAN IDs, subnets, reservations, and gateway addresses belong in private operational documentation.

## verification

From a trusted client verify:

```text
1. gateway reachable
2. internet reachable
3. DNS resolution works
4. kawaguchi reachable
5. motosu reachable
6. yamanaka reachable when deployed
7. active switches/APs reachable as expected
8. segmentation policy behaves as intended
```

Then verify application access such as Plex, Immich, and the Yamanaka application stack.

## power note

Do not assume the existing APC Smart-UPS SMT2200RM2U is compatible with the available receptacle until the actual UPS input plug/nameplate and site circuit are checked.

The preferred server-UPS candidate is the CyberPower CP1500PFCRM2U; final NUT behavior, load, runtime, and shutdown thresholds must be tested after deployment.

## completion criteria

Recovery is complete when:

- the active gateway provides DHCP/routing normally
- DNS works through the intended resolver design
- critical switching is reachable
- production hosts are reachable from trusted clients
- Internet access works
- segmentation matches policy
- the intended AP/wired admin path works
- critical self-hosted services are reachable
- private operational documentation matches the recovered addressing/port state
