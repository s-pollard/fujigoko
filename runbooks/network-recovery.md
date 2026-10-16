# network recovery

## purpose

Restore basic Fujigoko network connectivity after gateway, switch, VLAN, or addressing failure.

The goal is to recover trusted LAN connectivity first, then restore segmentation and nonessential network services.

## current pre-move core path

```text
internet
  |
bluepeak
  |
udm-pro
  |
10 gbe
  |
usw-aggregation
  |-- kawaguchi
  |-- u7 pro
  `-- usw-lite-8-poe
       |-- motosu
       `-- doorbell lite
```

Current known host addresses:

```text
kawaguchi  192.168.1.220
motosu     192.168.1.169
adguard    192.168.1.53
```

Current VLANs:

```text
default/trusted  192.168.1.0/24
IoT VLAN 20      192.168.20.0/24
Servers VLAN 30  192.168.30.0/24
```

## Miami target core path

```text
AT&T
  |
opnsense
  |
core switching
(SX3016F main candidate)
  |-- kawaguchi
  |-- motosu
  |-- yamanaka
  `-- access / AP switching
```

The OPNsense appliance is the permanent Miami router/firewall. The UDM-Pro remains relevant only to the current pre-move network and will eventually be sold after the new network is stable.

## recovery order

```text
1. restore gateway + trusted LAN
2. restore switching uplinks
3. restore one known-good AP or wired admin path
4. restore server/NAS connectivity
5. restore DNS
6. restore VLANs/firewall policy
7. restore IoT and optional devices
8. verify Internet and inter-VLAN behavior
```

## gateway failure

### current pre-move UDM-Pro

If the UDM-Pro is unavailable before the Miami migration:

1. verify power
2. verify Bluepeak handoff/link
3. verify the UDM-Pro boots and can be reached locally
4. restore known-good UniFi configuration if required and available
5. verify trusted LAN DHCP/gateway function
6. confirm access to Kawaguchi and Motosu
7. restore VLANs and firewall rules only after basic LAN function is stable

### Miami OPNsense

After the Miami migration, if OPNsense is unavailable:

1. verify appliance power and physical WAN/LAN links
2. verify the AT&T handoff/gateway path is up
3. connect through a known-good management/LAN interface if normal switching is suspect
4. verify OPNsense boots and interfaces are assigned as documented
5. restore the latest known-good OPNsense configuration backup if necessary
6. restore trusted LAN DHCP/routing first
7. verify access to Kawaguchi, Motosu, and Yamanaka
8. restore DNS and then VLAN/firewall policy

Do not troubleshoot every downstream device before confirming the gateway itself works.

## switching failure

### current USW-Aggregation

Current important links:

```text
port 1 -> UDM-Pro
port 7 -> kawaguchi
port 8 -> USW-Lite-8-PoE
port 2 -> U7 Pro
```

The U7 Pro link speed should be re-verified after the move rather than assuming the old 10 GbE interpretation was correct.

If the aggregation switch fails, restore a temporary trusted-LAN path for critical hosts before reproducing the final topology. A direct or temporary lower-speed connection is acceptable during recovery.

### Miami core switch

The Mellanox SX3016F is the main candidate, not yet deployed hardware. Once the Miami switch is finalized, replace this section with actual ports and recovery steps.

### USW-Lite-8-PoE

Current important links:

```text
port 4 -> motosu
port 6 -> Doorbell Lite
port 7 -> USW-Aggregation uplink
```

If this switch fails, prioritize restoring Motosu connectivity; the doorbell is lower priority.

## DNS recovery

### current

Kawaguchi-hosted AdGuard Home at `192.168.1.53` is currently the only resolver handed out to trusted clients.

If it fails:

1. confirm Kawaguchi itself is reachable
2. confirm the AdGuard container is running and listening on port 53
3. if necessary, temporarily change DHCP/client DNS to a known external resolver to restore basic name resolution
4. fix AdGuard and return clients to the intended configuration

### target

Miami DNS is designed as two AdGuard Home instances:

```text
yamanaka + motosu
```

If one resolver fails, verify clients continue resolving through the other before changing infrastructure. Restore the failed instance without taking down the surviving resolver.

## VLAN recovery

### trusted/default

```text
subnet: 192.168.1.0/24
```

Purpose: trusted clients, Kawaguchi, Motosu, and core management in the current design.

### IoT

```text
VLAN: 20
subnet: 192.168.20.0/24
```

Expected current policy:

```text
trusted -> IoT     allow
IoT -> trusted     block
IoT -> internet    allow
```

### servers

```text
VLAN: 30
subnet: 192.168.30.0/24
gateway: 192.168.30.1
```

Expected current policy:

```text
trusted -> servers   allow
servers -> trusted   block new connections
servers -> internet  allow
```

Bandai historically used this network at `192.168.30.211`. That machine becomes Saiko and is not part of required production infrastructure.

The exact Miami VLAN/IP plan should be documented after the OPNsense rebuild rather than assumed to remain identical.

## verification

After basic recovery, verify from a trusted client:

```text
1. gateway reachable
2. internet reachable
3. DNS resolution works
4. kawaguchi reachable
5. motosu reachable
6. yamanaka reachable once deployed
7. active switches/APs reachable
8. inter-VLAN behavior matches the documented policy
```

Then verify application-level access such as Plex, Immich, and the Yamanaka application stack.

## power note

The APC Smart-UPS SMT2200RM2U is owned but is not expected to be usable in the initial Miami setup because the required receptacle will not be available. Do not assume UPS-backed runtime or automated shutdown exists until the Miami replacement power plan is documented and tested.

## completion criteria

Recovery is complete when:

- the active production gateway provides DHCP/routing normally
- DNS resolution works through the intended resolver design
- critical switches are reachable
- Kawaguchi, Motosu, and Yamanaka (when deployed) are reachable from trusted clients
- Internet access works
- VLAN segmentation matches the currently documented policy
- at least the intended active AP works
- critical self-hosted services are reachable
- documentation matches the recovered physical topology
