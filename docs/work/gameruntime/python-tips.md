# Python 开发技巧

GameRuntime 开发过程中积累的 Python 经验和踩坑记录。

---

## 性能优化

### 异步编程

```python
import asyncio

async def perception_loop():
    """感知层主循环"""
    while True:
        data = await perceive()
        await process(data)
        await asyncio.sleep(0.1)
```

### 类型注解

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Perceptible(Protocol):
    async def perceive(self) -> dict:
        ...
```

## 踩坑记录

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| `asyncio` 任务泄漏 | 未正确取消子任务 | 使用 `asyncio.TaskGroup` |
| 内存泄漏 | 循环引用 | 使用 `weakref` |
| 事件堆积 | 消费速度 < 生产速度 | 引入背压机制 |
