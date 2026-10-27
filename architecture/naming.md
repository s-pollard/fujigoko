# naming conventions

**/pleblab/** is the name of the overall homelab. Fujigoko and Gusuku are the two environments beneath it.

```text
/pleblab/
├── fujigoko  -> production
└── gusuku    -> experimentation / learning
```

The environments retain their existing Japan-based naming schemes. Names should identify infrastructure consistently without encoding sensitive or personal information.

## homelab

`/pleblab/` is the umbrella name for the complete homelab.

`fujigoko` is the production environment/repository, referring to the Fuji Five Lakes.

`gusuku` is the learning and experimentation environment/repository, using Okinawan castle names for physical lab hosts.

## major hosts — Fuji Five Lakes

Major Fujigoko physical servers use Fuji Five Lakes names.

| Name | Assignment |
| --- | --- |
| `kawaguchi`, `motosu`, `yamanaka` | Active production hosts; see [host inventory](../hosts/README.md) |
| `saiko`, `shoji` | Reserved / currently unused in Fujigoko |

The physical machine that was briefly documented as `saiko` moved out of Fujigoko into the separate Gusuku environment and was renamed `shuri`. Do not use `saiko` and `shuri` interchangeably: `shuri` belongs to Gusuku; `saiko` is again only a reserved Fujigoko lake name.

A lake name represents a major Fujigoko host, not a container, VM, or temporary service.

## personal computers — Japanese mountains

Personal desktops and laptops use Japanese mountain, peak, or volcano names: `aso`, `ontake`, `norikura`, and `azuma`. Aso remains a personal workstation even though it is the main administration device. These names are separate from Fujigoko server lake names and Gusuku castle names.

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

1. `/pleblab/` is the umbrella name for the entire homelab.
2. Fujigoko is the production environment; Gusuku is the learning/experimental environment.
3. Keep the Japan theme coherent inside the two environments.
4. Major Fujigoko physical hosts use Fuji Five Lakes names.
5. Prefer role-based naming categories over arbitrary place names.
6. Do not rename working infrastructure unless the new name improves clarity.
7. Do not assign reserved names before a real role exists.
8. Service/container names should normally remain upstream names.
9. Document old/new names during active transitions, then remove obsolete transition language afterward.
10. Names must not encode personal information, physical addresses, usernames, account IDs, or other identifying data.

This file defines naming policy. [Hosts](../hosts/README.md) and [network](../network/README.md) take precedence for deployed state.
