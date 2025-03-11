def get_current_time():
    """Return the current time in a formatted string."""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def log_message(message):
    """Log a message with a timestamp."""
    current_time = get_current_time()
    print(f"[{current_time}] {message}")

def calculate_jitter(interval):
    """Calculate a jittered interval for sleep."""
    import random
    jitter = random.uniform(0.9, 1.1)
    return int(interval * jitter)

def clear_browser_cache(driver):
    """Clear the browser cache and cookies."""
    driver.execute_script("window.localStorage.clear();")
    driver.execute_script("window.sessionStorage.clear();")
    driver.delete_all_cookies()