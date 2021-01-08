# AutoRC

Automated Browser-driven RingCentral Account Management

## Dependenciens
- [Python3](https://www.python.org/downloads/)
- [Helium](https://github.com/mherrmann/selenium-python-helium)
- [Selenium](https://selenium-python.readthedocs.io/)
- [Chrome](https://www.google.com/chrome/)/[Chromium](https://download-chromium.appspot.com/)
- [Chrome Web Driver](https://chromedriver.chromium.org/)

## Setup

- Run from within the project folder/directory...

```
python -m pip -r requirements.txt
```

## Usage

- Assign extensions

```
python ./main.py --assign [file]
```

- Remove extensions

```
python ./main.py --remove [file]
```

- Help
```
python ./main.py -h

usage: Usage: .\main.py [-h] [-a | -r] [file]

Description: Automatically assign or remove RingCentral extensions.

positional arguments:
  file          Path to the userlist .csv file. The .csv must at least have the following case-sensitive headers: givenName,surname,name,emailAddress,Title "

optional arguments:
  -h, --help    show this help message and exit
  -a, --assign  Assign RingCentral extensions
  -r, --remove  Remove RingCentral extension assignments
```