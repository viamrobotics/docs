Viam's [data management service](/services/data/) lets you capture data locally from sensors and then sync it to the cloud where you can access all data across different {{< glossary_tooltip term_id="machine" text="machines" >}} or {{< glossary_tooltip term_id="location" text="locations" >}}.

{{< table >}}
{{< tablestep link="/services/data/">}}
{{<imgproc src="/services/icons/data-management.svg" class="fill alignleft" style="max-width: 150px" declaredimensions=true alt="Configure the data management service">}}
**1. Add the data management service**

On your machine's **CONFIGURE** tab, add the **data management** service.

Enable **Syncing** to ensure captured data is synced to the cloud and set the sync interval, for example to `0.05` minutes to sync every 3 seconds.

{{< /tablestep >}}
{{< tablestep >}}
{{<imgproc src="/icons/components/sensor.svg" class="fill alignleft" style="max-width: 150px" declaredimensions=true alt="configure a camera component">}}
**2. Capture data from sensor**

On the **CONFIGURE** tab, go to the **sensor**'s card and find the **Data capture** section.
Add a new method, `Readings`, to capture data for and set the frequency.
For example, setting a frequency of `0.1` will capture data once every ten seconds.

{{< /tablestep >}}
{{< tablestep >}}
{{<imgproc src="/services/ml/configure.svg" class="fill alignleft" style="max-width: 150px"  declaredimensions=true alt="Train models">}}
**3. Save to start capturing**

Save the config.
With cloud sync enabled, captured data is automatically uploaded to the Viam app after a short delay.

{{< /tablestep >}}
{{< tablestep link="/services/data/view/">}}
{{<imgproc src="/services/icons/data-capture.svg" class="fill alignleft" style="max-width: 150px" declaredimensions=true alt="Capture tabular data from a sensor">}}
**4. View data in the Viam app**

To confirm data is being synced, go to the **DATA** tab and select the **Sensors** subtab.
Confirm that you are seeing data appear.

{{< /tablestep >}}
{{< /table >}}

{{< alert title="Tip" color="tip" >}}
If you need to sync data conditionally, for example at a certain time, see [Trigger Sync](/services/data/trigger-sync/#configure-data-manager-to-sync-based-on-sensor).
{{< /alert >}}
