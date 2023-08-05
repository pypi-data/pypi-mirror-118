import subprocess
from getmac import get_mac_address

def get_interface_from_local_ip(ip_address:str) -> str:
    interfaces = subprocess.run(['ip', '-br', 'address'], stdout=subprocess.PIPE)
    interfaces = interfaces.stdout.decode('utf-8').split('\n')
    for interface in interfaces:
        if ip_address in interface:
            return interface.split(' ')[0]

def get_linux_mac_from_local_ip(ip_address: str) -> str:
    interface = get_interface_from_local_ip(ip_address)
    if interface:
        return get_mac_address(interface)