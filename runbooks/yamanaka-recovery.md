# yamanaka recovery

## purpose

Restore Yamanaka after host, storage, Docker, or application failure.

Yamanaka holds personal application state, so recovery prioritizes databases, identity, password-vault state, documents, and other persistent application data over convenience services.

## recovery references

- [Host baseline](../hosts/README.md#yamanaka) — physical hardware, Debian, Docker/Compose, network upgrade state
- [Service inventory](../services/README.md#yamanaka) — current applications and supporting dependencies
- [Storage layout](../storage/README.md#yamanaka) — live roots and backup staging location

Do not treat 32 GB RAM as a recovery requirement. Upgrade only if measured workload justifies it. Yamanaka is the production non-media application host and private application-access point; game servers and disposable lab workloads belong in gusuku.

## independent backup source

Use the dedicated encrypted Restic repository on Motosu. [Backup policy and scope](../backups/README.md#yamanaka), [schedule/retention](../backups/README.md#deployed-schedule-and-retention), and [verified recovery evidence](../backups/README.md#verified-yamanaka-to-motosu-recovery-path) are maintained in backups.

The repository password, SSH material, cloud credentials, bucket identifiers, and exact addressing are private. The B2 copy is a separate recovery path whose representative restore remains deferred; local Restic verification does not prove off-site recovery.

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

Use the [recorded production paths](../storage/README.md#yamanaka). Backup generation stages data under `/srv/backup-export` before Restic commits it to Motosu.

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
Kept
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

### kept

Kept is protected with a PostgreSQL custom-format dump plus its persistent data and recovery-critical configuration volumes. The live PostgreSQL data directory is not used as the database backup.

For recovery:

1. recreate the Kept Compose stack without starting the application against an empty database
2. restore the protected Kept persistent data and configuration volumes
3. restore PostgreSQL from the selected custom-format dump
4. restore required private environment/OIDC configuration
5. start Kept and verify locations, boxes, items, labels, and representative records
6. verify Pocket ID OIDC after both Kept and Pocket ID are healthy
7. confirm new writes persist after container recreation/restart

The production backup verification has confirmed that the Kept dump restored from Motosu is readable by `pg_restore` and that its persistent data/configuration is present in the restored backup tree.

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

The isolated test used the pinned Paperless-ngx 3.3.3 image and a separate Redis instance. The exact dataset, validation results, and limits are in [Paperless restore validation](../backups/README.md#paperless-restore-validation).

Recovery procedure established by the test:

1. preserve the source export read-only and use separate test data/media paths
2. use the pinned application image and an isolated Redis instance; prevent production access and external egress, and verify actual host port bindings
3. initialize the empty application using the normal container entrypoint so required directories exist before importing
4. run the application document importer against the export and rebuild/verify the search index as needed
5. verify document counts and IDs, representative content searches, original SHA-256 checksums, previews/thumbnails, authentication, and browser rendering
6. restart the restored stack and repeat data/search checks
7. remove temporary credentials, sessions, containers, and networks while preserving private evidence

No archive versions exist in the tested export; only originals and thumbnails are expected for that dataset. See the [backup evidence](../backups/README.md#paperless-restore-validation) before extending this procedure to untested formats, datasets, or clean-host recovery.

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

Restore configuration according to the [protected set and exclusions](../backups/README.md#service-priorities). Rebuild disposable images, caches, historical metrics/logs, and temporary test state rather than assuming they are in the backup. Restore PostgreSQL from its native dumps rather than raw live data directories.

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

Uptime Kuma shares Yamanaka's failure boundary; see the [accepted monitoring dependency](../architecture/README.md#accepted-dependencies).

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

Use the [dated backup evidence](../backups/README.md#verified-yamanaka-to-motosu-recovery-path) for the production Restic restore, file counts/checksums, database archive validation, automated verification, and separate Vaultwarden application-level test. This is the independent local recovery source for the current application set; representative B2 recovery remains a separate move-time test.

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
