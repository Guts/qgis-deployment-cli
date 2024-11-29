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

![QGIS UI - QDT demo profile](https://github.com/qgis-deployment/qgis-deployment-toolbelt-cli/blob/main/docs/static/examples_profiles_qdt-demo_qgis_ui.png?raw=true)

Splash screen:

![QGIS splash screen - QDT demo profile](./profiles/demo/images/splash.png)

As QDT developer, you might want to launch QGIS with this profile to edit or check it:

```sh
qgis --profile "demo" --profiles-path examples/
```

----

## Viewer Mode

![QGIS splash screen - QDT viewer profile](./profiles/Viewer%20Mode/images/splash.png)

As QDT developer, you might want to launch QGIS with this profile to edit or check it:

```sh
qgis --profile "Viewer Mode" --profiles-path examples/
```

----

## Only Linux

Just an empty profile to demonstrate that you can condition the profile deployment to rules. So:

- if you are running on Linux, you should have a profile called `QDT Only Linux`
- if you are running on Windows, you should not have it!
