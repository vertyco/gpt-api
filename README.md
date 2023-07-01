# API for GPT4All (Getting Started)

![Platform](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)
![Ubuntu package](https://img.shields.io/ubuntu/v/Linux/22.04?style=for-the-badge&color=red)

![Py](https://img.shields.io/badge/python-v3.11-orange?style=for-the-badge)
![black](https://img.shields.io/badge/style-black-000000?style=for-the-badge&?link=https://github.com/psf/black)

![license](https://img.shields.io/github/license/Vertyco/Vrt-Cogs?style=for-the-badge)
![GitHub repo size](https://img.shields.io/github/repo-size/Vertyco/gpt-api?color=blueviolet&style=for-the-badge)

![Forks](https://img.shields.io/github/forks/Vertyco/gpt-api?style=for-the-badge&color=9cf)
![Stars](https://img.shields.io/github/stars/Vertyco/gpt-api?style=for-the-badge&color=yellow)
![Lines of code](https://img.shields.io/tokei/lines/github/Vertyco/gpt-api?color=ff69b4&label=Lines&style=for-the-badge)

## Deploying as a service (Ubuntu 22.04)

_Run the following commands to get the api up and running on your server_

### Upgrade and update Ubuntu to the latest version

```
sudo apt update && sudo apt upgrade -y
```

### Upgrade and update Ubuntu to the latest version

```
sudo apt install wget build-essential libncursesw5-dev libssl-dev \
libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev git
```

### Download python 3.11

```
sudo add-apt-repository ppa:deadsnakes/ppa
```

### Install

```
sudo apt install python3.11 python3.11-dev python3.11-venv
```

### Clone The Repo

```
git clone https://github.com/vertyco/gpt-api.git
```

### Create/Activate Virtual Environment

```
cd gpt-api

python3.11 -m venv env

source env/bin/activate
```

### Install requirements

```
pip install -U pip

pip install -r requirements.txt
```

### Configure `.env` File

```
sudo nano .env
```

- Paste the following

```
SENTRY_DSN =
LOGS_PATH =
MODEL_NAME = orca-mini-3b.ggmlv3.q4_0.bin
MODEL_PATH =
THREADS =
EMBED_MODEL = all-MiniLM-L12-v2
LOW_MEMORY = 0
```

- Press `CTRL + O` to save, then `CRTL + X` to close out

### Setup Service File

```
sudo nano /etc/systemd/system/gptapi.service
```

- Paste the following.
- Change `username` to your username
- Set `workers` to however many you want
- To open up the api to external connections, change `--host localhost` to `--host 0.0.0.0`

```
[Unit]
Description=%I gptapi
After=multi-user.target
After=network-online.target
Wants=network-online.target

[Service]
ExecStart=/bin/bash -c 'cd /home/username/gpt-api/ && source env/bin/activate && python -m uvicorn  src.api:app --workers 3 --host localhost'
User=username
Group=username
Type=idle
Restart=on-abnormal
RestartSec=15
RestartForceExitStatus=1
TimeoutStopSec=10

[Install]
WantedBy=multi-user.target
```

- Press `CTRL + O` to save, then `CRTL + X` to close out

### Enable/Start Service

```
sudo systemctl daemon-reload

sudo systemctl enable gptapi

sudo systemctl start gptapi
```

# Deploying on Portainer with docker-compose

If using portainer's env variables, use `stack.env` for the `env_file` arg, otherwise specify the path to your env file.

## Pulling from docker images

```yml
version: "3.8"
services:
  api:
    container_name: gpt-api
    image: vertyco/gpt-api:latest
    restart: unless-stopped
    ports:
      - 8100:8100
    env_file:
      - stack.env
```

## Building from repo

The repo's docker-compose file can be used with the `Repository` option in Portainers stack UI which will build the image from source.

# NOTES

- If running on a VM, make sure the output of `cat /proc/cpuinfo | grep avx` is showing the AVX flag for your CPU, if running proxmox, make sure to set CPU type to `host` in the VM's hardware settings

_This API was written for the Assistant cog for Red Discord-Bot_
![Discord](https://img.shields.io/discord/133049272517001216?style=for-the-badge&label=Red%20Discord-Bot&color=red)
