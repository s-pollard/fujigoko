# documentation review — 2026-10-27

Scope: documentation only, starting at `d0446db6e94114da3e94ce65e7bf3b55611e912e`. No live-system checks or configuration changes. The upstream current-handoff correction at `dcecbc2297931b410c8d1e8dad73bc646fa11c70` was incorporated before completion.

## audit

The repository already has the required directories and 19 Markdown files. Most inventories are readable, but the same facts are maintained in several places. Recovery pages repeat inventories, and current-state pages carry migration results and incident details. Motosu's deployed services and target DNS role are sometimes grouped under one target/permanent heading.

## duplication and placement

| Topic | Repeated or misplaced locations | Cleanup |
| --- | --- | --- |
| Host hardware and roles | architecture, hosts, network, recovery runbooks, migration history | Keep current hardware in hosts; retain only recovery-specific context elsewhere. Historical baselines stay labeled historical. |
| Service lists and dependencies | hosts, architecture, services, classification, topology, runbooks | Keep the deployed/target inventory in services; link from policy and recovery pages. Move media flow out of network topology. |
| Backup scope, schedules, retention, evidence | hosts, architecture, storage, backups, Yamanaka recovery | Keep policy and verification results in backups; keep restore procedures in runbooks and data paths in storage. |
| DNS and private access | root, architecture, network, topology, services, classification | Network owns resolver/access behavior; services owns application authentication and verified integrations. |
| smartctl restoration and device-access troubleshooting | services inventory and Kawaguchi recovery | Move the detailed record and configuration to a dedicated runbook. |
| Migration and cleanup results | hosts, services, classification, migration history | Keep dated cleanup counts and retired services in history. |
| Motosu migration and mirror incident | architecture, hosts, storage, backups, recovery | Keep the incident record in history and a short current-health summary in storage. |
| Move-time work | root, hosts, backups, recovery, move checklist | Keep execution order in the move checklist; retain topic-specific gaps beside the relevant policy. |

## topic ownership

| Topic | Authoritative location |
| --- | --- |
| Overview and documentation index | [root README](../README.md) |
| Production boundary, placement invariants, accepted dependencies | [architecture](../architecture/README.md) |
| Naming conventions and reserved names | [naming](../architecture/naming.md) |
| Server/router physical inventory | [hosts](../hosts/README.md) |
| Personal PC hardware and administration access | [workstations](../hosts/workstations.md) |
| Service placement, purpose, dependencies, authentication verification | [services](../services/README.md) |
| Service lifecycle and placement decisions | [classification](../services/classification.md) |
| Network equipment/plans, DNS, ingress, segmentation | [network](../network/README.md) |
| Recorded physical connections | [topology](../network/topology.md) |
| Pools, shares, live data paths, storage ownership | [storage](../storage/README.md) |
| Backup scope, schedules, retention, restore evidence and limits | [backups](../backups/README.md) |
| Recovery, deployment, troubleshooting, move execution | [runbooks](../runbooks/README.md) |
| Completed migrations, incidents, retired state | [history](README.md) |
| Public repository information policy | [SECURITY.md](../SECURITY.md) |

## file plan

| File | Smallest useful change |
| --- | --- |
| `README.md` | Short overview, core-host table, index, linked current status; replace the duplicated move backlog with its checklist link. |
| `SECURITY.md` | Preserve the policy; flag the conflicting network wording rather than choosing a new rule. |
| `architecture/README.md` | Keep boundaries, rationale, placement invariants, and accepted monitoring dependency; link hardware, network, services, and backup details. |
| `architecture/naming.md` | Keep naming rules and reserved names; reduce repeated role/namespace lists. |
| `hosts/README.md` | Add a compact inventory table; keep physical specifications, link service lists, move incident history and backup policy out. |
| `hosts/workstations.md` | Keep hardware/access details; link backup scope to backups. |
| `services/README.md` | Consolidate host inventories into concise purpose/dependency tables; distinguish deployed Immich from target Motosu DNS; retain verified authentication details. Move smartctl troubleshooting and cleanup history out. |
| `services/classification.md` | Keep placement/lifecycle decisions; link inventory and retired-state history. Move backup-priority tables to backups and migration steps to a runbook. |
| `network/README.md` | Keep equipment state, DNS/access policy, plans, power details; link topology and router hardware. Flag publication-policy conflict. |
| `network/topology.md` | Own physical diagrams; label the undocumented Yamanaka attachment, link DNS/access and move application dependencies to services. |
| `storage/README.md` | Add ownership/path tables, retain shares and critical state; link hardware, incident history, and backup policy. Mark the GFX layout as undecided. |
| `backups/README.md` | Own backup scope, schedules, retention, service priorities, and all verification evidence; add a compact protection summary and workstation scope. Preserve off-site verification limits. |
| `runbooks/README.md` | Index the added operational pages; retain incident/recovery priorities. |
| `runbooks/kawaguchi-recovery.md` | Link the authoritative service list and storage paths; keep recovery steps and link detailed smartctl troubleshooting. |
| `runbooks/motosu-recovery.md` | Link inventory, paths, retention, and incident history; keep restore steps. Flag conflicting follow-up instructions. |
| `runbooks/yamanaka-recovery.md` | Link inventories, backup policy/evidence, and storage layout; preserve application-specific restore procedures and validation limits. |
| `runbooks/network-recovery.md` | Link topology, DNS, segmentation, and equipment inventories; retain procedures and deployment caveats. Correct the stale conditional about Yamanaka deployment and record that correction here. |
| `runbooks/move-checklist.md` | Keep execution order; link equipment choices, backup evidence, and storage policy. |
| `history/yamanaka-migration-2026.md` | Preserve migration-era facts, cleanup counts, measurements, and troubleshooting context; label historical follow-up and link later backup verification. |
| `history/README.md` (new) | Add a short history index. |
| `history/motosu-storage-2026.md` (new) | Collect the recorded TrueNAS/Immich migration and mirror-replacement history without inventing event dates. |
| `runbooks/smartctl-exporter.md` (new) | Preserve the 2026-10-21 configuration, root-user issue, device coverage, and verification limits. |
| `runbooks/service-deployment.md` (new) | Preserve the existing stateful-service migration/deployment checklist. |
| This review (new) | Record the audit, plan, unresolved facts, and final cleanup result. |

