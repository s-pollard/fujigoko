# smartctl-exporter

Restore and verify Kawaguchi's SMART exporter after container/template changes. It was restored on 2026-10-21 by recreating the container from the saved Unraid template.

## recorded configuration

```text
container  smartctl-Exporter
image      prometheuscommunity/smartctl-exporter:latest
port       9633
mode       privileged
runtime    --user=0:0
```

The run configuration requires `--user=0:0`. The image's default user is `nobody`, which cannot open the block device nodes that smartctl reads. Setting `USER=root` as a container environment variable did not change the runtime user: an environment variable does not override the image's default user or the user selected at run time.

## recovery and verification

1. Recreate the container from the saved Unraid template.
2. Verify privileged mode and an explicit root runtime user in the template/run configuration.
3. Confirm `Privileged=true` with `docker inspect` and runtime uid 0 with `docker exec smartctl-Exporter id`.
4. From Prometheus on Yamanaka, verify that the smartctl scrape target is UP.
5. Check actual device metrics and coverage against the live host inventory. A reachable exporter alone does not establish block-device access.
6. Investigate device errors separately from scrape health.

## recorded verification

Verified from Yamanaka on 2026-10-21: the Prometheus smartctl scrape target was UP and the exporter reported metrics for 9 devices. User-provided `docker inspect` output on Kawaguchi confirmed `Privileged=true`; subsequent `docker exec smartctl-Exporter id` output confirmed runtime uid 0.

The exported `smartctl_device_smart_status` values are not evidence that all disks are problem-free. SMART PASSED does not rule out incipient failure. This verification covers scrape health and device coverage only.

See [Kawaguchi recovery](kawaguchi-recovery.md) for the wider recovery sequence and [services](../services/README.md#kawaguchi) for inventory.
