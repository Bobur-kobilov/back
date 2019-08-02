## Setup local development environment on Ubuntu 16.04

### Download source

```sh
git clone https://github.com/syncodax/syncodax-bcoffice-back.git
cd syncodax-bcoffice-back
git checkout dev    
```

### [Install Python 3.6](https://askubuntu.com/a/865569)

```sh
sudo add-apt-repository ppa:jonathonf/python-3.6
sudo apt-get update
sudo apt-get install python3.6
sudo apt-get install python3.6-dev
```

### Install Virtualenv and requirements

```sh
virtualenv -p /usr/bin/python3.6 ~/virtualenvs/sbb
source ~/virtualenvs/sbb/bin/activate
pip install -r requirements/local.txt
```

### Run Django server

```sh
cd bcoffice
./manage.py runserver 0.0.0.0:8000 --settings=bcoffice.settings.local
```

### [Configure debugger in VS Code](https://code.visualstudio.com/docs/python/tutorial-django)

1. In VS Code, open the Command Palette (**View > Command Palette** or (```Ctrl+Shift+P```)). Then select the ```Python: Select Interpreter``` command.
2. Select `~/virtualenvs/sbb`
3. [Create a debugger launch profile](https://code.visualstudio.com/docs/python/tutorial-django#_create-a-debugger-launch-profile)
4. Set `launch.json` as follows

```javascript
{
    "name": "Python: Django",
    "type": "python",
    "request": "launch",
    "program": "${workspaceFolder}/bcoffice/manage.py",
    "console": "integratedTerminal",
    "args": [
        "runserver",
        "0.0.0.0:8000",
        "--noreload",
        "--settings=bcoffice.settings.local"
    ],
    "django": true
}
```