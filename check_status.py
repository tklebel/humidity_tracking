# This file checks whether all processes are running and alerts otherwise

import subprocess
import re  

result = subprocess.run('ps aux | grep python', shell=True, stdout=subprocess.PIPE)
result_decoded = result.stdout.decode('utf-8')

# print(result_decoded)

def check_status(filename):
	res = re.findall(filename, result_decoded)

	if res:
		print(filename + ' is running.')
	else: 
		print(filename + ' is not running.')


for file in ['read_sensor.py', 'bot.py', 'display_humidity.py']:
	check_status(file)