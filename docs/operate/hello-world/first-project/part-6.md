---
linkTitle: "Part 6: Productize"
title: "Part 6: Productize"
weight: 60
layout: "docs"
type: "docs"
description: "Build a customer-facing dashboard and configure white-label authentication."
date: "2025-01-30"
---

**Goal:** Build a customer-facing product.

**Skills:** Building apps with Viam SDKs, white-label deployment.

**Time:** ~10 min

## 6.1 Create a Dashboard

You've built a working system—but right now, only you can see it through the Viam app. Your customers need their own interface showing inspection results.

Viam offers two approaches:

1. **Built-in Teleop Dashboard** — No code, drag-and-drop widgets
2. **Custom Web App** — Full control with TypeScript SDK

### Option A: Built-in Teleop Dashboard (No Code)

Viam's Teleop dashboard lets you create custom views without writing code.

**Create a dashboard workspace:**

1. In the Viam app, go to **Fleet** → **Teleop** tab
2. Click **+ Create workspace**
3. Name it `Inspection Overview`
4. Select the location containing your inspection stations

**Add widgets:**

Click **+ Add widget** and configure:

1. **Camera Stream** — Select `inspection-cam` from any station to show live video
2. **Time Series Graph** — Plot detection confidence over time from `vision-service`
3. **Table Widget** — Display recent detection results with labels and timestamps
4. **Stat Widget** — Show current pass/fail counts

Drag widgets to arrange your layout. The dashboard updates in real-time.

[SCREENSHOT: Teleop dashboard with inspection widgets]

{{< alert title="Quick wins" color="tip" >}}
The Teleop dashboard is great for internal monitoring and demos. For customer-facing products with your branding, use Option B.
{{< /alert >}}

### Option B: Custom Web App (TypeScript SDK)

For full control over branding and features, build a custom dashboard with Viam's TypeScript SDK.

**Set up a TypeScript project:**

```bash
mkdir inspection-dashboard && cd inspection-dashboard
npm init -y
npm install @viamrobotics/sdk vite
```

**Create `src/main.ts`:**

```typescript
import * as VIAM from "@viamrobotics/sdk";

// Replace with your credentials (from Viam app → Organization → API Keys)
const API_KEY_ID = "YOUR_API_KEY_ID";
const API_KEY = "YOUR_API_KEY";
const ORG_ID = "YOUR_ORG_ID";

async function createClient(): Promise<VIAM.ViamClient> {
  return await VIAM.createViamClient({
    serviceHost: "https://app.viam.com:443",
    credentials: {
      type: "api-key",
      authEntity: API_KEY_ID,
      payload: API_KEY,
    },
  });
}

async function updateDashboard() {
  const client = await createClient();
  const dataClient = client.dataClient;

  // Query detection results from the last 24 hours
  const results = await dataClient.tabularDataBySQL(
    ORG_ID,
    `SELECT * FROM readings
     WHERE component_name = 'vision-service'
     AND time_received > datetime('now', '-1 day')
     ORDER BY time_received DESC
     LIMIT 100`,
  );

  // Calculate stats
  const total = results.length;
  const fails = results.filter((r: any) =>
    JSON.stringify(r).includes("FAIL"),
  ).length;
  const passRate = total > 0 ? (((total - fails) / total) * 100).toFixed(1) : 0;

  // Update UI
  document.getElementById("total-count")!.textContent = String(total);
  document.getElementById("fail-count")!.textContent = String(fails);
  document.getElementById("pass-rate")!.textContent = `${passRate}%`;
}

// Update on load and every 30 seconds
updateDashboard();
setInterval(updateDashboard, 30000);
```

**Create `index.html`:**

