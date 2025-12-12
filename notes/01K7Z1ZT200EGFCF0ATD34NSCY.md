---
title: LangChain 中 qwen embeddings 使用 openai embeddings 兼容性问题
tags:
  - langchain
  - embeddings
date: 2025-10-20
---

使用本地 embddings 遇到如下问题：

```python
qwen3_embdings = OpenAIEmbeddings(
    model="text-embedding-qwen3-embedding-0.6b",
    base_url="http://127.0.0.1:1234/v1",
)
```

运行时报错：

```
Traceback (most recent call last):
  File "/Users/zhaochunqi/ghq/github.com/zhaochunqi/ai-agents-learning/main.py", line 20, in <module>
    _ = vector_store.add_documents(documents=all_splits)
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/zhaochunqi/ghq/github.com/zhaochunqi/ai-agents-learning/.venv/lib/python3.12/site-packages/langchain_core/vectorstores/in_memory.py", line 195, in add_documents
    vectors = self.embedding.embed_documents(texts)
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/zhaochunqi/ghq/github.com/zhaochunqi/ai-agents-learning/.venv/lib/python3.12/site-packages/langchain_openai/embeddings/base.py", line 590, in embed_documents
    return self._get_len_safe_embeddings(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/zhaochunqi/ghq/github.com/zhaochunqi/ai-agents-learning/.venv/lib/python3.12/site-packages/langchain_openai/embeddings/base.py", line 480, in _get_len_safe_embeddings
    response = self.client.create(
               ^^^^^^^^^^^^^^^^^^^
  File "/Users/zhaochunqi/ghq/github.com/zhaochunqi/ai-agents-learning/.venv/lib/python3.12/site-packages/openai/resources/embeddings.py", line 132, in create
    return self._post(
           ^^^^^^^^^^^
  File "/Users/zhaochunqi/ghq/github.com/zhaochunqi/ai-agents-learning/.venv/lib/python3.12/site-packages/openai/_base_client.py", line 1259, in post
    return cast(ResponseT, self.request(cast_to, opts, stream=stream, stream_cls=stream_cls))
                           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/zhaochunqi/ghq/github.com/zhaochunqi/ai-agents-learning/.venv/lib/python3.12/site-packages/openai/_base_client.py", line 1047, in request
    raise self._make_status_error_from_response(err.response) from None
openai.BadRequestError: Error code: 400 - {'error': "'input' field must be a string or an array of strings"}
```

添加 `check_embedding_ctx_length` 参数即可

```python
qwen3_embdings = OpenAIEmbeddings(
    model="text-embedding-qwen3-embedding-0.6b",
    base_url="http://127.0.0.1:1234/v1",
    check_embedding_ctx_length=False,  # 关键：禁用长度检查以兼容 LM Studio
)
```

原因是这个参数默认 True, LangChain 会检查输入文本是否超过模型的最大上下文长度，如果文本太长，会被分割成多个 chunk，这样向 api 发送的是 token 数组，不是原始的字符串。


### 具体的执行流程差异：

#### 默认情况 (`True`) - 会出错的流程：
```python
# 输入："Hello world"
# 1. tiktoken 处理：[15496, 1917] (token IDs)
# 2. API 请求：{"input": [15496, 1917], "model": "..."}
# 3. LM Studio 收到整数数组，报错："'input' field must be a string"
```

#### 设为 `False` 后 - 正常的流程：
```python
# 输入："Hello world" 
# 1. 直接发送：{"input": "Hello world", "model": "..."}
# 2. LM Studio 收到字符串，正常处理
```
