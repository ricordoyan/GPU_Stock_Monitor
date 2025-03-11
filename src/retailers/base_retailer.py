from abc import ABC, abstractmethod
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

class BaseRetailer(ABC):
    """Base class for all retailer implementations."""
    
    def __init__(self, name, ai_agent):
        self.name = name
        self.ai_agent = ai_agent
        self.options = self._configure_chrome_options()
        self.driver = self._setup_driver()
        self.check_count = 0
        self.max_checks_before_restart = 20
        self.products = []
        
    def _configure_chrome_options(self):
        """Configure Chrome options with error suppression settings."""
        options = Options()
        
        # Basic headless mode settings
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        # Memory and performance optimization
        options.add_argument("--js-flags=--expose-gc")
        options.add_argument("--disable-renderer-backgrounding")
        options.add_argument("--memory-pressure-off")
        
        # WebGL settings
        options.add_argument("--disable-webgl")
        options.add_argument("--enable-unsafe-swiftshader")
        
        # Logging and notification settings
        options.add_argument("--disable-notifications")
        options.add_argument("--log-level=3")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        
        # Disable UI elements and automation flags
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # User agent
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36")
        
        return options
        
    def _setup_driver(self):
        """Initialize and configure Chrome WebDriver."""
        try:
            driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=self.options
            )
            driver.set_page_load_timeout(90)
            return driver
        except Exception as e:
            print(f"Error setting up Chrome driver for {self.name}: {e}")
            raise
    
    @abstractmethod
    def search_products(self, query):
        """Search for products with the given query."""
        pass
    
    @abstractmethod
    def check_product_availability(self, product_url):
        """Check if a product is available."""
        pass
    
    @abstractmethod
    def get_products_list(self):
        """Get list of tracked products."""
        pass
        
    def restart_browser(self):
        """Safely restart the Chrome browser."""
        print(f"Restarting Chrome browser for {self.name}...")
        try:
            self.driver.quit()
        except Exception as e:
            print(f"Error closing browser: {e}")
        
        import time
        time.sleep(10)
        self.driver = self._setup_driver()
        self.check_count = 0
        print(f"Browser for {self.name} restarted successfully")
        
    def cleanup(self):
        """Clean up resources."""
        try:
            self.driver.quit()
        except Exception as e:
            print(f"Error during cleanup for {self.name}: {e}")