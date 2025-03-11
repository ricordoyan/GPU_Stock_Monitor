import re
import json
import random
from datetime import datetime
from typing import List, Dict, Any

class ResponseGenerator:
    """
    Generates responses for the GPU Sourcing Chatbot using
    AI model and domain knowledge about GPUs and retailers.
    """
    
    def __init__(self, ai_agent):
        self.ai_agent = ai_agent
        
        # Knowledge base of common GPU questions and answers
        self.knowledge_base = {
            "bestbuy_strategy": (
                "For Best Buy RTX cards, 'See Details' typically means the item is coming soon or "
                "requires joining a queue. Best Buy often uses a queue system for high-demand GPUs. "
                "They typically restock on Thursdays or Fridays, usually between 9am-11am ET. "
                "Having a Best Buy account with payment details saved, and TotalTech membership "
                "can sometimes provide earlier access."
            ),
            "newegg_strategy": (
                "Newegg uses a shuffle system for high-demand GPUs. They announce shuffles on "
                "their website and social media. Sign up for shuffle events when available. "
                "They also release small quantities directly, usually late night ET. "
                "Items marked 'Auto-Notify' mean they're out of stock but will notify you when available."
            ),
            "priority_access": (
                "NVIDIA's Priority Access Program allows select users to purchase GPUs directly from "
                "NVIDIA before general availability. To qualify, you typically need to be registered "
                "on NVIDIA's site and receive an email invitation. The selection appears to be based on "
                "prior NVIDIA GPU ownership, GeForce Experience usage, and other factors. When active, "
                "the program allows invited users a time-limited window to purchase one GPU per account."
            ),
            "rtx_5080_specs": (
                "The RTX 5080 features the Blackwell architecture with 12,288 CUDA cores, 24GB of GDDR7 memory, "
                "and a boost clock of up to 2.4GHz. It's positioned as a high-end gaming card with excellent "
                "ray-tracing performance and DLSS 4 support."
            ),
            "rtx_5090_specs": (
                "The RTX 5090 is NVIDIA's flagship GPU with the Blackwell architecture, featuring 21,504 CUDA cores, "
                "32GB of GDDR7 memory, and a boost clock of up to 2.2GHz. It's designed for 4K and 8K gaming, "
                "professional content creation, and AI workloads."
            )
        }
        
        # Common retailer-specific phrases
        self.retailer_info = {
            "bestbuy": {
                "restock_pattern": "Best Buy typically restocks on Thursday or Friday mornings, 9-11am ET",
                "membership": "Best Buy TotalTech members sometimes get early access to GPU drops",
                "button_pattern": "Look for 'See Details' changing to 'Add to Cart' during drops"
            },
            "newegg": {
                "restock_pattern": "Newegg restocks throughout the week, often late night ET",
                "shuffle": "Check for Newegg Shuffle events that let you enter a drawing to buy GPUs",
                "combos": "Newegg often sells high-demand GPUs in combos with other components"
            },
            "asus": {
                "availability": "ASUS store often links to authorized retailers rather than selling directly",
                "notify": "Use the 'Notify Me' option to get email alerts for ASUS GPUs"
            },
            "msi": {
                "availability": "MSI's website typically redirects to partner retailers",
                "where_to_buy": "Use the 'Where to Buy' option to find authorized retailers"
            },
            "bhphoto": {
                "backorder": "B&H often allows backorders on out-of-stock GPUs",
                "notify": "Join their notification list for specific models",
                "restock_pattern": "They typically update inventory overnight Eastern Time"
            }
        }
        
    def generate_response(self, query: str, chat_history: List[Dict[str, str]]) -> str:
        """
        Generate a response to a user query using AI and domain knowledge.
        
        Args:
            query: User's input text
            chat_history: List of previous exchanges
            
        Returns:
            String response to the user query
        """
        # Check for keywords to provide specific knowledge-based responses
        knowledge_response = self._check_knowledge_base(query)
        if knowledge_response:
            return knowledge_response
        
        # Format chat history for the AI agent
        formatted_history = self._format_chat_history(chat_history)
        
        # Generate response using the AI agent
        ai_instructions = (
            "You are a specialized GPU sourcing assistant helping users find RTX 5080 and 5090 GPUs. "
            "Focus on providing accurate, helpful information about GPU availability, retailer strategies, "
            "and purchasing tips. Keep responses concise but informative."
        )
        
        response = self.ai_agent.process_text(
            f"{ai_instructions}\n\nUser query: {query}\n\nChat history: {formatted_history}"
        )
        
        return self._format_response(response)
    
    def _check_knowledge_base(self, query: str) -> str:
        """Check if the query can be answered directly from the knowledge base."""
        query_lower = query.lower()
        
        # Check for Best Buy strategy questions
        if re.search(r'best buy|bestbuy', query_lower) and re.search(r'strateg|tip|how|when', query_lower):
            return self.knowledge_base["bestbuy_strategy"]
            
        # Check for Newegg strategy questions
        elif re.search(r'newegg', query_lower) and re.search(r'strateg|tip|shuffle|how|when', query_lower):
            return self.knowledge_base["newegg_strategy"]
            
        # Check for priority access questions
        elif re.search(r'priority access|program|nvidia direct|drawing', query_lower):
            return self.knowledge_base["priority_access"]
            
        # Check for RTX 5080 specifications
        elif re.search(r'5080', query_lower) and re.search(r'spec|detail|performance|feature', query_lower):
            return self.knowledge_base["rtx_5080_specs"]
            
        # Check for RTX 5090 specifications
        elif re.search(r'5090', query_lower) and re.search(r'spec|detail|performance|feature', query_lower):
            return self.knowledge_base["rtx_5090_specs"]
            
        return None
    
    def _format_chat_history(self, chat_history: List[Dict[str, str]]) -> str:
        """Format chat history for the AI agent."""
        if not chat_history or len(chat_history) <= 1:
            return "No previous conversation."
            
        # Format only the relevant history (skip the current query)
        formatted = []
        for entry in chat_history[:-1]:
            role = "User" if entry["role"] == "user" else "Assistant"
            formatted.append(f"{role}: {entry['content']}")
            
        return "\n".join(formatted)
    
    def _format_response(self, response: str) -> str:
        """Format the AI response for user presentation."""
        # Remove any prefixes like "Assistant:" that the AI might add
        response = re.sub(r'^(Assistant|GPU Sourcing Assistant|AI):\s*', '', response)
        
        # Clean up any extra whitespace
        response = response.strip()
        
        return response
    
    def generate_retailer_response(self, retailer_name: str) -> str:
        """Generate a response about a specific retailer's GPU sourcing strategy."""
        retailer = retailer_name.lower()
        
        if retailer in self.retailer_info:
            info = self.retailer_info[retailer]
            # Randomly pick 2 pieces of information to share
            keys = list(info.keys())
            random.shuffle(keys)
            selected_keys = keys[:2]
            
            response = f"For {retailer_name.title()} GPU sourcing: "
            response += " ".join([info[key] for key in selected_keys]) + "."
            return response
        else:
            return f"I don't have specific information about {retailer_name} GPU sourcing strategies."
    
    def generate_availability_response(self, availability_data: Dict[str, Any]) -> str:
        """Generate a response based on current GPU availability data."""
        if not availability_data or sum(len(items) for items in availability_data.values()) == 0:
            return ("I don't see any RTX 5080 or 5090 GPUs in stock right now. "
                    "Stock typically goes quickly when available. I recommend setting "
                    "up alerts with the monitoring feature of this application.")
        
        # Format response based on what's available
        response = "Good news! I found some GPU availability:\n\n"
        
        for retailer, items in availability_data.items():
            if items:
                response += f"• {retailer.title()}: {len(items)} model(s) available\n"
                for item in items[:2]:  # Show at most 2 items per retailer
                    response += f"  - {item['name']}: {item.get('price', 'Price not listed')}\n"
                if len(items) > 2:
                    response += f"  - ...and {len(items)-2} more\n"
        
        response += "\nThese can sell out quickly, so act fast if interested!"
        return response
    
    def generate_priority_access_response(self, priority_data: List[Dict[str, Any]]) -> str:
        """Generate a response about current NVIDIA priority access information."""
        if not priority_data:
            return self.knowledge_base["priority_access"]
        
        response = "Here's the latest on NVIDIA's Priority Access Program:\n\n"
        
        for item in priority_data[:3]:  # Show at most 3 items
            response += f"• {item['title']}\n"
            if 'analysis' in item:
                response += f"  {item['analysis']}\n"
        
        response += "\nCheck your email regularly if you're registered with NVIDIA. Priority access invitations are sent directly."
        return response