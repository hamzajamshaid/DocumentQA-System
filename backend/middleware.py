from flask import request, jsonify
from functools import wraps
from datetime import datetime, timedelta
import threading

class RateLimiter:
    def __init__(self, max_requests=100, time_window=60):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = {}
        self.lock = threading.Lock()
    
    def is_allowed(self, key):
        with self.lock:
            now = datetime.now()
            
            if key not in self.requests:
                self.requests[key] = []
            
            self.requests[key] = [
                req_time for req_time in self.requests[key]
                if now - req_time < timedelta(seconds=self.time_window)
            ]
            
            if len(self.requests[key]) < self.max_requests:
                self.requests[key].append(now)
                return True
            
            return False

limiter = RateLimiter(max_requests=100, time_window=60)

def rate_limit(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        key = request.remote_addr
        
        if not limiter.is_allowed(key):
            return jsonify({'error': 'Rate limit exceeded'}), 429
        
        return f(*args, **kwargs)
    
    return decorated_function

