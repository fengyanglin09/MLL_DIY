import pytest
import pytest_mock
from httpx import AsyncClient

from storeapi.configs import jwt_conf, security_conf


async def create_post(body: str, async_client: AsyncClient, logged_in_token: str) -> dict:
    response = await async_client.post(
        "/post",
        json={"body": body},
        headers={"Authorization": f"Bearer {logged_in_token}"},
    )
    return response.json()


async def create_comment(body: str, post_id: int, async_client: AsyncClient, logged_in_token: str) -> dict:
    response = await async_client.post(
        "/comment",
        json={"body": body, "post_id": post_id},
        headers={"Authorization": f"Bearer {logged_in_token}"},
    )
    return response.json()


async def like_post(
    post_id: int, async_client: AsyncClient, logged_in_token: str
):
    response = await async_client.post(
        "/like",
        json={"post_id": post_id},
        headers={"Authorization": f"Bearer {logged_in_token}"},
    )
    return response



@pytest.fixture
async def created_post(async_client: AsyncClient, logged_in_token: str) -> dict:
    post = await create_post("Test Post", async_client, logged_in_token)
    return {**post, "likes": 0}


@pytest.fixture
async def created_comment(async_client: AsyncClient, created_post: dict, logged_in_token: str) -> dict:
    comment = await create_comment("Test Comment", created_post["id"], async_client, logged_in_token)
    return comment



@pytest.mark.anyio
@pytest.mark.parametrize(
    "sorting, expected_order",
    [
        ("new", [2, 1]),
        ("old", [1, 2]),
    ]
)
async def test_get_all_posts_sorting(async_client: AsyncClient, logged_in_token: str, sorting: str, expected_order: list[int]):
    await create_post("Test Post 1", async_client, logged_in_token)
    await create_post("Test Post 2", async_client, logged_in_token)
    response = await async_client.get("/post", params={"sorting": sorting})
    assert response.status_code == 200

    data = response.json()

    assert [post["id"] for post in data] == expected_order


@pytest.mark.anyio
async def test_get_all_posts_sort_likes(
    async_client: AsyncClient, logged_in_token: str
):
    post1 = await create_post("Test Post 1", async_client, logged_in_token)
    post2 = await create_post("Test Post 2", async_client, logged_in_token)
    await like_post(post1["id"], async_client, logged_in_token)
    response = await async_client.get("/post", params={"sorting": "most_likes"})
    assert response.status_code == 200

    data = response.json()

    assert [post["id"] for post in data] == [post1["id"], post2["id"]]


@pytest.mark.anyio
async def test_get_all_posts_wrong_sorting(
    async_client: AsyncClient, logged_in_token: str
):
    await create_post("Test Post 1", async_client, logged_in_token)
    await create_post("Test Post 2", async_client, logged_in_token)
    response = await async_client.get("/post", params={"sorting": "wrong_sorting"})
    print(f"hahahaha - {response.json()}")
    assert response.status_code == 422


@pytest.mark.anyio
async def test_like_post(
    async_client: AsyncClient, created_post: dict, logged_in_token: str
):
    response = await like_post(created_post["id"], async_client, logged_in_token)
    assert response.status_code == 201


@pytest.mark.anyio
async def test_get_post_with_comments(
    async_client: AsyncClient, created_post: dict, created_comment: dict
):
    response = await async_client.get(f"/post/{created_post['id']}/comment")
    assert response.status_code == 200
    assert response.json() == [created_comment]



@pytest.mark.anyio
async def test_create_post(async_client: AsyncClient, logged_in_token: str, registered_user: dict):
    body = "Test Post"

    response = await async_client.post(
        "/post",
        json={"body": body, "user_id": registered_user["id"]},
        headers={"Authorization": f"Bearer {logged_in_token}"},
    )

    assert response.status_code == 201
    assert {"id": 1,
            "body": body,
            "user_id": registered_user["id"]
            }.items() <= response.json().items()


@pytest.mark.anyio
async def test_create_post_expired_token(
    async_client: AsyncClient, registered_user: dict, mocker: pytest_mock.MockerFixture):
    # Mock the token expiration
    mocker.patch("storeapi.configs.jwt_conf.access_token_expires", return_value=-1)

    token = jwt_conf.create_access_token(registered_user["email"])

    response = await async_client.post(
        "/post",
        json={"body": "Test Post"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 401
    assert "Token has expired" in response.json()["detail"]



@pytest.mark.anyio
async def test_read_root(async_client):
    response = await async_client.get("/")
    assert response.status_code == 200


@pytest.mark.anyio
async def test_create_post_missing_data(async_client: AsyncClient, logged_in_token: str):
    response = await async_client.post(
        "/post",
        json={},
        headers={"Authorization": f"Bearer {logged_in_token}"},
    )
    assert response.status_code == 422


@pytest.mark.anyio
async def test_get_all_posts(async_client: AsyncClient, created_post: dict):
    response = await async_client.get("/post")

    assert response.status_code == 200
    assert response.json() <= [created_post]


@pytest.mark.anyio
async def test_create_comment(async_client: AsyncClient, created_post: dict, logged_in_token: str, registered_user: dict):
    body = "Test Comment"
    response = await async_client.post(
        "/comment",
        json={"body": body, "post_id": created_post["id"], "user_id": registered_user["id"]},
        headers={"Authorization": f"Bearer {logged_in_token}"},
    )
    assert response.status_code == 200
    assert {
        "id": 1,
        "body": body,
        "post_id": created_post["id"],
        "user_id": registered_user["id"],
    }.items() <= response.json().items()


@pytest.mark.anyio
async def test_get_comments_on_post(
    async_client: AsyncClient, created_post: dict, created_comment: dict
):
    response = await async_client.get(f"/post/{created_post['id']}/comment")

    assert response.status_code == 200
    assert response.json() == [created_comment]


@pytest.mark.anyio
async def test_get_comments_on_post_empty(
    async_client: AsyncClient, created_post: dict
):
    response = await async_client.get(f"/post/{created_post['id']}/comment")

    assert response.status_code == 200
    assert response.json() == []



