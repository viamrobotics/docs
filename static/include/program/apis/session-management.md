Method Name | Description
----------- | -----------
[`SafetyMonitor`](/program/apis/sessions/#safetymonitor) | Safety monitor this target {{< glossary_tooltip term_id="resource" text="resource" >}} so that if this session ends as the last session to monitor it, the `SessionManager` attempts to stop the resource by calling the `Stop()` method of the resource API.
[`SafetyMonitorResourceName`](/program/apis/sessions/#safetymonitorresourcename) | Safety monitor this target {{< glossary_tooltip term_id="resource" text="resource" >}} so that if this session ends as the last session to monitor it, the `SessionManager` attempts to stop the resource by calling the `Stop()` method of the resource API.
[`ToContext`](/program/apis/sessions/#tocontext) | Attach a session to the given context.