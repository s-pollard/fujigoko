# runbooks

Runbooks describe what to do when part of Fujigoko fails, needs to be rebuilt, or requires a coordinated production change.

They are intentionally short and operational. Architecture and inventory details belong elsewhere in the repository.

## runbooks

- [kawaguchi recovery](kawaguchi-recovery.md)
- [motosu recovery](motosu-recovery.md)
- [yamanaka recovery](yamanaka-recovery.md)
- [network recovery](network-recovery.md)
- [move checklist](move-checklist.md) — relocation-time network, DNS, backup, storage, and validation work
- [smartctl-exporter](smartctl-exporter.md) — Kawaguchi runtime permissions, restoration, and metric verification
- [service deployment](service-deployment.md) — migrations and new stateful applications

## general incident order

Use the same basic sequence for most failures:

```text
1. identify scope
2. preserve remaining good data
3. stop making unnecessary changes
4. restore basic host/network function
5. restore persistent data
6. restore services
7. verify from normal clients
8. document anything that differed from the runbook
```

Do not delete old data, old containers, or failed disks merely to make the environment look clean during recovery.

## recovery priorities

```text
highest
├── network/gateway availability
├── irreplaceable photos and personal application data
├── databases required to make those applications usable
│
├── media-service configuration where it has real recovery value
├── Plex / manga metadata where preservation is desired
│
└── replaceable movie/TV/download payloads and rebuildable automation state
lowest
```

The goal is to restore useful service, not to reproduce every byte or historical metric immediately.
