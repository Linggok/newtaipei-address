/**
 * 從 banqiao_real_data.csv 移除「number」欄位，覆寫原檔
 */
const fs = require('fs');
const path = require('path');

const filePath = path.join(__dirname, '..', 'banqiao_real_data.csv');
const raw = fs.readFileSync(filePath, 'utf8').replace(/\r\n/g, '\n');
const lines = raw.split('\n');

const out = lines.map((line, i) => {
  const cols = line.split(',');
  if (cols.length > 0) cols.pop(); // 移除最後一欄（number）
  return cols.join(',');
}).join('\n');

fs.writeFileSync(filePath, out, 'utf8');
console.log('已從 banqiao_real_data.csv 移除 number 欄位，共', lines.length, '行');
