# yamanaka migration record

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

Service cutover is complete as of 2026-10-18.

Completed:

- Debian 13 deployed on Yamanaka
- Docker Engine and Docker Compose installed
- retained non-media services migrated from Kawaguchi
- application-local PostgreSQL/Redis dependencies moved with their parent applications
- Prometheus and Grafana migrated
- Loki and Grafana Alloy deployed
- Uptime Kuma and Signal notification bridge deployed
- AdGuard Home moved from Kawaguchi to Yamanaka
- RomM and its MariaDB dependency stopped on Kawaguchi
- old shared Kawaguchi Redis stopped after dependency review
- Kawaguchi reduced to media/manga services plus cAdvisor
- Prometheus verified scraping Kawaguchi cAdvisor
- Yamanaka reboot-tested with all expected containers returning automatically

Remaining post-migration work:

- establish/verify independent Yamanaka backups on Motosu
- deploy the second AdGuard Home instance on Motosu
- finish Motosu Immich application/database restoration
- observe the new Yamanaka deployment before deleting old Kawaguchi appdata
- remove retired Kawaguchi containers/appdata only after backup and rollback confidence is sufficient

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
- cAdvisor / host-specific monitoring agent

Kawaguchi remains the media/manga host. Old copies of migrated services are stopped and may remain temporarily as rollback material.

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

### monitoring / logging

- Prometheus
- Grafana
- Loki
- Grafana Alloy
- Uptime Kuma

### infrastructure

- AdGuard Home
- signal-cli-rest-api

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

RomM and MariaDB are stopped. Dependency checks found no retained running service requiring that MariaDB instance.

The old shared Redis instance is also stopped after confirming no remaining running service depended on it.

Do not delete their data immediately. Retain rollback material until the observation/backup window is complete.

## persistence and backup rule

Important Yamanaka state must have an independent backup on Motosu before old Kawaguchi state is permanently deleted.

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

## cleanup gate

Permanent cleanup of old Kawaguchi application state should happen only after:

```text
1. Yamanaka remains stable through an observation period
2. important application data has independent Motosu backup coverage
3. representative restores/exports are understood
4. no clients still point at retired Kawaguchi application endpoints
5. the second DNS instance on Motosu is deployed if redundant DNS is required
```

Until then, stopped old containers/appdata are rollback material, not active production services.
