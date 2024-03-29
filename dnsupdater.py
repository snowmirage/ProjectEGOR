# Edit /conf/config.xml
# then restart service
# configctl dhcpd restart
# python3 is installed
# https://www.reddit.com/r/OPNsenseFirewall/comments/fnowyw/question_how_to_create_a_custom_cron_jobcommand/
# https://docs.opnsense.org/development/backend/configd.html

# Create a file called actions_localdnscheck.conf
# in
# /usr/local/opnsense/service/conf/actions.d/

# with this in that file

# [test]
# command:/usr/local/bin/python3 /usr/local/opnsense/scripts/localdnscheck/localdnscheck.py
# description: local dns check and dhcp config DNS update
# parameters:
# type:script_output
# message:executing dnsswitcher

# put this script in /usr/local/opensense/scripts/localdnscheck/localdnscheck.py

import subprocess

opnsense_config_file = "/conf/config.xml"
local_dns_ip_address = "10.2.0.66"
backup_dns_ip_address = "1.0.0.1"


def replace_string_in_file(file_path, old_string, new_string):
    try:
        # Read the content of the file
        with open(file_path, "r") as file:
            file_content = file.read()

        # Replace the old string with the new string
        modified_content = file_content.replace(old_string, new_string)

        # Write the modified content back to the file
        with open(file_path, "w") as file:
            file.write(modified_content)

        print(f"String {old_string} replaced with {new_string} in the file: {file_path}")

    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
    except Exception as e:
        print(f"Error: {e}")


def string_exists_in_file(file_path, search_string):
    try:
        # Open the file and read its contents
        with open(file_path, "r") as file:
            file_content = file.read()

        # Check if the search string exists in the file content
        if search_string in file_content:
            return True
        else:
            return False

    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
    except Exception as e:
        print(f"Error: {e}")


def ping_host(ip_address):
    try:
        # Run the ping command
        result = subprocess.run(["ping", "-c", "4", ip_address], capture_output=True, text=True)

        # Check if the ping was successful
        if result.returncode == 0:
            print(f"Host {ip_address} is reachable.\n{result.stdout}")
            return True
        else:
            print(f"Failed to ping host {ip_address}.\n{result.stderr}")
            return False

    except Exception as e:
        return f"Error: {e}"


def execute_linux_command(command):
    try:
        # Execute the command
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        # Check if the command executed successfully
        if result.returncode == 0:
            return result.stdout
        else:
            return result.stderr
    except Exception as e:
        return f"Error: {e}"


def main():
    is_restart_of_dns_service_needed = False

    print(f"Checking if local dns {local_dns_ip_address} is up")
    if ping_host(local_dns_ip_address):
        print(f"Local DNS {local_dns_ip_address} is up")
        # if we can ping our local DNS server
        # See if it is already set as the DNS server where appropriate in our config file
        if string_exists_in_file(opnsense_config_file, f"<dnsserver>{local_dns_ip_address}</dnsserver>"):
            print(f"Local DNS server {local_dns_ip_address} appears to already be configured exiting.")
            # Then we don"t need to take any action
            is_restart_of_dns_service_needed = False
            exit()
        else:
            # Then we should change the config
            print(
                f"Updating config to replace backup dns IP {backup_dns_ip_address} with local dns IP {local_dns_ip_address}")
            replace_string_in_file(opnsense_config_file, f"<dnsserver>{backup_dns_ip_address}</dnsserver>",
                                   f"<dnsserver>{local_dns_ip_address}</dnsserver>")
            is_restart_of_dns_service_needed = True
    else:
        print(f"Local DNS {local_dns_ip_address} is down")
        # if we can NOT ping our local DNS server
        # see if our alternate DNS server is already configured
        if string_exists_in_file(opnsense_config_file, f"<dnsserver>{backup_dns_ip_address}</dnsserver>"):
            print(f"Backup DNS server {backup_dns_ip_address} appears to be already configured")
            # Then we don"t need to take any action
            is_restart_of_dns_service_needed = False
            exit()
        else:
            # Then we should change the config
            print(
                f"Updating config to replace local dns IP {local_dns_ip_address} with backup dns IP {backup_dns_ip_address}")
            replace_string_in_file(opnsense_config_file, f"<dnsserver>{local_dns_ip_address}</dnsserver>",
                                   f"<dnsserver>{backup_dns_ip_address}</dnsserver>")
            is_restart_of_dns_service_needed = True

    if is_restart_of_dns_service_needed:
        print("Restarting the dhcpd service due to config update")
        execute_linux_command('configctl dhcpd restart')
        print("Restart command issued exiting.")


main()