"""Pytest 全局夹具：复用 HTTP Session，降低握手开销。"""

import pytest
import requests


@pytest.fixture(scope="session")
def client():
    """提供一个复用的 requests.Session。

    如需用 Charles/Fiddler 抓取 Python 发出的请求，取消下面两行注释：
    # session.proxies = {"http": "http://127.0.0.1:8888", "https": "http://127.0.0.1:8888"}
    # session.verify = False
    """
    session = requests.Session()
    session.headers.update({"User-Agent": "api-test-pytest/1.0"})
    yield session
    session.close()