## review needed

These are documentation findings, not live-system diagnoses.

| Topic | Existing evidence / unresolved question |
| --- | --- |
| ISP handoff | Upstream corrected the current handoff to Bluepeak ONT during this review. Older target/topology and move text used AT&T 620 ONT. Current inventory/topology use the author's corrected name; the target diagram uses a generic handoff. Confirm the actual device model and target handoff rather than carrying the old model forward. |
| Published private names | `SECURITY.md` explicitly permits the intentionally documented `plebworks.com` namespace and non-secret internal hostnames. `network/README.md` forbids publishing the namespace and application hostnames. Existing published names are retained; the policy needs a human decision. |
| Motosu follow-up | `runbooks/motosu-recovery.md` says to implement Yamanaka backups and add independent monitoring. Backups records deployed, tested coverage on 2026-10-26/27; architecture/backups accept monitoring on Yamanaka without an independent watchdog. Preserve the old conflicting instructions as review notes rather than a live deployment checklist. |
| Yamanaka off-site coverage | Backup/storage wording calls the B2 path intended, while the move checklist says to confirm Cloud Sync continues copying the repository. Local Restic recovery is verified; the reported completed photo upload does not establish a restored off-site Yamanaka repository. Confirm actual Cloud Sync selection/completion during the B2 restore test. |
| GFX archive | Storage shows a conceptual photo/archive layout, while the move checklist still leaves primary location and backup classification undecided. Do not present the sketch as a deployed dataset. |
| Motosu drive models | Hosts lists `2 × 6 TB Seagate ST6000NM0024 HDDs`; storage uses `ST6000NM0024-class`, and incident notes describe a temporary older spare without its model. Confirm the current members before changing the recorded hardware claim. |
| Kawaguchi backup availability | Architecture/storage value configuration and manga above replaceable media; backups intentionally allow reconstructing media automation without a full independent backup. No independent flash/config or manga backup is established by these docs. Conditional recovery instructions do not prove one exists. |
| Current physical topology | Yamanaka is deployed, but the current topology does not record its switch attachment. Keep that gap explicit; do not infer a port or link. |

## historical wording

- The migration record's outstanding-backup task describes earlier follow-up; link the later 2026-10-26/27 verification without erasing that history.
- `network-recovery.md` says to verify Yamanaka "when deployed" even though the host/service records describe it as deployed. Remove only that stale qualifier.
- Recorded snapshot counts, file counts, disk coverage, memory usage, and software versions remain dated evidence, not fresh verification.

## cleanup result

- Smartctl configuration, runtime-user troubleshooting, and 2026-10-21 verification moved from the service inventory to `runbooks/smartctl-exporter.md`.
- The stateful-service migration/deployment sequence moved from classification to `runbooks/service-deployment.md`.
- Motosu migration, completed Google Photos import, and temporary mirror replacement are collected in `history/motosu-storage-2026.md`.
- Media flow moved from network topology to services; Yamanaka layout and Kawaguchi share paths are consolidated in storage.
- Backup priorities moved from architecture/classification to backups; workstation backup scope moved from hosts to backups. Detailed Restic evidence now lives in backups rather than being repeated in recovery.
- Repeated hardware specifications, service lists, DNS/access descriptions, schedules, retention, and cleanup counts were replaced with short contextual summaries and links. The topic-ownership table above is the maintenance map.
- Migration-era inventories, cleanup counts, memory measurements, and delayed-startup observations remain in history. Vaultwarden and Paperless validation evidence and limitations are preserved verbatim in backups.
- Current/target Motosu service states are separate. The old Yamanaka deployment qualifier was corrected, and the network access description now covers all three hosts as already documented in services.
- The newer upstream Bluepeak ONT correction is retained; the older AT&T 620 target/move label is recorded for review rather than assumed to identify the current device.
- The review-needed questions above remain unresolved; no missing address, port assignment, disk model, dataset, schedule, or deployment was supplied.

Validation: all relative file links and GitHub heading anchors pass; Markdown fences/tables and `git diff --check` pass. All original inline code values remain somewhere in the revised documentation. Only Markdown files changed; `SECURITY.md` and `.gitignore` are unchanged. No live services, restore tests, or hardware were re-verified during this documentation cleanup.
