---
title: "Monitor Air Quality with a Fleet of Sensors"
linkTitle: "Air Quality Fleet"
type: "docs"
description: "Configure a fleet of machines to capture air quality sensor data across different locations."
images: ["/tutorials/air-quality-fleet/three-sensor-dash-wide.png"]
imageAlt: "A web dashboard showing PM2.5 readings from two air quality sensors."
tags: ["tutorial"]
authors: ["Jessamy Taylor"]
languages: ["typescript"]
viamresources: ["sensor", "data_manager"]
platformarea: ["data", "fleet"]
emailform: true
level: "Intermediate"
date: "2024-05-07"
# updated: ""  # When the tutorial was last entirely checked
cost: 200
# Learning goals:
# 1. The reader can distinguish the concepts of organizations and locations and can select the appropriate setup when creating their own projects for their business.
# 2. The reader can identify when to use fragments and evaluate when it is worth using fragments.
#    The reader can create their own fragments for their projects and knows what to include and exclude from them.
# 3. The reader recognizes how permissions enable the management of data for a business across multiple customers while providing each customer access to their own data.
# 4. The reader can deploy custom front ends that end users can use to operate their machines.
---

This tutorial walks you through how to set up a fleet or air quality monitoring machines as though you were creating a company selling air quality machines.
You will learn how to set up a fleet of devices for yourself or third parties to collect air quality data.
You will then create a web application that shows the most recent reading for any device a user has access to.

{{< alert title="Learning Goals" color="info" >}}

By completing this project, you will learn to:

- Configure a fleet of machines
- Organize your fleet using {{< glossary_tooltip term_id="location" text="locations" >}}
- Collect and sync data from multiple machines
- Use the Viam TypeScript SDK to query sensor data
- Create a custom dashboard that you and third parties can use to view data for their respective machines

{{< /alert >}}

{{<imgproc src="/tutorials/air-quality-fleet/three-sensor-dash-wide.png" resize="1000x" style="width:500px" declaredimensions=true alt="Air quality dashboard in a web browser with PM2.5 readings from three different sensor machines displayed." class="imgzoom">}}

## Requirements

You can create one or more machines to measure air quality.
For each machine, you need the following hardware:

