# yamanaka recovery

## purpose

Restore Yamanaka after host, storage, Docker, or application failure.

Yamanaka will hold personal application state, so recovery should prioritize databases and persistent application data over convenience services.

This runbook documents the intended recovery model before Yamanaka hardware is selected. Update it after deployment with actual storage paths, backup tooling, and network details.

## expected role

Yamanaka hosts non-media applications and monitoring.

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
```

Game servers are outside Yamanaka's role.

## recovery order

```text
1. restore host/network access
2. restore Docker + Compose capability
3. restore persistent storage
4. restore databases
5. restore high-value applications
6. restore utilities
7. restore monitoring
8. verify backup jobs
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
    └── grafana/
```

Do not assume these are final until the machine is deployed and the repository is updated.

## host-only failure

If persistent application data remains intact:

1. reinstall or repair the Linux host OS
2. restore hostname `yamanaka`
3. restore network configuration
4. install Docker Engine and Docker Compose
5. restore Compose definitions
6. verify persistent data mounts
7. start stacks one at a time
8. verify database-backed applications before utilities

Do not recreate empty application directories over existing data paths.

## storage loss

If Yamanaka application storage is lost:

1. stop attempting writes to failed storage
2. restore replacement storage
3. restore independent backups to staging or final application paths as appropriate
4. restore database dumps before starting dependent applications
5. restore file/document data
6. restore Compose definitions
7. start applications in dependency order

Priority order:

```text
Paperless
Actual Budget
HomeBox
Linkwarden
Mealie
Endurain
Grafana configuration
Homepage
Prometheus history
Stirling PDF
```

Prometheus historical metrics and cache data are lower priority than personal application state.

## database-backed applications

### linkwarden

Target dependency:

```text
linkwarden -> postgres
```

Restore PostgreSQL from an application-aware/database-native backup, then start Linkwarden against the restored database.

Verify users, saved links, collections/tags, and any file storage.

### paperless-ngx

Restore both the document/media files and required application metadata/database state.

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

Restore Grafana before worrying about Prometheus history if necessary.

Priority:

```text
1. Grafana configuration/dashboards
2. Prometheus configuration and scrape targets
3. Prometheus historical metrics if worth preserving
```

Verify Kawaguchi and Yamanaka scrape targets after recovery.

## complete host replacement

If Yamanaka hardware is replaced:

1. install Linux
2. configure hostname/network
3. install Docker + Compose
4. recreate the documented `/srv` structure or updated equivalent
5. restore Compose definitions
6. restore backups
7. restore database-backed services individually
8. restore remaining applications
9. update any DNS/bookmarks/reverse-proxy references if the address changed
10. configure and verify backups before declaring recovery complete

## completion criteria

Recovery is complete when:

- Yamanaka boots reliably
- Docker/Compose stacks survive reboot
- all retained personal applications are accessible
- database-backed applications show expected data
- Paperless documents are readable
- Actual Budget/HomeBox/Mealie data is present
- monitoring works
- no application depends on old Kawaguchi state
- an independent backup runs successfully
- the repository reflects the deployed recovery state
