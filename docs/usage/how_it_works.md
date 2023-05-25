# How does it works: concepts and global workflow

## Concepts

To run the workflow properly, you will need 3 items:

| QGIS profiles | A scenario | The QDT executable |
| -- | -- | -- |
| ![icon profiles](/static/icon_profiles.svg) | ![icon scenario](/static/icon_scenario.svg) | ![icon QDT](/static/logo_qdt.png) |

### QGIS profiles

> TO DOC

### Scenarios

Clearly inspired from Ansible and CI/CD platforms (especially GitLab CI, GitHub Actions), QDT uses scenario (YAML files) organised in sections, the main one allowing to define the tasks (called jobs) to be performed for the deployment.

```{button-link} ./scenario.html
:color: primary
:shadow:
:expand:

Write your scenario
```

----

## Functional workflow

### Typical roles

- GIS administrator: in charge of editing QGIS profiles and QDT scenarios
- IT team: in charge of automating the QDT execution with its favourite tool
- End-user: in charge of clicking on desktop Icons and playing with its favourite GIS software

### Flow chart

List of jobs mentioned here is just an example. Every scenario can adapt its own jobs to apply.

```{mermaid}
flowchart TB
    A1 --> | push | G1
    A2 --> It
    It ---> | send or deploy | Enduser
    E1 --> E2 --> E3 --> E4 --> E5 --> E6 --> E7
    E5 <--> | clone/pull profiles | G1
    E6 <--> | download | Plugins

    subgraph Org[Organization]
        direction LR
        subgraph It[IT Team]
            I1{{fa:fa-cog Deploy tools:<br>SCCM, GPO, remote script...}}
        end
        subgraph Admin[QGIS Administrator]
            A1(fa:fa-pen Edit profile.json files)
            A2(fa:fa-pen Edit scenario.qdt.yml)
        end
        subgraph Enduser[End-user computer]
            E1[QDT executable + scenario.qdt.yml]
            E2{RUN<br>cron / manual double-click}
            E3[Read scenario]
            E3>Set persistent environment variables]
            E5>Sync local profiles from repo]
            E6>Download and install plugins locally]
            E7>Create shortcuts to profiles]
        end
    end

    subgraph Git[Git repository]
        direction LR
        G1([fa:fa-git https://git.myorg.net/qgis/profiles.git])
    end

    subgraph Plugins[Plugins repositories]
        direction LR
        P1(["Official <br>plugins.qgis.org"])
        P2(["Custom <br>plugins.myorg.net"])
    end


    subgraph Legend
      direction LR
      L1>a QDT job]
      L2(["A website accessible through HTTP"])
    end
```
