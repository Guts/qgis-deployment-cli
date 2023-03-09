# Splash screen manager

Use this job to set your custom splash screen image.

----

## Use it

Sample job configuration in your scenario file:

```yaml
- name: Set splash screen
  uses: splash-screen-manager
  with:
    action: create_or_restore
    strict: true
```

----

## Options

### action

Tell the job what to do with splash screens:

Possible_values:

- `create`: add splash screen if not set
- `create_or_restore`: add splash screen if not set and replace eventual existing one
- `remove`: remove splash screen

### strict

Check image size against QGIS recomendations: 600x300.

Possible values:

- `true`: fail if the image dimensions does not comply with QGIS recomendations.
- `false`: do not fail if the image dimensions does not comply with QGIS recomendations. A warning is logged.

----

## How does it work

### Specify the file to use in the `profile.json`

Add the image file to the profile folder and specify the relative filepath under the `splash` attribute:

```json
{
    [...]
    "email": "qgis@oslandia.com",
    "icon": "images/qgis_icon.ico",
    "splash": "images/splash_qgis-fr_600x287.png",
    [...]
}
```

### Store the image file under the default path

If the path is not specified into the `profile.json`, the job looks for the default filepath `images/splash.png`. If the file exists, it will be used as splash screen image

----

## Schema

```{eval-rst}
.. literalinclude:: ../schemas/scenario/jobs/splash-screen-manager.json
  :language: json
```
