# shell-functools

[![Unit tests](https://github.com/sharkdp/shell-functools/actions/workflows/ci.yml/badge.svg)](https://github.com/sharkdp/shell-functools/actions/workflows/ci.yml)

*A collection of functional programming tools for the shell.*

This project provides higher order functions like `map`, `filter`, `foldl`, `sort_by` and `take_while` as simple command-line tools.
Following the UNIX philosophy, these commands are designed to be composed via pipes. A
[large collection](#available-function-arguments) of functions such as `basename`, `replace`, `contains` or `is_dir` are provided as
arguments to these commands.

## Contents

* [Demo](#demo)
* [Quick start](#quick-start)
* [Documentation and examples](#documentation-and-examples)
    * [Usage of `map`](#usage-of-map)
    * [Usage of `filter`](#usage-of-filter)
    * [Usage of `foldl`](#usage-of-foldl)
    * [Usage of `foldl1`](#usage-of-foldl1)
    * [Usage of `sort_by`](#usage-of-sort_by)
    * [Chaining commands](#chaining-commands)
    * [Lazy evaluation](#lazy-evaluation)
    * [Working with columns](#working-with-columns)
    * [Available function arguments](#available-function-arguments)

## Demo

<a href="https://asciinema.org/a/6zsp3hEPpM7tmWHrjThl7idqh" target="_blank"><img src="https://asciinema.org/a/6zsp3hEPpM7tmWHrjThl7idqh.png" width="600" /></a>

## Quick start

If you want to try it out on your own, run:
``` bash
pip install shell-functools
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

### Usage of `filter`

The `filter` command takes a [function argument](#available-function-arguments) with a `Bool`ean return type. It applies that function to each input line and shows only those that returned `true`:
``` bash
> find
.
./folder
./folder/me.jpg
./folder/subdirectory
./folder/subdirectory/song.mp3
./document.txt
./image.jpg

> find | filter is_file
./folder/me.jpg
./folder/subdirectory/song.mp3
./document.txt
./image.jpg
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
> seq 10 | map append " " | foldl append ""
1 2 3 4 5 6 7 8 9 10
```

### Usage of `foldl1`

The `foldl1` command is a variant of `foldl` that uses the first input as the initial value.
This can be used to shorten the example above to:
``` bash
> seq 100 | foldl1 add
> seq 10 | foldl1 mul
> seq 10 | map append " " | foldl1 append
```

### Usage of `sort_by`

The `sort_by` command also takes a [function argument](#available-function-arguments). In the
background, it calls the function on each input line and uses the results to sort the *original input*.
Consider the following scenario:
``` bash
> ls
a.mp4  b.tar.gz  c.txt
> ls | map filesize
7674860
126138
2214
```

We can use the `filesize` function to sort the entries by size:
```
> ls | sort_by filesize
c.txt
b.tar.gz
a.mp4
```

### Chaining commands

All of these commands can be composed by using standard UNIX pipes:
``` bash
> find
.
./folder
./folder/me.jpg
./folder/subdirectory
./folder/subdirectory/song.mp3
./document.txt
./image.jpg

> find | filter is_file | map basename | map append ".bak"
me.jpg.bak
song.mp3.bak
document.txt.bak
image.jpg.bak
```

### Lazy evaluation

All commands support lazy evaluation (i.e. they consume input in a streaming way) and never perform
unnecessary work (they exit early if the *output* pipe is closed).

As an example, suppose we want to compute the sum of all odd squares lower than 10000. Assuming we
have a command that prints the numbers from 1 to infinity (use `alias infinity="seq 999999999"` for
an approximation), we can write:
``` bash
> infinity | filter odd | map pow 2 | take_while less_than 10000 | foldl1 add
166650
```

### Working with columns

The `--column` / `-c` option can be used to apply a given function to a certain *column* in the input line (columns are separated by tabs). Column arrays can be created by using functions such as `duplicate`, `split sep` or `split_ext`:

``` bash
> ls | filter is_file | map split_ext
document	txt
image	jpg

> ls | filter is_file | map split_ext | map -c1 to_upper
DOCUMENT	txt
IMAGE	jpg

> ls | filter is_file | map split_ext | map -c1 to_upper | map join .
DOCUMENT.txt
IMAGE.jpg
```

Here is a more complicated example:
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

Get the login shell of user `shark`:
``` bash
> cat /etc/passwd | map split : | filter -c1 equal shark | map index 6
/usr/bin/zsh
```


### Available function arguments

You can call `ft-functions`, to get an overview of all available arguments to `map`, `filter`, etc.:

#### File and Directory operations ####
```
abspath             :: Path   → Path
dirname             :: Path   → Path
basename            :: Path   → Path
is_dir              :: Path   → Bool
is_file             :: Path   → Bool
is_link             :: Path   → Bool
is_executable       :: Path   → Bool
exists              :: Path   → Bool
has_ext ext         :: Path   → Bool
strip_ext           :: Path   → String
replace_ext new_ext :: Path   → Path
split_ext           :: Path   → Array
```
#### Logical operations ####
```
non_empty           :: *      → Bool
nonempty            :: *      → Bool
```
#### Arithmetic operations ####
```
add num             :: Int    → Int
sub num             :: Int    → Int
mul num             :: Int    → Int
even                :: Int    → Bool
odd                 :: Int    → Bool
pow num             :: Int    → Int
```
#### Comparison operations ####
```
eq other            :: *      → Bool
equal other         :: *      → Bool
equals other        :: *      → Bool
ne other            :: *      → Bool
not_equal other     :: *      → Bool
not_equals other    :: *      → Bool
ge i                :: Int    → Bool
greater_equal i     :: Int    → Bool
greater_equals i    :: Int    → Bool
gt i                :: Int    → Bool
greater i           :: Int    → Bool
greater_than i      :: Int    → Bool
le i                :: Int    → Bool
less_equal i        :: Int    → Bool
less_equals i       :: Int    → Bool
lt i                :: Int    → Bool
less i              :: Int    → Bool
less_than i         :: Int    → Bool
```
#### String operations ####
```
reverse             :: String → String
append suffix       :: String → String
strip               :: String → String
substr start end    :: String → String
take count          :: String → String
to_lower            :: String → String
to_upper            :: String → String
replace old new     :: String → String
prepend prefix      :: String → String
capitalize          :: String → String
drop count          :: String → String
duplicate           :: String → Array
contains substring  :: String → Bool
starts_with pattern :: String → Bool
startswith pattern  :: String → Bool
ends_with pattern   :: String → Bool
endswith pattern    :: String → Bool
len                 :: String → Int
length              :: String → Int
format format_str   :: *      → String
```
#### Array operations ####
```
at idx              :: Array  → String
index idx           :: Array  → String
join separator      :: Array  → String
split separator     :: String → Array
reverse             :: Array  → Array
```
#### Other operations ####
```
const value         :: *      → *
run command         :: Array  → !
id                  :: *      → *
identity            :: *      → *
```
