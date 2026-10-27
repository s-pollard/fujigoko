# topology

This document shows useful production infrastructure relationships without publishing exact addressing or other sensitive operational identifiers.

## current topology

```text
                         internet
                            |
                     AT&T 620 ONT
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
                  truenas     lite
```

Current notes:

- U7 Pro is attached to the aggregation switch and has a 2.5 GbE-capable uplink.
- Kawaguchi uses 10 GbE to the aggregation layer.
- Motosu reaches the network through the access-switch path (USW-Lite-8-PoE). Its storage/Immich rebuild is complete and validated.
- Exact switch-port assignments are intentionally omitted from the public repo.

## target topology

```text
                       AT&T 620 ONT
                            |
                         opnsense
                            |
                    core / aggregation
                    /       |        \
                   /        |         \
          kawaguchi      motosu      yamanaka
            media         photos       apps
                           + backups    + monitoring
                           + dns        + dns

             target wireless: EAP775-Wall
             future core candidate: SX3016F
```

Target state:

- OPNsense is the production router/firewall.
- UDM-Pro leaves the routing path after the replacement network is stable.
- TP-Link Omada SX3016F is the main future core-switch candidate, not deployed hardware.
- TP-Link Omada EAP775-Wall is the planned target AP.
- Yamanaka and Motosu provide redundant AdGuard Home DNS.
- experimental/lab infrastructure belongs in gusuku and is not part of the Fujigoko production topology.
- exact VLANs, IP reservations, physical ports, management URLs, and WAN details stay out of the public repository.

## DNS flow

Current:

```text
lan client -> adguard on yamanaka -> upstream resolver
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

Yamanaka hosts the production non-media applications and their application-local PostgreSQL/Redis dependencies. Those supporting databases and caches remain private to their relevant Compose networks unless external access is explicitly required.

Kawaguchi no longer hosts transitional copies of retained non-media applications; that migration and cleanup are complete.

Motosu Immich stack:

```text
immich
├── server
├── postgres
├── redis/valkey
└── machine learning
```

## management note

If UniFi switching remains after the UDM-Pro is sold, establish a replacement UniFi Network controller/management method first. The Omada AP management method is selected separately.
