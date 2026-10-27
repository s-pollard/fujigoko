# Fujigoko move checklist

Production work intentionally deferred until relocation, in execution order. Equipment choices and purchase/deployment states are in [network](../network/README.md#target-network); backup scope and evidence are in [backups](../backups/README.md).

## 1. physical setup

- place Motosu, Yamanaka, Kawaguchi, network equipment, UPS hardware, and printers in their final locations
- verify power distribution and UPS connections before bringing the full environment online
- establish final cable routing and airflow
- confirm the equipment layout remains serviceable without obstructing ventilation

## 2. network cutover

- bring up the dedicated OPNsense router
- verify the [ISP handoff](../network/README.md#current-hardware) before changing the production gateway; the older AT&T 620 label conflicts with the current Bluepeak record
- configure required LAN/VLAN interfaces, DHCP, firewall policy, and routing
- deploy the target wireless AP
- deploy the target core/aggregation switching design if the replacement switch has been purchased
- verify management access to any retained UniFi hardware without depending on the UDM-Pro
- verify normal LAN access, internet access, and Tailscale before proceeding

Do not retire or sell the UDM-Pro until the replacement network has remained stable and all required management functions are accounted for.

## 3. redundant DNS

- deploy the second AdGuard Home instance on Motosu
- align the intended filtering and private DNS policy with the Yamanaka resolver
- verify private `plebworks.com` resolution from normal clients
- verify clients can use both resolvers
- test resolver behavior with either DNS host unavailable

## 4. production service validation

Verify normal client access to the major production roles after the network and DNS changes:

- Yamanaka applications and reverse proxy
- Motosu / Immich
- Kawaguchi media services
- Plex
- private application names
- Tailscale access where required

Resolve network/DNS issues before changing unrelated application configuration.

## 5. backup validation

- confirm Yamanaka's nightly Restic timer still runs normally after relocation
- confirm the weekly restore-verification timer remains active
- confirm Yamanaka failure alerts still arrive through Signal
- confirm Motosu/TrueNAS email alerts still work
- confirm Motosu Cloud Sync continues to copy the Yamanaka Restic repository off-site
- perform a representative restore from the B2 off-site copy and document the result

The B2 test should prove that the off-site copy can be used for recovery rather than merely confirming that objects exist remotely. Confirm the actual Yamanaka repository selection and completed off-site copy: current backup wording describes that path as intended, while the checklist assumes it continues. See the [review note](../history/documentation-review-2026-10-27.md#review-needed).

## 6. Motosu storage work

The current mirror is healthy. Drive replacement is opportunistic rather than emergency work.

If two suitable replacement HDDs have been acquired by move time:

- replace drives according to the safe TrueNAS/ZFS replacement process
- allow each required resilver to complete before proceeding
- verify pool health
- verify SMART status/tests
- run or confirm a scrub as appropriate
- confirm alerting after the storage changes

If replacement drives have not been purchased, leave the healthy mirror in service.

## 7. GFX archive

After the final storage layout and available capacity are known:

- decide whether the GFX archive is irreplaceable, important, or reproducible
- choose its primary storage location
- decide whether it belongs in local snapshots, off-site backup, or neither
- document the primary location in [storage](../storage/README.md#photo-policy) and protection/retention in [backups](../backups/README.md#deferred--remaining-work)

## 8. final acceptance

Before considering the move complete, verify:

```text
routing / internet
DNS
Tailscale
private application names
Yamanaka applications
Immich
Plex / media services
Restic backup
TrueNAS Cloud Sync
Signal backup-failure alerts
TrueNAS email alerts
storage health
```

Only after the replacement network and production services are stable should obsolete network hardware or temporary move infrastructure be retired.
