import requests
import re
import argparse
from tabulate import tabulate
from termcolor import colored

print("[+] Description:")
data = [
    ('Name', colored('PHPInfo Insecure Configurations Checker', 'magenta')),
    ('Description', colored('This tool uses regular expressions to search for potentially insecure configurations in the PHP info page.', 'yellow')),
]

# Print the description table
print(tabulate(data, headers=['Attribute', 'Value'], tablefmt='grid'))
print("\n")

def check_phpinfo(url):
    # Send a GET request to the PHP info URL
	response = requests.get(url, verify=False)
	html = response.text
	print("[+] Insecure configurations:")
    # Use regular expressions to search for potentially insecure configurations
	insecure_configs = [
        'expose_php',
        'allow_url_fopen',
        'allow_url_include',
        'display_errors',
        'log_errors',
        'register_globals',
        'session.use_trans_sid',
        'magic_quotes_gpc'
	]

    # Check if any of the insecure configurations are enabled
	insecure_configs_data = []
	for config in insecure_configs:
		pattern = f'<tr><td class="e">{config}</td><td class="v">On</td>'
		if re.search(pattern, html):
			insecure_configs_data.append((config, colored('On', 'red')))
		else:
			insecure_configs_data.append((config, colored('Off', 'green')))

    # Print the insecure configurations in a table
	print(tabulate(insecure_configs_data, headers=['Configuration', 'Status'], tablefmt='grid'))
	
parser = argparse.ArgumentParser()
parser.add_argument('url', help='The URL of the PHP info page')
args = parser.parse_args()
url = args.url

check_phpinfo(url)
