import praw
import time
import re
from datetime import datetime, timedelta

class RedditMonitor:
    """Monitor Reddit for GPU availability information."""
    
    def __init__(self, ai_agent):
        self.name = "Reddit"
        self.ai_agent = ai_agent
        self.subreddits = ["nvidia", "buildapcsales"]
        self.reddit = self._setup_reddit()
        self.last_check = datetime.now() - timedelta(days=1)  # Start by checking posts from last 24h
        self.priority_keywords = [
            "priority access", "priority program", "purchase program", 
            "RTX 5080", "RTX 5090", "drawing", "lottery",
            "nvidia official", "founders edition", "fe", "queue"
        ]
        
    def _setup_reddit(self):
        """Set up the Reddit API client."""
        try:
            # Initialize with read-only access if no credentials provided
            return praw.Reddit(
                client_id=os.getenv("REDDIT_CLIENT_ID", ""),
                client_secret=os.getenv("REDDIT_CLIENT_SECRET", ""),
                user_agent="GPU_Monitor Bot v1.0 (by u/YourUsername)",
                check_for_async=False
            )
        except Exception as e:
            print(f"Error setting up Reddit API: {e}")
            print("Continuing with limited Reddit functionality")
            # Return a minimal placeholder that won't cause further errors
            return None
            
    def check_for_updates(self):
        """Check Reddit for new information about GPU availability programs."""
        if not self.reddit:
            return []
            
        relevant_posts = []
        current_time = datetime.now()
        
        try:
            for subreddit_name in self.subreddits:
                subreddit = self.reddit.subreddit(subreddit_name)
                
                # Check hot posts first (most likely to contain important announcements)
                for post in subreddit.hot(limit=20):
                    # Skip posts we've already seen
                    post_time = datetime.fromtimestamp(post.created_utc)
                    if post_time <= self.last_check:
                        continue
                        
                    # Check for priority access related keywords
                    if any(keyword.lower() in post.title.lower() for keyword in self.priority_keywords):
                        # Use AI agent to evaluate relevance
                        post_content = f"Title: {post.title}\nContent: {post.selftext[:1000]}"
                        
                        evaluation = self.ai_agent.process_text(
                            f"Is this Reddit post discussing NVIDIA GPU purchase opportunities, " 
                            f"priority access programs, or drawings to buy RTX 5080/5090? "
                            f"Post content: {post_content}"
                        )
                        
                        # If AI thinks it's relevant, add it to results
                        if "yes" in str(evaluation).lower() or "relevant" in str(evaluation).lower():
                            relevant_posts.append({
                                "title": post.title,
                                "url": f"https://reddit.com{post.permalink}",
                                "created": post_time.strftime("%Y-%m-%d %H:%M"),
                                "author": post.author.name if post.author else "[deleted]",
                                "score": post.score,
                                "subreddit": subreddit_name
                            })
                
                # Also check new posts for very recent info
                for post in subreddit.new(limit=30):
                    # Skip posts we've already seen
                    post_time = datetime.fromtimestamp(post.created_utc)
                    if post_time <= self.last_check:
                        continue
                        
                    # Check for priority access related keywords
                    if any(keyword.lower() in post.title.lower() for keyword in self.priority_keywords):
                        # For new posts, we'll include all that match keywords without AI filtering
                        # since they might not have enough content yet for proper evaluation
                        relevant_posts.append({
                            "title": post.title,
                            "url": f"https://reddit.com{post.permalink}",
                            "created": post_time.strftime("%Y-%m-%d %H:%M"),
                            "author": post.author.name if post.author else "[deleted]",
                            "score": post.score,
                            "subreddit": subreddit_name,
                            "type": "new_post"
                        })
                
            # Update last check time
            self.last_check = current_time
            return relevant_posts
            
        except Exception as e:
            print(f"Error checking Reddit: {e}")
            return []
            
    def check_nvidia_priority_access(self):
        """Specifically check for NVIDIA Priority Access Program information."""
        if not self.reddit:
            return None
            
        priority_info = []
        current_time = datetime.now()
        
        try:
            # Check both subreddits with more specific search
            for subreddit_name in self.subreddits:
                subreddit = self.reddit.subreddit(subreddit_name)
                
                # Search for priority access posts in the past week
                for post in subreddit.search("NVIDIA priority access OR priority program", sort="new", time_filter="week"):
                    post_time = datetime.fromtimestamp(post.created_utc)
                    
                    # Use AI to extract detailed information
                    post_content = f"Title: {post.title}\nContent: {post.selftext[:2000]}"
                    
                    analysis = self.ai_agent.process_input(
                        "Extract information about NVIDIA Priority Access Program or drawing details for RTX 5080/5090",
                        {
                            "text": post_content,
                            "html": None
                        }
                    )
                    
                    # Add the analyzed information
                    priority_info.append({
                        "title": post.title,
                        "url": f"https://reddit.com{post.permalink}",
                        "created": post_time.strftime("%Y-%m-%d %H:%M"),
                        "analysis": analysis.get("text", "No analysis available"),
                        "score": post.score,
                        "subreddit": subreddit_name
                    })
            
            return priority_info
            
        except Exception as e:
            print(f"Error checking for NVIDIA Priority Access: {e}")
            return []