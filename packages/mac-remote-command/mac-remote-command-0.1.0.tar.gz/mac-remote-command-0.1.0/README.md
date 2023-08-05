# mac-remote-command
Client for embedded systems to facilitate remote configuration.

MAC Remote Command facilitates the configuration of embedded remote and local systems by connecting to an remote web service.  A reference implementation is available and free to use at [https://mac-commander.deta.dev/](https://mac-commander.deta.dev/).  The source code for the web service is available on GitHub at [FlantasticDan/mac-commander](https://github.com/FlantasticDan/mac-commander).  MAC Remote Command optionally includes support to display it's detect Local IP and MAC Address via an [OLED Status Display](https://github.com/FlantasticDan/oled-status).

## Installation
For standard use:
```bash
pip install mac-remote-command
```

For optional use with an OLED Status Display:
```bash
pip install mac-remote-command[oled]
```
**Note** OLED Status Display is only compatiable on Linux devices with an I<sup>2</sup>C bus.

## Use
Currently the remote command functionality of the package is undeveloped.  Right now it only offers a pinging service to publically broadcast it's local and public IP address as referenced by it's MAC Address:
```bash
python -m mac_remote.ping
```

### Starting Remote Ping On Boot (Ubuntu)
Linux allows Python modules to be executed as part of a startup service.  These instructions assume MAC Remote Command is installed in a virtual environment.
1. Create a `start-mac-remote-ping.sh` script which activates the virtual environment and then starts the MAC Remote Command:
```bash
#!/bin/bash
cd <directory>
. venv/bin/activate
python -m mac_remote.ping
```
2. Modify the script so it is executable: `sudo chmod x+ start-mac-remote-ping.sh`
3. Create a service the run the script at startup by writing the following file at `/etc/systemd/system/mac-remote-ping.service`:
```
[Unit]
Description=MAC Remote Command Pinger
After=network.target
StartLimitIntervalSec=0

[Service]
Type=simple
Restart=always
RestartSec=1
User=<username>
ExecStart=/path/to/start-mac-remote-ping.sh

[Install]
WantedBy=multi-user.target
```
4. Enable the startup service: `systemctl enable mac-remote-ping`
5. Reboot