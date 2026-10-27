# security

This is a public infrastructure-documentation repository. It should describe architecture and recovery without publishing secrets or unnecessary identifying information.

## never commit

- passwords, API keys, tokens, private keys, recovery codes, or MFA/TOTP seeds
- `.env` files or application exports containing secrets
- public/WAN IP addresses or VPN endpoints
- the private application namespace or application/management DNS names beneath it
- MAC addresses, hardware serial numbers, device IDs, account IDs, or email addresses
- exact private IP assignments, DHCP reservations, VLAN IDs, or switch-port assignments that expose operational addressing
- credentials, secret-file contents, identity-provider client secrets, or callback configuration containing sensitive identifiers
- cloud bucket names or other unique external resource identifiers unless they are intentionally designated as public documentation
- street addresses, building names, or other personal location details
- password-vault contents, synchronization credentials, or recovery material

## okay to document publicly

- vendor/model names and non-unique hardware specifications
- high-level topology and host roles
- service names and non-secret dependencies
- storage/backup policy without credential details
- generic recovery order and architecture decisions
- RFC1918 addressing concepts without publishing the actual assignments
- generic descriptions of private DNS and reverse-proxy access without the application namespace or DNS names

Keep the application namespace and its DNS names in private operational documentation. Bare host names used for hardware inventory remain part of the public architecture.

## private operational documentation

Keep the following outside this repository:

- exact addressing/IPAM
- the private application namespace and its DNS names
- VLAN numbers and switch-port assignments where they are operationally sensitive
- WAN/ISP identifiers
- credentials and secret-file contents
- VPN configuration
- cloud resource identifiers that are not intentionally public
- SSO/OIDC client IDs, client secrets, sensitive callback configuration, and recovery material
- service-specific admin paths and management URLs

If local private notes are kept alongside a clone of this repo, use ignored files/directories rather than committing them.

## history warning

Deleting sensitive text in a later commit does not remove it from Git history. If an actual secret, personal identifier, or unique external resource identifier is ever committed, rotate/revoke the secret as appropriate and rewrite repository history before treating it as removed.
