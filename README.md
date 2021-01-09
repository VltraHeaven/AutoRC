# AutoRC

Automated Browser-driven RingCentral Account Management

## Dependenciens
---
- [Python3](https://www.python.org/downloads/)
- [Helium](https://github.com/mherrmann/selenium-python-helium)
- [Selenium](https://selenium-python.readthedocs.io/)
- [Chrome](https://www.google.com/chrome/)/[Chromium](https://download-chromium.appspot.com/)
- [Chrome Web Driver](https://chromedriver.chromium.org/)

## Setup
---
Run from within the project folder/directory...

```
python -m pip -r requirements.txt
```

## Usage
---

This program pulls it's user data from a list of users in a `.csv` that contains the following case-sensitive headers
```
givenName,surname,name,emailAddress,Title 
```

To assigning extensions to the users listed in a `.csv`

```
python ./autorc.py --assign [file]
```

Removing extensions from the users listed in a `.csv`

```
python ./autorc.py --remove [file]
```

A Chrome browser window will open, browse to the RingCentral Single Sign-On page and wait until sign in is successful. Once the admin panel is visible it will continue automatically.

Help
```
python ./autorc.py -h

usage: Usage: .\autorc.py [-h] [-a | -r] [file]

Description: Automatically assign or remove RingCentral extensions.

positional arguments:
  file          Path to the userlist .csv file. The .csv must at least have the following case-sensitive headers: givenName,surname,name,emailAddress,Title

optional arguments:
  -h, --help    show this help message and exit
  -a, --assign  Assign RingCentral extensions
  -r, --remove  Remove RingCentral extension assignments
```