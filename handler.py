import netmiko
import logging
from netmiko import ConnectHandler

# Define device parameters
Drouter1 = {
    'device_type': 'cisco_ios',
    'ip': '192.168.10.10',  
    'username': 'denis',
    'password': 'pass11',
}

Drouter2 = {
    'device_type': 'cisco_ios',
    'ip': '192.168.10.20',  
    'username': 'denis',
    'password': 'pass11',
}

try:
    # Connect to the device
    net_connect1 = ConnectHandler(**Drouter1)
    net_connect2 = ConnectHandler(**Drouter2)
    print("Connected successfully.")

    # Send a command to verify connectivity
    output = net_connect1.send_command("show ip interface brief")
    print(output)
    output = net_connect2.send_command("show ip interface brief")
    print(output)

    #Send interface config Command
    #For Drouter1
    config_commands1 = [
    'interface GigabitEthernet1/0',
    'ip address 10.10.10.1 255.255.255.0',
    'no shutdown'
    ]
    output = net_connect1.send_config_set(config_commands1)
    
    #For Drouter2
    config_commands2 = [
    'interface GigabitEthernet2/0',
    'ip address 10.10.10.2 255.255.255.0',
    'no shutdown'
    ]
    output = net_connect2.send_config_set(config_commands2)

    #Verify Gig Interface Setup
    output = net_connect1.send_command('show running-config interface GigabitEthernet1/0')
    print(output)
    output = net_connect2.send_command('show running-config interface GigabitEthernet2/0')
    print(output)

    output = net_connect1.send_command("show ip interface brief")
    print(output)
    output = net_connect2.send_command("show ip interface brief")
    print(output)

    #Routine Task (copy run start)
    output = net_connect1.send_command('show running-config')
    with open('backup_config1.txt', 'w') as f:
        f.write(output)

    output = net_connect2.send_command('show running-config')
    with open('backup_config2.txt', 'w') as f:
        f.write(output)

    #Configuring Logging
    logging.basicConfig(filename='automation_operations.log', level=logging.DEBUG)
    logger = logging.getLogger("netmiko")
    logger.debug("Has Connected to the Device")

    # Disconnect from the device
    net_connect1.disconnect()
    print("Disconnected successfully.")
    net_connect2.disconnect()
    print("Disconnected successfully.")

except ConnectionError as e1:
    logger.error('ConnectionError: ' + str(e1))

except Exception as e2:
    print("Error:", str(e2))

