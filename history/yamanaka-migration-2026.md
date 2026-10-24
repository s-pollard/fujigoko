# yamanaka migration record

Archived historical record. This migration is complete; current deployed state is documented in the active architecture, host, service, storage, backup, and runbook documents.

## goal

Move retained non-media self-hosted applications off `kawaguchi` and onto `yamanaka` without disrupting the media stack.

Current production role split:

```text
kawaguchi = media + manga + host-specific monitoring agent
motosu    = photos + Immich + backup storage + redundant DNS target
yamanaka  = non-media applications + centralized monitoring/logging + DNS
shoji     = reserved / unassigned
```

Experimental/lab workloads belong in gusuku, not Yamanaka.

## status

Service cutover was completed on 2026-10-18. Kawaguchi cleanup was completed on 2026-10-20.

Completed:

- Debian 13 deployed on Yamanaka
- Docker Engine and Docker Compose installed
- retained non-media services migrated from Kawaguchi
- application-local PostgreSQL/Redis dependencies moved with their parent applications
- Prometheus and Grafana migrated
- Loki and Grafana Alloy deployed
- Uptime Kuma and Signal notification bridge deployed
- AdGuard Home moved from Kawaguchi to Yamanaka
- SearXNG deployed on Yamanaka
- Dockhand deployed on Yamanaka
- RomM and its MariaDB dependency retired and removed from Kawaguchi
- old shared Kawaguchi Redis retired and removed after dependency review
- migrated non-media containers removed from Kawaguchi
- unused Kawaguchi Docker images and dangling volumes pruned
- retired Kawaguchi appdata removed
- TitleCardMaker, Kometa, Lidarr, and Listenarr appdata removed
- Kawaguchi reduced to media/manga services plus cAdvisor
- Prometheus verified scraping Kawaguchi cAdvisor
- Yamanaka reboot-tested with expected production containers returning automatically

Remaining post-migration work:

- establish/verify independent Yamanaka backups on Motosu
- deploy the second AdGuard Home instance on Motosu
- continue routine Motosu backup/restore validation and storage maintenance

## deployed yamanaka platform

```text
hardware        Dell OptiPlex 3070 SFF
cpu             Intel Core i5-9500, 6C/6T
os              Debian GNU/Linux 13 (trixie)
memory          16 GB DDR4-2666
memory maximum  32 GB
storage         Patriot P300 512 GB NVMe
network         onboard 1 GbE; Intel X520-DA2 upgrade planned/ordered
container       Docker Engine + Docker Compose
remote access   SSH + Tailscale
```

The prior assumption that Yamanaka required 32 GB before deployment is retired. Measured post-migration usage shows substantial memory headroom, so 16 GB remains appropriate unless future workload measurements justify an upgrade.

## stays on kawaguchi

- Plex
- Sonarr
- Radarr
- SABnzbd
- Bazarr
- Seerr
- Tautulli
- Recyclarr
- Unpackerr
- Komga
- Komf
- Tachidesk
- cAdvisor and smartctl-exporter / host-specific monitoring agents

Kawaguchi remains the media/manga host. Retired non-media rollback containers and appdata have been removed.

## stays on motosu

- Immich stack
- photo/archive storage
- Yamanaka backup datasets
- TrueNAS/ZFS snapshot functionality
- selected B2 backup jobs
- second AdGuard Home instance in the target state

## deployed on yamanaka

### applications

- Paperless-ngx + Redis
- Mealie
- Actual Budget
- HomeBox
- Linkwarden + PostgreSQL
- Stirling PDF
- Endurain + PostgreSQL + Redis
- Homepage
- SearXNG

### monitoring / logging

- Prometheus
- Grafana
- Loki
- Grafana Alloy
- Uptime Kuma

### infrastructure / operations

- AdGuard Home
- signal-cli-rest-api
- Dockhand

Supporting databases/caches stay with the application they serve rather than becoming shared LAN infrastructure.

## monitoring relationship

```text
                yamanaka
   prometheus / grafana / loki / alloy
             /               \
     kawaguchi               motosu
      cAdvisor              storage/services

                yamanaka
              uptime kuma
             /          \
        kawaguchi       motosu
         uptime          uptime
```

Uptime Kuma currently runs on Yamanaka. This simplifies the production application host but means a total Yamanaka outage also removes that monitoring path.

## DNS state

Current:

```text
yamanaka -> adguard-home
```

Target redundant state:

```text
yamanaka -> adguard-home
motosu   -> adguard-home
```

The Yamanaka instance retained the existing resolver identity during cutover so clients did not require a DNS-address change. Exact addressing remains intentionally undocumented in this public repository.

## retired from kawaguchi

The migration rollback state has been retired and removed.

Removed items include:

- RomM
- MariaDB used by RomM
- old shared Redis state
- migrated non-media containers and their retired appdata
- TitleCardMaker
- Kometa
- Lidarr
- Listenarr

Docker cleanup also removed dangling anonymous volumes and unused images. The post-cleanup state was 14 active containers, 14 active images, no local Docker volumes, and no reclaimable Docker image/container space.

## persistence and backup rule

Important Yamanaka state should have an independent backup on Motosu.

Use database-native dumps or application-aware exports where appropriate. Do not treat direct copies of live PostgreSQL/Redis directories as the primary backup method.

Highest-value Yamanaka state includes:

- Paperless documents/database
- Actual Budget data
- Mealie data
- HomeBox data
- Linkwarden PostgreSQL + stored archive data
- Endurain PostgreSQL + application data
- Grafana configuration/dashboards where worth retaining
- AdGuard Home configuration
- Uptime Kuma configuration

Metrics/log history is lower priority than application state and configuration.

## cutover verification

The post-migration reboot test verified that the expected Yamanaka Compose stacks restart automatically.

Application checks confirmed normal HTTP responses for the migrated services. Loki returned ready after its normal startup delay. Endurain reached a healthy state after its backend startup completed.

Measured immediately after migration, the system used roughly 4.3 GiB of 15 GiB RAM with no swap usage and low CPU/load, leaving substantial capacity for the current workload.

## cleanup result

Kawaguchi cleanup is complete. Following the 2026-10-21 smartctl-exporter restoration, it carries the intended media/manga production stack plus cAdvisor and smartctl-exporter. See the [service record](../services/README.md#smartctl-exporter) for the restoration and verification details.

The remaining migration-related operational priority is independent Yamanaka backup coverage on Motosu rather than preservation of rollback copies on Kawaguchi.
