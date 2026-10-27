# topology

Recorded production connections and target physical layout. Equipment state, DNS, ingress, segmentation, and power policy are maintained in [network](README.md).

## current topology

```text
                         internet
                            |
                     Bluepeak ONT
                            |
                         udm-pro
                            |
                    usw-aggregation
                    /      |       \
                   /       |        \
              u7 pro   usw-lite   kawaguchi
                         8-poe       unraid
                        /    \
                   motosu   doorbell
                  truenas     lite
```

- U7 Pro is attached to the aggregation switch and has a 2.5 GbE-capable uplink.
- Kawaguchi uses 10 GbE to the aggregation layer.
- Motosu reaches the network through USW-Lite-8-PoE.
- Yamanaka is deployed, but its current physical switch attachment is not recorded here. The diagram shows only documented links.
- Exact switch-port assignments remain private.

## target topology

```text
                       ISP handoff
                            |
                         opnsense
                            |
                    core / aggregation
                    /       |        \
                   /        |         \
          kawaguchi      motosu      yamanaka
            media         photos       apps
                           + backups    + monitoring
                           + dns        + dns
```

This is target state, not the current wiring or evidence that Motosu DNS is deployed. The older target handoff label is under [review](../history/documentation-review-2026-10-27.md#review-needed); no device model is assumed here. Equipment purchase/deployment states are in the [network plan](README.md#target-network); resolver state is in [DNS](README.md#dns).

If UniFi switching remains after UDM-Pro retirement, retain a working [management method](README.md#management-plane-dependency). The Omada AP management method is selected separately.

## application flows

- [Private application access](README.md#private-application-access) — trusted clients, private DNS, Caddy, production hosts
- [Media dependencies](../services/README.md#media-dependencies) — acquisition/import flow
- [Motosu services](../services/README.md#motosu) — Immich and its database/cache/machine-learning dependencies
- [Yamanaka services](../services/README.md#yamanaka) — application-local database/cache dependencies

Gusuku is outside this production topology. Exact addressing, VLANs, reservations, ports, management URLs, and WAN details remain private under [SECURITY.md](../SECURITY.md).