- A [SDS011 Nova PM sensor](https://www.amazon.com/SDS011-Quality-Detection-Conditioning-Monitor/dp/B07FSDMRR5)
  - If you choose to use a different air quality sensor, you may need to [create your own module](/operate/get-started/other-hardware/) implementing the [sensor API](/operate/reference/components/sensor/#api) for your specific hardware.
- A single-board computer (SBC) [capable of running `viam-server`](/operate/get-started/setup/)
- An appropriate power supply

## Set up one device for development

In this section we'll set up one air sensing machine as our development device.
Later in this tutorial, you will learn to provision multiple devices using {{< glossary_tooltip term_id="fragment" text="fragments" >}}.

### Create your machine

{{< table >}}
{{% tablestep number=1 %}}

Navigate to [Viam](https://app.viam.com) in a web browser.
Create an account and log in.

{{% /tablestep %}}
{{% tablestep number=2 %}}

Click the dropdown in the upper-right corner of the **FLEET** page and use the **+** button to create a new {{< glossary_tooltip term_id="organization" text="organization" >}}.

This tutorial walks you through how to set up your fleet as though you were creating a company selling air quality machines.
The organization represents this company.
If you already have a different suitable organization, you can use that instead.
Name the organization and click **Create**.

{{% /tablestep %}}
{{% tablestep number=3 %}}

Click **FLEET** in the upper-left corner of the page and click **LOCATIONS**.
A new {{< glossary_tooltip term_id="location" text="location" >}} called `First Location` is automatically generated for you.
Use the **...** menu next to edit the location name to `Development`, then click **Save**.

{{% /tablestep %}}
{{% tablestep number=4 %}}

Connect a PM sensor to a USB port on the machine's SBC.
Then connect your device to power.

If the computer does not already have a Viam-compatible operating system installed, follow the [prerequisite section of the setup guide]/operate/get-started/setup/#prerequisite-make-sure-you-have-a-supported-operating-system) to install a compatible operating system.
You _do not_ need to follow the "Install `viam-server`" section; you will do that in the next step!

Enable serial communication so that the SBC can communicate with the air quality sensor.
For example, if you are using a Raspberry Pi, SSH to it and [enable serial communication in `raspi-config`](/operate/reference/prepare/rpi-setup/#enable-communication-protocols).

{{% /tablestep %}}
{{% tablestep number=5 %}}

Add a new [_{{< glossary_tooltip term_id="machine" text="machine" >}}_](/operate/get-started/basics/#what-is-a-machine) using the button in the top right corner of the **LOCATIONS** tab.
Follow the **Set up your machine part** instructions to install `viam-server` on the machine and connect it to Viam.

When your machine shows as connected, continue to the next step.

{{% /tablestep %}}

{{< /table >}}

### Configure your sensor

{{< table >}}

{{% tablestep number=1 %}}

Navigate to the **CONFIGURE** tab of the machine, click the **+** button and select **Component or service**.
Click **sensor**, then search for `sds011` and add the **sds001:v1** {{< glossary_tooltip term_id="module" text="module" >}}.
Name the sensor `PM_sensor` and click **Create**.

{{<imgproc src="/tutorials/air-quality-fleet/add-sensor-module.png" resize="700x" declaredimensions=true alt="The Add Module button that appears after you click the model name." style="width:400px" class="imgzoom shadow">}}

{{% /tablestep %}}
{{% tablestep number=2 %}}

In the newly created **PM_sensor** card, replace the contents of the attributes box (the empty curly braces `{}`) with the following:

```json {class="line-numbers linkable-line-numbers"}
{
  "usb_interface": "<REPLACE WITH THE PATH YOU IDENTIFY>"
}
```

{{% /tablestep %}}
{{% tablestep number=3 %}}

<a name="usb-path"></a>To figure out which port your sensor is connected to on your board, SSH to your board and run the following command:

```sh{class="command-line" data-prompt="$"}
ls /dev/serial/by-id
```

This should output a list of one or more USB devices attached to your board, for example `usb-1a86_USB_Serial-if00-port0`.
If the air quality sensor is the only device plugged into your board, you can be confident that the only device listed is the correct one.
If you have multiple devices plugged into different USB ports, you may need to choose one path and test it, or unplug something, to figure out which path to use.

Now that you have found the identifier, put the full path to the device into your config, for example:

```json {class="line-numbers linkable-line-numbers"}
{
  "usb_interface": "/dev/serial/by-id/usb-1a86_USB_Serial-if00-port0"
}
```

{{% /tablestep %}}
{{% tablestep number=4 %}}

Save the config.

{{<imgproc src="/tutorials/air-quality-fleet/configured-sensor.png" resize="1000x" declaredimensions=true alt="Configure tab showing PM sensor and the sensor module configured." style="width:600px" class="imgzoom shadow">}}

{{% /tablestep %}}
{{% tablestep number=5 %}}

On your sensor configuration panel, click on the **TEST** panel to check that you are getting readings from your sensor.

{{<imgproc src="/tutorials/air-quality-fleet/get-readings.png" resize="1000x" declaredimensions=true alt="The sensor readings on the control tab." style="width:600px" class="imgzoom shadow">}}

If you do not see readings, check the **LOGS** tab for errors, double-check that serial communication is enabled on the single board computer, and check that the `usb_interface` path is correctly specified.

{{% /tablestep %}}

{{< /table >}}

### Configure data management

You have configured the sensor so the board can communicate with it, but sensor data is not yet being saved anywhere.
Viam's [data management service](/data-ai/capture-data/capture-sync/) lets you capture data locally from each sensor and then sync it to the cloud where you can access historical sensor data and see trends over time.
As you configure more sensing machines, you'll be able to remotely access data from all machines.

{{< table >}}

{{% tablestep number=1 %}}

Click **+** and add the **data management** service.

On the data manager panel:

- Toggle **Syncing** to the on position.
- Set the sync interval to `0.05` minutes (every 3 seconds).
- In the **Tags** field, add `air-quality`.
  This tag will now automatically be applied to all data collected by this data manager which will make querying data easier.

{{% /tablestep %}}
{{% tablestep number=2 %}}

On the **PM_sensor** panel, click **Add method** to add data capture.

- **Type**: **Readings**.
- **Frequency**: `0.1` (every 10 seconds).

Save the config.

You can check that your sensor data is being synced by clicking on the **...** menu and clicking **View captured data**.

{{% /tablestep %}}
{{< /table >}}

Congratulations.
If you made it this far, you now have a functional air sensing machine.
Let's create a dashboard for its measurements next.

## Create a dashboard

The [Viam TypeScript SDK](https://ts.viam.dev/) allows you to build custom web interfaces to interact with your machines.
For this project, you'll use it to build a page that displays air quality sensor data for a given location.
You'll host the website with Viam as a Viam Application.

The full code is available for reference on [GitHub](https://github.com/viam-labs/air-quality-fleet/blob/main/main.ts).

{{< alert title="Tip" color="tip" >}}
If you'd like to graph your data using a Grafana dashboard, try our [Visualize Data with Grafana tutorial](/tutorials/services/visualize-data-grafana/) next.
{{< /alert >}}

### Set up your TypeScript project

Complete the following steps on your laptop or desktop.
You don't need to install or edit anything else on your machine's single-board computer (aside from `viam-server` which you already did); you'll be developing your TypeScript app from your personal computer and hosting it with Viam.

{{< table >}}
{{% tablestep number=1 %}}

Make sure you have the latest version of [Node.JS](https://nodejs.org/en) installed on your computer.

{{% /tablestep %}}
{{% tablestep number=2 %}}

Create a directory on your laptop or desktop for your project.
Name it <file>aqi-dashboard</file>.

{{% /tablestep %}}
{{% tablestep number=3 %}}

Create a file in your <file>aqi-dashboard</file> folder and name it <file>package.json</file>.
The <file>package.json</file> file holds necessary metadata about your project.
Paste the following contents into it:

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "air-quality-dashboard",
  "description": "A dashboard for visualizing data from air quality sensors.",
  "scripts": {
    "start": "esbuild ./main.ts --bundle --outfile=static/main.js --servedir=static --format=esm",
    "build": "esbuild ./main.ts --bundle --outfile=static/main.js --format=esm"
  },
  "author": "<YOUR NAME>",
  "license": "ISC",
  "devDependencies": {
    "esbuild": "*"
  },
  "dependencies": {
    "@viamrobotics/sdk": "^0.42.0",
    "bson": "^6.6.0",
    "js-cookie": "^3.0.5"
  }
}
```

{{% alert title="Fun fact" color="info" %}}

The `--format=esm` flag in the `"start"` script is important because the ECMAScript module format is necessary to support the BSON dependency this project uses for data query formatting.
If you don't know what the proceeding sentence means, don't worry about it; just copy-paste the JSON above and it'll work.

{{% /alert %}}

{{% /tablestep %}}
{{% tablestep number=4 %}}

Install the project's dependencies by running the following command in your terminal:

```sh {class="command-line" data-prompt="$"}
npm install
```

{{% /tablestep %}}
{{< /table >}}

### Access machines from your application

Viam applications provide access to a machine by placing its API key into your local storage.
You can access the data from your browser's local storage with the following code.

Currently, Viam applications only provide access to single machines but in the future you will be able to access entire locations or organizations.

Create another file inside the <file>aqi-dashboard</file> folder and name it <file>main.ts</file>.
Paste the following code into <file>main.ts</file>:

```typescript {class="line-numbers linkable-line-numbers"}
// Air quality dashboard

import * as VIAM from "@viamrobotics/sdk";
import { BSON } from "bson";
import Cookies from "js-cookie";

let apiKeyId = "";
let apiKeySecret = "";
let host = "";
let machineId = "";

async function main() {
  const opts: VIAM.ViamClientOptions = {
    serviceHost: "https://app.viam.com",
    credentials: {
      type: "api-key",
      payload: apiKeySecret,
      authEntity: apiKeyId,
    },
  };

  // <Insert data client and query code here in later steps>

  // <Insert HTML block code here in later steps>
}

// <Insert getLastFewAv function definition here in later steps>

document.addEventListener("DOMContentLoaded", async () => {
  // Extract the machine identifier from the URL
  let machineCookieKey = window.location.pathname.split("/")[2];
  ({
    apiKey: { id: apiKeyId, key: apiKeySecret },
    machineId: machineId,
    hostname: host,
  } = JSON.parse(Cookies.get(machineCookieKey)!));
  main().catch((error) => {
    console.error("encountered an error:", error);
  });
  console.log(apiKeyId, apiKeySecret, host, machineId);
});
```

### Local development

For developing your application on localhost:

1. Run the following command to serve the application you are building:

   ```sh {class="command-line" data-prompt="$" data-output="2-10"}
   npm start
   ```

   {{<imgproc src="/tutorials/air-quality-fleet/terminal-url.png" resize="800x" declaredimensions=true alt="Terminal window with the command 'npm start' run inside the aqi-dashboard folder. The output says 'start' and then 'esbuild' followed by the esbuild string from the package.json file you configured. Then there's 'Local:' followed by a URL and 'Network:' followed by a different URL." class="imgzoom" style="width:800px">}}

1. Run the following command specifying the address where your app is running on localhost and a machine to test on.
   The command will proxy your local app and open a browser window and navigate to `http://localhost:8012/machine/<machineHostname>` for the machine provided with --machine-id.

   ```sh {class="command-line" data-prompt="$" data-output="3-10"}
   viam login
   viam module local-app-testing --app-url http://localhost:8000 --machine-id <MACHINE-ID>
   ```

### Add functionality to your code

Now that you have the connection code, you are ready to add code that establishes a connection from the computer running the code to the Viam Cloud where the air quality sensor data is stored.

{{< table >}}
{{% tablestep number=1 %}}

You'll first create a client to obtain the organization and location ID.
Then you'll get a `dataClient` instance which accesses all the data in your location, and then query this data to get only the data tagged with the `air-quality` tag you applied with your data service configuration.
The following code also queries the data for a list of the machines that have collected air quality data so that later, depending on the API key used with the code, your dashboard can show the data from any number of machines.

Paste the following code into the main function of your <file>main.ts</file> script, directly after the `locationID` line, in place of `// <Insert data client and query code here in later steps>`:

```typescript {class="line-numbers linkable-line-numbers"}
// Instantiate data_client and get all
// data tagged with "air-quality" from your location
const client = await VIAM.createViamClient(opts);
const machine = await client.appClient.getRobot(machineId);
const locationID = machine?.location;
const orgID = (await client.appClient.listOrganizations())[0].id;

const myDataClient = client.dataClient;
const query = {
  $match: {
    tags: "air-quality",
    location_id: locationID,
    organization_id: orgID,
  },
};
const match = { $group: { _id: "$robot_id" } };
// Get a list of all the IDs of machines that have collected air quality data
const BSONQueryForMachineIDList = [
  BSON.serialize(query),
  BSON.serialize(match),
];
let machineIDs: any = await myDataClient?.tabularDataByMQL(
  orgID,
  BSONQueryForMachineIDList,
);
// Get all the air quality data
const BSONQueryForData = [BSON.serialize(query)];
let measurements: any = await myDataClient?.tabularDataByMQL(
  orgID,
  BSONQueryForData,
);
```

{{% /tablestep %}}
{{% tablestep number=2 %}}

For this project, your dashboard will display the average of the last five readings from each air sensor.
You need a function to calculate that average.
The data returned by the query is not necessarily returned in order, so this function must put the data in order based on timestamps before averaging the last five readings.

Paste the following code into <file>main.ts</file> after the end of your main function, in place of `// <Insert getLastFewAv function definition here in later steps>`:

```typescript {class="line-numbers linkable-line-numbers"}
// Get the average of the last five readings from a given sensor
async function getLastFewAv(all_measurements: any[], machineID: string) {
  // Get just the data from this machine
  let measurements = new Array();
  for (const entry of all_measurements) {
    if (entry.robot_id == machineID) {
      measurements.push({
        PM25: entry.data.readings["pm_2.5"],
        time: entry.time_received,
      });
    }
  }

  // Sort the air quality data from this machine
  // by timestamp
  measurements = measurements.sort(function (a, b) {
    let x = a.time.toString();
    let y = b.time.toString();
    if (x < y) {
      return -1;
    }
    if (x > y) {
      return 1;
    }
    return 0;
  });

  // Add up the last 5 readings collected.
  // If there are fewer than 5 readings, add all of them.
  let x = 5; // The number of readings to average over
  if (x > measurements.length) {
    x = measurements.length;
  }
  let total = 0;
  for (let i = 1; i <= x; i++) {
    const reading: number = measurements[measurements.length - i].PM25;
    total += reading;
  }
  // Return the average of the last few readings
  return total / x;
}
```

{{% /tablestep %}}
{{% tablestep number=3 %}}

Now that you've defined the function to sort and average the data for each machine, you're done with all the `dataClient` code.
The final piece you need to add to this script is a way to create some HTML to display data from each machine in your dashboard.

Paste the following code into the main function of <file>main.ts</file>, in place of `// <Insert HTML block code here in later steps>`:

```typescript {class="line-numbers linkable-line-numbers"}
// Instantiate the HTML block that will be returned
// once everything is appended to it
let htmlblock: HTMLElement = document.createElement("div");

// Display the relevant data from each machine to the dashboard
for (let m of machineIDs) {
  let insideDiv: HTMLElement = document.createElement("div");
  let avgPM: number = await getLastFewAv(measurements, m._id);
  // Color-code the dashboard based on air quality category
  let level: string = "blue";
  switch (true) {
    case avgPM < 12.1: {
      level = "good";
      break;
    }
    case avgPM < 35.5: {
      level = "moderate";
      break;
    }
    case avgPM < 55.5: {
      level = "unhealthy-sensitive";
      break;
    }
    case avgPM < 150.5: {
      level = "unhealthy";
      break;
    }
    case avgPM < 250.5: {
      level = "very-unhealthy";
      break;
    }
    case avgPM >= 250.5: {
      level = "hazardous";
      break;
    }
  }
  let machineName = (await client.appClient.getRobot(m._id))?.name;
  // Create the HTML output for this machine
  insideDiv.className = "inner-div " + level;
  insideDiv.innerHTML =
    "<p>" +
    machineName +
    ": " +
    avgPM.toFixed(2).toString() +
    " &mu;g/m<sup>3</sup></p>";
  htmlblock.appendChild(insideDiv);
}

// Output a block of HTML with color-coded boxes for each machine
return document.getElementById("insert-readings")?.replaceWith(htmlblock);
```

{{% /tablestep %}}
{{< /table >}}

### Style your dashboard

You have completed the main TypeScript file that gathers and sorts the data.
Now, you'll create a page to display the data.

{{% alert title="Tip" color="tip" %}}
The complete code is available on [GitHub](https://github.com/viam-labs/air-quality-fleet) as a reference.
{{% /alert %}}

{{< table >}}
{{% tablestep number=1 %}}

Create a folder called <file>static</file> inside your <file>aqi-dashboard</file> folder.
Inside the <file>static</file> folder, create a file called <file>index.html</file>.
This file specifies the contents of the webpage that you will see when you run your code.
Paste the following into <file>index.html</file>:

```{class="line-numbers linkable-line-numbers" data-line="11"}
<!doctype html>
<html>
<head>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <div id="main">
    <div>
      <h1>Air Quality Dashboard</h1>
    </div>
    <script type="module" src="main.js"></script>
    <div>
      <h2>PM 2.5 readings</h2>
      <p>The following are averages of the last few readings from each machine:</p>
    </div>
    <div id="insert-readings">
      <p><i>Loading data...
        It may take a few moments for the data to load.
        Do not refresh page.</i></p>
    </div>
    <br>
    <div class="key">
      <h4 style="margin:5px 0px">Key:</h4>
      <p class="good">Good air quality</p>
      <p class="moderate">Moderate</p>
      <p class="unhealthy-sensitive">Unhealthy for sensitive groups</p>
      <p class="unhealthy">Unhealthy</p>
      <p class="very-unhealthy">Very unhealthy</p>
      <p class="hazardous">Hazardous</p>
    </div>
    <p>
      After the data has loaded, you can refresh the page for the latest readings.
    </p>
  </div>
</body>
</html>
```

{{% alert title="Fun fact" color="info" %}}

Line 11, highlighted above, is where the HTML output of the TypeScript file <file>main.ts</file> will get pulled in.

TypeScript is a superset of JavaScript with added functionality, and it transpiles to JavaScript, which is why your file is called <file>main.ts</file> even though line 11 indicates `src="main.js"`.
If you look at line 5 of <file>package.json</file>, you can see that `./main.ts` builds out to `static/main.js`.

{{% /alert %}}

{{% /tablestep %}}
{{% tablestep number=2 %}}

Now you'll create a style sheet to specify the fonts, colors, and spacing of your dashboard.
Create a new file inside your <file>static</file> folder and name it <file>style.css</file>.

{{% /tablestep %}}
{{% tablestep number=3 %}}

Paste the following into <file>style.css</file>:

```{class="line-numbers linkable-line-numbers"}
body {
  font-family: Helvetica;
  margin-left: 20px;
}

div {
  background-color: whitesmoke;
}

h1 {
  color: black;
}

h2 {
  font-family: Helvetica;
}

.inner-div {
  font-family: monospace;
  border: .2px solid;
  background-color: lightblue;
  padding: 20px;
  margin-top: 10px;
  max-width: 320px;
  font-size: large;
}

.key {
  max-width: 200px;
  padding: 0px 5px 5px;
}

.key p {
  padding: 4px;
  margin: 0px;
}

.good {
  background-color: lightgreen;
}

.moderate {
  background-color: yellow;
}

.unhealthy-sensitive {
  background-color: orange;
}

.unhealthy {
  background-color: red;
}

.very-unhealthy {
  background-color: violet;
}

.hazardous {
  color: white;
  background-color: purple;
}

#main {
  max-width:600px;
  padding:10px 30px 10px;
}
```

{{% /tablestep %}}
{{< /table >}}

### Full tutorial code

You can find all the code in the [GitHub repo for this tutorial](https://github.com/viam-labs/air-quality-fleet).

### Style the authentication screen

You can optionally add a logo for your company by placing it into the <FILE>static</FILE> folder.
If your logo's is not called <FILE>logo.png</FILE>, change it to that or update the `logoPath` in your <FILE>meta.json</FILE>.

### Run the code

1. Run the following command to serve the application you are building:

   ```sh {class="command-line" data-prompt="$" data-output="2-10"}
   npm start
   ```

   {{<imgproc src="/tutorials/air-quality-fleet/terminal-url.png" resize="800x" declaredimensions=true alt="Terminal window with the command 'npm start' run inside the aqi-dashboard folder. The output says 'start' and then 'esbuild' followed by the esbuild string from the package.json file you configured. Then there's 'Local:' followed by a URL and 'Network:' followed by a different URL." class="imgzoom" style="width:800px">}}

1. Run the following command specifying the address where your app is running on localhost and a machine to test on.
   The command will proxy your local app and open a browser window and navigate to `http://localhost:8012/machine/<machineHostname>` for the machine provided with --machine-id.

   ```sh {class="command-line" data-prompt="$" data-output="3-10"}
   viam login
   viam module local-app-testing --app-url http://localhost:8000 --machine-id <MACHINE-ID>
   ```

1. The data may take up to approximately 5 seconds to load, then you should see air quality data from all of your sensors.
   If the dashboard does not appear, right-click the page, select **Inspect**, and check for errors in the console.

   ![Air quality dashboard in a web browser with PM2.5 readings from three different sensor machines displayed.](/tutorials/air-quality-fleet/three-sensor-dash.png)

### Deploy the application as a Viam application

You've learned how to configure a machine and you can view its data in a custom TypeScript dashboard.
Let's deploy this dashboard as a Viam-hosted application so you don't have to run it locally.
This will also allow others to use the dashboard.

{{< table >}}
{{% tablestep number=1 %}}

**Create a <FILE>meta.json</FILE>** in your project folder using this template:

```json
{
  "module_id": "<your-namespace>:air-quality",
  "visibility": "public",
  "url": "https://github.com/viam-labs/air-quality-fleet/",
  "description": "Display air quality data from a machine",
  "applications": [
    {
      "name": "air-quality",
      "type": "single_machine",
      "entrypoint": "static/index.html",
      "fragmentIds": [],
      "logoPath": "static/logo.png",
      "customizations": {
        "machinePicker": {
          "heading": "Air monitoring dashboard",
          "subheading": "Sign in and select your devices to view your air quality metrics in a dashboard."
        }
      }
    }
  ]
}
```

In [Viam](https://app.viam.com), navigate to your organization settings through the menu in upper right corner of the page.
Find the **Public namespace** and copy that string.
Replace `<your-namespace>` with your public namespace.

{{< alert title="Tip" color="tip" >}}
For the deployed Viam application, you can require that a machine must have one or more fragments in its configuration to be able to use it.
This avoids users selecting a machine that does not work with your application.
Later in this tutorial, you'll [create a fragment](/tutorials/control/air-quality-fleet/#get-machines-ready-for-third-parties) for your machines.
Once you do that you can update the value for `fragmentIds`.
{{< /alert >}}

{{% /tablestep %}}
{{% tablestep number=2 %}}

**Register your module** with Viam:

```sh {class="command-line" data-prompt="$" data-output="3-10"}
viam module create --name="air-quality" --public-namespace="your-namespace"
```

{{% /tablestep %}}
{{% tablestep number=3 %}}

**Package your static files and your <FILE>meta.json</FILE> file and upload them** to the Viam Registry:

```sh {class="command-line" data-prompt="$" data-output=""}
npm run build
tar -czvf module.tar.gz static meta.json
viam module upload --upload=module.tar.gz --platform=any --version=0.0.1
```

For subsequent updates run these commands again with an updated version number.

{{% /tablestep %}}
{{% tablestep number=4 %}}

**Try your application** by navigating to:

```txt
https://air-quality_your-public-namespace.viamapplications.com
```

Log in and select your development machine.
Your dashboard should now load your data.

{{% /tablestep %}}
{{< /table >}}

## Organize devices for third-party usage

The following example shows how you can use {{< glossary_tooltip term_id="organization" text="organizations" >}} and {{< glossary_tooltip term_id="location" text="locations" >}} to provide users access to the right groups of machines.

Imagine you create an air quality monitoring company called Pollution Monitoring Made Simple.
Anyone can sign up and order one of your sensing machines.
When a new customer signs up, you assemble a new machine with a sensor, SBC, and power supply.

Before shipping the sensor machine to your new client, you provision the machine, so that the recipient only needs to connect the machine to their WiFi network for it to work.

To manage all your company's air quality sensing machines together, you create one organization called Pollution Monitoring Made Simple.
An organization is the highest level grouping, and often contains all the locations (and machines) of an entire company.

Inside that organization, you create a location for each customer.
A location can represent either a physical location or some other conceptual grouping.
You have some individual customers, for example Antonia, who has one sensor machine in her home and one outside.
You have other customers who are businesses, for example RobotsRUs, who have two offices, one in New York and one in Oregon, with multiple sensor machines in each.

Organization and locations allow you to manage permissions:

- When you provision Antonia's machines, you create them inside a new location called `Antonia's Home` and grant Antonia operator access to the location.
  This will later allow her to view data from the air sensors at her home.
- When you provision the machines for RobotsRUs, you create a location called `RobotsRUs` and two sub-locations for `New York Office` and `Oregon Office`.
  Then you create the machines in the sub-locations and grant RobotsRUs operator access to the `RobotsRUs` machines location.

You, as the organization owner, will be able to manage any necessary configuration changes for all air sensing machines in all locations created within the Pollution Monitoring Made Simple organization.

{{<imgproc class="imgzoom" src="/tutorials/air-quality-fleet/example-org-structure.png" resize="x900" declaredimensions=true alt="Diagram of the Pollution Monitoring Made Simple organization. In it are two locations: Antonia's HOme and Robots R Us. Robots R Us contains two sub-locations, each containing some machines. The Antonia's Home location contains two machines (and no sub-locations)." style="width:800px">}}

For more information, see [Fleet Management](/manage/reference/organize/) and [provisioning](/manage/fleet/provision/setup/).

### Organize your fleet

If you want to follow along, create the following locations:

- `Antonia's Home`
- `RobotsRUs`

For `RobotsRUs` crate two sublocations:

1. Add a new location called `Oregon Office` using the same **Add location** button.
1. Then, find the **New parent location** dropdown on the Oregon Office page.
1. Select **RobotsRUs** and click **Change**.

Repeat to add the New York office: Add a new location called `New York Office`, then change its parent location to **RobotsRUs**.

{{<imgproc class="imgzoom" src="/tutorials/air-quality-fleet/locations-done.png" resize="x900" declaredimensions=true alt="The New York Office fleet page. The left Locations navigation panel lists Antonia's Home and RobotsRUs, with New York Office and Oregon Office nested inside RobotsRUs." style="width:600px"  >}}

## Get machines ready for third parties

Let's continue with our fictitious company and assume you want to ship air sensing machines out to customers from your factory.
In other words, you want to provision devices.

Before an air sensing machine leaves your factory, you'd complete the following steps:

1. You'd flash the SD card for the single-board computer with an operating system.
2. You'd install `viam-agent` with the `preinstall` script.
3. You'd provide a machine configuration template: a _{{< glossary_tooltip term_id="fragment" text="fragment" >}}_.

Once a customer receives your machine, they will:

1. Plug it in and turn it on.
2. `viam-agent` will start a WiFi network.
3. The customer uses another device to connect to the machine's WiFi network and the user gives the machine the password for their WiFi network.
4. The machine can now connect to the internet and complete setup based on the specified fragment in the configuration template.

### Create the fragment for air sensing machines

In this section you will create the {{< glossary_tooltip term_id="fragment" text="fragment" >}}: the configuration template that all other machines will use.

1. Navigate to the **FLEET** page and go to the [**FRAGMENTS** tab](https://app.viam.com/fragments).
1. Click **Create fragment**.
1. Name the fragment `air-quality-configuration`.
1. Add the same components that you added to the development machine when you [set up one device for development](#set-up-one-device-for-development).

   As a shortcut, you can use the JSON mode on the machine you already configured and copy the machine's configuration to the fragment.

   {{< expand "Click here for info about the usb_interface value." >}}

If you only have one USB device plugged into each of your boards, the `usb_interface` value you configured in the sensor config is likely (conveniently) the same for all of your machines.

If not, you can use [fragment overwrite](/manage/fleet/reuse-configuration/#modify-fragment-settings-on-a-machine) to modify the value on any machine for which it is different.

{{< /expand >}}

1. Specify the version for the `sds011` module.
   At the point of writing the version is `0.2.1`.
   Specifying a specific version or a specific minor or major version of a module will ensure that even if the module you use changes, your machines remain functional.
   You can update your fragment at any point, and any machines using it will update to use the new configuration.

{{< alert title="Tip: Use the fragment on your development machine" color="tip" >}}
To avoid differences between fragment and development machines, we recommend you remove the configured resources from the development machine, and instead use the **+** button to add the fragment you just created.
{{< /alert >}}

### Provision your machines

{{< table >}}
{{% tablestep number=1 %}}

For each machine, flash the operating system to the device's SD card.
If you are using the Raspberry Pi Imager, you **must customize at least the hostname** for the next steps to work.

Then run the following commands to download the preinstall script and make the script executable:

```sh {class="command-line" data-prompt="$"}
wget https://storage.googleapis.com/packages.viam.com/apps/viam-agent/preinstall.sh
chmod 755 preinstall.sh
```

{{% /tablestep %}}
{{% tablestep number=2 %}}

Create a file called <FILE>viam-defaults.json</FILE> with the following configuration:

```json {class="line-numbers linkable-line-numbers"}
{
  "network_configuration": {
    "manufacturer": "Pollution Monitoring Made Simple",
    "model": "v1",
    "fragment_id": "<FRAGMENT-ID>",
    "hotspot_prefix": "air-quality",
    "hotspot_password": "WeLoveCleanAir123"
  }
}
```

Replace `<FRAGMENT-ID>` with the fragment ID from your fragment.

{{% /tablestep %}}
{{% tablestep number=3 %}}

In [Organize your fleet](#organize-your-fleet) you created several locations.
Navigate to one of the locations and create a machine.
Select the part status dropdown to the right of your machine's name on the top of the page.

Click the copy icon next to **Machine cloud credentials**.
Paste the machine cloud credentials into a file on your hard drive called <FILE>viam.json</FILE>.

{{< alert title="Tip: Fleet management API" color="tip" >}}
You can create locations and machines programmatically, with the [Fleet management API](/dev/reference/apis/fleet/).
{{< /alert >}}

{{% /tablestep %}}
{{% tablestep number=4 %}}

**Run the preinstall script** without options and it will attempt to auto-detect a mounted root filesystem (or for Raspberry Pi, bootfs) and also automatically determine the architecture.

```sh {class="command-line" data-prompt="$"}
sudo ./preinstall.sh
```

Follow the instructions and provide the <FILE>viam-defaults.json</FILE> file and the machine cloud credentials file when prompted.

{{% /tablestep %}}
{{< /table >}}

That's it!
Your device is now provisioned and ready for your end user!

Having trouble?
See [Provisioning](/manage/fleet/provision/setup/) for more information and troubleshooting.

<div id="emailform"></div>

## Next steps

You can now set up one or more air quality sensors for yourself or others and access them with your dashboard.
If you are selling your air quality sensing machines, users can use your dashboard to view _their_ data.

If you're wondering what to do next, why not set up a text or email alert when your air quality passes a certain threshold?
For instructions on setting up an email alert, see the [Monitor Helmet Usage tutorial](/tutorials/projects/helmet/) as an example.
For an example of setting up text alerts, see the [Detect a Person and Send a Photo tutorial](/tutorials/projects/send-security-photo/).

{{< cards >}}
{{% card link="/tutorials/projects/helmet/" %}}
{{% card link="/tutorials/projects/send-security-photo/" %}}
{{% card link="/tutorials/services/visualize-data-grafana/" %}}
{{< /cards >}}
