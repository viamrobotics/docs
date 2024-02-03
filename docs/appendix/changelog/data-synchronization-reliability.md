---
title: Data synchronization reliability
date: "2022-12-01"
color: "improved"
---

Previously, data synchronization used bidirectional streaming.
Now is uses a simpler unary approach that is more performant on batched unary calls, is easier to load balance, and maintains ordered captures.
