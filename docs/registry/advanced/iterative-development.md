---
title: "Iterative Module Development"
linkTitle: "Iterative Development"
weight: 40
type: "docs"
tags: ["modules", "modular resources", "registry"]
description: "Test your modules locally before uploading to the Viam registry, and use prerelease versioning to publish beta versions of your module."
icon: true
images: ["/services/icons/ml.svg"]
---

Once you have [created the first version of your module](/use-cases/create-module/), you can use the procedure outlined on this page to iterate on your design, and test changes quickly.

Generally, when developing a module, you have two options for iterative development, depending on the specific [platform](/cli/#using-the---platform-argument) you want your module to support:

- **Test Locally:** If you want your module to support the same platform as your development workstation, you can test your module locally.
  For example, if you are developing a module on a macOS computer with an M2 processor (the `arm64` architecture), and want your module to support only macOS computers running the `arm64` architecture, you can perform your module development and testing workflow entirely on your macOS workstation.
- **Sync Code and Test Remotely:** If you want your module to support a different architecture than your development workstation, you can sync your module code to a machine running your desired target architecture and test remotely.
  For example, if you are developing a module on a macOS computer, but want your module to support a Raspberry Pi running Linux on the `arm64` architecture, you can set up syncing for your module code to be able to continue development on your macOS workstation, but test on your remote Raspberry Pi.

Both of these options involve deploying your module to the target test system as a [local module](/registry/configure/#local-modules), without uploading it to the Viam registry.
Even if you have already published a version of your module to the registry, you might still find it useful to follow the steps in this section to verify that changes you make as part of releasing a new version work as expected on your target platform.

Then, once you have tested it, you can [upload your module](/use-cases/create-module/) to the Viam registry.
You can use [prerelease versioning](#use-prerelease-versioning) to publish a version of your module to the registry without affecting machines that are using stable versions of your module.

{{< tabs >}}
{{% tab name="Test Locally" %}}

If you are developing a module for the same target architecture as your development workstation, you can test your module locally using the following procedure:

1. Navigate to the [Viam app](https://app.viam.com/robots) and [add a new machine](/cloud/machines/#add-a-new-machine) to serve as your development machine.
   Be sure to follow the steps shown in the Viam app to install `viam-server` on your local machine.

1. If you are using a programming language that requires that you build your module, such as Go or C++, follow the instructions for your language to [compile or package](/use-cases/create-module/#compile-or-package-your-module) your module.
   If you are using a programming language that does not require compilation, such as Python, you can skip this step.

1. Navigate to the Viam app, select your machine, and [add your module as a local module](/registry/configure/#local-modules) to your machine.
   For the **Executable path** field, enter the absolute path on your machine's filesystem to either:

   - the module's [executable file](/use-cases/create-module/#compile-or-package-your-module), such as `run.sh` or a compiled binary.
   - a [packaged tarball](https://www.cs.swarthmore.edu/~newhall/unixhelp/howto_tar.html) of your module, ending in `.tar.gz` or `.tgz`.
     If you are providing a tarball file in this field, be sure that your packaged tarball contains your module's [`meta.json` file](/cli/#the-metajson-file) within it.

   If you have previously added your module as a _registry module_, you will need to first remove the registry version of your module before then adding the local version.

1. Click the **Save** button in the top right corner of the page.

1. Check the **LOGS** tab for your machine in the Viam app to ensure that `viam-server` properly started your module.
   For example, the following log message indicates that `viam-server` was able to find and start the local module named `my-module` successfully:

   ```sh
   1/16/24, 4:44:25.085 PM   info robot_server   modmanager/manager.go:862   registering component from module   module my-module   API rdk:component:base   model acme:demo:mybase  
   ```

1. Make your desired code changes to your module using your favorite editor.
   Save your changes.

1. If applicable (for example, using Go or C++), [compile or package](/use-cases/create-module/#compile-or-package-your-module) your module again.
   Otherwise (for example, using Python), skip this step.

1. Restart `viam-server` on your machine in order for it to pick up the code changes to your module, using your system's service management command.
   For example:

   - On macOS, using `brew`:

     ```sh { class="command-line"}
     brew services restart viam-server
     ```

   - On Linux, using `systemctl`:

     ```sh { class="command-line"}
     sudo systemctl restart viam-server
     ```

1. Once `viam-server` has restarted, check the **LOGS** tab for your machine in the Viam app again to ensure that `viam-server` properly started your module.

1. Then test your module to verify that your code changes work as expected.

1. Repeat steps 6 - 10 to continue developing your module, as needed.
   Remember to check the **LOGS** tab each time to verify that the module registered successfully, and to troubleshoot any error or warning messages.
   If you haven't already, you can [add custom log messages to your code](/use-cases/create-module/#optional-configure-logging), which appear under the **LOGS** tab to assist with troubleshooting.

{{% /tab %}}
{{% tab name="Sync Code and Test Remotely" %}}

If you are developing a module for a different target architecture than your development workstation, you can sync your module code and test your module remotely using the following procedure:

1. Navigate to the [Viam app](https://app.viam.com/robots) and [add a new machine](/cloud/machines/#add-a-new-machine) to serve as your development machine.
   Be sure to follow the steps shown in the Viam app to install `viam-server` on the target machine you want to test and build on.
   For example, to test and build your module on your Raspberry Pi, be sure to install `viam-server` on the Pi itself, not your macOS workstation.

1. Set up file sync between your development workstation and the machine running your target platform that you want to build and test on, using your favorite file sync utility.
   For example, you could use [mutagen.io](https://mutagen.io/) to sync your files using the following steps:

   1. Install Mutagen on your development workstation, following the [instructions for your operating system](https://mutagen.io/documentation/introduction/installation):

      - To install Mutagen on macOS:

        ```sh
        brew install mutagen-io/mutagen/mutagen
        ```

      - To install Mutagen on Linux, [download the latest release from GitHub](https://github.com/mutagen-io/mutagen/releases/latest).
        Mutagen is not currently available for Linux through package managers.

   1. If you haven't already, ensure that your target test system is up and running, and accessible to `ssh`.
      Mutagen uses `ssh` to sync files between your systems in an unattended manner (that is, without user input), and so requires that you set up a valid `ssh` key for it to use to authenticate during syncs.
      If you already have an `ssh` keypair configured to your remote testing system, you can skip this step and proceed to step 3.
      Follow the steps below to create a new `ssh` key to use, and copy it to your remote testing system:

      1. Create a new `ssh` key on your development workstation, meeting your security requirements.
         For example, on a macOS machine, you can generate an `ssh` key using the `ed25519` algorithm with a key size of `4096` bits using the following command:

         ```sh { class="command-line"}
         ssh-keygen -t ed25519 -b 4096 -C "developer@example.com"
         ```

         When prompted to select a file location, press enter to accept the default location.

         This command will generate a new key in your `~/.ssh/` directory.
         If you already have an `ssh` key in that directory with the same name, you will be prompted to overwrite your existing key: type `n` (for "no") to cancel.
         You can use your existing key in the next steps.

      1. Verify that you have both parts of the `ssh` keypair present as follows:

         ```sh { class="command-line"}
         ls -l ~/.ssh/id_ed25519*
         ```

         For example, on macOS, you should see files similar to `/Users/username/.ssh/id_ed25519` and `/Users/username/.ssh/id_ed25519.pub`.

      1. Copy the `.pub` file only to your target remote system using the `ssh-copy-id` command.
         For example, to transfer a `id_ed25519.pub` file from a macOS machine to a remote Linux system named `my-pi.local` for the user `username`, you could use the following commands:

         ```sh { class="command-line"}
         ssh-copy-id -i ~/.ssh/id_ed25519.pub username@my-pi.local
         ```

         Provide the `ssh` password for your user account when prompted.
         Do not copy the private key file, which does not have a file extension.

   1. Then, start a new `ssh` session to your remote system, and verify that you are able to connect without being prompted for a password.
      Mutagen requires a working, passwordless `ssh` configuration in order to be able to sync files.
      If you receive a `connection refused` error, or are still prompted for a password, see the [Troubleshooting `ssh` section](#troubleshooting-ssh) for further guidance.

1. Return to your local development system, and navigate to your module's directory. For example, if you are developing a module named `my-module` in the home directory:

   ```sh { class="command-line"}
   cd ~/my-module
   ```

1. Set up a new Mutagen sync from this directory to sync to your remote system, providing the local path to your module and the target path on the remote system to sync your module files:

   ```sh { class="command-line"}
   mutagen sync create /path/to/local/module username@remote-hostname.local:/path/to/remote/sync-target
   ```

   For example, you could use the following to transfer the example module from earlier to the same location on the remote system, if desired:

   ```sh { class="command-line"}
   mutagen sync create ~/my-module username@my-pi.local:/home/username/my-module
   ```

1. In an `ssh` session to your remote system, ensure that you now see the synced files appear as expected in the filesystem location you chose to sync to.
   If the files haven't appeared, consult the [Mutagen documentation](https://mutagen.io/documentation/introduction/getting-started) for further troubleshooting.

1. Return to your local development system, and navigate back to your module directory.

1. If you are using a programming language that requires that you build your module, such as Go or C++, follow the instructions for your language to [compile or package](/use-cases/create-module/#compile-or-package-your-module) your module.
   If you are using a programming language that does not require compilation, such as Python, you can skip this step.

1. Navigate to the Viam app, select your machine, and [add your module as a local module](/registry/configure/#local-modules) to your machine.
   Provide the **Executable path** in the configuration, pointing to the compiled or built binary, or the executable script, depending on your language.
   Provide the _remote system's_ path to this file, for example: <file>/home/username/my-module/run.sh</file>.
   With the Mutagen sync in place, Mutagen transfers the binary or executable automatically when you created it in the previous step.
   If you have previously added your module as a _registry module_, you will need to first remove the registry version of your module before then adding the local version.

1. Click the **Save** button in the top right corner of the page.

1. Check the **LOGS** tab for your machine in the Viam app to ensure that `viam-server` properly started your module.
   For example, the following log message indicates that `viam-server` was able to find and start the local module named `my-module` successfully:

   ```sh
   1/16/24, 4:44:25.085 PM   info robot_server   modmanager/manager.go:862   registering component from module   module my-module   API rdk:component:base   model acme:demo:mybase  
   ```

1. Make your desired code changes to your module using your favorite editor.
   Save your changes.

1. If applicable (for example, using Go or C++), [compile or package](/use-cases/create-module/#compile-or-package-your-module) your module again.
   Otherwise (for example, using Python), skip this step.

1. Restart `viam-server` on your remote system in order for it to pick up the code changes to your module, using your system's service management command.
   For example, on Linux using `systemctl`:

   ```sh { class="command-line"}
   sudo systemctl restart viam-server
   ```

1. Once `viam-server` has restarted, check the **LOGS** tab for your machine in the Viam app again to ensure that `viam-server` properly started your module.

1. Then test your module to verify that your code changes work as expected.

1. Repeat steps 11 - 15 to continue developing your module, as needed.
   Remember to check the **LOGS** tab each time to verify that the module registered successfully, and to troubleshoot any error or warning messages.
   If you haven't already, you can [add custom log messages to your code](/use-cases/create-module/#optional-configure-logging), which appear under the **LOGS** tab to assist with troubleshooting.

{{% /tab %}}
{{% /tabs %}}

When you are satisfied that your module is ready for release, follow the steps to [upload your module](/use-cases/create-module/) to the Viam registry, to facilitate streamlined deployment to other machines or to make it available to the Viam community.

## Troubleshooting `ssh`

### Connection refused

If you receive `connection refused` or similar messages when attempting to connect to the remote system using your `ssh` key, ensure the permissions of the key are correct:

- Start an `ssh` session to your remote system using your password.

- Make sure that the public key you created with `ssh-keygen` and copied with `ssh-copy-id` has the correct file permissions on the remote filesystem:

  ```sh { class="command-line"}
  ls -l ~/.ssh/id_ed25519.pub
  ```

- If the permissions shown are not exactly `-rw-r--r--`, use the following command to set them appropriately:

  ```sh { class="command-line"}
  chmod 644 ~/.ssh/id_ed25519.pub
  ```

Then test your `ssh` connection once more to ensure that you are connected without being prompted for a password.

### Prompted for `ssh` account password

If you are able to `ssh` to the remote system, but are still prompted for your password each time you attempt to connect with a message similar to `username@amy-pi.local's password:`, check your remote system's `sshd` configuration:

- Start an `ssh` session to your remote system using your password.

- Make sure that the `sshd` configuration for your remote system includes the following settings:

  ```sh
  PubkeyAuthentication yes
  ```

  For example, on Ubuntu, you can check your `sshd` configuration with the following command:

  ```sh { class="command-line"}
  grep -i pubkey /etc/ssh/sshd_config
  ```

  - If this value is set to `no`, change this value to `yes`.
  - If this value is prepended by `#` character, remove it so that the line reads exactly: `PubkeyAuthentication yes`.

- If you needed to change this value in either way listed, restart the `sshd` service from your `ssh` session to your remote system.
  For example, if your remote system is Linux, you would run the following on the remote system:

  ```sh { class="command-line"}
  sudo systemctl restart sshd
  ```

  Note that restarting the `sshd` service in this manner will disconnect your current `ssh` session to the remote system.
  For more information on the `sshd` service and related service management, please consult the documentation for your specific operating system.

Then test your `ssh` connection once more to ensure that you are connected without being prompted for a password.

### Prompted for `ssh` key passphrase

If you are prompted with a message similar to `Enter passphrase for key '/Users/username/.ssh/id_ed25519'`, add your `ssh` key passphrase to your local macOS keychain:

- For macOS 12.0 or later, run the following on your local macOS system:

  ```sh { class="command-line"}
  ssh-add --apple-use-keychain ~/.ssh/id_ed25519
  ```

- For macOS 11.0 or previous, run the following on your local macOS system:

  ```sh { class="command-line"}
  ssh-add -K ~/.ssh/id_ed25519
  ```

Then test your `ssh` connection once more to ensure that you are connected without being prompted for a password.

## Use prerelease versioning

To publish a module version that is not yet fully tested, you can publish it as a prerelease (also called "release candidate") version of a module to the modular registry.
Publishing a prerelease version will not affect any machines that are using the existing module.
Regardless of the machine’s version pinning setting, only machines that are set to the exact prerelease version will be updated.

For example, imagine your latest stable version is `0.1.2`.
If you publish a prerelease version tagged `0.1.2-rc0`, all machines continue to use version `0.1.2`.
Similarly, if you publish a prerelease version tagged `0.1.3-rc0`, all machines will stay on version `0.1.2`.
If you pin a machine to the exact version number `0.1.3-rc0`, only then will that machine use the prerelease version.

### Syntax

Your tags should adhere to [semantic versioning specification (SemVer)](https://semver.org), meaning that the tag should begin with a major version number, then a minor version number, then a patch version number, separated by periods.
It is up to you as the developer to choose when to increment each number.
You can append any label after the major, minor, and patch version numbers.
For example, you can label your prerelease version `0.1.2-rc0` or `0.1.2-beta`.
If your tag does not adhere to SemVer, cloud builds will fail.

### Update your GitHub action file

If you are using Cloud Build, be sure to update your [GitHub action file](/use-cases/create-module/#update-an-existing-module-using-a-github-action) tags to include the release candidate version.
You can use `"*"` to trigger the build action on all tags regardless of correct syntax, or you can use the following regular expression to trigger the build action on all tags that have valid syntax:

```regex
/^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$/gm
```
