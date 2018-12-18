# tap-darkskyapi

A [Singer Tap] Tap to extract currency exchange rate data from the [Dark Sky API](https://darksky.net/dev).

## How to use it

### Install and Run

First, make sure Python 3 is installed on your system or follow these
installation instructions for [Mac] or [Ubuntu].

Then, get an access key from [Dark Sky](https://darksky.net/dev).

Then, convert `config.sample.json` to
`~/singer.io/tap_darkskyapi_config.json`; fill out your parameters.

It's recommended to use a virtualenv:

```bash
python3 -m venv ~/.virtualenvs/tap-darkskyapi
source ~/.virtualenvs/tap-darkskyapi/bin/activate
pip install -U pip setuptools
pip install -e '.'
```

Set up the `target-csv` virtual environment according to the instructions
[here](https://github.com/singer-io/target-csv/blob/master/README.md).
These commands will install `tap-darkskyapi`  with pip, and then run it:

```bash
~/.virtualenvs/tap-darkskyapi/bin/tap-darkskyapi --config \ ~/singer.io/tap_darkskyapi_config.json | target-csv
```

The data will be written to a file called `forecast.csv` in your
working directory.

---

[Singer Tap]: https://singer.io
[Dark Sky API]: https://darksky.net/dev
[Mac]: http://docs.python-guide.org/en/latest/starting/install3/osx/
[Ubuntu]: https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-local-programming-environment-on-ubuntu-16-04
