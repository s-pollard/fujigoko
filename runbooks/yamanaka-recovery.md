# yamanaka recovery

## purpose

Restore Yamanaka after host, storage, Docker, or application failure.

Yamanaka will hold personal application state, so recovery should prioritize databases and persistent application data over convenience services.

Yamanaka hardware is now selected and the base Debian deployment exists. This runbook remains partly provisional until the production 500 GB NVMe, Docker layout, backup jobs, and final network configuration are deployed.

## host baseline

```text
hardware        Dell OptiPlex 3070 SFF
cpu             Intel Core i5-9500, 6C/6T
memory          16 GB DDR4-2666, 2 x 8 GB
memory maximum  32 GB
os              Debian GNU/Linux 13 (trixie)
boot            UEFI
current nvme    Patriot P300 128 GB
production nvme 500 GB ordered
onboard nic     Realtek 1 GbE
production nic  Intel X520-DA2 dual-port 10 GbE SFP+, ordered
```

Do not treat 32 GB RAM as a recovery requirement. The machine is intentionally starting with 16 GB; upgrade only if measured workload requires it.

## expected role

Yamanaka hosts non-media applications, centralized monitoring, and one of the two AdGuard Home DNS instances.

Expected workloads:

```text
Paperless-ngx
Mealie
Actual Budget
HomeBox
Linkwarden + PostgreSQL
Stirling PDF
Endurain + PostgreSQL + Redis
Homepage
Prometheus
Grafana
Loki
AdGuard Home
```

Game servers are outside Yamanaka's role.

## recovery order

```text
1. restore host/network access
2. restore production NVMe/filesystem
3. restore Docker + Compose capability
4. restore Compose definitions
5. restore persistent application files
6. restore databases
7. restore high-value applications
8. restore utilities
9. restore monitoring and DNS
10. verify backup jobs
```

## expected layout

Planned layout:

```text
/srv/
├── compose/
│   ├── paperless/
│   ├── mealie/
│   ├── actual-budget/
│   ├── homebox/
│   ├── linkwarden/
│   ├── stirling-pdf/
│   ├── endurain/
│   ├── homepage/
│   └── monitoring/
└── data/
    ├── paperless/
    ├── mealie/
    ├── actual-budget/
    ├── homebox/
    ├── linkwarden/
    ├── endurain/
    ├── homepage/
    ├── prometheus/
    ├── grafana/
    └── loki/
```

Do not assume these paths are final until the production NVMe and Docker stack are deployed and this repository is updated.

## host-only failure

If the production NVMe and persistent application data remain intact:

1. reinstall or repair Debian
2. restore hostname `yamanaka`
3. restore network configuration
4. install Docker Engine and Docker Compose
5. restore Compose definitions
6. verify persistent data mounts
7. start stacks one at a time
8. verify database-backed applications before utilities
9. verify AdGuard only after normal host networking is stable

Do not recreate empty application directories over existing data paths.

## production storage loss

If the Yamanaka application NVMe is lost:

1. stop attempting writes to failed storage
2. install/prepare replacement storage
3. recreate the documented filesystem and `/srv` layout
4. restore independent backups from Motosu
5. restore database dumps before starting dependent applications
6. restore file/document data
7. restore Compose definitions
8. start applications in dependency order

Priority order:

```text
Paperless
Actual Budget
HomeBox
Linkwarden
Mealie
Endurain
AdGuard configuration
Grafana configuration
Homepage
Prometheus history
Loki history
Stirling PDF
```

Prometheus/Loki historical data and cache state are lower priority than personal application state.

## database-backed applications

### linkwarden

Target dependency:

```text
linkwarden -> postgres
```

Restore PostgreSQL from a database-native backup, then start Linkwarden against the restored database.

Verify users, saved links, collections/tags, and any file storage.

### paperless-ngx

Restore both document/media files and required application metadata/database state.

Verify:

- document count
- representative PDFs/images open
- OCR/search works
- tags and correspondents exist
- consume/export paths are correct

Redis is rebuildable and should not block recovery if persistent Paperless state is intact.

### endurain

Restore the PostgreSQL backup and any required persistent application files.

Redis is treated as supporting cache/state unless deployment documentation later proves otherwise.

Verify users, activities, settings, and representative historical records.

## simple stateful applications

For Mealie, Actual Budget, and HomeBox:

1. restore application data from backup
2. recreate the Compose stack
3. verify login
4. verify representative records
5. confirm new writes persist after container recreation

## monitoring

Restore Grafana configuration before worrying about historical metrics if necessary.

Priority:

```text
1. Grafana configuration/dashboards
2. Prometheus configuration and scrape targets
3. Loki configuration
4. Prometheus/Loki historical data if worth preserving
```

Verify Kawaguchi, Motosu, Saiko, and Yamanaka scrape targets as applicable.

Uptime Kuma remains on Kawaguchi and should be able to detect Yamanaka downtime independently.

## DNS

Yamanaka is one of two target AdGuard Home resolvers; Motosu is the other.

A Yamanaka recovery should not require Yamanaka DNS to already be functional. Restore basic host/network access first, then restore AdGuard configuration and verify that clients still have a working resolver through Motosu during the recovery.

## complete host replacement

If the OptiPlex itself is replaced:

1. install Debian
2. configure hostname/network
3. install or attach suitable local application storage
4. install Docker + Compose
5. recreate the documented `/srv` structure or updated equivalent
6. restore Compose definitions
7. restore backups from Motosu
8. restore database-backed services individually
9. restore remaining applications
10. update DNS/bookmarks/reverse-proxy references if the address changed
11. configure and verify backups before declaring recovery complete

Replacement hardware does not need to duplicate the OptiPlex exactly. The recovery contract is Debian, Docker Compose, sufficient local storage, networking, and enough memory/CPU for the documented workloads.

## completion criteria

Recovery is complete when:

- Yamanaka boots reliably
- production storage is healthy and mounted correctly
- Docker/Compose stacks survive reboot
- all retained personal applications are accessible
- database-backed applications show expected data
- Paperless documents are readable
- Actual Budget/HomeBox/Mealie data is present
- monitoring works
- AdGuard works alongside the independent Motosu resolver
- no application depends on old Kawaguchi state
- an independent backup to Motosu runs successfully
- the repository reflects the deployed recovery state
