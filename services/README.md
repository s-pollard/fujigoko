# services

## kawaguchi

### monitoring / infrastructure

- prometheus
- grafana
- cadvisor
- uptime-kuma
- adguard-home

### media

- plex
- sonarr
- radarr
- sabnzbd
- bazarr
- seerr
- tautulli
- recyclarr
- unpackerr

### manga / books / games

- komga
- komf
- tachidesk
- romm

### documents / utilities / personal

- paperless-ngx
- stirling pdf
- linkwarden
- mealie
- homebox
- actual budget
- homepage

### fitness

- endurain

### supporting services

- postgresql17-linkwarden
- mariadb
- redis
- endurain-postgres
- endurain redis

## verified kawaguchi dependencies

```text
sabnzbd
  -> /mnt/user/downloads/complete
  -> /mnt/user/downloads/incomplete-downloads

sonarr
  -> /mnt/user/downloads/complete
  -> /mnt/user/media/tv

radarr
  -> /mnt/user/downloads/complete
  -> /mnt/user/media/movies

unpackerr
  -> /mnt/user/downloads/complete

bazarr
  -> /mnt/user/media/tv
  -> /mnt/user/media/movies

plex
  -> /mnt/user/media

komga
  -> /mnt/user/media/manga

komf
  -> /mnt/user/media/manga
  -> /mnt/user/Media/books  # legacy/unused candidate

tachidesk
  -> /mnt/user/media/manga

paperless-ngx
  -> /mnt/user/media/paperless/consume
  -> /mnt/user/media/paperless/export
  -> /mnt/user/media/paperless/media

linkwarden
  -> postgresql17-linkwarden via kawaguchi:5432

romm
  -> mariadb via kawaguchi:3306

paperless-ngx
  -> redis via kawaguchi:6379

endurain-app
  -> endurain-postgres
  -> redis

adguard-home
  -> LAN DNS service at 192.168.1.53
  -> upstream DNS via Quad9 DNS-over-HTTPS
```

## kawaguchi docker networking

- `host`
  - Plex-Media-Server
- `endurain_default`
  - endurain-app
  - endurain-postgres
  - redis
- custom `br0`
  - adguard-home at `192.168.1.53`
- default `bridge`
  - most remaining services
- currently unused networks
  - `homelable`
  - `wg0`

## motosu

### immich stack

- immich_server
- immich_postgres
- immich_redis
- immich_machine_learning

All four Immich containers use the dedicated `immich_default` Docker bridge.

### immich persistent data

```text
/volume1/docker/immich/library
  -> immich_server:/data

/volume1/docker/immich/postgres
  -> immich_postgres:/var/lib/postgresql/data

immich_model-cache docker volume
  -> immich_machine_learning:/cache
```

The model cache is rebuildable. The library and PostgreSQL data are the critical Immich persistence paths.

### remote access

- tailscale
  - network mode: host
  - state: `/volume1/docker/tailscale/state`

## planned yamanaka additions

### nextcloud

Nextcloud is the selected self-hosted replacement for Google Drive.

- target host: Yamanaka
- status: planned; not yet deployed
- live application state and database remain on Yamanaka local NVMe
- important user files, database backups, configuration, and recovery data should be backed up independently to Motosu
- Immich remains the photo system; Nextcloud should not replace the Motosu/Immich photo workflow

### vaultwarden

Vaultwarden is the selected self-hosted Bitwarden-compatible password vault.

Initial deployment model:

```text
Bitwarden Premium / Bitwarden Cloud
        primary
          |
          | daily one-way synchronization
          v
Vaultwarden on Yamanaka
        secondary
```

- target host: Yamanaka
- status: planned; not yet deployed
- Bitwarden Premium remains the authoritative vault until the existing subscription expires sometime in 2027
- Vaultwarden initially serves as a secondary copy and self-hosting trial
- synchronization should be one-way from Bitwarden Cloud to Vaultwarden; do not use bidirectional synchronization
- TOTP secrets stored with Bitwarden login items should be preserved by the vault migration/synchronization process
- before changing the primary vault, verify representative passwords, attachments, passkeys/TOTP behavior as applicable, backups, and a tested Vaultwarden restore path
- when Bitwarden Premium expires, reassess whether Vaultwarden should become the primary vault

Vaultwarden contains security-critical data. Its persistent data and configuration require independent backup to Motosu and selected off-site protection through the Yamanaka backup design.

## planned DNS target

The current single AdGuard Home instance on Kawaguchi is temporary.

Target placement:

```text
yamanaka
└── adguard-home

motosu
└── adguard-home
```

Both instances should be advertised to clients through DHCP and kept aligned so either resolver can continue serving filtered DNS when the other host is unavailable. Exact addresses and synchronization/upstream details will be finalized during the network rebuild.
