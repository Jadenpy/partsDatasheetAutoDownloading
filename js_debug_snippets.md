# 常用 JS 代码片段（用于人工验证网页元素）

这些代码可直接在浏览器开发者工具（DevTools）的 Console 中执行，用于调试和验证元素行为，适合在 Selenium 自动化前进行手动验证。

---

## 📌 1. 查找元素并查看属性

```javascript
// 通过 ID 查找元素
document.getElementById("your-element-id")

// 通过 class 查找
document.querySelector(".your-class-name")

// 查看元素是否可点击
const el = document.querySelector("#your-id");
el ? console.log("可点击?", !el.disabled && el.offsetParent !== null) : console.log("元素不存在");
```

---

## 🖱 2. 模拟点击元素

```javascript
document.querySelector("#your-button-id").click();
```

---

## ⌨ 3. 设置输入框的值

```javascript
const input = document.querySelector("#your-input-id");
input.value = "test value";
input.dispatchEvent(new Event('input', { bubbles: true }));
```

---

## ⏳ 4. 延迟点击（用于调试延时效果）

```javascript
setTimeout(() => {
    document.querySelector("#your-button-id").click();
}, 1000); // 1秒后点击
```

---

## ✅ 5. 检查元素是否在 iframe 中

```javascript
// 在顶层文档中查找所有 iframe
[...document.querySelectorAll("iframe")].forEach((frame, idx) => {
    console.log(`iframe[${idx}]:`, frame.src);
});
```

---

## 🔍 6. 查看弹窗、alert

```javascript
// 临时禁用 alert，避免弹窗中断调试
window.alert = function(msg){ console.log("Alert called with:", msg); };
```

---

## 📜 7. 打印选中元素的完整 outerHTML

```javascript
console.log(document.querySelector("#your-id").outerHTML);
```

---

> ## 
>     8.  debugger pause
>
> `document.querySelector('#myButton').addEventListener('click', function(e) {     debugger;  // 当点击按钮时，程序暂停     console.log('按钮被点击了'); }); `
>
> ✅ 提示：如果页面反应缓慢，可在浏览器里完全操作完页面并验证成功后，再回到 Python + Selenium 实现自动化。
