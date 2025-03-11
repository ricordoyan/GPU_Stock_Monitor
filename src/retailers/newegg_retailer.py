import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.retailers.base_retailer import BaseRetailer

class NeweggRetailer(BaseRetailer):
    """Implementation for Newegg website."""
    
    def __init__(self, ai_agent):
        super().__init__("Newegg", ai_agent)
        self.base_url = "https://www.newegg.com"
        self.search_url_template = "https://www.newegg.com/p/pl?d={}"
        
    def search_products(self, query):
        """Search for products on Newegg."""
        search_url = self.search_url_template.format(query.replace(' ', '+'))
        
        try:
            print(f"Searching Newegg for: {query}")
            self.driver.get(search_url)
            
            # Wait for search results to load
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".item-cell"))
            )
            
            # Use AI agent for visual analysis
            page_content = self.driver.page_source
            screenshot = self.driver.get_screenshot_as_png()
            
            products = self.ai_agent.process_input(
                f"Find RTX {query} products on Newegg search results page",
                {
                    "screenshot": screenshot,
                    "html": page_content
                }
            )
            
            available_products = []
            for product in products.get("visual", []):
                # For Newegg, check for "Add to cart" vs "Auto Notify" buttons
                if product.get("button_text") == "Add to cart":
                    product["retailer"] = self.name
                    available_products.append(product)
                    
            self.products = available_products
            return available_products
            
        except Exception as e:
            print(f"Error searching Newegg: {e}")
            return []
    
    def check_product_availability(self, product_url):
        """Check if a specific product is available on Newegg."""
        try:
            self.driver.get(product_url)
            
            # Wait for button to load
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".product-buy"))
            )
            
            # Check if "Add to cart" button exists vs "Auto Notify" button
            buy_buttons = self.driver.find_elements(By.CSS_SELECTOR, ".btn-primary")
            
            for button in buy_buttons:
                button_text = button.text.strip().upper()
                if "ADD TO CART" in button_text:
                    return {"available": True, "status": "AVAILABLE", "retailer": self.name, "url": product_url}
            
            # If we didn't find "Add to cart", check for "Auto Notify" indicating out of stock
            auto_notify_buttons = self.driver.find_elements(By.CSS_SELECTOR, ".btn-secondary")
            for button in auto_notify_buttons:
                if "AUTO NOTIFY" in button.text.strip().upper():
                    return {"available": False, "status": "OUT_OF_STOCK", "retailer": self.name, "url": product_url}
                    
            return {"available": False, "status": "UNKNOWN", "retailer": self.name, "url": product_url}
                
        except Exception as e:
            print(f"Error checking Newegg product availability: {e}")
            return {"available": False, "status": "ERROR", "retailer": self.name, "url": product_url}
    
    def get_products_list(self):
        """Get list of tracked products."""
        return self.products