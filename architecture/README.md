# architecture

## design intent

Fujigoko is the production homelab. Host roles should remain obvious, production services must not depend on the experimental [gusuku](https://github.com/s-pollard/gusuku) lab, and recovery design should follow data value rather than system size.

## placement

| Workload | Placement rule |
| --- | --- |
| Media, manga, bulk downloads | Kawaguchi |
| Photos, Immich, backup storage | Motosu |
| General personal applications | Yamanaka |
| Central monitoring/logging and uptime monitoring | Yamanaka |
| Host monitoring agents | Monitored host |
| Private HTTPS and OIDC identity | Yamanaka, serving applications across all production hosts |
| DNS | Yamanaka currently; Yamanaka + Motosu target pair |
| Routing/firewall | UDM-Pro currently; dedicated OPNsense appliance target |
| Disposable services, game servers, learning workloads | Gusuku |

Motosu remains storage/photo focused. Yamanaka is a simple always-on application server, not a general lab host. Shoji remains unassigned until a production requirement justifies another host. See [hosts](../hosts/README.md) for physical inventory and [services](../services/README.md) for deployed workloads.

Application databases/caches stay with their parent application. They remain private to the relevant Compose network unless external access is required; they are not shared LAN infrastructure.

## private access

User-facing services on Yamanaka, Kawaguchi, and Motosu share the private application-access layer on Yamanaka. Direct public-internet exposure is not part of the design.

Pocket ID is used where native OIDC works cleanly. Retain application-local/API authentication where useful for compatibility or recovery. Do not add authentication to intentionally login-free convenience UIs solely for uniformity.

The deployed DNS, Caddy, certificate, and trusted-client behavior is documented in [network](../network/README.md#private-application-access). Application-specific authentication and verified OIDC integrations are in [services](../services/README.md#authentication).

## accepted dependencies

Uptime Kuma runs on Yamanaka. A complete Yamanaka failure also removes that monitoring path. This is accepted current state; a separate watchdog is not required for the present home-use requirements. Loss of normal Yamanaka access is sufficient operational indication.

The private application front door also depends on Yamanaka. Host recovery must start with basic network access rather than depend on Yamanaka DNS, Caddy, or OIDC already working. See [Yamanaka recovery](../runbooks/yamanaka-recovery.md#dns-and-private-application-access).

## recovery design

Protect irreplaceable photos, documents, personal databases, identity, and password-vault state ahead of replaceable media, caches, and metrics/log history. Kawaguchi is intentionally comparatively rebuildable.

Storage ownership and live paths belong in [storage](../storage/README.md); backup scope, priorities, schedules, and evidence belong in [backups](../backups/README.md).

## principles

1. Keep production and experimentation separate.
2. Keep host roles obvious.
3. Prefer understandable systems over unnecessary clustering.
4. Keep application databases local to their application host; back them up independently.
5. Document storage, dependencies, and recovery before adding automation.
6. Remove retired experiments instead of preserving them by inertia.
7. Follow [SECURITY.md](../SECURITY.md) for public documentation; keep operational secrets private.
8. Treat deployed state—not old migration assumptions—as current state.
