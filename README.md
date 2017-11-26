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

## Documentation and examples

### Usage of `map`

The `map` command takes a [function argument](#available-function-arguments) and applies it to every line of input:
``` bash
> ls
document.txt
folder
image.jpg

> ls | map abspath
/tmp/demo/document.txt
/tmp/demo/folder
/tmp/demo/image.jpg
```

### Usage of `foldl`

The `foldl` command takes a [function argument](#available-function-arguments) and an initial value. The given function must be a binary function with two arguments, like `add` or `append`. The `foldl` command then applies this function iteratively by keeping an internal accumulator:

Add up the numbers from 0 to 100:
``` bash
> seq 100 | foldl add 0
5050
```

Multiply the numbers from 1 to 10:
``` bash
> seq 10 | foldl mul 1
3628800
```

Append the numbers from 1 to 10 in a string:
``` bash
> seq 1 10 | map append " " | foldl append ""
1 2 3 4 5 6 7 8 9 10 
```

### Advanced examples

Get the login shell of user `shark`:
``` bash
> cat /etc/passwd | map split : | filter -c1 equal shark | map index 6
/usr/bin/zsh
```

Working with columns:
``` bash
> find -name '*.jpg' 
./folder/me.jpg
./image.jpg
                                                                                   
> find -name '*.jpg' | map duplicate
./folder/me.jpg   ./folder/me.jpg
./image.jpg       ./image.jpg
                                                                                   
> find -name '*.jpg' | map duplicate | map -c2 basename
./folder/me.jpg   me.jpg
./image.jpg       image.jpg
                                                                                   
> find -name '*.jpg' | map duplicate | map -c2 basename | map -c2 prepend "thumb_"
./folder/me.jpg	  thumb_me.jpg
./image.jpg       thumb_image.jpg
                                                                                   
> find -name '*.jpg' | map duplicate | map -c2 basename | map -c2 prepend "thumb_" | map run convert
Running 'convert' with arguments ['./folder/me.jpg', 'thumb_me.jpg']
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
