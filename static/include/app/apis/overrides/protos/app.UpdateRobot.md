Update an existing machine's name and/or location.

You can change:

- The machine's name (within the same location)
- The machine's location (within the same organization)
- Both name and location simultaneously

**Requirements for location changes:**

- You must be an organization owner, or have owner permissions for both the current and destination locations
- The destination location must be within the same organization
- No other machine in the destination location can have the same name

{{< alert title="Important" color="note" >}}
Moving a machine has several important implications:

- **Machine address changes**: The machine's network address will change to `<machine-main-part-name>.<new-location-id>.viam.cloud`. You'll need to update any code that references the old address.
- **Permission changes**: Access permissions will be updated. Users with access to the current location lose access, and users with access to the new location gain access to the machine.
- **Data access**: Users in the new location cannot access historical data from when the machine was in the previous location.
{{< /alert >}}
