# yamanaka recovery

## purpose

Restore Yamanaka after host, storage, Docker, or application failure.

Yamanaka holds personal application state, so recovery prioritizes databases and persistent application data over convenience services.

## host baseline

```text
hardware        Dell OptiPlex 3070 SFF
cpu             Intel Core i5-9500, 6C/6T
memory          16 GB DDR4-2666
memory maximum  32 GB
os              Debian GNU/Linux 13 (trixie)
boot            UEFI
storage nvme    single NVMe, Patriot P300 512 GB
network         onboard 1 GbE; Intel X520-DA2 acquired for upgrade
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

## independent backup source

Yamanaka production state is backed up to a dedicated Restic repository on Motosu.

The deployed path is:

```text
Yamanaka application-aware exports/dumps
-> staged backup tree
-> Restic over SSH/SFTP
-> dedicated Motosu backup dataset
-> Motosu local protection
-> scheduled Backblaze B2 cloud sync
```

The repository password, SSH material, cloud credentials, bucket identifiers, and exact addressing are private and are not documented here.

Production backups run nightly through systemd. A weekly verification job restores the latest production snapshot to an isolated temporary location, verifies the SHA-256 manifest, performs a recursive 1:1 comparison against the staged source tree, and validates the restored PostgreSQL dump archives.

The current Restic retention policy keeps 14 daily, 8 weekly, and 6 monthly snapshots.

## recovery order

```text
1. restore host/network access
2. restore application storage
3. restore Docker + Compose
4. recover the latest suitable Restic snapshot from Motosu
5. restore Compose definitions and private environment/configuration
6. restore database dumps and application-aware exports
7. restore persistent application files
8. restore high-value applications
9. restore utilities, monitoring, and DNS
10. verify a new independent backup to Motosu
```

## expected layout

Current production data is primarily under:

```text
/srv/
├── compose/
├── data/
└── docker/
```

The independent backup uses a staged tree under `/srv/backup-export` before Restic commits the snapshot to Motosu.

Do not create empty application directories over existing/restored data paths.

## host-only failure

If application storage remains intact:

1. repair/reinstall Debian
2. restore hostname/networking
3. install Docker Engine and Docker Compose
4. restore Compose definitions if needed
5. verify data mounts before starting containers
6. start stacks in dependency order
7. verify database-backed applications before low-value utilities
8. restore AdGuard only after basic host networking is stable
9. run and verify a fresh backup to Motosu

## application-storage loss

If the Yamanaka application NVMe is lost:

1. stop writes to failed storage
2. prepare replacement storage
3. recreate the documented filesystem/layout
4. install Restic and establish the private Motosu repository access using recovery credentials
5. restore the selected production snapshot from Motosu to a temporary recovery location
6. verify the restored SHA-256 manifest before using the data
7. restore Compose definitions and private environment/configuration
8. restore database dumps before dependent applications
9. restore file/document/application state
10. start applications in dependency order
11. verify representative application data and persistence
12. run and verify a new independent backup before declaring recovery complete

High-value recovery priority:

```text
Paperless
Actual Budget
HomeBox
Linkwarden
Mealie
Endurain
Pocket ID
AdGuard configuration
Uptime Kuma
Grafana configuration
Homepage
Prometheus/Loki configuration
Stirling PDF
```

Historical Prometheus metrics and Loki logs are intentionally lower priority than personal application state and are not part of the current protected production set.

## database-backed applications

### linkwarden

The backup job creates a PostgreSQL custom-format dump rather than copying the live PostgreSQL data directory.

Restore PostgreSQL from the selected dump, then start Linkwarden against the restored database. Restore the separately protected application data and verify users, saved links, collections/tags, and representative records.

The production backup verification has confirmed that the dump restored from Motosu is readable by `pg_restore`.

### paperless-ngx

Paperless is protected through its application exporter plus private deployment configuration. Redis is rebuildable.

Restore the Paperless export using the application importer and restore the required Compose/environment/application-secret configuration separately. Verify document count, representative files, OCR/search, tags/correspondents, authentication, and persistence after restart.

#### verified export recovery

A 12-document Paperless-ngx 3.3.3 export has been restored successfully in an isolated test environment on Yamanaka, including normal startup, separate Redis, content search, browser rendering, original-file checksum verification, and restart persistence. See [backup validation and limitations](../backups/README.md#paperless-restore-validation).

Recovery procedure established by the test:

1. preserve the source export read-only and use separate test data/media paths
2. use the pinned application image and an isolated Redis instance; prevent production access and external egress, and verify actual host port bindings
3. initialize the empty application using the normal container entrypoint so required directories exist before importing
4. run the application document importer against the export and rebuild/verify the search index as needed
5. verify document counts and IDs, representative content searches, original SHA-256 checksums, previews/thumbnails, authentication, and browser rendering
6. restart the restored stack and repeat data/search checks
7. remove temporary credentials, sessions, containers, and networks while preserving private evidence

The later production Restic verification also restored the staged Paperless export from Motosu as part of a complete 1:1 backup-tree restore. The restored backup tree matched the source tree exactly.

No archive versions exist in the tested Paperless export; only originals and thumbnails are expected for that dataset. Classifier training, new-document consumption/OCR, archive generation, larger datasets, and a complete clean-host rebuild remain separate recovery tests.

Keep exports and configuration private: exports contain password hashes, and Compose/environment/application secret-key recovery is part of the protected private backup set.

### endurain

The backup job creates a PostgreSQL custom-format dump rather than copying the live PostgreSQL data directory. The database may be temporarily started for the dump if the Endurain stack is otherwise stopped, then returned to its prior state.

Restore PostgreSQL and the separately protected backend/application data. Verify users, activities, settings, and representative history.

The production backup verification has confirmed that the dump restored from Motosu is readable by `pg_restore`.

## file-backed and embedded-database applications

Current backup generation uses short controlled container stops for applications whose persistent state is copied as files, avoiding live copies of SQLite or embedded-database state.

Protected examples include:

- Mealie
- Actual Budget
- HomeBox
- Uptime Kuma
- FreshRSS
- Pocket ID
- Dockhand
- Grafana

For recovery:

1. recreate the Compose stack
2. restore the application's protected persistent directory
3. start the service
4. verify login and representative records
5. confirm new writes survive container recreation/reboot

## configuration-only / lower-value state

The staged backup also protects relevant configuration for services such as:

- AdGuard Home
- Homepage
- SearXNG
- Stirling PDF
- Prometheus
- Grafana Alloy
- Loki
- Caddy/Compose-managed services
- signal-cli state

Redis/Valkey caches, Docker images, Docker sockets, raw PostgreSQL data directories, temporary restore-test trees, Prometheus historical metrics, and Loki historical logs are intentionally excluded where they are rebuildable or low-value.

## monitoring

Restore configuration before historical data.

Priority:

```text
1. Grafana configuration/dashboards
2. Prometheus configuration and scrape targets
3. Loki configuration
4. Alloy configuration
5. rebuild disposable historical metrics/log data as needed
```

Verify production targets such as Kawaguchi, Motosu, and Yamanaka. Gusuku is not part of the required Fujigoko monitoring dependency chain.

Uptime Kuma is deployed on Yamanaka. It shares its monitored host, so it cannot independently detect a complete outage of Yamanaka; independent monitoring remains a separate follow-up item.

## DNS

Yamanaka is one of two target AdGuard Home resolvers; Motosu is the other.

Do not make host recovery depend on Yamanaka DNS already working. Restore basic host/network access first, then AdGuard. During deployment/transition, verify which resolver is actually live rather than assuming the target redundant pair is complete.

## complete host replacement

If the OptiPlex itself is replaced:

1. install Debian
2. configure hostname/network
3. prepare suitable local application storage
4. install Docker + Compose and Restic
5. recreate the documented storage layout
6. establish private access to the Motosu Restic repository
7. restore and verify the selected production backup from Motosu
8. restore Compose/environment configuration
9. restore database-backed services individually
10. restore remaining applications
11. update client-facing references if addressing changes
12. run and verify a fresh backup before declaring recovery complete

Replacement hardware does not need to duplicate the OptiPlex exactly. The recovery contract is Debian, Docker Compose, Restic access to the Motosu repository, sufficient local storage/networking, and adequate CPU/memory.

## verified backup state

The production Yamanaka-to-Motosu path was verified on 2026-10-26.

The verification demonstrated:

- successful application-aware export/dump generation
- successful Restic backup to Motosu
- successful repository integrity check
- successful restore of the latest production snapshot to an isolated temporary path
- 2,157 source files and 2,157 restored files
- no differences in recursive source/restored comparison
- successful restored SHA-256 manifest verification
- successful restored Linkwarden and Endurain PostgreSQL archive validation
- successful automated verification exit status 0

This establishes the Motosu Restic repository as an available independent recovery source for Yamanaka. A representative restore originating from the off-site B2 copy remains a separate outstanding test.

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
- an independent backup to Motosu succeeds after recovery
- backup verification succeeds
- the repository reflects the deployed state
