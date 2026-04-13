---
linkTitle: "C++ setup"
title: "C++ setup"
weight: 70
layout: "docs"
type: "docs"
description: "Set up a project for writing a Viam app in C++: an embedded application, a high-performance service, or any other C++ program that talks to a Viam machine."
date: "2026-04-13"
---

Set up a project for writing a Viam app in C++: an embedded application, a high-performance service, or any other C++ program that talks to a Viam machine. The C++ SDK has a heavier build setup than the other SDKs because it requires CMake and several system-level dependencies. For the connection patterns your app will actually use, see [Connect to a machine](../../tasks/connect-to-machine/).

## Prerequisites

- CMake 3.25 or later
- A C++ compiler with C++17 support
- The following system libraries, installed through your package manager:

  **Linux (apt):**

  ```sh {class="command-line" data-prompt="$"}
  sudo apt-get install cmake build-essential libboost-all-dev libgrpc++-dev libprotobuf-dev libxtensor-dev pkg-config ninja-build
  ```

  **macOS (Homebrew):**

  ```sh {class="command-line" data-prompt="$"}
  brew install cmake boost grpc protobuf xtensor pkg-config ninja buf
  ```

- A configured Viam machine
- The machine's URI (address), an API key ID, and an API key

Get the three credentials from the machine's **CONNECT** tab in the Viam app: go to the machine's page, click **CONNECT**, select **C++**, and toggle **Include API key** on.

## Build or install the SDK

The C++ SDK can be built from source or consumed through the [Conan package manager](https://github.com/viamrobotics/viam-cpp-sdk/blob/main/doc/conan.md). Building from source:

```sh {class="command-line" data-prompt="$"}
git clone https://github.com/viamrobotics/viam-cpp-sdk.git
cd viam-cpp-sdk
mkdir build
cd build
cmake .. -G Ninja
ninja
sudo ninja install
```

See the SDK's [BUILDING.md](https://github.com/viamrobotics/viam-cpp-sdk/blob/main/doc/BUILDING.md) for the full set of CMake options, Conan instructions, and Docker-based development workflows.

## Create a project

Create a directory for your app:

```sh {class="command-line" data-prompt="$"}
mkdir my-viam-app
cd my-viam-app
```

Create a `CMakeLists.txt`:

```cmake
cmake_minimum_required(VERSION 3.25)
project(my-viam-app)

find_package(viam-cpp-sdk REQUIRED)

add_executable(my-viam-app main.cpp)
target_link_libraries(my-viam-app PRIVATE viam-cpp-sdk::viamsdk)
```

## Verify the connection

Create `main.cpp`:

```cpp
#include <cstdlib>
#include <iostream>
#include <memory>
#include <string>
#include <vector>

#include <viam/sdk/common/instance.hpp>
#include <viam/sdk/robot/client.hpp>
#include <viam/sdk/rpc/dial.hpp>

using namespace viam::sdk;

int main() {
    Instance inst;

    const char* uri = std::getenv("MACHINE_ADDRESS");
    const char* key_id = std::getenv("API_KEY_ID");
    const char* key = std::getenv("API_KEY");

    if (!uri || !key_id || !key) {
        std::cerr << "Set MACHINE_ADDRESS, API_KEY_ID, and API_KEY\n";
        return 1;
    }

    ViamChannel::Options channel_options;
    channel_options.set_entity(std::string(key_id));
    Credentials credentials("api-key", std::string(key));
    channel_options.set_credentials(credentials);
    Options options(1, channel_options);

    auto robot = RobotClient::at_address(std::string(uri), options);

    std::vector<Name> resource_names = robot->resource_names();
    std::cout << "Connected. Found " << resource_names.size()
              << " resources." << std::endl;

    return 0;
}
```

Build and run:

```sh {class="command-line" data-prompt="$"}
mkdir build
cd build
cmake ..
make
MACHINE_ADDRESS=my-robot-main.xxxx.viam.cloud \
  API_KEY_ID=your-api-key-id \
  API_KEY=your-api-key-secret \
  ./my-viam-app
```

You should see:

```text
Connected. Found N resources.
```

where `N` is the number of components and services on your machine.

The `Instance` object must be created before any other SDK objects and must outlive them all. It initializes the SDK's internal state. Creating it at the top of `main()` and letting it go out of scope at the end is the standard pattern.

## WebRTC note

The C++ SDK's WebRTC support is implemented through a Rust FFI layer. The SDK's README notes that this implementation is still maturing and may have issues with streaming requests. If you encounter problems with WebRTC connections, disable WebRTC to fall back to direct gRPC. See the [SDK's README](https://github.com/viamrobotics/viam-cpp-sdk#a-note-on-connectivity-and-webrtc-functionality) for the current status.

## Troubleshooting

- **`find_package(viam-cpp-sdk)` fails.** The SDK is not installed or not on CMake's search path. Rebuild and install the SDK (`sudo ninja install`), or set `CMAKE_PREFIX_PATH` to where you installed it.
- **Linker errors referencing Boost, gRPC, or protobuf.** One of the system dependencies is missing or is an incompatible version. Reinstall through your package manager and confirm versions meet the minimums.
- **Connection hangs.** Verify the machine address matches the **CONNECT** tab exactly. If WebRTC is the issue, try disabling it to isolate the transport layer from your application logic.

## Next

- [Connect to a machine](../../tasks/connect-to-machine/) for the connection patterns your app will actually use
- [Handle connection state](../../tasks/handle-connection-state/) for reconnection and status indicators
- [C++ SDK reference](https://cpp.viam.dev/) for per-component API details
- [BUILDING.md](https://github.com/viamrobotics/viam-cpp-sdk/blob/main/doc/BUILDING.md) for the full build system documentation
