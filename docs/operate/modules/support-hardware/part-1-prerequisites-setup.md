---
title: "Part 1: Prerequisites and setup"
linkTitle: "Part 1: Setup"
weight: 31
layout: "docs"
type: "docs"
description: "Set up your development environment and prepare to create a custom Viam module."
---

**Part 1 of 5** | ⏱️ 15-20 minutes

In this tutorial series, you'll learn how to create a custom {{< glossary_tooltip term_id="module" text="module" >}} to add support for hardware that isn't already supported by existing registry modules.

## What you'll do in this part

- Install and authenticate the Viam CLI
- Set up a test machine (optional but recommended)
- Verify your development environment (Python 3.11+ or Go 1.20+)
- Write a test script to verify hardware connectivity
- Understand the module architecture

## What you'll build

Throughout this tutorial series, you'll create a **hello-world module** that demonstrates two common module capabilities:

1. **Camera model**: Returns an image from a configured file path
2. **Sensor model**: Returns a random number reading

This example shows how to implement multiple {{< glossary_tooltip term_id="resource" text="resources" >}} within a single module.

## Prerequisites

Before you begin, make sure you have the following:

### 1. Install and authenticate the Viam CLI

The Viam CLI is required to generate module code and upload modules to the registry.

Install the Viam CLI on your development machine:

{{< readfile "/static/include/how-to/install-cli.md" >}}

**Verify installation:**
```sh {class="command-line" data-prompt="$"}
viam version
```

You should see output like: `viam version 0.x.x`

**Authenticate to Viam:**

{{< readfile "/static/include/how-to/auth-cli.md" >}}

### 2. Set up a machine for testing

While you can develop a module without a machine, you'll need one to test your module.

{{% snippet "setup.md" %}}

**Already have a machine?** Great! You'll configure it in [Part 4](/operate/modules/support-hardware/part-4-test-locally/).

### 3. Development environment

Your module can be written in Python or Go. Choose your preferred language and verify your environment:

{{< tabs >}}
{{% tab name="Python" %}}

**Required:** Python 3.11 or newer

Check your version:
```sh {class="command-line" data-prompt="$"}
python3 --version
```

You should see: `Python 3.11.x` or higher

**Need to install Python 3.11+?**
- **macOS:** `brew install python@3.11`
- **Ubuntu/Debian:** `sudo apt install python3.11`
- **Windows:** Download from [python.org](https://python.org)

{{% /tab %}}
{{% tab name="Go" %}}

**Required:** Go 1.20 or newer

Check your version:
```sh {class="command-line" data-prompt="$"}
go version
```

You should see: `go version go1.20` or higher

**Need to install Go?**
Download from [go.dev](https://go.dev/dl/)

{{% /tab %}}
{{< /tabs >}}

## Write a test script

Before writing a module, it's helpful to write a simple test script to verify you can control your hardware.

For the example module, this script opens an image file and prints a random number.

{{< tabs >}}
{{% tab name="Python" %}}

Create a file named `test.py`:

```python {class="line-numbers linkable-line-numbers" data-start="1"}
import random
from PIL import Image

# Open an image
img = Image.open("example.png")
img.show()

# Return a random number
random_number = random.random()
print(random_number)
```

**Test it:**
```sh {class="command-line" data-prompt="$"}
python3 test.py
```

{{% /tab %}}
{{% tab name="Go" %}}

Create a file named `test.go`:

```go {class="line-numbers linkable-line-numbers" data-start="1"}
package main

import (
  "fmt"
  "math/rand"
  "os"
)

func main() {
  // Open an image
  imgFile, err := os.Open("example.png")
  if err != nil {
    fmt.Printf("Error opening image file: %v\n", err)
    return
  }
  defer imgFile.Close()
  imgByte, err := os.ReadFile("example.png")
  fmt.Printf("Image file type: %T\n", imgByte)
  if err != nil {
    fmt.Printf("Error reading image file: %v\n", err)
    return
  }

  // Return a random number
  number := rand.Float64()
  fmt.Printf("Random number: %f\n", number)
}
```

**Test it:**
```sh {class="command-line" data-prompt="$"}
go run test.go
```

{{% /tab %}}
{{< /tabs >}}

{{< alert title="Tip" color="tip" >}}
For your own hardware, replace this test script with code that uses the manufacturer's API or SDK to control your device.
{{< /alert >}}

## Understanding module architecture

A module is essentially a packaged wrapper around your hardware control code. The module:

1. **Registers** with `viam-server` when it starts
2. **Validates** user configuration when they add your component
3. **Implements** standard Viam API methods (like `GetImages` for cameras)
4. **Communicates** with your hardware using your control code

In [Part 2](/operate/modules/support-hardware/part-2-choose-api-generate/), you'll choose which Viam API best matches your hardware's capabilities.

## What you've accomplished

**Environment ready:**
- Viam CLI installed and authenticated
- Machine set up for testing (optional)
- Development environment verified (Python 3.11+ or Go 1.20+)
- Test script working

**Understanding:**
- What modules are and why you'd create one
- Basic module architecture

## Next steps

Now that your environment is ready, continue to [Part 2: Choose an API and generate code](/operate/modules/support-hardware/part-2-choose-api-generate/) to select the right API for your hardware and generate your module structure.

---

**Tutorial navigation:**
- **Current:** Part 1: Prerequisites and setup
- **Next:** [Part 2: Choose an API and generate code →](/operate/modules/support-hardware/part-2-choose-api-generate/)
- **All parts:** [Module creation tutorial](/operate/modules/support-hardware/)
