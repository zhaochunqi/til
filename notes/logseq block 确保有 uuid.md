---
tags:
  - logseq
  - uuid
date: 2025-10-21
---
# logseq block 确保有 uuid

logseq 中 api 返回的 uuid 在真实的 block 中未必会有，需要检查是否有 id 这个属性才能够正确获取到：

```python
    def ensure_uuid_property(self, blocks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        updated_blocks = []
        for block in blocks:
            if 'properties' not in block or 'id' not in block['properties']:
                # Logseq block UUID is typically in block['uuid']
                block_uuid = block.get('uuid')
                if block_uuid:
                    print(f"Ensuring uuid property for block: {block_uuid}")
                    self.upsert_block_property(block_uuid, "id", block_uuid)
                    # Update the block in memory for consistency
                    if 'properties' not in block:
                        block['properties'] = {}
                    block['properties']['id'] = block_uuid
            updated_blocks.append(block)
        return updated_blocks
```

参考：https://github.com/vipzhicheng/logseq-plugin-comment-block/blob/8da0b723c2ec4660d2136a6aed213aa022d03113/src/main.ts#L69-L71