import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.retailers.base_retailer import BaseRetailer

class MSIRetailer(BaseRetailer):
    """Implementation for MSI website."""
    
    def __init__(self, ai_agent):
        super().__init__("MSI", ai_agent)
        self.base_url = "https://us.msi.com"
        self.search_url_template = "https://us.msi.com/search/{}"
        
    def search_products(self, query):
        """Search for products on MSI."""
        search_url = self.search_url_template.format(query.replace(' ', '%20'))
        
        try:
            print(f"Searching MSI for: {query}")
            self.driver.get(search_url)
            
            # Wait for search results to load
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".product-item"))
            )
            
            # Use AI agent for visual analysis
            page_content = self.driver.page_source
            screenshot = self.driver.get_screenshot_as_png()
            
            products = self.ai_agent.process_input(
                f"Find RTX {query} products on MSI search results page",
                {
                    "screenshot": screenshot,
                    "html": page_content
                }
            )
            
            # Filter for available products
            available_products = []
            for product in products.get("visual", []):
                # Check for "Buy Now", "Add to Cart", "Check Retailers" indicators
                if any(text in product.get("button_text", "").lower() for text in ["buy now", "add to cart", "check retailers"]):
                    product["retailer"] = self.name
                    available_products.append(product)
                    
            self.products = available_products
            return available_products
            
        except Exception as e:
            print(f"Error searching MSI: {e}")
            return []
    
    def check_product_availability(self, product_url):
        """Check if a specific product is available on MSI."""
        try:
            self.driver.get(product_url)
            
            # Wait for product page to load
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".product-detail"))
            )
            
            # Use AI agent to analyze the page
            screenshot = self.driver.get_screenshot_as_png()
            page_content = self.driver.page_source
            
            page_analysis = self.ai_agent.process_input(
                "Check if this RTX GPU is available for purchase on MSI website",
                {
                    "screenshot": screenshot,
                    "html": page_content
                }
            )
            
            # MSI often directs to retailers rather than direct sales
            # Look for "Buy Now" or "Where to Buy" buttons
            buy_buttons = self.driver.find_elements(By.XPATH, 
                "//a[contains(text(), 'Buy Now') or contains(text(), 'Where to Buy')]")
                
            if buy_buttons:
                return {"available": True, "status": "RETAILER_AVAILABLE", "retailer": self.name, "url": product_url}
            else:
                return {"available": False, "status": "NOT_AVAILABLE", "retailer": self.name, "url": product_url}
                
        except Exception as e:
            print(f"Error checking MSI product availability: {e}")
            return {"available": False, "status": "ERROR", "retailer": self.name, "url": product_url}
    
    def get_products_list(self):
        """Get list of tracked products."""
        return self.products