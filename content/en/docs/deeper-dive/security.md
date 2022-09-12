---
title: "Security"
linkTitle: "Security"
weight: 10
type: "docs"
description: "Explanation of how we manage shared secrets and authentication throughout the Viam system."
---
## Authentication
Authentication in the app is represented by an `auth.State` object.
It is the source of truth for what resources an entity (some object, not necessarily a user) is authorized to access/manipulate.
There are presently two ways that entities can authenticate into the app.

The first is a human user.
This is done via a streamlined auth0 integration that uses cookies to carry session state.
The session conveys the user's email which we consider unique across the system.
We have Google Single Sign-On and email/password enabled which creates a user on auth0's side but is only allowed to fully log in on our side if they are either an @viam.com email or invited to participate on the website.
The cookie we write for this is consumed in `server.authMiddleware` and produces an `auth.State` comprised of the organizations the user is a part of.

The second is a robot part running the RDK.
Every robot part has a secret key associated with it that, when starting up the RDK server, it uses to pull the configuration file from the Viam App at [https://app.viam.com](https://app.viam.com), as well as where to send logs from the robot to.
The `auth.State` for this is also built in `server.authMiddleware` but conveys no information about who the user is and instead has them logged out with a secret attached to its context.
This happens over a legacy JSON API.

In addition to the RDK using the legacy JSON API, it also uses gRPC along with `go.viam.com/utils/rpc` to access both the WebRTC signaling server to answer peer-to-peer connections and a TLS certificate provided by the app to talk to other robot parts in its same location.

Authentication into gRPC works by configuring our server with a series of authentication handlers provided by the `go.viam.com/utils/rpc` framework.
Each handler is associated with a type of credentials to handle (`rpc.CredentialsType`) and an `rpc.AuthHandler` which contains two methods: Authenticate and VerifyEntity.
Authenticate is responsible for taking the name of an entity and a payload that proves the caller is allowed to assume the role of that entity.
It returns metadata about the entity (e.g. an email, a user ID, or in our case the robot part ID).
The framework then returns a JWT to the client (the RDK) to use in subsequent requests.
On those subsequent requests, the JWT is included in an HTTP header called Authorization with a value of Bearer <token>.
The framework then intercepts all calls and ensures that there is a JWT present in the header, it is cryptographically valid, and then hands it off to the VerifyEntity method which will pull metadata out of the JWT from Authenticate and return a value that represents the authenticated entity to use in the actual gRPC call.
It is accessed via `rpc.MustContextAuthEntity`.

Bridging is the concept of translating app's concept of authentication to the gRPC framework and vice versa.
Since all of our code cares about `auth.State`, we have gRPC interceptors that take the auth entity and convert it into an `auth.State` which is returned in all of our VerifyEntity methods.
This is the process of bridging gRPC into our native way of thinking about authentication and authorization (`auth.State`).
A special note is that we have an extra authentication handler in app for gRPC called internal that only gets used locally to the server itself.
The sole purpose of it is that if your authentication is via a cookie or the secret header, we will have your `auth.State` in authMiddleware and in order to call gRPC based methods (e.g. save a robot part config in the UI), we bridge `auth.State` into the gRPC framework by using a synthetic JWT that has no identifying information but the VerifyEntity method will pull the `auth.State` out of the context so that it can be converted into an auth entity and later converted back into an `auth.State` in the interceptor mentioned above.

## Authorization
As mentioned in Authentication, `auth.State` is the source of truth about who an entity is and what resources they are authorized to access/manipulate.
This is represented by organizations they are a part of, what specific robots they are okay to access, as well as an associated secret (of a robot part).
Almost every action on the app involves either looking up data or manipulating data.
As such, the best place to do authorization is on every data access and manipulation.
This happens in `auth.permissionedData` which implements the `data.Data` interface and wraps a MongoDB based `data.Data`.
It does all authorization checks by consulting the `auth.State` present in the context.
Some methods don't require an explicit authorization check in code.
RobotPartByIDAndSecret, for example, is implicitly authorized because if a document can be found by supplying both unique robot part ID and secret, clearly the use is authenticated and authorized.
In fact, the gRPC based robot secret `rpc.AuthHandler` uses this to be able to use `auth.permissionedData` and look up the part and then build an `auth.State` where it is logged in and has access to the org and robot part.
There are however some areas where authorization must still be done where data doesn't need to be explicitly accessed.
In these cases, we need to explicitly attempt to access data being referred to in order to invoke authorization primitives.
One place where this happens is the WebRTC signaling server.
We wrap the provided `rpc.WebRTCSignalingServer` with a `server.authorizingWebRTCSignalingServer` where for every host mentioned that wishes to either make an offer to start a connection or answer said offer, we do a lookup for the associated robot part which invokes authorization for that part.
Currently a robot part can connect to any other robot part in the same organization.

### Authentication/connection to to other robot parts in the RDK/SDKs

Every robot in the same location shares both a TLS certificate and a secret.
A robot part managed by `viam.cloud` (`app.viam.com`'s robot domain) receives both pieces of this information on startup and periodically asks if there is a new TLS certificate (once an hour).

Using the TLS certificate, an RDK can 1. host a secure server and 2. use the certificate with mutual TLS to authenticate itself to other robots without having to send any secrets when on the same local network; this is accomplished by using multicast DNS.
If the other robot cannot be found locally, a WebRTC connection will be established using the robot's personal secret, not the location secret.

## TLS Certificates

As soon as a location is created for the first time, the `auth.CertificateManager` gets word of this and goes into action by beginning to issue the location a TLS certificate.
It uses the [ACME protocol](https://datatracker.ietf.org/doc/html/rfc8555)[^acme] to talk to our
configured TLS provider ([Let's Encrypt](https://letsencrypt.org/)[^le]) and then issue a TLS certificate that will last for 90 days for the location under the wildcard DNS names of `*.<location_id>.viam.cloud` and `*.<location_id>.local.viam.cloud`.

[^acme]:ACME protocol: [https://datatracker.ietf.org/doc/html/rfc8555](https://datatracker.ietf.org/doc/html/rfc8555)

[^le]:Let's Encrypt:[https://letsencrypt.org/](https://letsencrypt.org/)

When a certificate is 1/3 through its way of its lifetime, we will make a note to renew it.
This means we expect robots in a single location to come online once within 2 months after getting its last certificate in order to not have an expired certificate.
In order to provide a better user experience around having a TLS certificate as soon as a location is created, we employ the `data.LocationPreallocator` to have a minimum number of locations always created and unassigned such that the certificate manager picks those up for certificate issuance.
