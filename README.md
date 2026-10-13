# fujigoko

Fujigoko is my homelab.

The current design is intentionally simple: document what exists first, then automate or add complexity only when there is a concrete reason.

## Core hosts

- **kawaguchi** — primary media server and Unraid host
- **motosu** — Immich NAS
- **future lake host** — planned low-power general application server

## Documentation

- [architecture](architecture.md)
- [hosts](hosts.md)
- [network](network.md)
- [services](services.md)
- [topology](topology.md)

## Current priorities

1. Keep an accurate inventory of hosts, services, storage, and network dependencies.
2. Document service-to-service and service-to-storage relationships.
3. Build the infrastructure map from the documented source of truth.
4. Separate media, photo, and general application workloads by host role.
5. Add automation only where it solves a real maintenance or recovery problem.
