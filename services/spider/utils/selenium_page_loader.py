from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
import time

class PageLoader(object):
    def __init__(self, driver, timeout=30):
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)

    def is_page_loaded(self):
        """Check if page is fully loaded"""
        return self.driver.execute_script(
            "return document.readyState === 'complete'"
        )

    def wait_for_page_load(self):
        """Wait for page to fully load"""
        try:
            # Wait for document.readyState
            self.wait.until(lambda d: self.is_page_loaded())
            
            # Additional checks for common frameworks
            self.wait_for_jquery()
            self.wait_for_angular()
            self.wait_for_network_idle()
            # bypass as capcha here
            
            time.sleep(2)
            
            return True
        except TimeoutException:
            return False

    def wait_for_jquery(self):
        """Wait for jQuery to finish (if present)"""
        try:
            self.wait.until(
                lambda d: d.execute_script(
                    "return typeof jQuery === 'undefined' || jQuery.active === 0"
                )
            )
        except:
            pass

    def wait_for_angular(self):
        """Wait for Angular to finish (if present)"""
        try:
            self.wait.until(
                lambda d: d.execute_script(
                    "return typeof angular === 'undefined' || angular.element(document).injector().get('$http').pendingRequests.length === 0"
                )
            )
        except:
            pass

    def wait_for_network_idle(self, idle_time=2):
        """Wait for network to be idle"""
        network_active = True
        start_time = time.time()
        
        while network_active and (time.time() - start_time) < self.timeout:
            time.sleep(0.5)
            network_active = self.driver.execute_script(
                "return window.performance.getEntriesByType('resource').some(r => !r.responseEnd);"
            )
            
            if not network_active:
                # Wait additional idle time to confirm
                time.sleep(idle_time)
                network_active = self.driver.execute_script(
                    "return window.performance.getEntriesByType('resource').some(r => !r.responseEnd);"
                )