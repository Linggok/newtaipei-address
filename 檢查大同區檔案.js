/**
 * 檢查大同區檔案格式
 */

const fs = require('fs');
const path = require('path');

const datongFile = path.join(__dirname, '大同區門牌位置數值資料.CSV');
const zhongzhengFile = path.join(__dirname, '中正區門牌位置數值資料.CSV');

console.log('比較兩個檔案...\n');

const datongBuffer = fs.readFileSync(datongFile);
const zhongzhengBuffer = fs.readFileSync(zhongzhengFile);

console.log('大同區檔案大小:', datongBuffer.length);
console.log('中正區檔案大小:', zhongzhengBuffer.length);

console.log('\n大同區檔案前 100 bytes (hex):');
console.log(datongBuffer.slice(0, 100).toString('hex'));

console.log('\n中正區檔案前 100 bytes (hex):');
console.log(zhongzhengBuffer.slice(0, 100).toString('hex'));

console.log('\n大同區檔案前 200 bytes (UTF-8):');
console.log(datongBuffer.slice(0, 200).toString('utf8'));

console.log('\n中正區檔案前 200 bytes (UTF-8):');
console.log(zhongzhengBuffer.slice(0, 200).toString('utf8'));

// 檢查 BOM
console.log('\n檢查 BOM:');
console.log('大同區 BOM:', datongBuffer.slice(0, 3).toString('hex'));
console.log('中正區 BOM:', zhongzhengBuffer.slice(0, 3).toString('hex'));
