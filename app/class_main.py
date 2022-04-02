from charset_normalizer import from_bytes
from fastapi import Body, FastAPI, Response, status, HTTPException
from typing import Optional
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

######################
# Send data and consume it
# Example request body
# {
#     "title": "My Title",
#     "content": "This is my Content"
# }

# @app.post("/posts")
# def create_posts(payload: dict = Body(...)):
#     # print(payload)
#     return {'new_post': f"{payload['title']} - {payload['content']}"}

# Posts mock DB
# my_posts = [
#     {"title": "First Post",
#      "content": "The first post is always",
#      "truth": True,
#      "id": 1},
#     {"title": "Second Post",
#      "content": "The second post is always",
#      "truth": False,
#      "id": 2}
# ]

# Enforcing structure in post methods
class Post(BaseModel):
    title: str
    content: str
    published: bool = True


db_conn_check = True
while db_conn_check:
    try:
        conn = psycopg2.connect(host='172.17.0.2', 
                                database='fastapi_db', 
                                user='postgres', 
                                password='mysecretpassword',
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Connection was succesfull!")
        db_conn_check = False
    except Exception as err:
        print(f"{Exception}: {err}")
        time.sleep(2)

@app.get("/")
def root():
    return {"message": "Hello World!!!!"}

@app.get("/posts")
def get_post():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts}

# GET SINGLE POST WITH DB
@app.get("/posts/{id}")
def get_posts(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s """,
                   (str(id)))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
    
    return {"result": post}

# GET SINGLE POST WITHOUT DB
# # Another way with HTTPException method from fastapi
# @app.get("/posts/{id}")
# def get_posts(id: int):
#     result_post = {}
#     # cursor.execute("""SELECT * FROM posts""")
#     # posts = cursor.fetchall()
#     for post in posts:
#         if post['id'] == id:
#             result_post = post
#     if not result_post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f'post with id {id} was not found')
        
#     return {"result": result_post}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
                   (post.title, post.content, post.published))
    
    new_post = cursor.fetchone()
    
    conn.commit()
    
    return {'data': new_post}

# One way of doing this
# @app.get("/posts/{id}")
# def get_posts(id: int, response: Response):
#     result_post = {}
#     for post in my_posts:
#         if post['id'] == id:
#             result_post = post
#     if not result_post:
#         response.status_code = status.HTTP_404_NOT_FOUND
#         return {'msg': f'post with id {id} was not found'}
    
#     return {"result": result_post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",
                   (str(id)))
    deleted_post = cursor.fetchone()
    if delete_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id {id} was not found')
    
    conn.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
                   (post.title, post.content, post.published, str(id)))
    
    updated_post = cursor.fetchone()
    
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id {id} was not found')
    else:
        conn.commit()    
        return {"data": updated_post}

