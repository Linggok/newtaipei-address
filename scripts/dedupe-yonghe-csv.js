/**
 * 從 永和區門牌位置數值資料.csv 刪除重複列（依整行內容，保留第一次出現）
 */
const fs = require('fs');
const path = require('path');

const filePath = path.join(__dirname, '..', '永和區門牌位置數值資料.csv');

if (!fs.existsSync(filePath)) {
  console.error('找不到檔案：永和區門牌位置數值資料.csv');
  process.exit(1);
}

const raw = fs.readFileSync(filePath, 'utf8').replace(/\r\n/g, '\n').replace(/\r/g, '\n');
const lines = raw.split('\n');

const seen = new Set();
const unique = [lines[0]];

for (let i = 1; i < lines.length; i++) {
  const line = lines[i];
  if (!line.trim()) continue;
  if (seen.has(line)) continue;
  seen.add(line);
  unique.push(line);
}

fs.writeFileSync(filePath, '\uFEFF' + unique.join('\n'), 'utf8');
console.log('已刪除重複列。原本', lines.length, '行 → 現在', unique.length, '行（刪除', lines.length - unique.length, '筆重複）');