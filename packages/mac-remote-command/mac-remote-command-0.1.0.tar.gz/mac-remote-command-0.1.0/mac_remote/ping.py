import time

import httpx

try:
    from oled_status import Status
    OLED = True
except ImportError:
    OLED = False

from . import get_summary

class EndlessPing():
    '''Ping MAC Commander every 30 seconds'''
    def __init__(self, commander_url: str) -> None:
        self.target = commander_url + 'ping'
        if OLED:
            self.ip = Status('Local IP Address', 'Unknown')
            self.mac = Status('MAC Address', 'Unknown')
        while True:
            try:
                payload = get_summary()
                if OLED:
                    self.ip.update(payload['local'])
                    self.mac.update(payload['mac'].upper())
                httpx.post(self.target, json=payload)
            except Exception:
                pass
            time.sleep(30)

if __name__ == '__main__':
    EndlessPing('https://mac-commander.deta.dev/')