// 修正 server.js 中的變數名稱錯誤
const fs = require('fs');
const path = require('path');

const filePath = path.join(__dirname, 'server.js');
let content = fs.readFileSync(filePath, 'utf8');

// 將 constangangDoorplate 改為 constangangDoorplate（在 const 和 angang 之間加上空格）
// 使用正則表達式來匹配
content = content.replace(/constangangDoorplate\s*=/g, 'constangangDoorplate =');

fs.writeFileSync(filePath, content, 'utf8');
console.log('已修正變數名稱');
