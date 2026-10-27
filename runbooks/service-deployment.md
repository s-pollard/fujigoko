# service deployment

Use this sequence for future migrations or new stateful production services. Placement and lifecycle decisions belong in [classification](../services/classification.md).

1. Identify persistence and dependencies.
2. Create an independent backup/export.
3. Deploy on the destination host.
4. Restore/copy persistence when applicable.
5. Verify application behavior.
6. Verify dependencies and authentication.
7. Establish independent backup coverage.
8. Perform a representative restore test.
9. Observe production behavior before removing fallback paths.

Record deployed service state in [services](../services/README.md), live paths in [storage](../storage/README.md), and protected scope and restore evidence in [backups](../backups/README.md). Keep completed cutovers and retired state in [history](../history/README.md).
