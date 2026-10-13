# fujigoko

Fujigoko is my homelab.

The current design is intentionally simple: document what exists first, then automate or add complexity only when there is a concrete reason.

## Core hosts

- **kawaguchi** — primary Unraid server and main Docker host
- **motosu** — Immich NAS

## Documentation

- [hosts](hosts.md)
- [network](network.md)
- [services](services.md)
- [topology](topology.md)

## Current priorities

1. Keep an accurate inventory of hosts, services, storage, and network dependencies.
2. Document service-to-service and service-to-storage relationships.
3. Build the infrastructure map from the documented source of truth.
4. Add automation only where it solves a real maintenance or recovery problem.
