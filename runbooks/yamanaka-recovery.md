# yamanaka recovery

## purpose

Restore Yamanaka after host, storage, Docker, or application failure.

Yamanaka holds personal application state, so recovery prioritizes databases, identity, password-vault state, documents, and other persistent application data over convenience services.

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

Yamanaka is the production non-media application host and common private application-access point.

Expected workloads include:

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
- Grocy
- TriliumNext
- Vaultwarden

### monitoring / infrastructure

- Prometheus
- Grafana
- Loki
- Grafana Alloy
- Uptime Kuma
- AdGuard Home
- Caddy
- Pocket ID
- signal-cli-rest-api
- Dockhand

Game servers and disposable lab workloads belong in gusuku.

## independent backup source

Yamanaka production state is backed up to a dedicated encrypted Restic repository on Motosu.

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

Production backups run nightly through systemd. A weekly verification job restores the latest production snapshot to an isolated temporary location, verifies the SHA-256 manifest, performs a recursive 1:1 comparison against the staged source tree, and validates restored database archives.

The current Restic retention policy keeps 14 daily, 8 weekly, and 6 monthly snapshots.

## recovery order

```text
1. restore host/network access
2. restore application storage
3. restore Docker + Compose
4. recover the latest suitable Restic snapshot from Motosu
5. restore Compose definitions and private environment/configuration
6. restore database dumps and application-aware exports
7. restore persistent application files and identity/vault state
8. restore high-value applications
9. restore utilities, monitoring, reverse proxy, and DNS
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
7. verify identity, password-vault, and database-backed applications before low-value utilities
8. restore Caddy and AdGuard only after basic host networking is stable
9. run and verify a fresh backup to Motosu

## application-storage loss

If the Yamanaka application NVMe is lost:

1. stop writes to failed storage
2. prepare replacement storage
3. recreate the documented filesystem/layout
4. install Restic and establish private Motosu repository access using recovery credentials
5. restore the selected production snapshot from Motosu to a temporary recovery location
6. verify the restored SHA-256 manifest before using the data
7. restore Compose definitions and private environment/configuration
8. restore database dumps before dependent applications
9. restore file/document/application state
10. restore identity and password-vault state carefully
11. start applications in dependency order
12. verify representative application data and persistence
13. run and verify a new independent backup before declaring recovery complete

High-value recovery priority:

```text
Vaultwarden
Paperless
Actual Budget
HomeBox
Linkwarden
Mealie
Endurain
Grocy
TriliumNext
Pocket ID
FreshRSS
Uptime Kuma
AdGuard configuration
Caddy configuration
Grafana configuration
Homepage
Prometheus/Loki/Alloy configuration
Stirling PDF
SearXNG
```

Historical Prometheus metrics and Loki logs are intentionally lower priority than personal application state and are not part of the current protected production set.

## database-backed applications

### linkwarden

The backup job creates a PostgreSQL custom-format dump rather than copying the live PostgreSQL data directory.

Restore PostgreSQL from the selected dump, then start Linkwarden against the restored database. Restore the separately protected application data and verify users, saved links, collections/tags, and representative records.

The production backup verification has confirmed that the dump restored from Motosu is readable by `pg_restore`.

### endurain

The backup job creates a PostgreSQL custom-format dump rather than copying the live PostgreSQL data directory. The database may be temporarily started for the dump if the Endurain stack is otherwise stopped, then returned to its prior state.

Restore PostgreSQL and the separately protected backend/application data. Verify users, activities, settings, and representative history.

The production backup verification has confirmed that the dump restored from Motosu is readable by `pg_restore`.

### vaultwarden

Vaultwarden is treated as critical application state.

The production backup uses SQLite's online backup mechanism for the live database rather than copying the active database file blindly. The resulting backup is validated with `PRAGMA integrity_check` before staging. The signing key and other required persistent application state are protected separately in the private backup set.

A separate isolated application-level restore test has already verified that the backed-up database and signing key can launch a disposable Vaultwarden instance successfully.

For recovery:

1. restore the protected Vaultwarden persistent data into an isolated recovery location first
2. verify the SQLite backup with `PRAGMA integrity_check`
3. confirm the expected schema is present
4. restore the signing key and required private deployment configuration
5. start Vaultwarden without exposing a new public path
6. verify login, representative vault items, and second-factor behavior using the normal recovery process
7. confirm persistence after restart before returning the restored instance to normal service

Do not weaken email-verification, MFA, master-password, or other authentication requirements merely to simplify recovery.

## paperless-ngx

Paperless is protected through its application exporter plus private deployment configuration. Redis is rebuildable.

Restore the Paperless export using the application importer and restore the required Compose/environment/application-secret configuration separately. Verify document count, representative files, OCR/search, tags/correspondents, authentication, and persistence after restart.

### verified export recovery

A 12-document Paperless-ngx 3.3.3 export has been restored successfully in an isolated test environment on Yamanaka, including normal startup, separate Redis, content search, browser rendering, original-file checksum verification, and restart persistence. See [backup validation and limitations](../backups/README.md#paperless-restore-validation).

Recovery procedure established by the test:

1. preserve the source export read-only and use separate test data/media paths
2. use the pinned application image and an isolated Redis instance; prevent production access and external egress, and verify actual host port bindings
3. initialize the empty application using the normal container entrypoint so required directories exist before importing
4. run the application document importer against the export and rebuild/verify the search index as needed
5. verify document counts and IDs, representative content searches, original SHA-256 checksums, previews/thumbnails, authentication, and browser rendering
6. restart the restored stack and repeat data/search checks
7. remove temporary credentials, sessions, containers, and networks while preserving private evidence

The production Restic verification also restored the staged Paperless export from Motosu as part of the complete backup-tree restore. The restored backup tree matched the source tree exactly.

No archive versions exist in the tested Paperless export; only originals and thumbnails are expected for that dataset. Classifier training, new-document consumption/OCR, archive generation, larger datasets, and a complete clean-host rebuild remain separate recovery tests.

Keep exports and configuration private: exports contain password hashes, and Compose/environment/application secret-key recovery is part of the protected private backup set.

## file-backed and embedded-database applications

For applications whose state is copied as files, backup generation uses a consistency-preserving workflow rather than blindly copying live embedded-database state.

Protected examples include:

- Mealie
- Actual Budget
- HomeBox
- Grocy
- TriliumNext
- Uptime Kuma
- FreshRSS
- Pocket ID
- Dockhand
- Grafana

For recovery:

1. recreate the Compose stack
2. restore the application's protected persistent directory
3. restore any private environment/configuration required by the service
4. start the service
5. verify login and representative records
6. confirm new writes survive container recreation/reboot

Grocy and TriliumNext were added to the production backup path and included in the later byte-for-byte Motosu restore verification. TriliumNext Pocket ID OIDC should be checked after restoring both TriliumNext and Pocket ID.

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

Uptime Kuma is deployed on Yamanaka and therefore cannot independently detect a complete Yamanaka outage. A separate external Yamanaka watchdog is not currently required for the present home-use requirements; loss of normal Yamanaka access is accepted as sufficient operational indication.

## DNS and private application access

Yamanaka currently hosts the production AdGuard Home resolver and Caddy private HTTPS entry point. Motosu is the target second AdGuard Home resolver after the move.

Do not make host recovery depend on Yamanaka DNS already working. Restore basic host/network access first, then restore AdGuard and Caddy. Verify private application resolution and HTTPS from a trusted client only after the underlying services are healthy.

During deployment/transition, verify which resolver is actually live rather than assuming the target redundant pair is complete.

Restore Pocket ID before relying on OIDC for application validation. Retain application-local authentication or documented recovery paths where they exist.

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
9. restore database-backed, vault, and identity services individually
10. restore remaining applications
11. restore Caddy, DNS, and monitoring
12. update client-facing references if addressing changes
13. run and verify a fresh backup before declaring recovery complete

Replacement hardware does not need to duplicate the OptiPlex exactly. The recovery contract is Debian, Docker Compose, Restic access to the Motosu repository, sufficient local storage/networking, and adequate CPU/memory.

## verified backup state

The production Yamanaka-to-Motosu path was first verified on 2026-10-26 and re-verified after adding Grocy, TriliumNext, and Vaultwarden on 2026-10-27.

The current verification demonstrated:

- successful application-aware export/dump generation
- successful Grocy and TriliumNext consistent-state capture
- successful Vaultwarden SQLite online backup and integrity validation
- successful Restic backup to Motosu
- successful repository integrity check
- successful restore of the latest production snapshot to an isolated temporary path
- 2,301 source files and 2,301 restored files
- about 873 MiB of logical staged backup data
- no differences in recursive source/restored comparison
- successful restored SHA-256 manifest verification
- successful restored Linkwarden and Endurain PostgreSQL archive validation
- successful automated verification
- separate successful isolated Vaultwarden application-level restore test

This establishes the Motosu Restic repository as an available independent recovery source for the current Yamanaka application set. A representative restore originating from the off-site B2 copy remains a separate outstanding move-time test.

## completion criteria

Recovery is complete when:

- Yamanaka boots reliably
- application storage is healthy and mounted
- Docker/Compose stacks survive reboot
- retained applications show expected data
- Vaultwarden state is intact and authentication behaves normally
- Paperless documents and other high-value records are readable
- Pocket ID and intended OIDC integrations work
- private DNS and Caddy access work according to the currently deployed design
- monitoring works
- no application depends on old Kawaguchi state
- an independent backup to Motosu succeeds after recovery
- backup verification succeeds
- the repository reflects the deployed state
