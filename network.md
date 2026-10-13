# network

## active physical topology

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
  |-- 10 gbe --> kawaguchi
  |-- 2.5 gbe -> u7 pro
  |
  `-- 1 gbe --> usw-lite-8-poe
                 |
                 `-- 1 gbe --> motosu
```

Only the U7 Pro is currently active on the wireless side while preparing for the move. Other owned UniFi APs are intentionally offline.

## unifi hardware inventory

### gateway / controller

- UDM-Pro
  - gateway
  - UniFi controller
  - 10 GbE SFP+ connectivity

### switching

- USW-Aggregation
  - eight 10 GbE SFP+ ports
- USW-Lite-8-PoE
  - eight 1 GbE ports
  - four PoE+ outputs
  - 52 W shared PoE budget

### wireless inventory

- U7 Pro — active
- U6 Enterprise — currently offline for move
- U6 Lite — currently offline for move
- AC Pro — currently offline for move

### power

- APC Smart-UPS SMT2200RM2U

## networks

### default / trusted

- subnet: `192.168.1.0/24`
- purpose: normal trusted clients and primary NAS/Unraid systems
- kawaguchi: `192.168.1.220`
- motosu: `192.168.1.169`

### iot

- vlan: `20`
- subnet: `192.168.20.0/24`
- purpose: IoT / smart-home devices
- default -> iot: allow
- iot -> default: block
- iot -> internet: allow

### servers

- vlan: `30`
- subnet: `192.168.30.0/24`
- gateway: `192.168.30.1`
- purpose: isolated server workloads
- default -> servers: allow
- servers -> default: block new connections
- servers -> internet: allow

## known server vlan host

- `bandai`
  - fixed ip: `192.168.30.211`
  - game server
  - WireGuard relay path documented separately in the home repo
