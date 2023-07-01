# GPTAPI

GPT API for the Assistant cog or other uses

# Deploying as a service

To deply as a service, pull the repo and copy `example.env` to `.env` and edit to your liking.

1. `sudo nano /etc/systemd/system/gptapi.service`

2.

```
[Unit]
Description=%I gptapi
After=multi-user.target
After=network-online.target
Wants=network-online.target

[Service]
ExecStart=/bin/bash -c 'cd /home/username/GPTAPI/ && source env/bin/activate && python -m uvicorn  src.api:app --workers 3'
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

3. `sudo systemctl daemon-reload`
4. `sudo systemctl enable gptapi`
5. `sudo systemctl start gptapi`
   <br/>to check status<br/>
6. `sudo systemctl status gptapi`

<br/>

# Deploying with docker-compose on portainer

If using portainer's env variables, use `stack.env` for the `env_file` arg, otherwise specify the path to your env file

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

# If running on a VM

- Make sure the output of `cat /proc/cpuinfo | grep avx` is showing the AVX flag for your CPU, if running proxmox, make sure to set CPU type to `host` in the VM's hardware settings
