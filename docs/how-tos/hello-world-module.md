---
title: "Create a Hello World module"
linkTitle: "Hello World module"
type: "docs"
weight: 24
images: ["/registry/module-puzzle-piece.svg"]
icon: true
tags: ["modular resources", "components", "services", "registry"]
description: "Get started with custom module creation by creating a Hello World modular resource."
languages: ["python", "go"]
viamresources: ["components"]
platformarea: ["registry"]
level: "Beginner"
date: "2024-10-22"
# updated: ""  # When the tutorial was last entirely checked
cost: "0"
---

This guide will walk you through creating a simple {{< glossary_tooltip term_id="modular-resource" text="modular resource" >}} that responds to API calls by returning a random number, and a configured image.
The goal is to familiarize you with how to create your own {{< glossary_tooltip term_id="module" text="modules" >}} and [modular resources](/registry/modular-resources/).

{{% alert title="In this page" color="tip" %}}

1. [Concepts](#what-is-a-module-what-is-a-modular-resource)
1. [Write the basic functionality into a test script](#write-the-basic-functionality-into-a-test-script)
1. [Choose an API](#choose-an-api-to-implement)
1. [Generate code stub files](#generate-stub-files)
1. [Implement the API](#implement-the-API)
1. Test your module
1. Package the module

{{% /alert %}}

## Prerequisites

{{< expand "Install the Viam CLI and authenticate" >}}
Install the Viam CLI and authenticate to Viam, from the same machine that you intend to upload your module from.

{{< readfile "/static/include/how-to/install-cli.md" >}}

Authenticate your CLI session with Viam using one of the following options:

{{< readfile "/static/include/how-to/auth-cli.md" >}}
{{< /expand >}}

## What is a module? What is a modular resource?

A module is a set of files that provides support for one or more {{< glossary_tooltip term_id="component" text="components" >}} or {{< glossary_tooltip term_id="service" text="services" >}} that are not built into `viam-server`.
The {{< glossary_tooltip term_id="resource" text="resources" >}} supported by a module are called modular resources.

## Write the basic functionality into a test script

The point of creating a module is to add functionality to your machine, so before you do anything else, you need to define some functionality that you will later package into a module.

For the purposes of this guide, you're going to make a module that does two things: It opens an image file from a configured path on your machine, and it prints `Hello, World! The latest random number is __.` with a random number in the blank.

1. Find an image you'd like to display when your program runs.
   We used [this image of a computer with "hello world" on the screen](https://unsplash.com/photos/a-laptop-computer-sitting-on-top-of-a-wooden-desk-8q6e5hu3Ilc).
   Save the image to your computer.

1. Create a test script file on your computer and copy the following code in the programming language of your choice into it:

    {{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
# test.py opens an image and prints a random number
from PIL import Image
import random

# TODO: Replace path with path to where you saved your photo
photo = Image.open("/Users/jessamyt/Downloads/hello-world.jpg")

photo.show()

number = random.random()

print("Hello, World! The latest random number is ", number, ".")
```

{{% /tab %}}
{{% tab name="Go" %}}

```go {class="line-numbers linkable-line-numbers"}
// test.go opens an image and prints a random number
package main

import "fmt"
import "math/rand"

func main() {

  number := rand.Float64()
  fmt.Println("Hello, World! The latest random number is ", number, ".")

  // TODO
}
```

{{% /tab %}}
{{< /tabs >}}

1. Replace the path in the script above with the path to where you saved your photo.
   Save the file.

1. Run the test script in your terminal:

    {{< tabs >}}
{{% tab name="Python" %}}

It's best practice to use a virtual environment for running Python scripts.
You'll also need to install the dependency Pillow in the virtual environment before running the test script.

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
source venv/bin/activate
pip install Pillow
python3 test.py
```

{{% /tab %}}
{{% tab name="Go" %}}

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
go run test.go
```

{{% /tab %}}
{{< /tabs >}}

    The image you saved should open on your screen, and a random number should print to your terminal.

## Choose an API to implement

Now it's time to decide which standard Viam [API](/appendix/apis/) makes the most sense for your module.
You need a way to return an image, and you need a way to return a number.

If you look at the [camera API](/appendix/apis/components/camera/), you can see the `GetImage` method, which returns an image.
This seems promising.
None of the camera API methods return a number though.

Look at the [sensor API](/appendix/apis/components/sensor/), which includes the `GetReadings` method.
You could return a number with that, but the sensor API can't return an image.

Your module can support multiple modular resources, so for our purposes here, let's make two modular resources: a camera to return the image, and a sensor to return a random number.

## Generate stub files

The easiest way to generate the necessary files for your module is to use the [Viam CLI](/cli/).

1. Run the `module generate` command in your terminal:

    ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
    viam module generate
    ```

1. Follow the prompts, selecting the following options:

   - Module name: `hello-world`
   - Language: Your choice
   - Visibility: `Private`
   - Namespace/Organization ID:
     - In the [Viam app](https://app.viam.com), navigate to your organization settings through the menu in upper right corner of the page.
       Find the **Public namespace** and copy that string.
   - Resource to add to the module (API): `Camera Component`.
   We will add the sensor later.
   - Model name: `hello-camera`
   - Enable cloud build: `No`
   - Register module: `No`

1. Hit your Enter key and the generator will generate a folder called <file>hello-world</file> containing stub files for your modular camera.

## Implement the API