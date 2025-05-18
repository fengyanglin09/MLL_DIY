import logging
from enum import Enum
from typing import Annotated

import sqlalchemy
from fastapi import APIRouter, Depends, HTTPException, Request

from storeapi.configs.jwt_conf import oauth2_scheme
from storeapi.configs.security_conf import get_current_user
from storeapi.database.database import comment_table, database, post_table, like_table
from storeapi.models.post import (Comment, CommentIn, PostLike, PostLikeIn,
                                  UserPost, UserPostIn, UserPostWithComments, UserPostWithLikes)
from storeapi.models.user import User

router = APIRouter()


logger = logging.getLogger(__name__)


select_post_and_likes = (
    sqlalchemy.select(post_table, sqlalchemy.func.count(like_table.c.id).label("likes"))
    .select_from(post_table.outerjoin(like_table))
    .group_by(post_table.c.id)
)


async def find_post(post_id: int):
    query = post_table.select().where(post_table.c.id == post_id)
    return await database.fetch_one(query)


@router.get("/", status_code=200)
async def read_root():
    return {"message": "Welcome to the Store API!"}


@router.post("/post", response_model=UserPost, status_code=201)
async def create_post(post: UserPostIn, current_user: Annotated[User, Depends(get_current_user)]):

    logger.info("Creating post with body: %s", post.body)

    # current_user = await get_current_user(await oauth2_scheme(request))

    data = {**post.model_dump(), "user_id": current_user.id}
    query = post_table.insert().values(**data)
    last_record_id = await database.execute(query)
    return {**data, "id": last_record_id}


class PostSorting(str, Enum):
    new = "new"
    old = "old"
    most_likes = "most_likes"


@router.get("/post", response_model=list[UserPostWithLikes], status_code=200)
async def get_all_posts(sorting: PostSorting = PostSorting.new):

    logger.info("Fetching all posts with sorting: %s", sorting)

    if sorting == PostSorting.new:
        query = select_post_and_likes.order_by(post_table.c.id.desc())

    elif sorting == PostSorting.old:
        query = select_post_and_likes.order_by(post_table.c.id.asc())

    elif sorting == PostSorting.most_likes:
        query = select_post_and_likes.order_by(sqlalchemy.desc("likes"))

    logger.debug(query)
    return await database.fetch_all(query)


@router.post("/comment", response_model=Comment)
async def create_comment(comment: CommentIn, current_user: Annotated[User, Depends(get_current_user)]):

    logger.info("Creating comment with body: %s", comment.body)
    # current_user = await get_current_user(await oauth2_scheme(request))

    post = await find_post(comment.post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    data = {**comment.model_dump(), "user_id": current_user.id}
    query = comment_table.insert().values(**data)
    last_record_id = await database.execute(query)
    return {**data, "id": last_record_id}


@router.get("/post/{post_id}/comment", response_model=list[Comment])
async def get_comments_on_post(post_id: int):
    query = comment_table.select().where(comment_table.c.post_id == post_id)
    return await database.fetch_all(query)


@router.get("/post/{post_id}", response_model=UserPostWithComments)
async def get_post_with_comments(post_id: int):

    logger.info("Fetching post with id: %s", post_id)

    query = select_post_and_likes.where(post_table.c.id == post_id)

    logger.debug(query)

    post = await database.fetch_one(query)

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    comments = await get_comments_on_post(post_id)
    return UserPostWithComments(**post, comments=comments)



@router.post("/like", response_model=PostLike, status_code=201)
async def like_post(post_like: PostLikeIn, current_user: Annotated[User, Depends(get_current_user)]):

    logger.info("Liking post with id: %s", post_like.post_id)
    # current_user = await get_current_user(await oauth2_scheme(request))

    post = await find_post(post_like.post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    data = {**post_like.model_dump(), "user_id": current_user.id}
    query = like_table.insert().values(**data)
    logger.debug(query)
    last_record_id = await database.execute(query)
    return {**data, "id": last_record_id}