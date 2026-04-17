---
linkTitle: "Custom queries"
title: "Custom dashboard queries"
weight: 30
layout: "docs"
type: "docs"
description: "Write MQL aggregation pipelines to create advanced dashboard visualizations."
---

When the built-in window and aggregation methods are not enough, you can write custom MQL (MongoDB Query Language) aggregation pipelines to transform your data. Custom queries give you full control over how data is processed before it reaches a widget.

For an explanation of the built-in methods and when you need custom queries, see [Data dashboards overview](/monitor/dashboards/overview/#when-you-need-custom-queries).

## Where custom queries apply

You can use a custom query as either the **window method** or the **aggregation method** (or both) on any time series, stat, or table widget. In the widget configuration panel, select **Custom query** from the method dropdown and enter your MQL pipeline stages.

## Write a custom query

Each custom query is one or more MQL aggregation pipeline stages. Each stage is a JSON object with a single key that is a MongoDB aggregation operator.

For example, a `$group` stage that computes the average temperature per hour:

```json
{
  "$group": {
    "_id": { "$dateTrunc": { "date": "$time_received", "unit": "hour" } },
    "value": { "$avg": "$data.readings.temperature" }
  }
}
```

You can chain multiple stages. Each stage receives the output of the previous stage.

### Supported operators

Custom queries support the following MQL aggregation pipeline stages:

`$addFields`, `$bucket`, `$bucketAuto`, `$collStats`, `$count`, `$densify`, `$documents`, `$facet`, `$fill`, `$geoNear`, `$graphLookup`, `$group`, `$indexStats`, `$limit`, `$listSessions`, `$lookup`, `$match`, `$merge`, `$out`, `$planCacheStats`, `$project`, `$redact`, `$replaceRoot`, `$replaceWith`, `$sample`, `$search`, `$searchMeta`, `$set`, `$setWindowFields`, `$skip`, `$sort`, `$sortByCount`, `$unionWith`, `$unset`, `$unwind`, `$vectorSearch`

For documentation on each operator, see the [MongoDB aggregation pipeline stages reference](https://www.mongodb.com/docs/manual/reference/mql/aggregation-stages/).

### Output format

For **time series** and **stat** widgets, your custom query must produce documents with this structure:

```json
{
  "time": "<timestamp>",
  "value": "<number>",
  "robot_id": "<robot_id>"
}
```

- `time`: a timestamp for the data point
- `value`: the numeric value to display
- `robot_id`: the machine that produced the data (used to distinguish lines in time series graphs)

For **table** widgets, the output can be any structure. Each field in the output document becomes a column.

## Examples

### Rolling hourly average

Compute the average temperature for each hour, per machine:

```json
{
  "$group": {
    "_id": {
      "hour": { "$dateTrunc": { "date": "$time_received", "unit": "hour" } },
      "robot_id": "$robot_id"
    },
    "value": { "$avg": "$data.readings.temperature" }
  }
}
```

```json
{
  "$project": {
    "time": "$_id.hour",
    "robot_id": "$_id.robot_id",
    "value": 1,
    "_id": 0
  }
}
```

### Rate of change

Compute how fast a value is changing by comparing consecutive readings using `$setWindowFields`:

```json
{
  "$setWindowFields": {
    "partitionBy": "$robot_id",
    "sortBy": { "time_received": 1 },
    "output": {
      "prev_value": {
        "$shift": {
          "output": "$data.readings.temperature",
          "by": -1
        }
      },
      "prev_time": {
        "$shift": {
          "output": "$time_received",
          "by": -1
        }
      }
    }
  }
}
```

```json
{
  "$project": {
    "time": "$time_received",
    "robot_id": 1,
    "value": {
      "$divide": [
        { "$subtract": ["$data.readings.temperature", "$prev_value"] },
        {
          "$divide": [{ "$subtract": ["$time_received", "$prev_time"] }, 1000]
        }
      ]
    }
  }
}
```

### Table with derived columns

For a table widget, compute temperature in both Celsius and Fahrenheit:

```json
{
  "$project": {
    "Time": "$time_received",
    "Celsius": "$data.readings.temperature",
    "Fahrenheit": {
      "$add": [{ "$multiply": ["$data.readings.temperature", 1.8] }, 32]
    },
    "Humidity": "$data.readings.humidity"
  }
}
```
