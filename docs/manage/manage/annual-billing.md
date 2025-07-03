---
title: "Annual Billing"
linkTitle: "Annual Billing"
weight: 75
layout: "docs"
type: "docs"
description: "Configure annual billing for improved revenue retention and customer flexibility."
date: "2025-07-03"
---

Viam's annual billing feature allows organizations to offer 12-month subscription billing cycles alongside traditional monthly billing. This feature helps improve revenue retention by providing customers with annual pricing options and reduces churn from seasonal cancellations.

## Key Features

Annual billing provides several advantages over monthly-only billing:

- **Revenue retention**: Customers commit to longer billing cycles, reducing seasonal cancellations
- **Upfront payment options**: Charge customers immediately rather than in arrears
- **Flexible pricing models**: Offer monthly, annual, or combined billing options
- **Automated billing cycles**: Handle 12-month billing periods automatically
- **Enhanced invoicing**: Generate annual invoices with proper billing period tracking

## Billing Configuration Options

You can configure billing in three ways:

### Monthly Billing Only
Traditional monthly billing charged in arrears (after usage):

```json
{
  "billing": {
    "cost_per_month": {
      "per_machine": 10
    },
    "tier_name": "monthly-tier",
    "in_arrears": true
  }
}
```

### Annual Billing Only
Annual billing with upfront payment:

```json
{
  "billing": {
    "cost_per_year": {
      "per_machine": 100
    },
    "tier_name": "annual-tier",
    "in_arrears": false
  }
}
```

### Combined Billing
Offer both monthly and annual options:

```json
{
  "billing": {
    "cost_per_month": {
      "per_machine": 10
    },
    "cost_per_year": {
      "per_machine": 100
    },
    "tier_name": "flexible-tier",
    "in_arrears": true
  }
}
```

## Configuration Attributes

### Core Billing Attributes

<!-- prettier-ignore -->
| Name | Type | Required? | Description |
| ---- | ---- | --------- | ----------- |
| `cost_per_month` | object | Optional | Monthly pricing configuration. See [monthly pricing attributes](#monthly-pricing-attributes). |
| `cost_per_year` | object | Optional | Annual pricing configuration. See [annual pricing attributes](#annual-pricing-attributes). |
| `tier_name` | string | **Required** | The name of the billing tier. |
| `description` | string | Optional | Description for the billing tier. Default: `""`. |
| `tier_credit` | number | Optional | Credit applied to final total for the organization. Default: `0`. |
| `in_arrears` | boolean | Optional | Whether billing is charged in arrears (after usage) or upfront. Set to `true` for monthly billing in arrears, `false` for upfront annual billing. Default: `true`. |

### Annual Pricing Attributes

<!-- prettier-ignore -->
| Name | Type | Required? | Description |
| ---- | ---- | --------- | ----------- |
| `per_machine` | number | Optional | Charge a flat annual fee per machine. Default: `0`. |

### Monthly Pricing Attributes

<!-- prettier-ignore -->
| Name | Type | Required? | Description |
| ---- | ---- | --------- | ----------- |
| `per_machine` | number | Optional | Charge a flat monthly fee per machine. Default: `0`. |
| `binary_data_upload_bytes` | float | Optional | Cost per byte for binary data upload. Default: `0`. |
| `binary_data_egress_bytes` | float | Optional | Cost per byte for binary data download. Default: `0`. |
| `binary_data_cloud_storage_bytes` | float | Optional | Cost per byte per month for binary data stored. Default: `0`. |
| `tabular_data_upload_bytes` | float | Optional | Cost per byte per month for tabular data upload. Default: `0`. |
| `tabular_data_egress_bytes` | float | Optional | Cost per byte per month for tabular data egress. Default: `0`. |
| `tabular_data_cloud_storage_bytes` | float | Optional | Cost per byte per month for tabular data cloud storage. Default: `0`. |
| `history_cloud_storage_bytes` | float | Optional | Cost per byte per month for config history stored. Default: `0`. |
| `logs_cloud_storage_bytes` | float | Optional | Cost per byte per month for logs cloud storage. Default: `0`. |
| `logs_data_upload_bytes` | float | Optional | Cost per byte per month for logs data upload. Default: `0`. |
| `logs_data_egress_bytes` | float | Optional | Cost per byte per month for logs data egress. Default: `0`. |

## Billing Behavior

### Payment Timing

- **Monthly billing (`in_arrears: true`)**: Customers are charged at the end of each month for usage during that month
- **Annual billing (`in_arrears: false`)**: Customers are charged upfront at the beginning of each 12-month period

### Invoice Generation

- **Monthly billing**: Invoices are generated monthly with usage from the previous month
- **Annual billing**: Invoices are generated every 12 months for the upcoming annual period
- **Combined billing**: Customers can choose between monthly and annual billing cycles

### Billing Cycle Management

Annual billing automatically handles:

- 12-month billing periods starting from the initial subscription date
- Automatic renewal after each 12-month cycle
- Proper invoice timing and generation
- Usage tracking across annual periods

## Implementation Considerations

### Migration from Monthly to Annual

When migrating existing customers from monthly to annual billing:

1. **Timing**: Consider waiting until the next billing cycle to avoid mid-cycle complications
2. **Communication**: Notify customers about billing cycle changes in advance
3. **Pricing**: Ensure annual pricing provides appropriate value compared to monthly rates

### Pricing Strategy

When setting annual pricing:

- **Discount incentive**: Annual pricing typically offers savings compared to 12 months of monthly billing
- **Cash flow**: Consider the impact of upfront payments on your cash flow
- **Customer value**: Balance customer savings with revenue optimization

### Technical Requirements

Annual billing requires:

- Updated billing fragments with `cost_per_year` configuration
- Proper `in_arrears` setting based on payment timing preferences
- Billing system configuration to handle 12-month cycles
- Invoice templates updated for annual billing periods

## Use Cases

### Seasonal Business Models

Annual billing is particularly valuable for businesses with seasonal usage patterns:

- **Boating industry**: Customers might cancel during off-season without annual commitments
- **Agricultural applications**: Seasonal farming operations benefit from annual pricing
- **Tourism and recreation**: Businesses with seasonal peaks can maintain year-round revenue

### Enterprise Customers

Large organizations often prefer annual billing for:

- **Budget planning**: Annual costs are easier to budget and approve
- **Procurement processes**: Many enterprises prefer annual contracts
- **Cost savings**: Annual discounts provide value to enterprise customers

## Troubleshooting

### Common Issues

**Billing cycle confusion**: Ensure customers understand when they'll be charged and for what period.

**Invoice timing**: Annual invoices are generated at the beginning of each 12-month period, not at calendar year boundaries.

**Mixed billing models**: When offering both monthly and annual options, ensure clear communication about which option customers have selected.

### Configuration Validation

Verify your billing configuration:

1. **Required fields**: Ensure `tier_name` is set
2. **Pricing consistency**: Check that annual pricing provides appropriate value
3. **Payment timing**: Confirm `in_arrears` setting matches your business model
4. **Fragment deployment**: Ensure billing fragments are properly deployed to target machines

## Support

For questions about annual billing configuration or implementation:

- **Technical support**: [Contact Viam support](mailto:support@viam.com)
- **Billing questions**: [Contact billing team](mailto:billing@viam.com)
- **White-labelled billing**: See [white-labelled billing documentation](/manage/manage/white-labelled-billing/)