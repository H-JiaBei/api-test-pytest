"""httpbin 用例：查询参数回显、状态码校验、POST 请求体回显。

被测系统：https://httpbin.org
"""

import pytest

from config import HTTPBIN_BASE as BASE


def test_get_echo_query_params(client):
    """正常：GET /get 回显查询参数。"""
    resp = client.get(f"{BASE}/get", params={"a": "1", "b": "2"})
    assert resp.status_code == 200
    args = resp.json()["args"]
    assert args["a"] == "1"
    assert args["b"] == "2"


@pytest.mark.parametrize("code", [200, 201, 404, 500])
def test_status_endpoint(client, code):
    """状态码校验：/status/{code} 返回对应状态码。"""
    resp = client.get(f"{BASE}/status/{code}")
    assert resp.status_code == code


def test_post_echo_json_body(client):
    """正常：POST /post 回显请求体。"""
    payload = {"name": "claude", "n": 1}
    resp = client.post(f"{BASE}/post", json=payload)
    assert resp.status_code == 200
    assert resp.json()["json"] == payload
