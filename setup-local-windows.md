## Setup local development environment on Windows 10

### Download source

```sh
[powershell]
git clone https://github.com/syncodax/syncodax-bcoffice-back.git
cd syncodax-bcoffice-back
git checkout dev
```

### Install Python 3.6

Download : [Python3.6.8](https://www.python.org/ftp/python/3.6.8/python-3.6.8-amd64.exe)

### Install Virtualenv and requirements

```sh
[powershell]
python -m venv ..\virtualenvs\sbb
..\virtualenvs\sbb\Scripts\activate
pip install -r .\requirements\local.txt
```

### Run Django server

```sh
cd bcoffice
python .\manage.py runserver 0.0.0.0:8000 --settings=bcoffice.settings.local
```
