---
linkTitle: "Tutorial: multi-machine fleet dashboard"
title: "Build a multi-machine fleet dashboard"
weight: 120
layout: "docs"
type: "docs"
description: "Build a TypeScript web dashboard that connects to the Viam cloud, enumerates machines across an organization, and displays aggregated sensor data from a fleet."
date: "2026-04-10"
---

In this tutorial, you will build a browser-based dashboard that reads captured sensor data from a fleet of Viam machines and displays aggregated values per machine. The finished dashboard:

- Connects to the Viam cloud using a user API key
- Lists the machines in your organization
- Runs an MQL aggregation query over the last hour of sensor readings for each machine
- Renders the results as a table

You will learn the patterns for working with multi-machine Viam apps: connecting to the cloud rather than to one machine, enumerating resources across an organization, and aggregating captured data with MQL. The dashboard runs locally in your browser for most of the tutorial, with an optional final step to deploy it as a hosted Viam Application.

The tutorial uses the air-quality use case as a concrete example: each machine has an air quality sensor that captures PM2.5 readings, and the dashboard shows the average for each machine over the last hour. The patterns work the same for any fleet and any captured data; substitute your own sensor type and field names as needed.

## What you need

- A Viam organization with at least two machines configured. Any machines work as long as each has a sensor you can capture data from. For the tutorial's air-quality framing, each machine has a sensor that returns a PM2.5 value under a field named `pm_2_5`, but you can use any field name as long as you update the MQL query in step 4 to match.
- Data capture configured on the sensors, with enough data synced to the cloud that there are recent readings to aggregate. See [Capture and sync data](/data/capture-sync/capture-and-sync-data/) if you need to set this up.
- An organization-scoped or location-scoped API key and its ID. Create one in [Admin and access](/organization/access/). A machine-scoped key will not work for this tutorial because you need access to multiple machines.
- A completed [TypeScript setup](/build-apps/setup/typescript/) with Vite, the Viam TypeScript SDK, a `.env` file, and an `index.html` plus `src/main.ts` from the setup page.
- Your organization ID. Find it in the Viam app by clicking your organization name and selecting **Settings**.

Before continuing, update your `.env` file to use an organization-scoped API key instead of a machine-scoped one, and add your organization ID:

```text
VITE_API_KEY_ID=your-org-api-key-id
VITE_API_KEY=your-org-api-key-secret
VITE_ORG_ID=your-organization-id
```

You no longer need `VITE_HOST` for this tutorial; the cloud client does not connect to a specific machine address.

## Step 1: Replace the HTML

Open `index.html` and replace its contents:

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <title>Fleet Dashboard</title>
    <style>
      body {
        font-family: system-ui, sans-serif;
        padding: 1rem;
      }
      table {
        border-collapse: collapse;
        margin-top: 1rem;
      }
      th,
      td {
        border: 1px solid #ccc;
        padding: 0.5rem 1rem;
        text-align: left;
      }
      th {
        background: #f0f0f0;
      }
      .good {
        color: green;
      }
      .moderate {
        color: orange;
      }
      .unhealthy {
        color: red;
      }
    </style>
  </head>
  <body>
    <h1>Fleet Dashboard</h1>
    <p id="status">Connecting...</p>
    <div id="dashboard"></div>
    <script type="module" src="/src/main.ts"></script>
  </body>
</html>
```

Save. If Vite is running, it reloads automatically.

## Step 2: Connect to the Viam cloud

Replace the contents of `src/main.ts` with a cloud connection that uses `createViamClient` instead of `createRobotClient`:

```ts
import * as VIAM from "@viamrobotics/sdk";

const statusEl = document.getElementById("status") as HTMLParagraphElement;
const dashboardEl = document.getElementById("dashboard") as HTMLDivElement;

const ORG_ID = import.meta.env.VITE_ORG_ID;

let client: VIAM.ViamClient;

async function main() {
  client = await VIAM.createViamClient({
    credentials: {
      type: "api-key",
      authEntity: import.meta.env.VITE_API_KEY_ID,
      payload: import.meta.env.VITE_API_KEY,
    },
  });

  statusEl.textContent = "Connected to Viam cloud";
}

