# reta_limit.py
import time
from fastapi import Request, HTTPException

# 简单漏桶：每IP每分钟最多 N 次
class RateLimiter:
    def __init__(self, max_per_min: int = 30):
        self.max = max_per_min
        self.bucket: dict[str, list[float]] = {}

    async def __call__(self, request: Request, call_next):
        ip = request.client.host if request.client else "unknown"
        now = time.time()
        window = 60.0
        self.bucket.setdefault(ip, [])
        # 清理过期
        self.bucket[ip] = [t for t in self.bucket[ip] if now - t < window]
        if len(self.bucket[ip]) >= self.max:
            raise HTTPException(status_code=429, detail="Too many requests")
        self.bucket[ip].append(now)
        return await call_next(request)