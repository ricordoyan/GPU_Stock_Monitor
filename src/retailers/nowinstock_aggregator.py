import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.retailers.base_retailer import BaseRetailer

class NowInStockAggregator(BaseRetailer):
    """Implementation for NowInStock tracking website."""
    
    def __init__(self, ai_agent):
        super().__init__("NowInStock", ai_agent)
        self.base_url = "https://www.nowinstock.net"
        # URL for RTX 5080/5090 tracking page - this would need to be updated when these pages exist
        self.tracking_url = "https://www.nowinstock.net/computers/videocards/nvidia/rtx5080/"
        self.alt_tracking_url = "https://www.nowinstock.net/computers/videocards/nvidia/rtx5090/"
        
    def search_products(self, query=None):
        """Search for available GPU products on NowInStock."""
        products = []
        
        try:
            # Check RTX 5080 page
            print("Checking NowInStock for RTX 5080...")
            self.driver.get(self.tracking_url)
            products.extend(self._extract_available_products())
            
            # Check RTX 5090 page if different
            print("Checking NowInStock for RTX 5090...")
            self.driver.get(self.alt_tracking_url)
            products.extend(self._extract_available_products())
            
            self.products = products
            return products
            
        except Exception as e:
            print(f"Error searching NowInStock: {e}")
            return []
    
    def _extract_available_products(self):
        """Extract available products from current page."""
        try:
            # Wait for tracker table to load
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.ID, "tracker-table"))
            )
            
            # Use AI agent for visual analysis
            page_content = self.driver.page_source
            screenshot = self.driver.get_screenshot_as_png()
            
            result = self.ai_agent.process_input(
                "Find in-stock RTX 5080 or RTX 5090 products on NowInStock page. "
                "Look for green IN STOCK indicators in the availability column.",
                {
                    "screenshot": screenshot,
                    "html": page_content
                }
            )
            
            # Also perform direct DOM inspection for in-stock items
            # NowInStock typically uses green text and "IN STOCK" label
            in_stock_rows = self.driver.find_elements(By.XPATH, 
                "//tr[contains(@class, 'inStock') or .//td[contains(@class, 'stockStatus')][contains(text(), 'In Stock')]]")
            
            available_products = []
            
            # Process DOM-extracted items
            for row in in_stock_rows:
                try:
                    product_name = row.find_element(By.CSS_SELECTOR, "td.product").text
                    retailer_name = row.find_element(By.CSS_SELECTOR, "td.merchant").text
                    price_text = row.find_element(By.CSS_SELECTOR, "td.price").text
                    
                    # Get link to product
                    link_elem = row.find_element(By.CSS_SELECTOR, "td.product a")
                    product_url = link_elem.get_attribute("href")
                    
                    available_products.append({
                        "name": product_name,
                        "retailer": retailer_name,
                        "price": price_text,
                        "url": product_url,
                        "status": "AVAILABLE",
                        "source": "NowInStock"
                    })
                except Exception as e:
                    print(f"Error extracting product from row: {e}")
            
            # Combine with AI-detected products
            for product in result.get("visual", []):
                if product not in available_products:  # Avoid duplicates
                    product["source"] = "NowInStock"
                    available_products.append(product)
                    
            return available_products
            
        except Exception as e:
            print(f"Error extracting products: {e}")
            return []
    
    def check_product_availability(self, product_url):
        """Check if a specific product is available via NowInStock."""
        # For NowInStock, we redirect to the actual retailer page
        try:
            self.driver.get(product_url)
            
            # Wait for page to load
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Screenshot for AI analysis
            screenshot = self.driver.get_screenshot_as_png()
            page_content = self.driver.page_source
            
            # Use the AI agent to determine if the product is available
            is_available = self.ai_agent.identify_gpu_availability({
                "screenshot": screenshot,
                "html": page_content
            })
            
            status = "AVAILABLE" if is_available else "OUT_OF_STOCK" 
            return {"available": is_available, "status": status, "retailer": "NowInStock Link", "url": product_url}
                
        except Exception as e:
            print(f"Error checking product availability via NowInStock: {e}")
            return {"available": False, "status": "ERROR", "retailer": "NowInStock Link", "url": product_url}
    
    def get_products_list(self):
        """Get list of tracked products."""
        return self.products