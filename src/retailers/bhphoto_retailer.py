import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.retailers.base_retailer import BaseRetailer

class BHPhotoRetailer(BaseRetailer):
    """Implementation for B&H Photo website."""
    
    def __init__(self, ai_agent):
        super().__init__("B&H Photo", ai_agent)
        self.base_url = "https://www.bhphotovideo.com"
        self.search_url_template = "https://www.bhphotovideo.com/c/search?q={}"
        
    def search_products(self, query):
        """Search for products on B&H Photo."""
        search_url = self.search_url_template.format(query.replace(' ', '%20'))
        
        try:
            print(f"Searching B&H Photo for: {query}")
            self.driver.get(search_url)
            
            # Wait for search results to load
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".productCard"))
            )
            
            # Use AI agent for visual analysis
            page_content = self.driver.page_source
            screenshot = self.driver.get_screenshot_as_png()
            
            products = self.ai_agent.process_input(
                f"Find RTX {query} products on B&H Photo search results page",
                {
                    "screenshot": screenshot,
                    "html": page_content
                }
            )
            
            # Filter for available products
            available_products = []
            for product in products.get("visual", []):
                # B&H uses "Add to Cart" for available items, "Notify When Available" or "Pre-Order" for others
                button_text = product.get("button_text", "").lower()
                if "add to cart" in button_text:
                    product["retailer"] = self.name
                    product["status"] = "AVAILABLE"
                    available_products.append(product)
                elif "pre-order" in button_text:
                    product["retailer"] = self.name
                    product["status"] = "PRE_ORDER"
                    available_products.append(product)
                    
            self.products = available_products
            return available_products
            
        except Exception as e:
            print(f"Error searching B&H Photo: {e}")
            return []
    
    def check_product_availability(self, product_url):
        """Check if a specific product is available on B&H Photo."""
        try:
            self.driver.get(product_url)
            
            # Wait for product page to load
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".product-info"))
            )
            
            # Screenshot for AI analysis
            screenshot = self.driver.get_screenshot_as_png()
            page_content = self.driver.page_source
            
            # B&H typically shows availability status clearly
            add_to_cart = self.driver.find_elements(By.XPATH, "//button[contains(text(), 'Add to Cart')]")
            pre_order = self.driver.find_elements(By.XPATH, "//button[contains(text(), 'Pre-Order')]")
            notify = self.driver.find_elements(By.XPATH, "//button[contains(text(), 'Notify When Available')]")
            
            if add_to_cart:
                return {"available": True, "status": "AVAILABLE", "retailer": self.name, "url": product_url}
            elif pre_order:
                return {"available": True, "status": "PRE_ORDER", "retailer": self.name, "url": product_url}
            elif notify:
                return {"available": False, "status": "OUT_OF_STOCK", "retailer": self.name, "url": product_url}
            else:
                # Use AI to analyze ambiguous status
                is_available = self.ai_agent.identify_gpu_availability({
                    "screenshot": screenshot,
                    "html": page_content
                })
                status = "AVAILABLE" if is_available else "OUT_OF_STOCK"
                return {"available": is_available, "status": status, "retailer": self.name, "url": product_url}
                
        except Exception as e:
            print(f"Error checking B&H Photo product availability: {e}")
            return {"available": False, "status": "ERROR", "retailer": self.name, "url": product_url}
    
    def get_products_list(self):
        """Get list of tracked products."""
        return self.products