// 这是记录在控制台里运行的代码

// myFrame = window.frames[0];
// Window { window: Window, self: Window, document: document, name: 'uxtabiframe-1040-frame', location: Location, … }
// console.log(myFrame);
// undefined
// 在iframe里找到下拉框
let dropDownBtn = document.querySelector('#uxfilteroperator-1251');
// undefined
// 点击下拉
dropDownBtn.click();
// undefined
// 在iframe里找到下拉框里的选项
// document.querySelectorAll('.x-menu')
// <=选项
let lessThanorEquals = document.querySelector('#menuitem-1256');
// 点击
lessThanorEquals.click();

let inputBoxDate = document.querySelector('#uxdate-1261-inputEl');

if (inputBoxDate) {
    inputBoxDate.value = '2025-08-06'

    // 触发输入事件
    inputBoxDate.dispatchEvent(new Event('input', { bubbles: true }));
    inputBoxDate.dispatchEvent(new Event('change', { bubbles: true }));

    // 模拟用户按下 Enter 键
    ['keydown', 'keypress', 'keyup'].forEach(type => {
        const keyboardEvent = new KeyboardEvent(type, {
            key: 'Enter',
            code: 'Enter',
            keyCode: 13,
            which: 13,
            bubbles: true,
            cancelable: true
        });
        inputBoxDate.dispatchEvent(keyboardEvent);
    });
} else {
    console.log('❌ 找不到 input 框');
}

//  左下角的工单数量    ---有问题  document.querySelector('').innerText 正常反馈，但是let  woNumber = document.querySelector(').innerText;  获取不到