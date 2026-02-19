/**
 * 從 banqiao_real_data.csv 刪除重複列（依整行內容），覆寫原檔
 */
const fs = require('fs');
const path = require('path');

const filePath = path.join(__dirname, '..', 'banqiao_real_data.csv');
const raw = fs.readFileSync(filePath, 'utf8').replace(/\r\n/g, '\n');
const lines = raw.split('\n');

const header = lines[0];
const seen = new Set();
const unique = [header];

for (let i = 1; i < lines.length; i++) {
  const line = lines[i];
  if (!line.trim()) continue;
  if (seen.has(line)) continue;
  seen.add(line);
  unique.push(line);
}

fs.writeFileSync(filePath, unique.join('\n'), 'utf8');
console.log('已刪除重複列。原本', lines.length, '行 → 現在', unique.length, '行（刪除', lines.length - unique.length, '筆重複）');
