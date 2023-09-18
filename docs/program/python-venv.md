---
title: "Prepare your Python Virtual Environment"
linkTitle: "Prepare Virtualenv"
weight: 10
type: "docs"
description: "Prepare your Python Virtual Environment to program machines with the Python SDK."
images: ["/services/icons/sdk.svg"]
tags: ["client", "sdk", "application", "sdk", "fleet", "program", "python", "venv"]
---

To manage Python packages for your Viam application, it is recommended that you use a virtual environment, or `venv`.
By using a `venv`, you can install Python packages like Viam's client SDK within a virtual environment, avoiding conflicts with other projects or your system.

Follow this guide to set up a fresh virtual environment on your working computer and install the Python SDK as a requirement for your Viam client application.

## Setup your project

First, create a directory for your project.
For example, name your directory `viam-python`:

```sh {class="command-line" data-prompt="$"}
mkdir viam-python
cd viam-python
```

## Create and Activate a Virtual Environment

In the project directory, create and activate a virtual environment for Python to run in.

```bash
python3 -m venv viam-env
source viam-env/bin/activate
```

Now, `(viam-env)` prepends the commands in your terminal window to indicate the Python packages being used are from this particular environment.
You can exit this environment by running `deactivate`.

## Install Viam

Inside the activated `viam-env` python environment, you can now install the Viam SDK:

```bash
pip3 install viam-sdk
```

This installs Viam and all required dependencies.

If you need to install your own requirements, also install them in this virtual environment.
To make your required packages easier to install in the future, you can also [create a](https://openclassrooms.com/en/courses/6900846-set-up-a-python-environment/6990546-manage-virtual-environments-using-requirements-files) <file>requirements.txt</file> file with a list of all the packages you need and then install the requirements for your client application by running `pip3 install -r requirements.txt`.

## Setup your IDE

If you would like to be able to use the environment you created with your IDE, point your IDE to use the python interpreter of your new environment, rather than the default interpreter, likely the global python interpreter.

The following steps are for VS Code.
If you're not using VS Code, please read your IDE's documentation on selecting python interpreters.

1. Open the `viam-python` directory in VS Code
1. Open the Command Palette (using `⇧⌘P` or through the menus View -> Command Palette)
1. Select the command `Python: Select Interpreter`.
There, you should see all the interpreters available to you.
You're looking for the on you just made: `viam-env`.
It will look something like: `Python 3.XX.X ('viam-env': venv) ./viam-env/bin/python`.
If you don't see it, click the `Refresh` icon on the top right of the Command Palette.
Select the `viam-env` interpreter.

Your IDE will now recognize all packages installed in this environment.

## Start building

You are now ready to [start using Viam's Python SDK](/program/)!
