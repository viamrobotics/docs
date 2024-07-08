<!-- preserve-formatting -->
A `PlanHistoryReq` which contains the following values:
  - `componentName` [(resource.Name)](https://pkg.go.dev/go.viam.com/rdk/resource#Name): The `resource.Name` of the base to stop.
  - `lastPlanOnly` [(bool)](https://pkg.go.dev/builtin#bool): If `true`, the response will only return the the last plan for the component / execution
  - `executionID` [(ExecutionID)](https://pkg.go.dev/go.viam.com/rdk/services/motion#PlanHistoryReq): If non empty, the response will return the plans of the provided execution & component. Useful for retrieving plans from executions before the current execution.
  - `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.
