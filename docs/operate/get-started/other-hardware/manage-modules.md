---
title: "Update and manage modules you created"
linkTitle: "Update and manage modules"
type: "docs"
weight: 27
images: ["/registry/create-module.svg"]
icon: true
tags: ["modular resources", "components", "services", "registry"]
description: "Update or delete your existing modules, or change their privacy settings."
aliases:
  - /use-cases/deploy-code/
  - /use-cases/manage-modules/
  - /how-tos/manage-modules/
languages: []
viamresources: []
platformarea: ["registry"]
level: "Beginner"
date: "2024-06-30"
# updated: ""  # When the tutorial was last entirely checked
cost: "0"
---

After you [create and deploy a module](/operate/get-started/other-hardware/), you can update, delete, or change its visibility settings.

For information on pinning module deployments to versions, see [Module versioning](/operate/reference/module-configuration/#module-versioning).

## Update a module

Once your module is in the [Viam Registry](https://app.viam.com/registry), there are two ways to update it:

- [Update automatically](#update-automatically) using GitHub Actions: Recommended for ongoing projects with continuous integration (CI) workflows, or if you want to build for multiple platforms.

  - If you enabled cloud build when you generated your module, the GitHub actions are already set up for you.

- [Update manually](#update-manually) using the [Viam CLI](/dev/tools/cli/): Fine for small projects with one contributor.

### Update automatically

Use GitHub Actions to automatically build and deploy your new module version when you create a tag or release in GitHub:

1. Edit your module code and update the [`meta.json`](/operate/get-started/other-hardware/#metajson-reference) file if needed.

1. If you used `viam module generate` to create your module and enabled cloud build, **all you need to do is create a tag and publish a release in GitHub as you did when you [first published the module](/operate/get-started/other-hardware/#upload-your-module)**.
   You can skip to step 5.

   If you did not use the Viam CLI generator and enable cloud build, you can set up one of the following GitHub actions up manually:

   {{< tabs >}}
   {{% tab name="build-action (Recommended)" %}}

   The `build-action` GitHub action provides a simple cross-platform build setup for multiple platforms: x86, ARM Linux, and macOS.

   Add this to your GitHub workflow:

   ```yaml
   on:
     push:
       tags:
         - "[0-9]+.[0-9]+.[0-9]+"

   jobs:
     publish:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v3
         - uses: viamrobotics/build-action@v1
           with:
             version: ${{ github.ref_name }}
             ref: ${{ github.sha }}
             key-id: ${{ secrets.viam_key_id }}
             key-value: ${{ secrets.viam_key_value }}
   ```

The `build-action` GitHub action relies on a build command that you need to specify in the <file>meta.json</file> file.
At the end of your <file>meta.json</file>, add the build configuration:

<!-- { {< tabs >}}
{ {% tab name="Single Build File" %}} -->

```json {class="line-numbers linkable-line-numbers" data-line="5-8"}
{
  "module_id": "example-module",
  ...
  "build": {
    "setup": "./setup.sh", // optional - command to install your build dependencies
    "build": "./build.sh", // command that will build your module
    "path" : "dist/archive.tar.gz", // optional - path to your built module
    "arch" : ["linux/amd64", "linux/arm64"] // architecture(s) to build for
  }
}
```

{{%expand "Click to view example setup.sh" %}}

```sh {class="command-line" data-prompt="$"}
#!/bin/bash
set -e
UNAME=$(uname -s)

if [ "$UNAME" = "Linux" ]
then
    echo "Installing venv on Linux"
    sudo apt-get install -y python3-venv
fi
if [ "$UNAME" = "Darwin" ]
then
    echo "Installing venv on Darwin"
    brew install python3-venv
fi

python3 -m venv .venv
. .venv/bin/activate
pip3 install -r requirements.txt
```

{{% /expand%}}

{{%expand "Click to view example build.sh (with setup.sh)" %}}

```sh { class="command-line" data-prompt="$"}
#!/bin/bash
pip3 install -r requirements.txt
python3 -m PyInstaller --onefile --hidden-import="googleapiclient" src/main.py
tar -czvf dist/archive.tar.gz <PATH-TO-EXECUTABLE>
```

{{% /expand%}}

{{%expand "Click to view example build.sh (without setup.sh)" %}}

```sh { class="command-line" data-prompt="$"}
#!/bin/bash
set -e
UNAME=$(uname -s)

if [ "$UNAME" = "Linux" ]
then
    echo "Installing venv on Linux"
    sudo apt-get install -y python3-venv
fi
if [ "$UNAME" = "Darwin" ]
then
    echo "Installing venv on Darwin"
    brew install python3-venv
fi

python3 -m venv .venv
. .venv/bin/activate
pip3 install -r requirements.txt
python3 -m PyInstaller --onefile --hidden-import="googleapiclient" src/main.py
tar -czvf dist/archive.tar.gz <PATH-TO-EXECUTABLE>
```

{{% /expand%}}

You can test this build configuration by running the Viam CLI's [`build local` command](/dev/tools/cli/#using-the-build-subcommand) on your development machine:

```sh {class="command-line" data-prompt="$"}
viam module build local
```

The command will run your build instructions locally without running a cloud build job.

For more details, see the [`build-action` GitHub Action documentation](https://github.com/viamrobotics/build-action), or take a look through one of the following example repositories that show how to package and deploy modules using the Viam SDKs:

- [Golang CI yaml](https://github.com/viam-labs/wifi-sensor/blob/main/.github/workflows/build.yml)
- [Golang Example CI meta.json](https://github.com/viam-labs/wifi-sensor/blob/main/meta.json)
<!-- - [C++ Example CI yaml](https://github.com/viamrobotics/module-example-cpp/blob/main/.github/workflows/build2.yml)
- [C++ Example CI meta.json](https://github.com/viamrobotics/module-example-cpp/blob/main/meta.json) -->

  {{% /tab %}}
  {{% tab name="upload-module" %}}

  If you already have your own CI with access to arm runners or only intend to build on `x86` or `mac`, you can use the `upload-module` GitHub action instead which allows you to define the exact build steps.

  Add this to your GitHub workflow:

  ```yaml {class="line-numbers linkable-line-numbers"}
  on:
    push:
    release:
      types: [released]

  jobs:
    publish:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v3
        - name: build
          run: echo "your build command goes here" && false # <-- replace this with the command that builds your module's tar.gz
        - uses: viamrobotics/upload-module@v1
          # if: github.event_name == 'release' # <-- once the action is working, uncomment this so you only upload on release
          with:
            module-path: module.tar.gz
            platform: linux/amd64 # <-- replace with your target architecture, or your module will not deploy
            version: ${{ github.event_name == 'release' && github.ref_name || format('0.0.0-{0}.{1}', github.ref_name, github.run_number) }} # <-- see 'Versioning' section below for explanation
            key-id: ${{ secrets.viam_key_id }}
            key-value: ${{ secrets.viam_key_value }}
  ```

Set `run` to the command you use to build and package your module, such as invoking a makefile or running a shell script.
When you are ready to test the action, uncomment `if: github.event_name == 'release'` to enable the action to trigger a run when you [issue a release](https://docs.github.com/en/repositories/releasing-projects-on-github).

For guidance on configuring the other parameters, see the documentation for each:

- [`org-id`](/dev/tools/cli/#using-the---org-id-and---public-namespace-arguments): Not required if your module is public.
- [`platform`](/dev/tools/cli/#using-the---platform-argument): You can only upload one platform at a time.
- [`version`](https://github.com/viamrobotics/upload-module/blob/main/README.md#versioning): See [Using the --version argument](/dev/tools/cli/#using-the---version-argument) for more details on the types of versioning supported.

For more details, see the [`upload-module` GitHub Action documentation](https://github.com/viamrobotics/upload-module), or take a look through one of the following example repositories that show how to package and deploy modules using the Viam SDKs:

- [Python with virtualenv](https://github.com/viam-labs/python-example-module)
- [Python with docker](https://github.com/viamrobotics/python-container-module)
- [Golang](https://github.com/viam-labs/wifi-sensor)
- [C++](https://github.com/viamrobotics/module-example-cpp)

  {{% /tab %}}
  {{< /tabs >}}

1. [Create an organization API key](/dev/tools/cli/#create-an-organization-api-key) with owner role:

   ```sh {class="command-line" data-prompt="$"}
   viam organizations api-key create --org-id <org-id> --name <key-name>
   ```

1. Add the key ID and value as GitHub repository secrets named `viam_key_id` and `viam_key_value`.

1. Push a tag or create a [release](https://docs.github.com/en/repositories/releasing-projects-on-github) in GitHub to trigger the build.
   Once the build is complete, the module will automatically update in the [Viam Registry](https://app.viam.com/registry), and the machines set to use the latest [version](/operate/reference/module-configuration/#module-versioning) of the module will automatically update to the new version.

### Update manually

Use the [Viam CLI](/dev/tools/cli/) to manually update your module:

1. Edit your module code and update the [`meta.json`](/operate/get-started/other-hardware/#metajson-reference) file if needed.
   For example, if you've changed the module's functionality, update the description in the `meta.json` file.

2. For Python modules only, package your files as an archive:

   ```sh {class="command-line" data-prompt="$"}
   tar -czf module.tar.gz run.sh requirements.txt src
   ```

   Supply the path to the resulting archive file in the next step.

3. Upload to the Viam Registry:

   ```sh {class="command-line" data-prompt="$"}
   viam module upload --version <version> --platform <platform> <module-path>
   ```

   For example, `viam module upload --version 1.0.1 --platform darwin/arm64 my-module.tar.gz`.

When you `upload` a module, the command performs basic [validation](/dev/tools/cli/#upload-validation) of your module to check for common errors.

For more information, see the [`viam module` command](/dev/tools/cli/#module).

## Change module visibility

You can change the visibility of a module from public to private if:

- you are an [owner](/manage/manage/rbac/) in the {{< glossary_tooltip term_id="organization" text="organization" >}} that owns the module, AND
- no machines outside of the organization that owns the module have the module configured (no other orgs are using it).

To change the visibility, navigate to its page in the [**REGISTRY** section of the Viam app](https://app.viam.com/registry), hover to the right of the visibility indicator near the right side of the page until an **Edit** button appears, and click it to make changes.

{{<imgproc src="/registry/upload/edit-module-visibility.png" resize="x600" declaredimensions=true alt="A module page with a Visibility heading on the right side. Under it, an Edit button has appeared." max-width="900px" class="shadow" >}}

You can also edit the visibility by editing the <file>meta.json</file> file and then running the following [CLI](/dev/tools/cli/#module) command:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
viam module update
```

## Delete a module

You can delete a module if:

- you are an [owner](/manage/manage/rbac/) in the {{< glossary_tooltip term_id="organization" text="organization" >}} that owns the module, AND
- no machines have the module configured.

To delete a module, navigate to its page in the [**REGISTRY** section of the Viam app](https://app.viam.com/registry), click the **...** menu in the upper-right corner of the page, and click **Delete**.

{{<imgproc src="/registry/upload/delete-module.png" resize="x600" declaredimensions=true alt="A module page with the ... menu open. Delete is the only option in the menu." max-width="500px" class="shadow" >}}

{{% alert title="Note" color="note" %}}

If you need to delete a module and the delete option is unavailable to you, please [contact our support team](https://support.viam.com/hc/en-us) for assistance.

{{% /alert %}}

### Delete just one version of a module

Deleting a version of a module requires the same org owner permissions as deleting the entire module, and similarly, you cannot delete a version if any machines are using it.
To delete just one version of a module:

1. Navigate to its page in the [**REGISTRY** section of the Viam app](https://app.viam.com/registry)
2. Click **Show previous versions** under the **Latest version** heading.
3. Hover next to the version you'd like to delete and click the trash icon.

You cannot upload a new file with the same version number as the deleted one.
To upload another version, you must increment the version number to a later version number.

## Next steps

{{< cards >}}
{{% manualcard link="/operate/reference/module-configuration/#module-versioning" %}}

### Pin a version

Configure version update management for a registry module on your machine.

{{% /manualcard %}}
{{< /cards >}}
