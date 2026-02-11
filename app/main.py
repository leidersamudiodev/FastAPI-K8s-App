from fastapi import FastAPI
import redis
import os
import psycopg2

app = FastAPI()
r = redis.Redis(host=os.getenv("REDIS_HOST", "redis"), port=6379)

@app.get("/")
def read_root():
    r.incr("hits")
    return {"message": "Hello World", "hits": int(r.get("hits") or 0)}

@app.get("/db")
def db_check():
    conn = psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "postgres"),
        dbname=os.getenv("POSTGRES_DB", "testdb"),
        user=os.getenv("POSTGRES_USER", "postgres"),
        password=os.getenv("POSTGRES_PASSWORD", "postgres"),
    )
    cur = conn.cursor()
    cur.execute("SELECT 1")
    cur.close()
    conn.close()
    return {"db": "ok"}