# How to dwonload the latest QDT's version

QDT comes with an upgrade command that check if a new version has been released in comparison with the used on, read the changelog and download the newest version: see [command-line usage](../usage/cli.md#upgrade-\(auto-update,-update\)).

Sometimes a system script fits better to usage, use-case or IT policy. We give below an example in PowerShell for Windows.

:::{info}
This script is a sample et might be not adapted to your environment or your IT policy. If you intend to use it in production, take time to review it before. If you improve or fix it, please share it.
:::

```{eval-rst}
.. literalinclude:: ../../scripts/qdt_dowloader.ps1
  :language: powershell
```
