# services

This file records production service placement and dependencies without publishing private addresses, credentials, admin URLs, or other sensitive operational details.

## kawaguchi

### monitoring / infrastructure

- cAdvisor / host monitoring agent
- smartctl-exporter / SMART device metrics for Prometheus

### media

- Plex
- Sonarr
- Radarr
- SABnzbd
- Bazarr
- Seerr
- Tautulli
- Recyclarr
- Unpackerr

### manga

- Komga
- Komf
- Tachidesk

The former Kawaguchi copies of migrated non-media services have been removed. RomM, its MariaDB dependency, and other retired appdata have also been removed. Kawaguchi now contains only the active media/manga stack plus cAdvisor and the smartctl-exporter.

User-facing Kawaguchi applications are available through the private `plebworks.com` access layer via Caddy on Yamanaka. This has been verified from trusted clients.

Known dependency examples:

```text
sabnzbd -> download storage
sonarr  -> downloads + tv library
radarr  -> downloads + movie library
bazarr  -> tv + movie libraries
plex    -> media library
komga / komf / tachidesk -> manga library
```

### smartctl-exporter

Restored on 2026-10-21 by recreating the container from the saved Unraid template.

```text
container  smartctl-Exporter
image      prometheuscommunity/smartctl-exporter:latest
port       9633
mode       privileged
runtime    --user=0:0
```

The run configuration requires `--user=0:0`. The image's default user is `nobody`, which cannot open the block device nodes that smartctl reads. Setting `USER=root` as a container environment variable did not change the runtime user: an environment variable does not override the image's default user or the user selected at run time, so the runtime user had to be set to root in the template/run configuration.

Verified from Yamanaka on 2026-10-21: the Prometheus smartctl scrape target is UP and the exporter reports metrics for 9 devices. User-provided `docker inspect` output on Kawaguchi confirmed `Privileged=true`; subsequent `docker exec smartctl-Exporter id` output confirmed runtime uid 0. The exported `smartctl_device_smart_status` values are not evidence that all disks are problem-free; a PASSED SMART status does not rule out incipient failure, so this verification covers scrape health and device coverage only.

## motosu

Motosu is now a TrueNAS SCALE host.

Target/permanent service classes:

- Immich server
- Immich PostgreSQL
- Immich Valkey/Redis
- Immich machine learning
- storage/snapshot services provided by TrueNAS
- one AdGuard Home instance as the second DNS node

The Immich application/database restoration is complete and validated. The restored photo library is operating normally.

Immich is available through the private `plebworks.com` access layer via Caddy on Yamanaka, and this route has been verified from a trusted client.

Critical persistence is the Immich library, database recovery data, photo/archive data, and Yamanaka backup datasets. Redis/Valkey state and machine-learning caches are rebuildable.

## yamanaka

Yamanaka hosts the retained non-media production services migrated from Kawaguchi. Supporting databases/caches stay with the application they serve rather than becoming shared LAN infrastructure.

Current services:

### applications

- Paperless-ngx + private Redis
- Mealie
- Actual Budget
- HomeBox
- Linkwarden + PostgreSQL
- Stirling PDF
- Endurain + PostgreSQL + Redis
- Homepage
- SearXNG
- FreshRSS

### monitoring / logging

- Prometheus
- Grafana
- Loki
- Grafana Alloy
- Uptime Kuma

Prometheus continues to scrape cAdvisor on Kawaguchi for host/container metrics and the Kawaguchi smartctl-exporter for SMART device metrics. Alloy collects Yamanaka Docker logs into Loki for Grafana exploration.

### infrastructure / operations

- AdGuard Home
- Caddy reverse proxy / private HTTPS entry point
- Pocket ID identity provider for OIDC-capable applications
- signal-cli-rest-api for Uptime Kuma notifications
- Dockhand for Docker operations/management

The Yamanaka stack has been reboot-tested successfully and expected production containers return automatically.

### private application access and SSO

`plebworks.com` is the private application namespace for Fujigoko.

Yamanaka provides the common access layer for user-facing applications across all three active production hosts:

```text
trusted LAN / Tailscale
        |
 *.plebworks.com
        |
 private DNS
        |
 Yamanaka / Caddy
   |      |      |
Yamanaka Kawaguchi Motosu
```

- AdGuard Home provides the private wildcard DNS policy.
- Caddy terminates HTTPS and reverse-proxies services hosted on Yamanaka, Kawaguchi, and Motosu.
- The namespace is intended for trusted LAN and Tailscale clients, not direct public-internet exposure.
- Caddy uses DNS-01 certificate validation; credentials and provider tokens remain only in private runtime configuration.
- Pocket ID provides OIDC/passkey-based identity where the application supports it cleanly.
- Application-local authentication is retained where it is useful for API/mobile compatibility or as a recovery path.

Verified Pocket ID/OIDC integration currently includes:

- FreshRSS
- Actual Budget
- Mealie
- Linkwarden
- Grafana
- Stirling PDF
- Paperless-ngx

Do not add authentication in front of applications that intentionally have no login merely for consistency. The trusted LAN/Tailscale boundary is acceptable for low-risk convenience UIs unless requirements change.

Planned additions:

- Grocy — pantry/fridge/freezer inventory, quantities, expiration tracking, and barcode-oriented household inventory
- TriliumNext — structured personal notes, backlinks, and synchronized/offline-capable note access
- Nextcloud — general file sync/collaboration if retained after testing
- Vaultwarden — security-sensitive service with operational details kept private

These remain optional until actually deployed and found useful.

## DNS target

Current deployed state:

```text
yamanaka -> adguard-home -> private *.plebworks.com resolution
```

Target redundant state:

```text
yamanaka -> adguard-home
motosu   -> adguard-home
```

Both instances should provide equivalent filtering and private `plebworks.com` policy on separate physical hosts. Exact resolver addresses and synchronization details stay in private operational configuration.

## completed cleanup

Kawaguchi cleanup completed on 2026-10-20:

- migrated non-media containers removed
- RomM and MariaDB removed
- obsolete stopped containers removed
- dangling Docker volumes removed
- unused Docker images pruned
- retired appdata removed
- TitleCardMaker, Kometa, Lidarr, and Listenarr appdata removed

The resulting Docker state was 14 active containers, 14 active images, no local Docker volumes, and no reclaimable Docker image/container space.

## lab boundary

Disposable services, VMs, Kubernetes experiments, game servers, and other learning workloads belong in the separate gusuku lab. Fujigoko production services must not depend on them.
