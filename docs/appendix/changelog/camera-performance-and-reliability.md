---
title: Camera performance and reliability
date: "2022-12-01"
color: "improved"
---

- Improved server-side logic to choose a mime type based on the camera image type, unless a specified mime type is supplied in the request.
  **The default mime type for color cameras is now JPEG**, which improves the streaming rate across every SDK.
- Added discoverability when a camera reconnects without changing video paths.
  This now triggers the camera discovery process, where previously users would need to manually restart the RDK to reconnect to the camera.
