---
title: "Build a composite model"
linkTitle: "Build a composite model"
weight: 22
type: "docs"
layout: "docs"
description: "Register one Go model under several resource APIs, so users add a multi-capability device to a machine once."
capabilities: ["module-development"]
diataxis: how-to
date: "2026-11-23"
---

Build a model that serves several resource APIs from one instance, such as a device that is both a sensor and a button.
Users configure it once, and client code reaches it through each API's usual getter.
To decide between a composite and separate models, see [Composite models](/build-modules/composite-models/).

## Prerequisites {#prerequisites}

- A Go module that builds and runs one model. See [Write a driver module](/build-modules/write-a-driver-module/).
  - You can only write composite models in Go.
  - `viam module generate` and `viam module add-model` don't create composite models, so you change the generated code by hand.
- `go.viam.com/rdk` v1.17.0 or later in your module's `go.mod`. Update it with `go get go.viam.com/rdk@latest`.
- `viam-server` v1.17.0 or later on the machine you test on, and the Viam CLI v1.17.0 or later. See [Update viam-server](/set-up-a-machine/viam-agent-and-server/) and [Install the CLI](/cli/overview/).

## How composite registration works {#how-composite-registration-works}

`resource.RegisterMultiAPI` registers one constructor under every API in a list, and records that the model serves all of them.
The constructor returns one resource.
`resource.Compose` assembles that resource from one part per API, each tagged with the API it serves by that API package's `AsSub` function.

`AsSub` takes the API's Go interface, so the compiler checks that each part implements every method of its API.
When the APIs share no method names, one struct implements all of them and is every part.
When two APIs have a method with the same name and different signatures, such as `Properties` on camera and movement sensor, one struct can't implement both.
Each of those APIs gets a small wrapper type, a facade, that embeds the shared struct and adds its own version of the method.

## 1. Register the model under each API {#register-the-model-under-each-api}

In your module's entry point, call `resource.RegisterMultiAPI` with every API the model serves, then pass `resource.ExpandModel` to `module.ModularMain`.
`ExpandModel` returns one entry per API the model was registered under, so you list the APIs only once.

```go
package main

import (
    "go.viam.com/rdk/components/button"
    "go.viam.com/rdk/components/sensor"
    "go.viam.com/rdk/module"
    "go.viam.com/rdk/resource"
)

var Model = resource.NewModel("my-org", "my-module", "my-combo")

func main() {
    resource.RegisterMultiAPI(
        []resource.API{sensor.API, button.API}, Model,
        resource.Registration[resource.Resource, resource.NoNativeConfig]{
            Constructor: newMyCombo,
        },
    )

    module.ModularMain(resource.ExpandModel(Model)...)
}
```

Use your own config type in place of `resource.NoNativeConfig` if the model has attributes, as in a single-API model.
In a module from `viam module generate`, the model's `init()` function calls `resource.RegisterComponent`, and `main` passes a `resource.APIModel` to `ModularMain`.
Replace the `RegisterComponent` call with `RegisterMultiAPI`, and the `APIModel` argument with `resource.ExpandModel(...)...`, passing the same model variable.
Don't register the model both ways.

A model can serve at most one of the arm, gantry, and gripper APIs.
If you list more than one, `RegisterMultiAPI` panics and the module exits at startup.

## 2. Implement every API on one struct {#implement-every-api-on-one-struct}

Write one struct that holds the device's state and implements the methods of every API.
In the constructor, pass it to each API's `AsSub` and combine the results with `resource.Compose`:

```go
func newMyCombo(
    ctx context.Context, deps resource.Dependencies, conf resource.Config, logger logging.Logger,
) (resource.Resource, error) {
    d := &myCombo{Named: conf.ResourceName().AsNamed()}
    return resource.Compose(
        sensor.AsSub(d),
        button.AsSub(d),
    )
}

type myCombo struct {
    resource.Named
    resource.TriviallyCloseable
}

// Readings implements the sensor API.
func (d *myCombo) Readings(ctx context.Context, extra map[string]interface{}) (map[string]interface{}, error) {
    return map[string]interface{}{"reading": 7}, nil
}

// Push implements the button API.
func (d *myCombo) Push(ctx context.Context, extra map[string]interface{}) error {
    return nil
}
```

Add `context` and `go.viam.com/rdk/logging` to the imports from step 1.
If the struct is missing a method of one of the APIs, the module doesn't compile.

`DoCommand` and `Status` belong to every API.
Because both parts are the same struct, a call through either API, or on the composite's own handle, reaches the same method.
When the composite closes, `Close` runs once on each distinct object you passed to `Compose`.

## 3. Add a facade for each colliding method {#add-a-facade-for-each-colliding-method}

Skip this step if your APIs share no method names; the compiler tells you in step 2 if they do.

The sensor and button APIs in step 2 share no method names.
The camera and movement sensor APIs do: both have a `Properties` method, with different signatures, so one struct can't implement both.
This step uses a device that serves both APIs, with its state on a shared struct named `myDevice`.

For APIs that collide, remove the colliding method from the shared struct.
Then define one facade type per API that embeds the shared struct and implements that API's version of the method:

