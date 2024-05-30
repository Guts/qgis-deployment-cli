# How to publish to an HTTP server

## Generate the `qdt-files.json` index file

> Typically on Ubuntu 22.04

Install tree > 2:

```sh
sudo apt install tree
```

Check version:

```sh
tree --version
```

Run it:

```sh
# move to your QDT profiles folder. Here we take the QDT repository as example:
cd examples/
# generate the qdt-files.json
tree --gitignore -D -J --prune -s --timefmt="%Y-%m-%dT%H:%M:%S%Z" -o qdt-files.json .
```

Detailed explanation:

- `tree`: command that displays the directory tree structure.
<!-- - `-f`: display the full path for each file and directory. -->
- `--gitignore`: apply gitignore-style rules to exclude files and directories.
- `-D`: print the modification time for each file or directory.
- `-J`: output the directory tree in JSON format.
- `--prune`: do not include empty folders
- `-s`: print the size of each file.
- `--timefmt="%Y-%m-%dT%H:%M:%S%Z"`: specify the time format as ISO8601 with UTC (Coordinated Universal Time).
- `-o qdt-files.json`: save the output to a file named 'qdt-files.json'.
- `.`: specify the current directory as the starting point for the tree.
