# shell-functools

*A collection of functional programming tools for the shell.*

This project provides higher order functions like `map` and `filter` as simple command-line tools.
Following the UNIX philosophy, these commands are designed to be composed via pipes. A large
collection of functions such as `basename`, `replace`, `contains` or `is_dir` are provided as
arguments to these commands.

## Demo

<a href="https://asciinema.org/a/6zsp3hEPpM7tmWHrjThl7idqh" target="_blank"><img src="https://asciinema.org/a/6zsp3hEPpM7tmWHrjThl7idqh.png" width="600" /></a>

## Examples

Assume we have the following directory contents:
``` bash
> tree
.
├── deeply
│   ├── nested
│   │   └── directory
│   │       └── song.mp3
│   └── portrait.jpg
├── doc_symlink.txt -> doc.txt
├── doc.txt
└── image.jpg

3 directories, 5 files
```

Basic usage of `map` and `filter`:
``` bash
> find | filter is_file | map basename
doc.txt
doc_symlink.txt
portrait.jpg
song.mp3
image.jpg
```

Get the login shell of user `shark`:
``` bash
> cat /etc/passwd | map split : | filter -c1 equal shark | map index 6
/usr/bin/zsh
```

Basic usage of `foldl`:
``` bash
> seq 100 | foldl add 0
5050

> seq 10 | foldl mul 1
3628800
```

Working with two arguments:
```
> find -name '*.jpg' | map duplicate | map -c2 basename | map -c2 prepend "thumb_" | map run convert
Running 'convert' with arguments ['./deeply/portrait.jpg', 'thumb_portrait.jpg']
Running 'convert' with arguments ['./image.jpg', 'thumb_image.jpg']
```
