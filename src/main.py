from dotenv import load_dotenv
import os
import sys
import argparse
from src.monitor import GPUMonitor
from src.notification import NotificationManager
from src.ai_agent.multimodal_agent import MultimodalAgent
from src.chatbot.gpu_sourcing_chatbot import GPUSourcingChatbot

# Retailer check intervals (seconds)
INTENSIVE_CHECK_INTERVAL=60
NORMAL_CHECK_INTERVAL=300
EXTENDED_CHECK_INTERVAL=3600
REDDIT_CHECK_INTERVAL=1800

# Reddit API credentials (for Reddit monitoring)
REDDIT_CLIENT_ID=os.getenv("REDDIT_CLIENT_ID", "your_client_id")
REDDIT_CLIENT_SECRET=os.getenv("REDDIT_CLIENT_SECRET", "your_client_secret")

def main():
    parser = argparse.ArgumentParser(description="GPU Stock Monitor with Chatbot Assistant")
    parser.add_argument("--chatbot", action="store_true", help="Start in chatbot mode")
    args = parser.parse_args()
    
    # Load environment variables
    load_dotenv()
    
    if args.chatbot:
        print("Starting GPU Sourcing Chatbot...")
        chatbot = GPUSourcingChatbot()
        try:
            chatbot.start()
        except KeyboardInterrupt:
            print("\nChatbot stopped by user")
        except Exception as e:
            print(f"Fatal error: {e}")
        finally:
            print("Cleaning up resources...")
            chatbot.cleanup()
    else:
        print("Starting GPU Stock Monitor...")
        
        # Initialize the notification manager
        notification_manager = NotificationManager()
        
        # Initialize the stock monitor with AI agent
        ai_agent = MultimodalAgent()
        monitor = GPUMonitor(notification_manager, ai_agent)
        
        try:
            monitor.monitor_stock()
        except KeyboardInterrupt:
            print("\nMonitoring stopped by user")
        except Exception as e:
            print(f"Fatal error: {e}")
        finally:
            print("Cleaning up resources...")
            monitor.cleanup()

if __name__ == "__main__":
    main()
