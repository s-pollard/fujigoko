# yamanaka recovery

## purpose

Restore Yamanaka after host, storage, Docker, or application failure.

Yamanaka will hold personal application state, so recovery prioritizes databases and persistent application data over convenience services.

The runbook remains partly provisional until the production application NVMe, final Docker layout, backup jobs, and network configuration are fully deployed.

## host baseline

```text
hardware        Dell OptiPlex 3070 SFF
cpu             Intel Core i5-9500, 6C/6T
memory          16 GB DDR4-2666
memory maximum  32 GB
os              Debian GNU/Linux 13 (trixie)
boot            UEFI
boot nvme       Patriot P300 128 GB
app nvme        500 GB device planned/ordered
network         onboard 1 GbE; Intel X520-DA2 upgrade planned/ordered
```

Do not treat 32 GB RAM as a recovery requirement. Upgrade only if measured workload justifies it.

## expected role

Yamanaka hosts retained non-media applications, centralized monitoring, and one of the two target AdGuard Home resolvers.

Expected workloads include:

- Paperless-ngx
- Mealie
- Actual Budget
- HomeBox
- Linkwarden + PostgreSQL
- Stirling PDF
- Endurain + PostgreSQL + Redis
- Homepage
- Prometheus
- Grafana
- Loki
- AdGuard Home

Game servers and disposable lab workloads belong in gusuku.

## recovery order

```text
1. restore host/network access
2. restore application storage
3. restore Docker + Compose
4. restore Compose definitions
5. restore persistent files
6. restore databases
7. restore high-value applications
8. restore utilities
9. restore monitoring and DNS
10. verify independent backup to motosu
```

## expected layout

Target pattern:

```text
/srv/
├── compose/
└── data/
```

Do not assume a more specific directory tree is final until the production application storage is deployed and documented.

## host-only failure

If application storage remains intact:

1. repair/reinstall Debian
2. restore hostname/networking
3. install Docker Engine and Docker Compose
4. restore Compose definitions
5. verify data mounts before starting containers
6. start stacks in dependency order
7. verify database-backed applications before low-value utilities
8. restore AdGuard only after basic host networking is stable

Do not create empty application directories over existing data paths.

## application-storage loss

If the Yamanaka application NVMe is lost:

1. stop writes to failed storage
2. prepare replacement storage
3. recreate the documented filesystem/layout
4. restore independent backups from Motosu
5. restore database dumps before dependent applications
6. restore file/document data
7. restore Compose definitions
8. start applications in dependency order

High-value recovery priority:

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
Prometheus/Loki history
Stirling PDF
```

Historical metrics/logs are lower priority than personal application state.

## database-backed applications

### linkwarden

Restore PostgreSQL from a database-native backup, then start Linkwarden against the restored database. Verify users, saved links, collections/tags, and any separate file storage.

### paperless-ngx

Restore document/media files and required application/database state. Verify document count, representative files, OCR/search, tags/correspondents, and persistence after restart.

Redis is rebuildable unless future deployment documentation establishes otherwise.

### endurain

Restore PostgreSQL and required persistent files. Verify users, activities, settings, and representative history.

## simpler stateful applications

For Mealie, Actual Budget, and HomeBox:

1. restore application data
2. recreate the Compose stack
3. verify login and representative records
4. confirm new writes survive container recreation/reboot

## monitoring

Restore configuration before historical data.

Priority:

```text
1. Grafana configuration/dashboards
2. Prometheus configuration and scrape targets
3. Loki configuration
4. historical metrics/logs if worth preserving
```

Verify production targets such as Kawaguchi, Motosu, and Yamanaka. Gusuku is not part of the required Fujigoko monitoring dependency chain.

Uptime Kuma remains on Kawaguchi so Yamanaka downtime can be detected independently.

## DNS

Yamanaka is one of two target AdGuard Home resolvers; Motosu is the other.

Do not make host recovery depend on Yamanaka DNS already working. Restore basic host/network access first, then AdGuard. During deployment/transition, verify which resolver is actually live rather than assuming the target redundant pair is complete.

## complete host replacement

If the OptiPlex itself is replaced:

1. install Debian
2. configure hostname/network
3. prepare suitable local application storage
4. install Docker + Compose
5. recreate the documented storage layout
6. restore Compose definitions
7. restore independent backups from Motosu
8. restore database-backed services individually
9. restore remaining applications
10. update client-facing references if addressing changes
11. verify backups before declaring recovery complete

Replacement hardware does not need to duplicate the OptiPlex exactly. The recovery contract is Debian, Docker Compose, sufficient local storage/networking, and adequate CPU/memory.

## completion criteria

Recovery is complete when:

- Yamanaka boots reliably
- application storage is healthy and mounted
- Docker/Compose stacks survive reboot
- retained applications show expected data
- Paperless documents and other high-value records are readable
- monitoring works
- DNS works according to the currently deployed resolver design
- no application depends on old Kawaguchi state
- an independent backup to Motosu succeeds
- the repository reflects the deployed state
