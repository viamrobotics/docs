Update an existing machine's name and/or location.

You can change:
- The machine's name (within the same location)
- The machine's location (within the same organization)
- Both name and location simultaneously

**Requirements for location changes:**
- You must be an organization owner, or have owner permissions for both the current and destination locations
- The destination location must be within the same organization
- No other machine in the destination location can have the same name

**Important:** Changing a machine's location updates its network address to `<machine-main-part-name>.<new-location-id>.viam.cloud`. You'll need to update any code that references the old address.