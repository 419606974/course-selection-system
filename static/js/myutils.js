/**
 * 发送POST请求
 *
 * @param {string} url 请求的URL
 * @param {object} data 请求的数据，以JSON对象形式提供
 * @param {function} successCallback 成功时的回调函数，接收一个参数，为响应的数据
 * @param {function} errorCallback 失败时的回调函数，接收一个参数，为错误信息
 */
function sendPostRequest(url, data, successCallback, errorCallback) {
    // 使用jQuery的ajax方法发送POST请求
    $.ajax({
        url: url, // 请求的URL
        type: 'POST', // 请求类型为POST
        contentType: 'application/json', // 设置发送的数据类型为JSON
        headers: {'Content-Type': 'application/json;charset=UTF-8'}, // 设置请求头，指定字符集为UTF-8
        data: JSON.stringify(data), // 将请求数据转换为JSON字符串
        success: function (data) {
            // 成功时执行回调函数，如果存在的话
            if (successCallback) {
                successCallback(data);
            }
        },
        error: function (error) {
            // 失败时执行回调函数，如果存在的话
            if (errorCallback) {
                errorCallback(error);
            }
        }
    });
}


function accessControl() {
    const permissionIds = localStorage.getItem('permissionIds');
    if (permissionIds) {
        // 将 permissionIds 字符串拆分为数组
        const permissionIdsArray = permissionIds.split(',');

        // 获取所有带有 permission-id 属性的元素
        const elementsWithPermission = document.querySelectorAll('[permission-id]');
        elementsWithPermission.forEach(element => {
            const elementPermissionId = element.getAttribute('permission-id');
            // 检查 elementPermissionId 是否存在于 permissionIdsArray 中
            if (permissionIdsArray.includes(elementPermissionId)) {
                element.style.display = 'block';
            } else {
                element.style.display = 'none';
            }
        });
    }
}

/**
 * 显示加载中的提示信息，并在一段时间后自动关闭
 * 这个函数用于在执行一些耗时操作时，给用户一个视觉反馈，表示系统正在处理中，让用户等待
 */
function loadingMessage(message='请求处理中，请稍后...',textColor='text-info') {
    // 创建一个加载中的提示层，默认配置参数
    var l = $('body').lyearloading({
        // 设置遮罩层的透明度为0.2，让背景变暗但仍然可以看到
        opacity: 0.2,
        // 设置加载中的图标大小为大（lg），提高视觉显著性
        spinnerSize: 'lg',
        // 设置加载中的提示文字为“后台处理中，请稍后...”，告知用户当前状态
        spinnerText: message,
        // 设置文字颜色类为'	text-info'，使得文字颜色符合主题
        textColorClass: textColor,
        // 设置加载图标颜色类为'text-info'，使得图标颜色符合主题
        spinnerColorClass: textColor
    });
    // 在1秒（1000毫秒）后执行关闭加载提示
    setTimeout(function () {
        l.destroy();
    }, 1e3)
}



/**
 * 显示通知消息
 *
 * 该函数用于在页面上显示一个通知消息，可以根据参数设置消息的内容、类型以及显示时间
 *
 * @param {string} message - 要显示的消息内容
 * @param {string} level - 消息的类型，如success、warning、error等
 * @param {number} [delayMs=1000] - 消息自动关闭的延迟时间（毫秒），默认为1000毫秒
 */
function notice(message, level, delayMs = 1000) {
    $.notify({message: message}, {type: level, delay: delayMs, placement: {align: 'center'}});
}


function validateStringLength(string, minlength, maxlength) {
    return !(string.length = 0 || string.length < minlength || string.length > maxlength);
}

function validateUsername(username) {
    return !(username.length < 4 || username.length > 32);
}


/**
 * 判断一个字符串是否为数值
 *
 * @param {string} str - 待验证的字符串
 * @returns {boolean} 返回一个布尔值，表示字符串是否为数值
 *
 * 该函数使用正则表达式来判断输入的字符串是否仅由数字组成。
 * 正则表达式 /^\d+$/ 的作用是匹配字符串是否是由一个或多个数字字符组成。
 * 如果字符串满足条件，即仅包含数字字符，则返回 true，否则返回 false。
 */
function isNumeric(str) {
    return /^\d+$/.test(str);
}

/**
 * 验证密码是否符合长度要求
 *
 * 该函数用于检查提供的密码是否符合指定的长度规则，即密码长度必须在8到128个字符之间
 * 这是因为过短的密码容易被破解，而过长的密码可能会超出存储限制或不便于用户使用
 *
 * @param {string} password 待验证的密码字符串
 * @return {boolean} 返回true表示密码长度符合要求，返回false表示密码长度不符合要求
 */
function validatePassword(password) {
    // 检查密码长度是否在8到128个字符之间（包含边界值）
    return !(password.length < 8 || password.length > 128);
}


/**
 * 验证电子邮件地址是否有效
 *
 * 该函数使用正则表达式来检查传入的电子邮件地址是否符合常见的电子邮件格式
 * 它确保了地址包含一个@符号，并且@符号后有一个域名和顶级域名
 *
 * @param {string} email - 要验证的电子邮件地址
 * @returns {boolean} - 如果电子邮件地址有效，则返回true；否则返回false
 */
function validateEmail(email) {
    // 定义电子邮件正则表达式，用于匹配电子邮件地址的模式
    const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    // 使用正则表达式的test方法检查电子邮件地址是否匹配定义的模式，并返回结果
    return emailRegex.test(email);
}

/**
 * 验证电话号码是否符合指定格式
 *
 * 该函数使用正则表达式来判断传入的电话号码是否符合中国大陆的手机号码格式
 * 电话号码格式要求以1开头，第二位为3到9之间的数字，后九位为数字
 *
 * @param {string} phone - 待验证的电话号码
 * @returns {boolean} - 如果电话号码符合指定格式，返回true；否则返回false
 */
function validatePhone(phone) {
    // 定义电话号码的正则表达式，匹配以1开头，第二位为3到9之间的数字，后九位为数字的字符串
    const phoneRegex = /^1[3-9]\d{9}$/;
    // 使用正则表达式测试电话号码是否匹配
    return phoneRegex.test(phone);
}



