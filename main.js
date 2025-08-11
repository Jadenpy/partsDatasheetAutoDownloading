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



// 对第一个工单进行操作   '#tableview-1103-record-452 > tbody > tr'      规律   #tableview-1103-record-453    #tableview-1103-record-454  #tableview-1103-record-455    ....... #tableview-1103-record-465
// 问题： 1.  获取的规律
//        2.  #tableview下的结构
//        3.  #tableview-1103 > div.x-grid-item-container  这个容器下有多少个tabview(工单)
// 双击  '#tableview-1103-record-452 > tbody > tr'
const el = document.querySelector('#tableview-1103-record-452 > tbody > tr');
if (el) {
    const dblClickEvent = new MouseEvent('dblclick', {
        bubbles: true,
        cancelable: true,
        view: window
    });
    el.dispatchEvent(dblClickEvent);
} else {
    console.log('❌ 没找到元素');
}

// 获取工时  #uxnumber-1425-inputEl


//待工单展开后，点击 book labor 标签     #tab-1166-btnInnerEl
const el = document.querySelector('#tab-1166-btnInnerEl');  // 或任何选择器
if (el) {
    const clickEvent = new MouseEvent('click', {
        bubbles: true,
        cancelable: true,
        view: window
    });
    el.dispatchEvent(clickEvent);
    console.log('✅ 已模拟点击该 span');
} else {
    console.log('❌ 没找到目标 span 元素');
}

// 输入工单执行的 详细信息
// 输入人员姓名   #lovmultiselectfield-2388-inputEl  输入之前的工单所属人员
const input = document.querySelector('#lovmultiselectfield-2388-inputEl'); // 替换成你的选择器

if (input) {
    input.value = 'HXSH'; // 设置值
};   // 这里估计要回车一下
// 输入工时     #uxnumber-2391-inputEl   输入值为之前的获取的工单的工时
const input = document.querySelector('#uxnumber-2391-inputEl'); // 替换成你的选择器

if (input) {
    input.value = '0.5'; // 设置值
};
// 输入日期    #uxdate-2392-inputEl
const input = document.querySelector('#uxdate-2392-inputEl'); // 替换成你的选择器

if (input) {
    input.value = '2025-08-06'; // 设置值
};

// 信息输入完成，点击保存按钮    #button-2373-btnIconEl
const span = document.querySelector('#button-2373-btnIconEl');  // 替换成真实选择器
if (span) {
    const clickEvent = new MouseEvent('click', {
        bubbles: true,
        cancelable: true,
        view: window
    });
    span.dispatchEvent(clickEvent);

    console.log('✅ 已模拟点击 span 元素');
} else {
    console.log('❌ 没找到 span 元素');
};

// 保存完成，待反馈，是否有提示无效的项目      #dataview-1011 > div > div > h6       错误文本：No valid Rate exists for this Department, Trade, Date Worked, and Occupation Type. Continue?
// 如果有这个，则代表输入有不合规的

// 如果没有这个，则代表输入合规，可以继续



