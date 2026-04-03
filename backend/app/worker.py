import os
import redis
from rq import Worker, Queue, Connection

redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
redis_conn = redis.from_url(redis_url)

if __name__ == "__main__":
    with Connection(redis_conn):
        worker = Worker(Queue("tickets"))
        print("🚀 Worker started...")
        worker.work()