main().catch((err) => {
  statusEl.textContent = `Connection failed: ${err.message ?? err}`;
});
```

Save and refresh. The status line should change to `Connected to Viam cloud`. If you see `Connection failed:`, check that the API key you put in `.env` is organization-scoped (not machine-scoped) and that the organization ID matches your Viam account.

Unlike `createRobotClient`, the cloud client does not open a WebRTC connection. It holds a transport that makes HTTP-based gRPC calls to the Viam cloud API. Each subsequent method call is a separate request.

## Step 3: List the machines in the organization

Add a function that lists all machines across all locations in your organization using `appClient.listMachineSummaries`:

```ts
interface Machine {
  id: string;
  name: string;
  locationName: string;
}

async function listMachines(): Promise<Machine[]> {
  const summaries = await client.appClient.listMachineSummaries(ORG_ID);
  const machines: Machine[] = [];
  for (const location of summaries) {
    for (const m of location.machines) {
      machines.push({
        id: m.machineId,
        name: m.machineName,
        locationName: location.locationName,
      });
    }
  }
  return machines;
}
```

Call `listMachines()` at the end of `main()` and log the result:

```ts
async function main() {
  client = await VIAM.createViamClient({
    // ... (unchanged)
  });

  statusEl.textContent = "Connected to Viam cloud";

  const machines = await listMachines();
  console.log(`Found ${machines.length} machines`);
  for (const m of machines) {
    console.log(`  ${m.name} (${m.id}) in ${m.locationName}`);
  }
}
```

Save and refresh. Open the browser's developer console. You should see a list of every machine in your organization with its name, ID, and location. If you have more than one location, machines from all of them are listed.

## Step 4: Query aggregated data

Now run an MQL aggregation query for each machine to get the average PM2.5 reading over the last hour. The TypeScript SDK accepts plain JavaScript objects for MQL queries and serializes them to BSON internally:

```ts
interface MachineReading {
  machineId: string;
  machineName: string;
  locationName: string;
  avgPm25: number | null;
  sampleCount: number;
}

async function getReadingForMachine(m: Machine): Promise<MachineReading> {
  const oneHourAgo = new Date(Date.now() - 3600 * 1000);

  const pipeline = [
    {
      $match: {
        robot_id: m.id,
        component_name: "air_quality_sensor",
        time_received: { $gte: oneHourAgo },
      },
    },
    {
      $group: {
        _id: null,
        avgPm25: { $avg: "$data.readings.pm_2_5" },
        sampleCount: { $sum: 1 },
      },
    },
  ];

  const results = await client.dataClient.tabularDataByMQL(ORG_ID, pipeline);

  if (results.length === 0) {
    return {
      machineId: m.id,
      machineName: m.name,
      locationName: m.locationName,
      avgPm25: null,
      sampleCount: 0,
    };
  }

  const row = results[0] as { avgPm25: number; sampleCount: number };
  return {
    machineId: m.id,
    machineName: m.name,
    locationName: m.locationName,
    avgPm25: row.avgPm25,
    sampleCount: row.sampleCount,
  };
}
```

The `$match` stage filters the captured data to:

- Only the current machine's readings (`robot_id` matches)
- Only the air quality sensor component (change `"air_quality_sensor"` to your sensor's component name)
- Only the last hour of data

The `$group` stage computes the average of the `pm_2_5` field across all matching readings and counts how many samples contributed to the average. Change `$data.readings.pm_2_5` to the actual field path your sensor captures.

Add a function that runs the query for every machine in parallel:

```ts
async function getFleetReadings(
  machines: Machine[],
): Promise<MachineReading[]> {
  return Promise.all(machines.map(getReadingForMachine));
}
```

Update `main()` to call it and log the results:

```ts
async function main() {
  client = await VIAM.createViamClient({
    // ... (unchanged)
  });

  statusEl.textContent = "Connected to Viam cloud";

  const machines = await listMachines();
  const readings = await getFleetReadings(machines);
  console.log(readings);
}
```

Save and refresh. The console now shows one entry per machine with the average PM2.5 value and sample count. If a machine has no data in the last hour, its `avgPm25` is `null` and its `sampleCount` is `0`.

## Step 5: Render the dashboard

Replace the console logging with a table rendered into the `#dashboard` element:

