/**
 * 從 新北市門牌位置數值資料_with_area.csv 只保留 新莊區 的資料，其餘刪除
 * 執行：node scripts/filter-xinzhuang-only.js
 */

const fs = require('fs');
const path = require('path');

const CSV_PATH = path.join(__dirname, '..', '新北市門牌位置數值資料_with_area.csv');

const raw = fs.readFileSync(CSV_PATH, 'utf8').replace(/\r\n/g, '\n');
const lines = raw.split('\n');
const header = lines[0];
const dataLines = lines.slice(1);

const kept = dataLines.filter((line) => {
  const cols = line.split(',');
  const area = (cols[0] || '').trim();
  return area === '新莊區';
});

const out = [header, ...kept].join('\n');
fs.writeFileSync(CSV_PATH, out, 'utf8');
console.log('已將 新北市門牌位置數值資料_with_area.csv 改為只保留新莊區');
console.log('原筆數:', dataLines.length, '→ 保留:', kept.length, '筆');
