# Environment variables manager

Use this job to set/delete environment variables. For example to set a value for a QGIS environment variable or to set a parameter which is used by a plugin.

----

## Compatibility

This job is compatible with:

- Windows: storing environment variables in registry
- Linux (bash): storing environment variables in `~/.profile` for `scope=user` and `/etc/profile.d/qdt` for `scope=system`.

----

## Use it

Sample job configuration in your scenario file:

```yaml
- name: Set environment variables
  uses: manage-env-vars
  with:
    - name: QGIS_GLOBAL_SETTINGS_FILE
      action: "add"
      scope: "user"
      value: "\\SIG\\QGIS\\CONFIG\\qgis_global_settings.ini"
      value_type: path
```

----

## Options

### action

Tell the job what to do with the environment variable:

Possible_values:

- `add`: add environment variable
- `remove`: remove environment variable

### name

Name of the environment variable.

### scope

Level of the environment variable.

Possible_values:

- `system`: environment variable is set at system level. QDT needs to be run as administrator.
- `user`: environment variable is set at user level. Default value.

### value

Value to set to the environment variable.

### value_type

Value type to avoid ambiguity.

Possible_values:

- `bool`: a boolean (True, true, False, false, 0, 1)
- `path`: a valid local path (user and variables expansion are supported)
- `str`: a raw and simple string. Default value.
- `url`: an HTTP/S URL