```ts
function categorize(pm25: number | null): string {
  if (pm25 === null) return "";
  if (pm25 < 12) return "good";
  if (pm25 < 35) return "moderate";
  return "unhealthy";
}

function renderDashboard(readings: MachineReading[]) {
  const rows = readings
    .map((r) => {
      const category = categorize(r.avgPm25);
      const value = r.avgPm25 === null ? "—" : `${r.avgPm25.toFixed(1)} µg/m³`;
      return `
        <tr>
          <td>${r.machineName}</td>
          <td>${r.locationName}</td>
          <td class="${category}">${value}</td>
          <td>${r.sampleCount}</td>
        </tr>
      `;
    })
    .join("");

  dashboardEl.innerHTML = `
    <table>
      <thead>
        <tr>
          <th>Machine</th>
          <th>Location</th>
          <th>Avg PM2.5 (last hour)</th>
          <th>Samples</th>
        </tr>
      </thead>
      <tbody>${rows}</tbody>
    </table>
  `;
}
```

Replace the `console.log(readings)` in `main()` with a call to `renderDashboard(readings)`:

```ts
const readings = await getFleetReadings(machines);
renderDashboard(readings);
statusEl.textContent = `Showing ${readings.length} machines`;
```

Save and refresh. You should now see a table with one row per machine, showing the machine name, location, average PM2.5 value over the last hour, and the number of samples that contributed to the average. Values below 12 µg/m³ display in green (good), 12–35 in orange (moderate), and above 35 in red (unhealthy).

The category thresholds follow the United States EPA's air quality index breakpoints for PM2.5. Use whatever thresholds are appropriate for the data you are actually showing.

## Step 6: Refresh on a timer

A fleet dashboard is most useful when it updates on its own. Wrap the query-and-render in a function and run it on a 30-second interval:

```ts
async function refresh() {
  try {
    const machines = await listMachines();
    const readings = await getFleetReadings(machines);
    renderDashboard(readings);
    statusEl.textContent = `Last updated ${new Date().toLocaleTimeString()}, ${readings.length} machines`;
  } catch (err) {
    statusEl.textContent = `Update failed: ${(err as Error).message}`;
  }
}
```

Replace the manual calls in `main()` with one initial call to `refresh()` followed by a `setInterval`:

```ts
async function main() {
  client = await VIAM.createViamClient({
    // ... (unchanged)
  });

  await refresh();
  setInterval(refresh, 30_000);
}
```

Save and refresh. The dashboard updates every 30 seconds. The status line shows the last update time and the number of machines displayed. If a refresh fails (network error, query timeout), the status line shows the error but the previous dashboard state stays on screen.

## What you built

You now have a multi-machine dashboard that:

- Connects to the Viam cloud with an organization-scoped API key
- Enumerates every machine in the organization across all locations
- Runs an MQL aggregation query for each machine to compute the average PM2.5 reading over the last hour
- Renders the results as a color-coded table
- Refreshes every 30 seconds

The full `src/main.ts` is around 130 lines. The patterns you used (cloud client, machine enumeration, MQL aggregation, periodic refresh) are the same patterns any multi-machine Viam app uses. Whether your fleet monitors air quality, tracks warehouse rovers, or aggregates manufacturing telemetry, the dashboard shape is the same.

## Deploy as a Viam Application (optional)

The dashboard runs locally right now. To host it at a Viam URL with built-in authentication, follow [Deploy a Viam application](/build-apps/hosting/deploy/). The key change when deploying: instead of reading credentials from `import.meta.env`, your deployed app reads them from a browser cookie that Viam injects after the user logs in.

Replace the `createViamClient` call with code that reads the access token from the `userToken` cookie. The [hosting platform reference](/build-apps/hosting/hosting-reference/) documents the exact cookie format. When deployed as a multi-machine Viam Application, the rest of the dashboard code works unchanged; only the credential loading changes.

## Next steps

- **Filter by fragment.** If you configured the machines in your fleet with a shared fragment, pass `fragmentIds` to `listMachineSummaries` to scope the dashboard to only machines that include that fragment. Useful for multi-tenant apps where one organization has several customer fleets.
- **Show historical trends.** Change the MQL pipeline to use `$bucket` or `$bucketAuto` to group readings into time buckets, then render a chart instead of a single aggregate value. [Query captured data](/build-apps/tasks/query-data/) covers more aggregation patterns.
- **Aggregate across multiple sensor types.** Run a different MQL pipeline for each sensor you care about (PM2.5, PM10, VOC, temperature) and show all of them in the same row per machine.
- **Add a machine detail view.** When the user clicks a row, open a second view that queries minute-by-minute data for that one machine. The common fleet dashboard pattern is an overview table plus a detail view per machine.
- **Deploy to Viam Applications.** Follow [Deploy a Viam application](/build-apps/hosting/deploy/) for the packaging and upload workflow.
