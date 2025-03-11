import os
import sys
import time
from datetime import datetime
from src.chatbot.response_generator import ResponseGenerator
from src.ai_agent.multimodal_agent import MultimodalAgent
from src.retailers.bestbuy_retailer import BestBuyRetailer
from src.retailers.newegg_retailer import NeweggRetailer
from src.retailers.msi_retailer import MSIRetailer
from src.retailers.asus_retailer import ASUSRetailer
from src.retailers.bhphoto_retailer import BHPhotoRetailer
from src.retailers.nowinstock_aggregator import NowInStockAggregator
from src.retailers.reddit_monitor import RedditMonitor
from dotenv import load_dotenv

class GPUSourcingChatbot:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        # Initialize AI agent
        self.ai_agent = MultimodalAgent()
        self.response_generator = ResponseGenerator(self.ai_agent)
        
        # Initialize retailer connections for real-time info
        self.retailers = {
            'bestbuy': BestBuyRetailer(self.ai_agent),
            'newegg': NeweggRetailer(self.ai_agent),
            'msi': MSIRetailer(self.ai_agent),
            'asus': ASUSRetailer(self.ai_agent),
            'bhphoto': BHPhotoRetailer(self.ai_agent)
        }
        
        # Initialize aggregator and Reddit monitor
        self.aggregator = NowInStockAggregator(self.ai_agent)
        self.reddit_monitor = RedditMonitor(self.ai_agent)
        
        # Knowledge base on GPU models
        self.gpu_models = ["RTX 5080", "RTX 5090"]
        
        # Session state
        self.chat_history = []
        
    def start(self):
        """Start the chatbot interface."""
        print("\n" + "=" * 80)
        print(f"{'GPU Sourcing Assistant':^80}")
        print("=" * 80)
        print("Welcome! I'm your GPU sourcing assistant, specialized in helping you find RTX 5080 and 5090 GPUs.")
        print("You can ask me about current availability, retailer strategies, priority access programs, and more.")
        print("Type 'exit' or 'quit' to end our conversation.")
        print("=" * 80)
        
        while True:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() in ['exit', 'quit', 'bye', 'goodbye']:
                print("\nGPU Sourcing Assistant: Thanks for chatting! Good luck with your GPU search!")
                break
                
            # Process user query
            response = self.process_query(user_input)
            print(f"\nGPU Sourcing Assistant: {response}")
    
    def process_query(self, query):
        """Process a user query and generate a response."""
        # Add query to chat history
        self.chat_history.append({"role": "user", "content": query})
        
        # Check for specific query types
        if self._is_availability_check(query):
            response = self._check_current_availability()
        elif self._is_priority_access_query(query):
            response = self._get_priority_access_info()
        elif self._is_retailer_strategy_query(query):
            response = self._get_retailer_strategy(query)
        else:
            # General query - use response generator
            response = self.response_generator.generate_response(
                query, 
                self.chat_history
            )
        
        # Add response to chat history
        self.chat_history.append({"role": "assistant", "content": response})
        
        return response
    
    def _is_availability_check(self, query):
        """Check if the query is asking about current GPU availability."""
        availability_keywords = [
            'available', 'availability', 'in stock', 'where can i buy', 'where to buy',
            'find', 'purchase', 'get', 'buy'
        ]
        
        query_lower = query.lower()
        
        # Check if query contains both GPU model reference and availability keywords
        has_gpu_reference = any(gpu.lower() in query_lower for gpu in self.gpu_models) or 'gpu' in query_lower
        has_availability_keyword = any(keyword in query_lower for keyword in availability_keywords)
        
        return has_gpu_reference and has_availability_keyword
    
    def _is_priority_access_query(self, query):
        """Check if the query is about NVIDIA priority access program."""
        priority_keywords = [
            'priority access', 'priority program', 'nvidia direct', 
            'purchase program', 'drawing', 'lottery', 'invitation'
        ]
        
        query_lower = query.lower()
        
        return any(keyword in query_lower for keyword in priority_keywords)
    
    def _is_retailer_strategy_query(self, query):
        """Check if the query is about retailer strategies."""
        retailer_names = ['bestbuy', 'best buy', 'newegg', 'msi', 'asus', 'b&h', 'bhphoto']
        strategy_keywords = ['strategy', 'tip', 'advice', 'how to', 'when', 'restock']
        
        query_lower = query.lower()
        
        has_retailer = any(retailer in query_lower for retailer in retailer_names)
        has_strategy_keyword = any(keyword in query_lower for keyword in strategy_keywords)
        
        return has_retailer and has_strategy_keyword
    
    def _check_current_availability(self):
        """Check and report current GPU availability across retailers."""
        print("Checking current GPU availability across retailers...")
        
        availability = {}
        
        # Check NowInStock first (most efficient)
        try:
            in_stock_products = self.aggregator.search_products()
            if in_stock_products:
                availability['nowinstock'] = in_stock_products
        except Exception as e:
            print(f"Error checking NowInStock: {e}")
        
        # Check individual retailers if needed
        if not availability:
            for retailer_name, retailer in self.retailers.items():
                try:
                    # Check each GPU model
                    products = []
                    for gpu_model in self.gpu_models:
                        model_products = retailer.search_products(gpu_model)
                        if model_products:
                            products.extend(model_products)
                    
                    if products:
                        availability[retailer_name] = products
                except Exception as e:
                    print(f"Error checking {retailer_name}: {e}")
        
        # Generate response based