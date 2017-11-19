# shell-functools

A collection of functional programming tools for the shell.

## Examples

Assume we have the following directory contents:
``` bash
> tree
.
├── deeply
│   └── nested
│       └── directory
│           └── song.mp3
├── image.jpg
└── doc.txt

3 directories, 3 files
```

Basic usage of `map` and `filter`:
``` bash

> find | filter is_file | map basename
song.mp3
doc.txt
image.jpg
```

Operations on integers:
``` bash
> seq 1 3 | map add 10
11
12
13
```