```html
<!doctype html>
<html>
  <head>
    <title>Inspection Dashboard</title>
    <style>
      body {
        font-family: system-ui;
        max-width: 800px;
        margin: 0 auto;
        padding: 20px;
      }
      .stats {
        display: flex;
        gap: 20px;
        margin: 20px 0;
      }
      .stat-card {
        background: #f5f5f5;
        padding: 20px;
        border-radius: 8px;
        flex: 1;
      }
      .stat-value {
        font-size: 48px;
        font-weight: bold;
      }
      .pass {
        color: #22c55e;
      }
      .fail {
        color: #ef4444;
      }
    </style>
  </head>
  <body>
    <h1>Quality Inspection Dashboard</h1>
    <div class="stats">
      <div class="stat-card">
        <div>Recent Inspections</div>
        <div class="stat-value" id="total-count">--</div>
      </div>
      <div class="stat-card">
        <div>Pass Rate</div>
        <div class="stat-value pass" id="pass-rate">--%</div>
      </div>
      <div class="stat-card">
        <div>Failures</div>
        <div class="stat-value fail" id="fail-count">--</div>
      </div>
    </div>
    <script type="module" src="/src/main.ts"></script>
  </body>
</html>
```

**Run it:**

```bash
npx vite
```

Open `http://localhost:5173` to see your dashboard.

[SCREENSHOT: Custom dashboard showing inspection stats]

{{< alert title="This is your product" color="tip" >}}
No Viam branding—your interface, your design. The same APIs can power a React app, mobile app, or enterprise dashboard.
{{< /alert >}}

## 6.2 Set Up White-Label Auth

Your customers shouldn't log into Viam—they should log into _your_ product. Viam supports white-label authentication so your branding appears throughout the experience.

**Add your logo:**

Your logo appears on login screens and emails sent to your users:

```bash
# Get your organization ID from Viam app → Organization Settings
viam organization logo set --org-id <YOUR_ORG_ID> --logo-path logo.png
```

The logo must be PNG format, under 200KB.

**Enable custom authentication:**

```bash
viam organization auth-service enable --org-id <YOUR_ORG_ID>
```

This enables OAuth/OIDC integration so users authenticate through your identity provider.

**Set support email:**

```bash
viam organization support-email set --org-id <YOUR_ORG_ID> --email support@yourcompany.com
```

Now password recovery and verification emails come from your support address, not Viam's.

[SCREENSHOT: Branded login screen with custom logo]

With this configured:

- Users see your logo on login
- Emails come from your support address
- Your branding, your experience

{{< alert title="Going further" color="tip" >}}
For full SSO integration with your identity provider (Okta, Auth0, etc.), see the [Authentication documentation](/manage/manage/access/).
{{< /alert >}}

**Create customer organizations:**

For multi-tenant deployments, create separate organizations for each customer:

1. Each customer gets their own organization
2. They see only their machines
3. You maintain access to all organizations as the provider

This lets you ship a product where each customer has isolated access to their own inspection stations.

## 6.3 (Optional) Configure Billing

If you're selling inspection-as-a-service, you need to bill customers. Viam can meter usage and integrate with your billing system.

**Usage metering:**

Viam tracks:

- Number of machines
- Data captured and stored
- API calls
- ML inference operations

You can query this data to build usage-based billing:

```typescript
// Example: Get machine usage for billing
const usage = await dataClient.getUsageByOrganization({
  organizationId: "YOUR_ORG_ID",
  startTime: billingPeriodStart,
  endTime: billingPeriodEnd,
});

// Calculate charges based on your pricing model
const machineCharges = usage.machineCount * PRICE_PER_MACHINE;
const dataCharges = usage.dataGB * PRICE_PER_GB;
```

**Billing integration:**

For production billing, you'd integrate Viam's usage data with your billing system (Stripe, your own invoicing, etc.). The data is available through APIs, so you have full flexibility in how you present and charge for usage.

{{< alert title="Business model flexibility" color="tip" >}}
Charge per machine, per inspection, per GB of data, or a flat subscription. Viam provides the metering data; you decide the pricing.
{{< /alert >}}

**Checkpoint:** You have a customer-ready product. You've gone from prototype to shippable product in one tutorial.

## Congratulations

You've completed the entire tutorial. Here's what you built:

1. **Vision Pipeline** — Camera, ML model, and vision service
2. **Data Capture** — Automatic recording and cloud sync
3. **Control Logic** — Custom inspector that detects and rejects defects
4. **Module Deployment** — Packaged and deployed to run autonomously
5. **Scale** — Fragment-based fleet management
6. **Productize** — Customer dashboard and white-label auth

**[← Back to Overview](../)** to review what you learned.
