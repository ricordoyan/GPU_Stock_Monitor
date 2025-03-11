from src.notification import NotificationManager
from src.ai_agent.multimodal_agent import MultimodalAgent
from src.retailers.bestbuy_retailer import BestBuyRetailer
from src.retailers.newegg_retailer import NeweggRetailer
from src.retailers.msi_retailer import MSIRetailer
from src.retailers.asus_retailer import ASUSRetailer
from src.retailers.bhphoto_retailer import BHPhotoRetailer
from src.retailers.nowinstock_aggregator import NowInStockAggregator
from src.retailers.reddit_monitor import RedditMonitor
import time
import random
import os
from datetime import datetime
import pytz

class GPUMonitor:
    def __init__(self, notification_manager: NotificationManager, ai_agent: MultimodalAgent):
        self.notification_manager = notification_manager
        self.ai_agent = ai_agent
        self.pst_timezone = pytz.timezone('US/Pacific')
        
        # Initialize retailers
        self.retailers = {
            'bestbuy': BestBuyRetailer(ai_agent),
            'newegg': NeweggRetailer(ai_agent),
            'msi': MSIRetailer(ai_agent),
            'asus': ASUSRetailer(ai_agent),
            'bhphoto': BHPhotoRetailer(ai_agent)
        }
        
        # Add NowInStock aggregator
        self.aggregator = NowInStockAggregator(ai_agent)
        
        # Add Reddit monitor
        self.reddit_monitor = RedditMonitor(ai_agent)
        
        # Configure check intervals
        self.intensive_check_interval = int(os.getenv("INTENSIVE_CHECK_INTERVAL", "60"))  # 1 minute
        self.normal_check_interval = int(os.getenv("NORMAL_CHECK_INTERVAL", "300"))  # 5 minutes
        self.extended_check_interval = int(os.getenv("EXTENDED_CHECK_INTERVAL", "3600"))  # 1 hour
        self.reddit_check_interval = int(os.getenv("REDDIT_CHECK_INTERVAL", "1800"))  # 30 minutes
        
        # Products to monitor - only RTX 5080 and 5090
        self.gpu_models = ["RTX 5080", "RTX 5090"]
        
        # Results tracking
        self.last_check_results = {}
        self.last_reddit_check = 0

    def monitor_stock(self):
        """Monitor stock across all retailers and Reddit."""
        print(f"Starting multi-retailer GPU monitor for: {', '.join(self.gpu_models)}")
        print(f"Monitoring retailers: {', '.join(self.retailers.keys())}")
        
        while True:
            try:
                current_time = datetime.now(self.pst_timezone)
                current_interval = self.get_check_interval()
                
                print(f"\nChecking stock at {current_time.strftime('%Y-%m-%d %H:%M:%S %Z')}")
                
                # Check NowInStock aggregator first (less resource intensive)
                self.check_aggregator()
                
                # Check individual retailers
                for gpu_model in self.gpu_models:
                    self.check_gpu_model(gpu_model)
                
                # Check Reddit periodically (not every loop)
                if time.time() - self.last_reddit_check >= self.reddit_check_interval:
                    self.check_reddit()
                    self.last_reddit_check = time.time()
                
                # Add some randomness to the interval to avoid detection
                jitter = random.uniform(0.9, 1.1)
                actual_interval = int(current_interval * jitter)
                
                print(f"Next check in {actual_interval/60:.1f} minutes")
                time.sleep(actual_interval)
                
            except KeyboardInterrupt:
                print("\nMonitoring stopped by user")
                break
            except Exception as e:
                print(f"Error during monitoring: {e}")
                # Wait before retrying
                time.sleep(60)
    
    def check_reddit(self):
        """Check Reddit for GPU availability and priority access information."""
        print("Checking Reddit for GPU information...")
        
        try:
            # Check for general GPU posts
            relevant_posts = self.reddit_monitor.check_for_updates()
            
            if relevant_posts:
                message = f"Found {len(relevant_posts)} relevant Reddit posts about RTX 5080/5090!"
                self.notification_manager.notify(message)
                
                for post in relevant_posts:
                    post_message = f"[{post.get('subreddit')}/{post.get('score')}] {post.get('title')}: {post.get('url')}"
                    self.notification_manager.notify(post_message)
            
            # Specifically check for priority access information
            priority_info = self.reddit_monitor.check_nvidia_priority_access()
            
            if priority_info:
                message = f"Found information about NVIDIA Priority Access Program!"
                self.notification_manager.notify(message)
                
                for info in priority_info:
                    priority_message = f"[PRIORITY ACCESS] {info.get('title')}: {info.get('url')}"
                    self.notification_manager.notify(priority_message)
                    
                    # Also notify about the analysis if available
                    if info.get("analysis"):
                        analysis_message = f"DETAILS: {info.get('analysis')}"
                        self.notification_manager.notify(analysis_message)
            
            print(f"Reddit check complete. Found {len(relevant_posts)} general posts and {len(priority_info) if priority_info else 0} priority access posts.")
            
        except Exception as e:
            print(f"Error checking Reddit: {e}")
    
    def check_aggregator(self):
        """Check the NowInStock aggregator."""
        print("Checking NowInStock aggregator...")
        try:
            in_stock_products = self.aggregator.search_products()
            
            if in_stock_products:
                message = f"NowInStock reports {len(in_stock_products)} RTX 5080/5090 in stock!"
                self.notification_manager.notify(message)
                
                for product in in_stock_products:
                    product_message = f"{product.get('name')} at {product.get('retailer')}: {product.get('url')}"
                    self.notification_manager.notify(product_message)
            else:
                print("No products in stock according to NowInStock")
                
        except Exception as e:
            print(f"Error checking NowInStock: {e}")
    
    def check_gpu_model(self, gpu_model):
        """Check a specific GPU model across all retailers."""
        print(f"Checking {gpu_model} across all retailers...")
        
        for retailer_name, retailer in self.retailers.items():
            try:
                print(f"Checking {retailer_name} for {gpu_model}...")
                
                # Search for products
                products = retailer.search_products(gpu_model)
                
                if products:
                    message = f"Found {len(products)} {gpu_model} in stock at {retailer_name}!"
                    self.notification_manager.notify(message)
                    
                    for product in products:
                        product_message = f"{product.get('name')} at {retailer_name}: {product.get('url')}"
                        self.notification_manager.notify(product_message)
                else:
                    print(f"No {gpu_model} in stock at {retailer_name}")
                    
            except Exception as e:
                print(f"Error checking {retailer_name} for {gpu_model}: {e}")
    
    def get_check_interval(self):
        """Determine the current check interval based on time of day."""
        current_hour = datetime.now(self.pst_timezone).hour
        
        if 0 <= current_hour < 6:
            return self.extended_check_interval
        elif 6 <= current_hour < 12:
            return self.normal_check_interval
        else:
            return self.intensive_check_interval
    
    def cleanup(self):
        """Clean up resources for all retailers."""
        print("Cleaning up resources...")
        for retailer_name, retailer in self.retailers.items():
            try:
                if hasattr(retailer, 'cleanup'):
                    retailer.cleanup()
            except Exception as e:
                print(f"Error cleaning up {retailer_name}: {e}")
        
        try:
            if hasattr(self.aggregator, 'cleanup'):
                self.aggregator.cleanup()
        except Exception as e:
            print(f"Error cleaning up aggregator: {e}")