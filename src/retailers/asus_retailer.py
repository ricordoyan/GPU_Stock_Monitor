import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.retailers.base_retailer import BaseRetailer

class ASUSRetailer(BaseRetailer):
    """Implementation for ASUS website."""
    
    def __init__(self, ai_agent):
        super().__init__("ASUS", ai_agent)
        self.base_url = "https://www.asus.com/us"
        self.search_url_template = "https://www.asus.com/us/search/{}"
        
    def search_products(self, query):
        """Search for products on ASUS."""
        search_url = self.search_url_template.format(query.replace(' ', '-'))
        
        try:
            print(f"Searching ASUS for: {query}")
            self.driver.get(search_url)
            
            # Wait for search results to load
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".product-card"))
            )
            
            # Use AI agent for visual analysis
            page_content = self.driver.page_source
            screenshot = self.driver.get_screenshot_as_png()
            
            products = self.ai_agent.process_input(
                f"Find RTX {query} products on ASUS search results page",
                {
                    "screenshot": screenshot,
                    "html": page_content
                }
            )
            
            # Filter for available products
            available_products = []
            for product in products.get("visual", []):
                # Look for "Buy" or "Check Availability" indicators
                if any(text in product.get("button_text", "").lower() for text in ["buy", "check availability", "shop now"]):
                    product["retailer"] = self.name
                    available_products.append(product)
                    
            self.products = available_products
            return available_products
            
        except Exception as e:
            print(f"Error searching ASUS: {e}")
            return []
    
    def check_product_availability(self, product_url):
        """Check if a specific product is available on ASUS."""
        try:
            self.driver.get(product_url)
            
            # Wait for product page to load
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".product-info"))
            )
            
            # Screenshot for AI analysis
            screenshot = self.driver.get_screenshot_as_png()
            page_content = self.driver.page_source
            
            # Use visual analysis to determine availability
            is_available = self.ai_agent.identify_gpu_availability({
                "screenshot": screenshot,
                "html": page_content
            })
            
            # ASUS typically uses "Buy" or "Where to buy" buttons
            buy_buttons = self.driver.find_elements(By.XPATH, 
                "//a[contains(text(), 'Buy') or contains(@class, 'buy')]")
                
            where_to_buy = self.driver.find_elements(By.XPATH, 
                "//a[contains(text(), 'Where to buy') or contains(@class, 'where-to-buy')]")
                
            if buy_buttons or is_available:
                return {"available": True, "status": "AVAILABLE", "retailer": self.name, "url": product_url}
            elif where_to_buy:
                return {"available": True, "status": "RETAILER_AVAILABLE", "retailer": self.name, "url": product_url}
            else:
                return {"available": False, "status": "NOT_AVAILABLE", "retailer": self.name, "url": product_url}
                
        except Exception as e:
            print(f"Error checking ASUS product availability: {e}")
            return {"available": False, "status": "ERROR", "retailer": self.name, "url": product_url}
    
    def get_products_list(self):
        """Get list of tracked products."""
        return self.products