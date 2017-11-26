# shell-functools

*A collection of functional programming tools for the shell.*

This project provides higher order functions like `map` and `filter` as simple command-line tools.
Following the UNIX philosophy, these commands are designed to be composed via pipes. A
[large collection](#available-function-arguments) of functions such as `basename`, `replace`, `contains` or `is_dir` are provided as
arguments to these commands.

## Demo

<a href="https://asciinema.org/a/6zsp3hEPpM7tmWHrjThl7idqh" target="_blank"><img src="https://asciinema.org/a/6zsp3hEPpM7tmWHrjThl7idqh.png" width="600" /></a>

## Quick start

If you want to try it out on your own, run:
``` bash
git clone https://github.com/sharkdp/shell-functools /tmp/shell-functools
export PATH="$PATH:/tmp/shell-functools/ft"
```

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

## Available function arguments

You can call `ft-functions`, to get an overview of all available arguments to `map`, `filter`, etc.:

```
abspath             :: Path   → Path
add num             :: Int    → Int
append suffix       :: String → String
at idx              :: Array  → String
basename            :: Path   → Path
capitalize          :: String → String
contains substring  :: String → Bool
dirname             :: Path   → Path
drop count          :: String → String
duplicate           :: String → Array
eq other            :: *      → Bool
equal other         :: *      → Bool
equals other        :: *      → Bool
exists              :: Path   → Bool
has_ext ext         :: Path   → Bool
id                  :: *      → *
identity            :: *      → *
index idx           :: Array  → String
is_dir              :: Path   → Bool
is_file             :: Path   → Bool
is_link             :: Path   → Bool
join separator      :: Array  → String
length              :: String → Int
mul num             :: Int    → Int
non_empty           :: *      → Bool
nonempty            :: *      → Bool
prepend prefix      :: String → String
replace old new     :: String → String
replace_ext new_ext :: Path   → Path
run command         :: Array  → !
split separator     :: String → Array
starts_with pattern :: String → Bool
startswith pattern  :: String → Bool
strip               :: String → String
strip_ext           :: Path   → String
substr start end    :: String → String
take count          :: String → String
to_lower            :: String → String
to_upper            :: String → String
```
