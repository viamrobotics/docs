Copy and paste the following attribute template into your board's **Attributes** box.
Then remove and fill in the attributes as applicable to your board, according to the table below.

{{< tabs >}}
{{% tab name="Attributes template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "digital_interrupts": [
    {
      "name": "<your-digital-interrupt-name>",
      "pin": "<pin-number>"
    }
  ]
}
```

{{% /tab %}}
{{% tab name="Attributes example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "digital_interrupts": [
    {
      "name": "your-interrupt-1",
      "pin": "15"
    },
    {
      "name": "your-interrupt-2",
      "pin": "16"
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}
