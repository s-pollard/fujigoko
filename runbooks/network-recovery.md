# network recovery

## purpose

Restore basic Fujigoko network connectivity after gateway, switch, VLAN, or addressing failure.

The goal is to recover trusted LAN connectivity first, then restore segmentation and nonessential network services.

## expected core path

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
```

Current VLANs:

```text
default/trusted  192.168.1.0/24
IoT VLAN 20      192.168.20.0/24
Servers VLAN 30  192.168.30.0/24
```

## recovery order

```text
1. restore gateway + trusted LAN
2. restore switching uplinks
3. restore one known-good AP or wired admin path
4. restore server/NAS connectivity
5. restore VLANs/firewall policy
6. restore IoT and optional devices
7. verify Internet and inter-VLAN behavior
```

## gateway failure

If the UDM-Pro is unavailable:

1. verify power and UPS state
2. verify Bluepeak handoff/link
3. verify the UDM-Pro boots and can be reached locally
4. restore known-good UniFi configuration if required and available
5. verify trusted LAN DHCP/gateway function
6. confirm access to `192.168.1.220` and `192.168.1.169`
7. restore VLANs and firewall rules only after basic LAN function is stable

Do not troubleshoot every downstream device before confirming the gateway itself works.

## switching failure

### aggregation switch

Expected important links:

```text
port 1 -> UDM-Pro
port 7 -> kawaguchi
port 8 -> USW-Lite-8-PoE
```

The U7 Pro is also attached to the aggregation switch, currently documented on port 2.

If the aggregation switch fails, restore a temporary trusted-LAN path for critical hosts before reproducing the final topology. A direct or temporary 1 GbE connection is acceptable during recovery.

### USW-Lite-8-PoE

Expected important links:

```text
port 4 -> motosu
port 6 -> Doorbell Lite
port 7 -> USW-Aggregation uplink
```

If this switch fails, prioritize restoring Motosu connectivity; the doorbell is lower priority.

## VLAN recovery

### trusted/default

```text
subnet: 192.168.1.0/24
```

Purpose: trusted clients, Kawaguchi, Motosu, and core management.

### IoT

```text
VLAN: 20
subnet: 192.168.20.0/24
```

Expected policy:

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

Expected policy:

```text
trusted -> servers   allow
servers -> trusted   block new connections
servers -> internet  allow
```

Bandai historically used this network at `192.168.30.211`, but it is not part of the current always-on target architecture.

## verification

After basic recovery, verify from a trusted client:

```text
1. gateway reachable
2. internet reachable
3. kawaguchi reachable
4. motosu reachable
5. UniFi devices adopt/connect normally
6. trusted clients can initiate toward Servers and IoT as intended
7. IoT cannot initiate new connections into trusted LAN
8. Servers cannot initiate new connections into trusted LAN
```

Then verify application-level access such as Plex and Immich.

## post-move note

The physical topology is currently documented from the pre-Miami/move-preparation state. Update this runbook after the Miami network is physically rebuilt.

Do not treat old switch-port assignments as immutable if cabling changes during the move.

## completion criteria

Recovery is complete when:

- UDM-Pro provides gateway/DHCP/routing normally
- critical switches are reachable
- Kawaguchi and Motosu are reachable from trusted clients
- Internet access works
- VLAN segmentation matches policy
- at least the intended active AP works
- critical self-hosted services are reachable
- documentation matches the recovered physical topology
