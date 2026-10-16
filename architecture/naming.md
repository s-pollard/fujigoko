# naming conventions

Fujigoko uses a Japan-based naming scheme. Names should describe infrastructure roles consistently rather than being assigned randomly.

## homelab

### Fujigoko

`fujigoko` is the name of the overall homelab and repository.

The name refers to the Fuji Five Lakes and establishes the naming family used for major compute/storage hosts.

## major hosts — Fuji Five Lakes

Major servers use names from the Fuji Five Lakes.

```text
kawaguchi  -> media / Unraid
motosu     -> photos / NAS / Immich
yamanaka   -> general applications
saiko      -> Proxmox lab / experimentation
shoji      -> reserved / undecided
```

The role may evolve, but a lake name should represent a major host rather than a container, VM, or temporary service.

The former host name `bandai` is legacy and is being replaced by `saiko` as that machine becomes the lab host.

## physical networking — rivers

Japanese river names are reserved for physical network infrastructure where useful.

Rationale: rivers connect regions and provide a natural naming metaphor for switches, links, or other physical network fabric.

Potential uses include:

- core switch
- aggregation switch
- access switches
- other major physical networking devices

Do not rename existing production network hardware solely to satisfy the convention. Apply the convention when the Miami network is rebuilt or when replacement hardware makes the name useful.

## logical networking / transit — Shinkansen

Shinkansen-related names are reserved for logical or transit-oriented networking concepts.

Potential uses include:

- VPN/transit networks
- inter-site links
- logical network backbones
- routing/transit projects

The convention is conceptual; do not assign a Shinkansen name until a real component needs one.

## hubs / centralized infrastructure — stations

Japanese station or major hub names are reserved for centralized infrastructure where the hub metaphor fits.

Potential uses include:

- central dashboards
- management/control-plane services
- shared infrastructure hubs

Do not use station names for ordinary application containers simply because a name is needed.

## naming rules

1. Keep the Japan theme coherent.
2. Major physical hosts use Fuji Five Lakes names.
3. Prefer role-based categories over arbitrary Japanese place names.
4. Do not rename working infrastructure unless the new name improves clarity.
5. Do not assign reserved names before a real role exists.
6. Container/service names should generally remain their normal upstream names unless there is a practical reason to alias them.
7. Documentation should record both old and new names during transitions.

## current reserved namespace

```text
homelab                 -> Fujigoko
major hosts             -> Fuji Five Lakes
physical networking     -> Japanese rivers
logical/transit network -> Shinkansen
central hubs            -> stations / major hubs
```

This document is the naming reference; individual host and network documents remain the source of truth for what is actually deployed.
