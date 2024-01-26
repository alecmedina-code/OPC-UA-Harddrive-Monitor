# OPC-UA Harddrive Monitor
The OPC-UA hardrive monitor is used to monitor harddrive states on remote machines. The service will create a OPC-UA server using asynua, monitor drives based on settings.yaml then provide the states as OPC-UA variables. The states are true/false boolean values based on if the drive passed the S.M.A.R.T drive assessment.
## Files
- drive-monitoring.py
- settings.yaml
- opcua-drive-monitor.service

## Install requirements
### Modules
- asynua
```
pip install asynua
```

### Files
The code should be placed in the following directories:

|#| File                        | Location                          | Dependent Files |
|-|-----------------------------|-----------------------------------|-----------------|
|1| drive-monitorying.py        | /usr/lib/opcua/monitoring/drives/ | 3               |
|2| settings.yaml               | /etc/opcua/monitoring/drives      | 1               |
|3| opcua-drive-monitor.service | /etc/systemd/system               | N/A             |

Feel free to change the locations of `drive-monitoring.py` or `settings.yaml`. If you change either you need to update date the dependent files with the correct path.

## Settings
The settings file has the following variables:
- host (**Required**: IP address of machine running the code.)
- port (**Optional**: Default 4840.)
- remote_hosts (**Required**: Dictionary of remote host to monitor.)

The remote_hosts variable should have the following format:
```
remote_hosts:
    name-1:
        host: <ip address of remote host>
        drives: [drive1, drive2, ...]
```

## Run
To run the service enter the following commands:
```
sudo systemctl enable opcua-drive-monitor.service
sudo systemctl start opcua-drive-monitor.service
```

You should now be able to connect to the OPC-UA server at `opc.tcp://192.168.1.1:4840`. Be sure to substitute your IP and port.