# shortcut manager

Use this job to create shortcuts in desktop and/or start menu allowing the end-user opening QGIS with a profile.

----

## Use it

Sample job configuration in your scenario file:

```yaml
- name: Create shortcuts for profiles
  uses: shortcuts-manager
  with:
    action: create_or_restore
    include:
      - profile: conf_qgis_fr
        label: "QGIS - Conf QGIS FR"
        additional_arguments: "--noversioncheck"
        desktop: false
        start_menu: true
        icon: "qgis_icon.ico"
      - profile: Oslandia
        label: "QGIS - Profil Oslandia"
        additional_arguments: "--noversioncheck"
        desktop: true
        start_menu: true
        icon: "qgis_icon_oslandia.ico"
```

----

## Options

### action

Tell the job what to do with shortcuts:

Possible_values:

- `create`: add shortcut if not set
- `create_or_restore` (_default_): add shortcut if not set and replace eventual existing one
- `remove`: remove shortcut

### include

List of shortcuts to create.  
See below for the suboptions.

#### additional_arguments

Arguments to pass to QGIS executable.

#### desktop

If true, create a desktop shortcut.

#### icon

Filename of the icon to use for the shortcut.

#### label

Text to display on the shortcut.

#### profile

Name of the profile to associate with the shortcut.

#### start_menu

If true, create a desktop in start menu.

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

If the path is not specified into the `profile.json`, the job looks for the default filepath `images/splash.png`. If the file exists, it will be used as shortcut image.

----

## Schema

```{eval-rst}
.. literalinclude:: ../schemas/scenario/jobs/shortcuts-manager.json
  :language: json
```
