# pwordg
Password generator with emphasis on word.

## Background

Many organizations require their users to change passwords regurarly. This requirement
has the back-side that users tend to stick to a basic password and only increase 
a counter at the end of the password, thereby "fooling" the system requirement and
allowing them to keep their favourite password. 

I beleive a remedy to this flaw is to generate passwords that are easy to remember.
This will naturally decrease the randomness of the password, but in practice, it will
be more random that the counter approach.

I've used the linux tool [pwgen](https://github.com/tytso/pwgen) for a long time
to generate "easy to rembember" passwords. I realized that I preferred the generated
passwords that contained words over the more random suggestions. Then I got the idea
to generate paswords from a word list, thereby ensuring that the generated password
indeed came from a real word.

To maintain some sort of security in the password, I decided to ditch the idea of a
fixed-length password. Instead, a minimum lenght would be sufficient. Also, special
characters and numbers should be included, as that is a requirement by many organizations.

# Getting started

## Python
This project is written in [Python](https://www.python.org/), so you'll need to install
a python environment. The package depends on the _requests_ package, which is available 
to install using _pip.
```
$ python3 -m pip install requests
```

## Download pwordg
Clone the repository using git or simply download [pwordg.py](pwordg.py) to a suitable
folder.

# License
Pword is licensed under the GNU General Public License v 3.0 
(see [LICENSE.txt](license.txt) for details).

The source code allows for downloading word lists from https://github.com/dwyl/english-words,
which in turn sourced the word list from https://web.archive.org/web/20131118073324/http://www.infochimps.com/datasets/word-list-350000-simple-english-words-excel-readable (archived). Copyright to the word list
belongs to them.