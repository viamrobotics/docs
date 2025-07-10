---
title: "Configuration notes"
linkTitle: "Configuration notes"
weight: 50
type: "docs"
description: "Add descriptive notes to any resource in your machine configuration to document purpose, settings, and important information."
tags: ["configuration", "documentation", "notes"]
date: "2025-07-10"
---

You can add descriptive notes to any resource in your machine configuration to help document its purpose, configuration details, or other important information. The Notes section is available for all resource types and appears in both machine builder and fragment builder interfaces.

## Supported resource types

Notes can be added to all resource types in your configuration:

- **Components**: All component types including cameras, motors, sensors, arms, bases, and more
- **Services**: Motion, vision, SLAM, navigation, data management, and other services
- **Remotes**: Remote machine parts and connections
- **Local resources**: Local modules and processes
- **Triggers**: Data capture and notification triggers
- **Packages**: ML models and other packages
- **Modules**: Both registry and local modules

## Adding notes to resources

### Using the configuration builder

1. Navigate to your machine's **CONFIGURE** tab
2. Find the resource you want to add notes to
3. In the resource configuration card, scroll to the bottom to find the **Notes** section
4. Click **Add notes** to create a text field
5. Type your descriptive information in the textarea that appears
6. Save your configuration

The Notes section always appears as the last section in every resource configuration card, maintaining consistency with other configuration sections like "Data Capture" or "Frame".

### Using JSON configuration

Notes are stored as a first-order property in your configuration JSON, appearing at the same level as other resource properties:

```json
{
  "components": [
    {
      "name": "my-camera",
      "model": "webcam",
      "type": "camera",
      "attributes": {
        "video_path": "video0"
      },
      "notes": "Main surveillance camera - positioned at front entrance, requires good lighting"
    }
  ],
  "services": [
    {
      "name": "motion",
      "type": "motion",
      "attributes": {},
      "notes": "Motion planning service configured with custom constraints for warehouse environment"
    }
  ],
  "modules": [
    {
      "type": "registry",
      "name": "viam_ultrasonic",
      "module_id": "viam:ultrasonic",
      "version": "0.0.2",
      "notes": "Ultrasonic sensor module for obstacle detection - version pinned for stability"
    }
  ]
}
```

## What to include in notes

Use notes to document information that helps you and your team understand and maintain your configuration:

### Hardware information
- Physical location or mounting details
- Hardware specifications or model numbers
- Calibration settings or procedures
- Wiring or connection details

### Configuration details
- Purpose or role of the resource
- Custom settings or non-standard configurations
- Dependencies or relationships with other resources
- Performance characteristics or limitations

### Operational information
- Maintenance schedules or requirements
- Known issues or troubleshooting notes
- Usage patterns or operational constraints
- Integration details with external systems

### Examples

**Camera component:**
```
"notes": "Warehouse security camera #3 - mounted 12ft high on east wall, covers loading dock area. Requires manual focus adjustment after power cycles. IP: 192.168.1.103"
```

**Motor component:**
```
"notes": "Left drive motor for rover base. Encoder ratio 1:50, max safe RPM 200. Replace brushes every 6 months. Last maintenance: 2025-06-15"
```

**Motion service:**
```
"notes": "Configured with conservative speed limits for safety in shared workspace. Obstacle detection enabled with 0.5m safety margin. Emergency stop connected to GPIO pin 18"
```

**Module:**
```
"notes": "Custom sensor module v2.1.3 - includes temperature compensation algorithm. Built from source on 2025-07-01. Contact: engineering@company.com"
```

## Notes in fragments

When you add notes to resources in a [fragment](/manage/fleet/reuse-configuration/), those notes are included when the fragment is used on machines. This allows you to document standard configurations and share that documentation across your fleet.

Notes in fragments can be overridden on individual machines using [fragment modifications](/manage/fleet/reuse-configuration/#modify-fragment-settings-on-a-machine) if needed:

```json
{
  "fragment_mods": [
    {
      "fragment_id": "your-fragment-id",
      "mods": [
        {
          "$set": {
            "components.camera1.notes": "Modified for outdoor use - weatherproof housing installed"
          }
        }
      ]
    }
  ]
}
```

## Best practices

### Keep notes current
- Update notes when you make configuration changes
- Include dates for time-sensitive information
- Remove outdated information to avoid confusion

### Be specific and actionable
- Include specific model numbers, settings, or procedures
- Provide contact information for custom components
- Document any special requirements or constraints

### Use consistent formatting
- Develop a standard format for your team
- Include key information like location, purpose, and maintenance details
- Use clear, concise language

### Consider your audience
- Write notes that will be helpful to other team members
- Include context that might not be obvious from the configuration alone
- Document any tribal knowledge or institutional memory

## Searching and managing notes

Notes are stored as part of your machine configuration and can be:

- Searched within the Viam app's configuration interface
- Included in configuration exports and backups
- Version controlled along with your configuration changes
- Shared when you duplicate or template machine configurations

Since notes are stored as standard JSON fields, you can also use external tools to search across multiple machine configurations or generate documentation from your fleet's configuration notes.