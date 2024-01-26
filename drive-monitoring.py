#!/usr/bin/env python3

import os
import yaml
import asyncio
from asyncua import Server
from asyncua import ua
from yaml.loader import SafeLoader

async def main():
	# Import Settings
	settings_file = open('/etc/opcua/monitoring/drives/settings.yaml')
	settings_data = yaml.load(settings_file, Loader=SafeLoader)

	# Define Server
	host = str(settings_data['host'])
	port = str(settings_data.get('port',4840))
	url = "opc.tcp://"+host+":"+port
	server = Server()
	await server.init()
	server.set_endpoint(url)
	print("Starting server at: "+url)

	# Define Root Folder
	root = await server.nodes.objects.add_folder(0,"Remote Servers")

	# Define Namespace Objects & Variables
	remote_hosts = settings_data['remote_hosts']
	for name, obj in remote_hosts.items():
		# Define Namespace Object
		name_obj = await root.add_folder(0, name)
		
		# Define Variables
		variables = []
		drives = obj['drives']
		for drive in drives:
			variable_name = drive.split('/')[-1] + "-status"
			variable_address = "ns=0;s="+"/"+name+"/"+variable_name
			variable = await name_obj.add_variable(ua.NodeId.from_string(variable_address), variable_name, False)
			await variable.set_writable()
			variables.append(variable)
		remote_hosts[name]['variables'] = variables

	# Start Server
	print("Server has started...")
	async with server:
		# Poll for Variables
		while True:
			# Loop Through Remote Hosts
			for name, obj in remote_hosts.items():
				address	= obj['address']
				drives = obj['drives']
				variables = obj['variables']
				
				print("Target Host: "+name+"...")
				
				# Loop Through Drives
				for i in range(len(drives)):
										
					# Define Command
					command = "ssh root@"+str(address)+" 'smartctl -a " + drives[i] +" | grep PASSED'"

					# Run Command & Read Output
					command_output = os.popen(command)
					command_output = command_output.read()

					# If 'PASSED' is in the line the drive test passed.
					if "PASSED" in command_output:
						command_output = "PASSED"
						await variables[i].set_value(True) 
					# Otherwise, the drive test did not pass.
					else:
						command_output = "FAILED"
						await variables[i].set_value(False)

			# Sleep for 60 seconds
			await asyncio.sleep(60)

if __name__ == '__main__':
	asyncio.run(main())