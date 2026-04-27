---
title: "Workflowy 的 inline editing 实现"
display: true
tags:
  - css
  - html
  - javascript
  - workflowy
date: 2026-04-27
---

Workflowy 早期的 inline editing 不是直接用 `contenteditable`，而是把一个透明的 `textarea` 精确覆盖在当前 hover 的文本上，点击后再切换可见层。

实现思路：

1. 页面上正常渲染文本内容。
2. 鼠标 hover 某一项时，把一个 `opacity: 0` 的 `textarea` 移动到这段文本上方。
3. 点击时 focus `textarea`，把 `textarea` 设为 `opacity: 1`，同时把底层文本设为 `opacity: 0`。
4. 输入时同步 `textarea.value` 到底层渲染节点。
5. blur 后恢复底层文本显示，隐藏编辑框。

这样做的好处是输入、选区、键盘行为都交给原生 `textarea` 处理，同时显示层仍可以自己控制高亮、链接、tag 等富文本效果。

```html
<!doctype html>
<meta charset="utf-8" />
<style>
  .item {
    position: relative;
    padding: 4px 8px;
    font: 16px/1.5 system-ui, sans-serif;
    white-space: pre-wrap;
  }

  #editor {
    position: absolute;
    z-index: 10;
    opacity: 0;
    resize: none;
    overflow: hidden;
    border: 0;
    padding: 4px 8px;
    margin: 0;
    font: 16px/1.5 system-ui, sans-serif;
    background: transparent;
    outline: none;
  }
</style>

<div class="item">Buy milk #todo</div>
<div class="item">Read https://example.com</div>
<textarea id="editor"></textarea>

<script>
  const editor = document.querySelector('#editor');
  let currentItem = null;

  document.querySelectorAll('.item').forEach((item) => {
    item.addEventListener('mouseenter', () => {
      if (document.activeElement === editor) return;
      moveEditorOver(item);
    });
  });

  function moveEditorOver(item) {
    currentItem = item;
    const rect = item.getBoundingClientRect();

    editor.value = item.textContent;
    editor.style.left = `${rect.left + window.scrollX}px`;
    editor.style.top = `${rect.top + window.scrollY}px`;
    editor.style.width = `${rect.width}px`;
    editor.style.height = `${rect.height}px`;
    editor.style.opacity = 0;
  }

  editor.addEventListener('mousedown', () => {
    if (!currentItem) return;
    currentItem.style.opacity = 0;
    editor.style.opacity = 1;
  });

  editor.addEventListener('input', () => {
    if (!currentItem) return;
    currentItem.textContent = editor.value;
  });

  editor.addEventListener('blur', () => {
    if (!currentItem) return;
    currentItem.style.opacity = 1;
    editor.style.opacity = 0;
  });
</script>
```

来源：[How does workflowy implemented inline editing?](https://stackoverflow.com/questions/10510217/how-does-workflowy-implemented-inline-editing)
