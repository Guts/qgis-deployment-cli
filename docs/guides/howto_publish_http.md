# How to publish to an HTTP server

## Generate the `qdt-files.json` index file

> Typically on Ubuntu

Install tree:

```sh
sudo apt install tree
```

Run it:

```sh
# move to your QDT profiles folder. Here we take the QDT repository as example:
cd examples/
# generate the qdt-files.json
tree --gitignore -D --timefmt="%Y-%m-%dT%H:%M:%S%Z" -s -J -o qdt-files.json .
```

Detailed explanation:

- `tree`: command that displays the directory tree structure.
<!-- - `-f`: display the full path for each file and directory. -->
- `--gitignore`: apply gitignore-style rules to exclude files and directories.
- `-D`: print the modification time for each file or directory.
- `--timefmt="%Y-%m-%dT%H:%M:%S%Z"`: specify the time format as ISO8601 with UTC (Coordinated Universal Time).
- `-s`: print the size of each file.
- `-J`: output the directory tree in JSON format.
- `-o qdt-files.json`: save the output to a file named 'qdt-files.json'.
- `.`: specify the current directory as the starting point for the tree.
