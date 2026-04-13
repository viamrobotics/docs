---
linkTitle: "Go setup"
title: "Go setup"
weight: 60
layout: "docs"
type: "docs"
description: "Set up a project for writing a Viam app in Go: a backend service, a fleet orchestrator, a CLI tool, or any other Go program that talks to a Viam machine."
date: "2026-04-13"
---

Set up a project for writing a Viam app in Go: a backend service, a fleet orchestrator, a CLI tool, or any other Go program that talks to a Viam machine. The Go client lives in the RDK package at `go.viam.com/rdk/robot/client`, not in a separate SDK. For the connection patterns your app will actually use, see [Connect to a machine](../../tasks/connect-to-machine/).

## Prerequisites

- Go 1.21 or later
- A configured Viam machine
- The machine's address, an API key, and an API key ID

Get the three credentials from the machine's **CONNECT** tab in the Viam app: go to the machine's page, click **CONNECT**, select **Golang**, and toggle **Include API key** on. Copy the address, API key, and API key ID from the generated code sample.

## Create a project

```sh {class="command-line" data-prompt="$"}
mkdir my-viam-app
cd my-viam-app
go mod init my-viam-app
```

## Install the client package

```sh {class="command-line" data-prompt="$"}
go get go.viam.com/rdk/robot/client
```

This pulls the RDK client package and its dependencies. After writing the code below, run `go mod tidy` to clean up the module file.

## Verify the connection

Create `main.go`:

```go
package main

import (
    "context"
    "fmt"
    "os"

    "go.viam.com/rdk/logging"
    "go.viam.com/rdk/robot/client"
    "go.viam.com/utils/rpc"
)

func main() {
    logger := logging.NewDebugLogger("client")

    address := os.Getenv("MACHINE_ADDRESS")
    apiKeyID := os.Getenv("API_KEY_ID")
    apiKey := os.Getenv("API_KEY")

    machine, err := client.New(
        context.Background(),
        address,
        logger,
        client.WithDialOptions(rpc.WithEntityCredentials(
            apiKeyID,
            rpc.Credentials{
                Type:    "api-key",
                Payload: apiKey,
            },
        )),
    )
    if err != nil {
        logger.Fatal(err)
    }
    defer machine.Close(context.Background())

    fmt.Printf("Connected. Found %d resources.\n", len(machine.ResourceNames()))
}
```

Run `go mod tidy` to resolve dependencies, then run with your credentials:

```sh {class="command-line" data-prompt="$"}
go mod tidy
MACHINE_ADDRESS=my-robot-main.xxxx.viam.cloud \
  API_KEY_ID=your-api-key-id \
  API_KEY=your-api-key-secret \
  go run main.go
```

You should see:

```text
Connected. Found N resources.
```

where `N` is the number of components and services on your machine.

Always call `machine.Close(ctx)` when done (or use `defer` as shown above) to release the connection cleanly.

## Credentials in production

The example above reads credentials from environment variables set inline on the command line. For a deployed service, set environment variables through your deployment platform (systemd unit file, Kubernetes secret, Docker Compose `.env`, or similar) rather than passing them on the command line.

## Troubleshooting

- **`go mod tidy` errors.** The RDK has many transitive dependencies. If `go mod tidy` fails with version conflicts, check that your Go version is 1.21 or later and that you are not inside another module's directory.
- **Connection hangs or times out.** Verify the machine address matches the **CONNECT** tab exactly. Verify the machine is online in the Viam app.
- **Credentials wrong.** The `rpc.WithEntityCredentials` call takes the API key ID as the first argument and the API key secret as `Payload`. Reversing them causes an authentication failure with a generic error message.

## Next

- [Connect to a machine](../../tasks/connect-to-machine/) for the connection patterns your app will actually use
- [Handle disconnection and reconnection](../../tasks/handle-connection-state/) for reconnection and status indicators
- [Go SDK reference](https://pkg.go.dev/go.viam.com/rdk) for per-component API details
