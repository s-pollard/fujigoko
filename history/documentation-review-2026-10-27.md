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

## confirmed state

Owner clarifications on 2026-10-27 resolved the original review questions:

| Topic | Clarification / action |
| --- | --- |
| Private application names | Keep the namespace and its DNS names private. Remove literal names from current documentation, including this review, and update SECURITY to match. |
| ISP handoff | Current: Bluepeak ONT, model unknown. After relocation: AT&T, with a plan to request the 620 ONT. Requested hardware is not deployed hardware. |
| Motosu drives | Both current members are the deployed model recorded in [hosts](../hosts/README.md#motosu). Future upgrades depend on a good deal, using drives moved down from Kawaguchi or bought for Motosu. |
| Yamanaka attachment | Yamanaka connects through USW-Lite-8-PoE, USW-Aggregation, UDM-Pro, ONT, and ISP. See [topology](../network/topology.md#current-topology). |
| B2 scope | Motosu syncs Immich and Yamanaka backups to separate B2 buckets. Source selection is confirmed; latest Yamanaka upload completion and B2 restore verification remain separate checks. |
| Kawaguchi backups | Put flash/config and manga protection on the [backup to-do list](../backups/README.md#kawaguchi-backup-to-do-list); do not describe it as deployed. |
| Motosu follow-up | The old requests to implement Yamanaka backups and add independent monitoring were stale. The current backup path is deployed and verified; the accepted monitoring boundary is unchanged. Earlier instructions are retained here as historical context. |

## review needed

Remaining decisions and verification work:

- [Kawaguchi backups](../backups/README.md#kawaguchi-backup-to-do-list): retained scope, destination, frequency, retention, and representative restore.
- [B2 copies](../backups/README.md#off-site-copies): verify latest upload completion and perform representative restores during the move.
- [GFX archive](../storage/README.md#photo-policy): decide final location, recovery classification, and protection during the move.

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
- Owner clarification separates the current Bluepeak ONT from the planned AT&T handoff and request for the 620 model.
- The confirmed-state table records the resolved questions. Remaining backup/storage decisions are listed above; no missing addresses, port assignments, schedules, or unverified deployments were supplied.

Initial cleanup validation passed relative links/heading anchors, fences/tables, and `git diff --check`. The clarification follow-up also updates `SECURITY.md` and intentionally removes private application names from current documentation. `.gitignore` is unchanged. No live services, restore tests, or hardware were re-verified; confirmed state is based on the owner's answers.
