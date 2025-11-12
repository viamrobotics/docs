Execute model-specific commands that are not otherwise defined by the component API.
Most models do not implement `DoCommand`.
Any available model-specific commands should be covered in the model's documentation.
If you are implementing your own arm and want to add features that have no corresponding built-in API method, you can implement them with [`DoCommand`](/dev/reference/sdks/docommand/).
