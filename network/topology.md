# topology

This document separates the current pre-move network from the planned Miami target state.

## current pre-move topology

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
                              /      |       \
                             /       |        \
                        u7 pro     1 gbe    10 gbe
                                     |         |
                                  usw-lite   kawaguchi
                                   8-poe       unraid
                                   /    \          |
                              1 gbe      fe         +-- docker services
                                |         |         +-- /mnt/user/appdata
                              motosu   doorbell     +-- /mnt/user/media
                            immich nas   lite       +-- /mnt/user/downloads
                                |                   +-- adguard-home 192.168.1.53
                                |                   `-- /mnt/user/roms
                                |
                                +-- immich_server
                                +-- immich_postgres
                                +-- immich_redis
                                `-- immich_machine_learning
```

The U7 Pro is connected to USW-Aggregation port 2. It is a 2.5 GbE-capable AP; the previously documented 10 GbE negotiated-link interpretation should not be treated as verified. Re-check the actual negotiated link after the Miami rebuild.

## current verified switch ports

```text
udm-pro
├── port 10 / sfp+ 1 -> bluepeak wan            10 gbe
└── port 11 / sfp+ 2 -> usw-aggregation port 1  10 gbe

usw-aggregation
├── port 1 -> udm-pro port 11                    10 gbe
├── port 2 -> u7 pro                             connected; speed to re-verify
├── port 7 -> kawaguchi                          10 gbe
└── port 8 -> usw-lite-8-poe port 7               1 gbe

usw-lite-8-poe
├── port 4 -> motosu                              1 gbe
├── port 6 -> doorbell lite                          fe
└── port 7 -> usw-aggregation port 8              1 gbe
```

## current logical network overlay

```text
default / trusted — 192.168.1.0/24
├── adguard-home — 192.168.1.53
├── kawaguchi    — 192.168.1.220
└── motosu       — 192.168.1.169

iot — vlan 20 — 192.168.20.0/24

servers — vlan 30 — 192.168.30.0/24
└── bandai — 192.168.30.211 — offline / packed for move
```

## current DNS flow

```text
lan client
   |
   | DHCP DNS = 192.168.1.53
   v
adguard-home
192.168.1.53
   |
   | DNS-over-HTTPS
   v
quad9
```

AdGuard Home currently runs on Kawaguchi but has its own `br0` address. It is the only DNS server handed out by the default/trusted UniFi network.

## target Miami topology

The exact switch and port layout remains pending the physical rebuild. The routing decision is settled; the core switch is not.

```text
                         AT&T fiber
                              |
                              v
                         OPNsense
                     i5-8500 appliance
                              |
                              v
                    core / aggregation
                  SX3016F main candidate
                    /       |        \
                   /        |         \
          kawaguchi      motosu      yamanaka
            media         photos       apps
                                         |
                                   monitoring + DNS

                    motosu also runs DNS
```

Target network state:

- OPNsense is the permanent router/firewall
- UDM-Pro leaves the production path and will eventually be sold
- SX3016F is the main core-switch candidate but is not yet treated as deployed hardware
- Yamanaka and Motosu provide redundant AdGuard Home DNS
- Saiko is a non-production Proxmox lab host and does not carry required infrastructure
- final VLANs, IP reservations, physical ports, and AP placement are re-documented after the Miami rebuild

## primary media flow

```text
internet
   |
sabnzbd
   |
/mnt/user/downloads
   |
   +--> sonarr --> /mnt/user/media/tv ------+
   |                                        |
   +--> radarr --> /mnt/user/media/movies --+--> plex
   |
   `--> unpackerr
```

## current application dependencies

```text
kawaguchi
├── linkwarden --> postgresql17-linkwarden :5432
├── romm -------> mariadb                  :3306
├── paperless --> redis                    :6379
└── endurain
    ├── endurain-postgres
    └── redis

motosu
└── immich_default
    ├── immich_server
    ├── immich_postgres
    ├── immich_redis
    └── immich_machine_learning
```

The non-media Kawaguchi dependencies are transitional and should disappear after the Yamanaka migration.

## notes

- The U7 Pro is the only currently active AP while preparing for the move.
- U6 Enterprise, U6 Lite, and AC Pro remain owned inventory but are intentionally offline.
- Bandai is offline and packed for the move; the machine becomes Saiko later.
- AdGuard Home at `192.168.1.53` is currently a single DNS dependency for the default/trusted network.
- The current APC SMT2200RM2U is not expected to be usable in the initial Miami setup because the required receptacle will not be available.
- Rebuild this map from actual links after the Miami physical network is installed.
