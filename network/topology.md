# topology

This document shows the useful infrastructure relationships without publishing exact addressing or other sensitive operational identifiers.

## current topology

```text
                         internet
                            |
                    current ISP handoff
                            |
                         udm-pro
                            |
                    usw-aggregation
                    /      |       \
                   /       |        \
              u7 pro   usw-lite   kawaguchi
                         8-poe       unraid
                        /    \
                   motosu   doorbell
                 immich nas   lite
```

Current notes:

- U7 Pro is attached to the aggregation switch and has a 2.5 GbE-capable uplink.
- Kawaguchi uses 10 GbE to the aggregation layer.
- Motosu currently reaches the network through the 1 GbE access switch even though its onboard NIC supports 2.5 GbE.
- Exact switch-port assignments are intentionally omitted from the public repo.

## target topology

```text
                       fiber handoff
                            |
                         opnsense
                            |
                    core / aggregation
                    /       |        \
                   /        |         \
          kawaguchi      motosu      yamanaka
            media         photos       apps
                           + backups    + monitoring
                                       + dns

             target wireless: EAP775-Wall
             future core candidate: SX3016F
```

Target state:

- OPNsense is the production router/firewall.
- UDM-Pro leaves the routing path after the replacement network is stable.
- TP-Link Omada SX3016F is the main future core-switch candidate, not deployed hardware.
- TP-Link Omada EAP775-Wall is the planned target AP.
- Yamanaka and Motosu provide redundant AdGuard Home DNS.
- Saiko remains a non-production Proxmox lab host.
- exact VLANs, IP reservations, physical ports, management URLs, and WAN details stay out of the public repository.

## DNS flow

Current:

```text
lan client -> temporary AdGuard on kawaguchi -> upstream resolver
```

Target:

```text
lan client
  |---> adguard on yamanaka
  `---> adguard on motosu
```

## media flow

```text
internet
   |
sabnzbd
   |
download storage
   |
   +--> sonarr --> tv ------+
   |                        |
   +--> radarr --> movies --+--> plex
   |
   `--> unpackerr
```

## application dependencies

Current transitional dependencies on Kawaguchi:

```text
linkwarden -> postgres
romm ------> mariadb
paperless -> redis
endurain --> postgres + redis
```

Motosu:

```text
immich
├── server
├── postgres
├── redis/valkey
└── machine learning
```

The non-media Kawaguchi dependencies disappear as retained applications move to Yamanaka.

## management note

If UniFi switching remains after the UDM-Pro is sold, establish a replacement UniFi Network controller/management method first. The Omada AP management method is selected separately.
