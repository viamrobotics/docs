Method Name | Description
----------- | -----------
[`SafetyMonitor`](/program/apis/sessions/#safetymonitor) | Signal to the session that the given target resource should be safety monitored so that if the session ends and this session was the last to monitor the target, it will attempt to be stopped.
[`SafetyMonitorResourceName`](/program/apis/sessions/#safetymonitorresourcename) | Signal to the session that the given target resource attached to this resource name should be safety monitored so that if the session ends and this session was the last to monitor the target, it will attempt to be stopped.
[`ToContext`](/program/apis/sessions/#tocontext) | Attach a session to the given context.