# 基于 Pytest 的接口测试实践（个人练习）

选取公开 API 作为被测对象，使用 **Postman** 完成接口请求调试与断言设计，使用 **Python + requests + Pytest** 编写并执行接口测试用例，使用 **Fiddler/Charles** 抓包验证接口实际行为与预期一致。

## 一、被测系统

| 被测系统 | 用途 | 地址 |
|---|---|---|
| jsonplaceholder | 带业务字段的假数据 REST 接口，用于正常/异常/边界参数 + 字段断言 | https://jsonplaceholder.typicode.com |
| httpbin | 专为测试设计的接口，用于请求回显 + 状态码校验 | https://httpbin.org |

> 均为公开、免费、免 Token 接口。

## 二、技术栈

- Python 3.12
- requests：发送 HTTP 请求
- Pytest + pytest-html：用例组织、参数化、执行与 HTML 报告
- Postman：接口调试与断言设计
- Fiddler / Charles：抓包分析

## 三、目录结构

```
api-test-pytest/
├── README.md
├── config.py                 # 被测接口地址常量
├── conftest.py               # 全局 fixture（复用 Session）
├── pytest.ini                # pytest 配置（自动生成 HTML 报告）
├── requirements.txt
├── testcases/
│   ├── test_jsonplaceholder.py
│   └── test_httpbin.py
├── postman/
│   └── api-test.postman_collection.json   # 可导入 Postman 的集合
├── docs/
│   └── 抓包验证.md
└── reports/
    └── report.html           # pytest-html 生成的测试报告
```

## 四、用例设计（正常 / 异常 / 边界）

| 编号 | 接口 | 场景 | 参数 | 预期状态码 | 断言 |
|---|---|---|---|---|---|
| TC01 | GET /posts/{id} | 正常 | id=1、100 | 200 | 返回对象，`id` 与请求一致 |
| TC02 | GET /posts/{id} | 边界·越界 | id=0、101、-1 | 404 | — |
| TC03 | GET /posts/{id} | 异常·类型错 | id=abc | 404 | — |
| TC04 | GET /posts | 正常 | — | 200 | 数组，长度 100 |
| TC05 | POST /posts | 正常 | 合法 JSON | 201 | 返回 `id=101` |
| TC06 | POST /posts | 异常·缺字段 | 空 body | 201 | mock 不校验，记录行为 |
| TC07 | GET /get?a=1 | 正常 | a=1 | 200 | `args.a == "1"` |
| TC08 | GET /status/{code} | 状态码 | 200/201/404/500 | 对应码 | — |
| TC09 | POST /post | 正常 | JSON body | 200 | `json` 字段回显请求体 |

字段断言覆盖：`id` / `userId`（int）、`title` / `body`（str）。

## 五、快速开始

```bash
# 1. 安装依赖（Windows 下建议加 PYTHONUTF8=1 避免编码报错）
PYTHONUTF8=1 pip install -r requirements.txt

# 2. 运行测试（自动生成 reports/report.html）
pytest
```

## 六、Postman 调试与断言

1. 打开 Postman → Import → 选择 `postman/api-test.postman_collection.json`。
2. 逐个请求点 Send，右侧 Tests 标签页查看断言结果。
3. 或对整个 Collection 点 Run，一次跑完全部用例。

## 七、抓包验证

见 [docs/抓包验证.md](docs/抓包验证.md)。

## 八、测试结果（实测）

本机 `pytest` 执行结果：**15 passed in 7.74s**，0 失败。HTML 报告见 [reports/report.html](reports/report.html)。
