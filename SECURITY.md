# security

This is a public infrastructure-documentation repository. It should describe architecture and recovery without publishing secrets or unnecessary identifying information.

## never commit

- passwords, API keys, tokens, private keys, recovery codes, or MFA/TOTP seeds
- `.env` files or application exports containing secrets
- public/WAN IP addresses or VPN endpoints
- MAC addresses, hardware serial numbers, device IDs, account IDs, or email addresses
- exact private IP assignments, DHCP reservations, VLAN IDs, or management URLs
- cloud bucket names or other unique external resource identifiers
- street addresses, building names, or other personal location details
- password-vault contents, synchronization credentials, or recovery material

## okay to document publicly

- vendor/model names and non-unique hardware specifications
- high-level topology and host roles
- service names and non-secret dependencies
- storage/backup policy without credential details
- generic recovery order and architecture decisions
- RFC1918 addressing concepts without publishing the actual assignments

## private operational documentation

Keep the following outside this repository:

- exact addressing/IPAM
- VLAN numbers and switch-port assignments where they are operationally sensitive
- WAN/ISP identifiers
- credentials and secret-file locations
- VPN configuration
- cloud resource identifiers
- service admin URLs

If local private notes are kept alongside a clone of this repo, use ignored files/directories rather than committing them.

## history warning

Deleting sensitive text in a later commit does not remove it from Git history. If an actual secret, personal identifier, or unique external resource identifier is ever committed, rotate/revoke the secret as appropriate and rewrite repository history before treating it as removed.
