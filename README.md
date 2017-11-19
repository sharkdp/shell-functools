# shell-functools

A collection of functional programming tools for the shell.

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
