"""Rate limiter to prevent API abuse"""
import time
from collections import defaultdict
from typing import Dict

class RateLimiter:
    def __init__(self, max_requests: int = 10, window_seconds: int = 60):
        """
        Simple rate limiter
        
        Args:
            max_requests: Maximum requests allowed in the time window
            window_seconds: Time window in seconds
        """
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: Dict[str, list] = defaultdict(list)
    
    def is_allowed(self, client_id: str) -> bool:
        """Check if request is allowed for this client"""
        now = time.time()
        
        # Clean old requests
        self.requests[client_id] = [
            req_time for req_time in self.requests[client_id]
            if now - req_time < self.window_seconds
        ]
        
        # Check if under limit
        if len(self.requests[client_id]) < self.max_requests:
            self.requests[client_id].append(now)
            return True
        
        return False
    
    def get_wait_time(self, client_id: str) -> float:
        """Get seconds to wait before next request is allowed"""
        if not self.requests[client_id]:
            return 0.0
        
        oldest_request = min(self.requests[client_id])
        wait_time = self.window_seconds - (time.time() - oldest_request)
        return max(0.0, wait_time)

# Global rate limiter instance
rate_limiter = RateLimiter(max_requests=5, window_seconds=60)
