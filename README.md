# GPTAPI

GPT API for the Assistant cog or other uses

1. `sudo nano /etc/systemd/system/gptapi.service`

2. ```
   [Unit]
   Description=%I gptapi
   After=multi-user.target
   After=network-online.target
   Wants=network-online.target

   [Service]
   ExecStart=path/to/env/python -O -m uvicorn src.api:app --workers 2
   User=username
   Group=username
   Type=idle
   Restart=on-abnormal
   RestartSec=15
   RestartForceExitStatus=1
   RestartForceExitStatus=26
   TimeoutStopSec=10

   [Install]
   WantedBy=multi-user.target
   ```

3. `sudo systemctl daemon-reload`
4. `sudo systemctl enable gptapi`
5. `sudo systemctl start gptapi`
