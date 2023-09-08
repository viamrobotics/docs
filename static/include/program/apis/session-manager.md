Method Name | Description
----------- | -----------
[`Start`](/program/apis/sessions/#start) | Create a new session that expects at least one heartbeat within the configured window.
[`All`](/program/apis/sessions/#all) | Get all active sessions.
[`FindByID`](/program/apis/sessions/#findbyid) | Find a session by the given ID. If found, trigger a heartbeat and extend the lifetime of the session.
[`AssociateResource`](/program/apis/sessions/#associateresource) | Associate a session ID to a monitored resource. All associated resources will be stopped with this session is expired.
[`Close`](/program/apis/sessions/#close) | Stop the session manager without directing any sessions to expire.
[`expireLoop`](/program/apis/sessions/#expireloop) | Set an expiration loop to be associated with a specific context.