```go
// camFacade adds the camera API's Properties to the shared struct.
type camFacade struct{ *myDevice }

func (f camFacade) Properties(ctx context.Context) (camera.Properties, error) {
    return camera.Properties{SupportsPCD: true}, nil
}

// imuFacade adds the movement sensor API's Properties to the shared struct.
type imuFacade struct{ *myDevice }

func (f imuFacade) Properties(
    ctx context.Context, extra map[string]interface{},
) (*movementsensor.Properties, error) {
    return &movementsensor.Properties{AngularVelocitySupported: true}, nil
}
```

In the constructor, pass each API its facade:

```go
d := &myDevice{Named: conf.ResourceName().AsNamed()}
return resource.Compose(
    camera.AsSub(camFacade{d}),
    movementsensor.AsSub(imuFacade{d}),
)
```

Every other method stays on `myDevice`, and both facades share its state.
For a complete module with a colliding pair and a custom API, see [`complexcombomodule`](https://github.com/viamrobotics/rdk/tree/main/examples/customresources/demos/complexcombomodule) in the RDK repository.

## 4. Declare the APIs in meta.json {#declare-the-apis-in-meta-json}

The registry lists a model under the APIs in its `meta.json` entry.
Without `apis`, the registry knows only the one API in `api`, so users find the model under that API alone.

Build the module, then let the CLI write the entry from the binary:

```sh {class="command-line" data-prompt="$"}
viam module update-models --binary=<path-to-module-binary>
```

`update-models` writes one entry for the model, with every API it serves in `apis` and the API that sorts first in `api`:

```json
{
  "api": "rdk:component:button",
  "apis": ["rdk:component:button", "rdk:component:sensor"],
  "model": "my-org:my-module:my-combo"
}
```

You can also write the entry by hand.
`api` is required and must be one of the values in `apis`.
The CLI warns when it isn't, and the registry rejects the upload.
See the [meta.json schema](/build-modules/module-reference/#metajson-schema).

## 5. Run the module on a machine {#run-the-module-on-a-machine}

Deploy the module and add the model to your machine in one command, from your module's root directory:

```sh {class="command-line" data-prompt="$"}
viam module reload-local --part-id=<part-id> \
  --model-name=my-org:my-module:my-combo --resource-name=my-combo
```

Use `viam module reload` instead to build in the cloud when your machine has a different architecture.
See [Test locally](/build-modules/write-a-driver-module/#3-test-locally) for both commands.

The command adds one config entry, with the `api` from `meta.json`:

```json
{
  "name": "my-combo",
  "api": "rdk:component:button",
  "model": "my-org:my-module:my-combo"
}
```

Add the model once, whichever of its APIs you name.
A second entry with a different name creates a second instance, which opens the same hardware again.

## 6. Test each API {#test-each-api}

Connect to the machine with the Go SDK and reach the composite through each API.
Start from the Go code sample on your machine's **CONNECT** tab, which connects with your API key.
In its `realMain` function, after `defer machine.Close(ctx)`, add:

```go
for _, name := range machine.ResourceNames() {
    if name.Name == "my-combo" {
        logger.Infof("advertised as %s", name.API)
    }
}

combo, err := resource.NamedFromProvider(machine, "my-combo")
if err != nil {
    logger.Fatal(err)
}
logger.Infof("serves %v", resource.APIsOf(combo))

s, err := sensor.FromProvider(machine, "my-combo")
if err != nil {
    logger.Fatal(err)
}
readings, err := s.Readings(context.Background(), nil)
if err != nil {
    logger.Fatal(err)
}
logger.Infof("readings: %v", readings)

b, err := resource.AsType[button.Button](combo)
if err != nil {
    logger.Fatal(err)
}
if err := b.Push(context.Background(), nil); err != nil {
    logger.Fatal(err)
}
logger.Info("button pushed")
```

Add any of `go.viam.com/rdk/components/button`, `go.viam.com/rdk/components/sensor`, and `go.viam.com/rdk/resource` that the sample doesn't already import.

The output lists `my-combo` once per API, `serves` lists both APIs, and both the sensor and button calls succeed.

## Troubleshooting {#troubleshooting}

{{% expand "module cannot service api \"...\" for model \"...\"" %}}

The config entry's `api` names an API the module didn't register the model under.
Check that the API is in the list you pass to `RegisterMultiAPI` and that you pass `resource.ExpandModel(Model)` to `ModularMain`, then rebuild the module.

{{% /expand %}}

{{% expand "model \"...\" does not implement declared api \"...\"" %}}

The constructor returned a resource that doesn't serve one of the APIs the model is registered under.
Pass one `AsSub` for every API in the `RegisterMultiAPI` list to `Compose`.

{{% /expand %}}

{{% expand "Compose given sub-resources with mismatched names" %}}

The parts passed to `Compose` don't share a name.
Build every part from the same struct, named with `conf.ResourceName().AsNamed()`.

{{% /expand %}}

{{% expand "The module exits with \"registers 2 kinematic APIs\"" %}}

The model lists more than one of the arm, gantry, and gripper APIs.
Split them into separate models.

{{% /expand %}}

## What's next {#whats-next}

- [Deploy a module](/build-modules/deploy-a-module/#readme-templates): publish the module, with a README that tells users how to configure a composite.
- [Capture from a composite](/data/capture-sync/capture-and-sync-data/#capture-from-a-composite): choose which API each captured method is tagged with.
- [Module developer reference](/build-modules/module-reference/#composite-functions): the Go functions for composites.
