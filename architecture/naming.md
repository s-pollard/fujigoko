# naming conventions

Fujigoko uses a Japan-based naming scheme. Names should identify infrastructure consistently without encoding sensitive or personal information.

## homelab

`fujigoko` is the production homelab/repository name, referring to the Fuji Five Lakes.

## major hosts — Fuji Five Lakes

Major Fujigoko physical servers use Fuji Five Lakes names.

```text
kawaguchi  -> media / Unraid
motosu     -> photos / TrueNAS / Immich / backups
yamanaka   -> general applications
saiko      -> reserved / currently unused in fujigoko
shoji      -> reserved / currently unused
```

The physical machine that was briefly documented as `saiko` moved out of Fujigoko into the separate gusuku lab and was renamed `shuri`. Do not use `saiko` and `shuri` interchangeably: `shuri` belongs to gusuku; `saiko` is again only a reserved Fujigoko lake name.

A lake name represents a major Fujigoko host, not a container, VM, or temporary service.

## physical networking — rivers

Japanese river names are reserved for physical network infrastructure where useful, such as core, aggregation, or access switching.

Do not rename working production hardware solely to satisfy the convention. Apply the convention when it improves clarity during a rebuild or replacement.

## logical networking / transit — Shinkansen

Shinkansen-related names are reserved for logical or transit-oriented networking concepts where useful, such as VPN/transit networks, inter-site links, or routing projects.

Do not assign one until a real component needs it.

## hubs / centralized infrastructure — stations

Japanese station or major-hub names are reserved for centralized infrastructure where the metaphor fits, such as management/control-plane services or shared infrastructure hubs.

Ordinary application containers should generally keep their normal upstream names.

## naming rules

1. Keep the Japan theme coherent.
2. Major Fujigoko physical hosts use Fuji Five Lakes names.
3. Prefer role-based naming categories over arbitrary place names.
4. Do not rename working infrastructure unless the new name improves clarity.
5. Do not assign reserved names before a real role exists.
6. Service/container names should normally remain upstream names.
7. Document old/new names during active transitions, then remove obsolete transition language afterward.
8. Names must not encode personal information, physical addresses, usernames, account IDs, or other identifying data.

## namespace

```text
homelab                 -> Fujigoko
major hosts             -> Fuji Five Lakes
physical networking     -> Japanese rivers
logical/transit network -> Shinkansen
central hubs            -> stations / major hubs
```

This file defines naming policy. Host and network documents remain the source of truth for what is actually deployed.
