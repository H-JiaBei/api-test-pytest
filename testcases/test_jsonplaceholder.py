"""jsonplaceholder 接口用例：正常 / 边界 / 异常参数 + GET/POST + 状态码与字段断言。

被测系统：https://jsonplaceholder.typicode.com
"""

import pytest

from config import JSONPLACEHOLDER_BASE as BASE


# ---------- GET /posts ----------

def test_get_posts_list(client):
    """正常：获取帖子列表返回 200，且为长度 100 的数组。"""
    resp = client.get(f"{BASE}/posts")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) == 100


@pytest.mark.parametrize("post_id", [1, 100])
def test_get_post_valid(client, post_id):
    """正常参数：id 在 [1, 100] 内返回 200，字段类型正确且 id 与请求一致。"""
    resp = client.get(f"{BASE}/posts/{post_id}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == post_id
    assert isinstance(data["userId"], int)
    assert isinstance(data["title"], str)
    assert isinstance(data["body"], str)


@pytest.mark.parametrize("post_id", [0, 101, -1])
def test_get_post_out_of_range(client, post_id):
    """边界值：id 超出 [1, 100] 返回 404。"""
    resp = client.get(f"{BASE}/posts/{post_id}")
    assert resp.status_code == 404


def test_get_post_invalid_type(client):
    """异常参数：非数字 id 返回 404。"""
    resp = client.get(f"{BASE}/posts/abc")
    assert resp.status_code == 404


# ---------- POST /posts ----------

def test_post_create_post(client):
    """正常：合法 JSON 创建帖子返回 201，返回 id=101（mock 固定返回值）。"""
    payload = {"title": "foo", "body": "bar", "userId": 1}
    resp = client.post(f"{BASE}/posts", json=payload)
    assert resp.status_code == 201
    data = resp.json()
    assert data["id"] == 101
    assert data["title"] == payload["title"]
    assert data["body"] == payload["body"]


def test_post_create_empty_body(client):
    """异常：缺必填字段时该 mock 不校验业务规则，仍返回 201 且 id=101（记录实际行为）。"""
    resp = client.post(f"{BASE}/posts", json={})
    assert resp.status_code == 201
    assert resp.json()["id"] == 101
