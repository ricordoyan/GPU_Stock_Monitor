import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from src.retailers.base_retailer import BaseRetailer

class BestBuyRetailer(BaseRetailer):
    """Implementation for Best Buy website."""
    
    def __init__(self, ai_agent):
        super().__init__("Best Buy", ai_agent)
        self.base_url = "https://www.bestbuy.com"
        self.search_url_template = "https://www.bestbuy.com/site/searchpage.jsp?st={}"
        
    def search_products(self, query):
        """Search for products on Best Buy."""
        search_url = self.search_url_template.format(query.replace(' ', '+'))
        
        try:
            print(f"Searching Best Buy for: {query}")
            self.driver.get(search_url)
            
            # Wait for search results to load
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".sku-item"))
            )
            
            # Use AI agent to analyze the page and extract product information
            # focusing on "See Details" vs "Add to Cart" buttons
            page_content = self.driver.page_source
            screenshot = self.driver.get_screenshot_as_png()
            
            # Use visual language model to analyze products
            products = self.ai_agent.process_input(
                f"Find RTX {query} products on Best Buy search results page",
                {
                    "screenshot": screenshot,
                    "html": page_content
                }
            )
            
            # Filter products based on availability using "See Details" indicator
            # which is specific to high-demand Best Buy products
            available_products = []
            for product in products.get("visual", []):
                if product.get("button_text") == "See Details":
                    product["retailer"] = self.name
                    available_products.append(product)
                    
            # Save products to instance
            self.products = available_products
            return available_products
            
        except Exception as e:
            print(f"Error searching Best Buy: {e}")
            return []
    
    def check_product_availability(self, product_url):
        """Check if a specific product is available on Best Buy."""
        try:
            self.driver.get(product_url)
            
            # Wait for button to load
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".add-to-cart-button"))
            )
            
            # Get button text
            button = self.driver.find_element(By.CSS_SELECTOR, ".add-to-cart-button")
            button_text = button.text.strip().upper()
            
            # Check if the button shows "See Details" which for GPU products is important
            is_see_details = "SEE DETAILS" in button_text
            
            # For Best Buy, "See Details" often indicates a special high-demand purchase process
            # which means the product is potentially available but requires additional steps
            if is_see_details:
                return {"available": True, "status": "SEE_DETAILS", "retailer": self.name, "url": product_url}
            elif "ADD TO CART" in button_text:
                return {"available": True, "status": "AVAILABLE", "retailer": self.name, "url": product_url}
            elif "SOLD OUT" in button_text:
                return {"available": False, "status": "SOLD_OUT", "retailer": self.name, "url": product_url}
            else:
                return {"available": False, "status": "UNKNOWN", "retailer": self.name, "url": product_url}
                
        except Exception as e:
            print(f"Error checking Best Buy product availability: {e}")
            return {"available": False, "status": "ERROR", "retailer": self.name, "url": product_url}
    
    def get_products_list(self):
        """Get list of tracked products."""
        return self.products