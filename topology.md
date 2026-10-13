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
                         2.5 gbe    1 gbe    10 gbe
                            |         |         |
                         u7 pro   usw-lite     kawaguchi
                                    8-poe       unraid
                                      |            |
                                    1 gbe          +-- docker services
                                      |            +-- /mnt/user/appdata
                                    motosu         +-- /mnt/user/media
                                  immich nas       +-- /mnt/user/downloads
                                      |            `-- /mnt/user/roms
                                      |
                                      +-- immich_server
                                      +-- immich_postgres
                                      +-- immich_redis
                                      `-- immich_machine_learning
```

## logical network overlay

```text
default / trusted — 192.168.1.0/24
├── kawaguchi — 192.168.1.220
└── motosu    — 192.168.1.169

iot — vlan 20 — 192.168.20.0/24

servers — vlan 30 — 192.168.30.0/24
└── bandai — 192.168.30.211
```

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
- This map should be updated when the physical network is rebuilt after the move.
