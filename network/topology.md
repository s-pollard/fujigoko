# topology

This is the current working infrastructure map for Fujigoko. It reflects the active setup during move preparation rather than every owned device.

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
                          10 gbe    1 gbe    10 gbe
                            |         |         |
                         u7 pro   usw-lite     kawaguchi
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

## verified switch ports

```text
udm-pro
├── port 10 / sfp+ 1 -> bluepeak wan            10 gbe
└── port 11 / sfp+ 2 -> usw-aggregation port 1  10 gbe

usw-aggregation
├── port 1 -> udm-pro port 11                    10 gbe
├── port 2 -> u7 pro                             10 gbe
├── port 7 -> kawaguchi                          10 gbe
└── port 8 -> usw-lite-8-poe port 7               1 gbe

usw-lite-8-poe
├── port 4 -> motosu                              1 gbe
├── port 6 -> doorbell lite                          fe
└── port 7 -> usw-aggregation port 8              1 gbe
```

## logical network overlay

```text
default / trusted — 192.168.1.0/24
├── adguard-home — 192.168.1.53
├── kawaguchi    — 192.168.1.220
└── motosu       — 192.168.1.169

iot — vlan 20 — 192.168.20.0/24

servers — vlan 30 — 192.168.30.0/24
└── bandai — 192.168.30.211 — offline / packed for move
```

## dns flow

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

## primary service flow

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

## primary application dependencies

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

## notes

- The U7 Pro is the only currently active AP while preparing for the move.
- U6 Enterprise, U6 Lite, and AC Pro remain part of the hardware inventory but are intentionally offline.
- Bandai is offline and packed for the move.
- AdGuard Home at `192.168.1.53` is currently a single DNS dependency for the default/trusted network.
- This map should be updated when the physical network is rebuilt after the move.
