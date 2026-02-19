/**
 * 從 永和區門牌位置數值資料.csv 刪除第 I、J、K 欄（index 8, 9, 10：number, x_3826, y_3826）
 */
const fs = require('fs');
const path = require('path');

const filePath = path.join(__dirname, '..', '永和區門牌位置數值資料.csv');
const REMOVE = new Set([8, 9, 10]);

if (!fs.existsSync(filePath)) {
  console.error('找不到檔案：永和區門牌位置數值資料.csv');
  process.exit(1);
}

const raw = fs.readFileSync(filePath, 'utf8').replace(/\r\n/g, '\n').replace(/\r/g, '\n');
const lines = raw.split('\n');

const out = lines.map((line) => {
  const cols = line.split(',');
  return cols.filter((_, i) => !REMOVE.has(i)).join(',');
}).join('\n');

fs.writeFileSync(filePath, '\uFEFF' + out, 'utf8');
console.log('已刪除 I、J、K 欄（number, x_3826, y_3826）');
console.log('共處理', lines.length, '行');
