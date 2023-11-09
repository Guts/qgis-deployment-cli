# Demonstration profiles to be deployed with QDT

This subfolder contains some QGIS profiles meant to be deployed using QDT.

## demo

Some of customizations to make it recognizable:

- locale is overridden with English/US
- theme is set to _Night Mapping_
- experimental plugins are enabled
- most of the default plugns are disabled except Processing
- at least one plugin is installed: [Profile Manager](https://plugins.qgis.org/plugins/profile-manager/)
- custom icon and splash screen

![QGIS UI - QDT demo profile](https://github.com/Guts/qgis-deployment-cli/blob/main/docs/static/examples_profiles_qdt-demo_qgis_ui.png?raw=true)


Splash screen:

![QGIS splash screen - QDT demo profile](../demo/images/splash.png)

As QDT developer, you might want to launch QGIS with this profile to edit or check it:

```sh
qgis --profile "demo" --profiles-path examples/
```

----

## Viewer Mode

![QGIS splash screen - QDT viewer profile](../Viewer%20Mode/images/splash.png)

As QDT developer, you might want to launch QGIS with this profile to edit or check it:

```sh
qgis --profile "Viewer Mode" --profiles-path examples/
```
