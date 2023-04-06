---
title: Remote
id: remote
full_link: /manage/parts-and-remotes/
short_description: A robot part which is controlled by another robot part.
aka:
---

A robot part which is controlled by another robot part.

A robot part which is controlled by another robot part. The connection from one part to another part. Remotes are established using direct gRPC or gRPC through WebRTC. Within a robot, a main part always establishes a remote to each of the other parts associated with the robot. When a remote is established, the part establishing the remote will surface all of the other part’s resources as its own. A client application connecting to the part will see all of the part’s local resources and remote resources.
