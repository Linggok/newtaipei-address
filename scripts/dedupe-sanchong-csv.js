/**
 * 從 三重區門牌位置數值資料.csv 刪除重複列（依整行內容，保留第一次出現）
 */
const fs = require('fs');
const path = require('path');

const filePath = path.join(__dirname, '..', '三重區門牌位置數值資料.csv');

if (!fs.existsSync(filePath)) {
  console.error('找不到檔案：三重區門牌位置數值資料.csv');
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

const out = '\uFEFF' + unique.join('\n');
const altPath = path.join(__dirname, '..', '三重區門牌位置數值資料_已去重.csv');
try {
  fs.writeFileSync(filePath, out, 'utf8');
  console.log('已刪除重複列。原本', lines.length, '行 → 現在', unique.length, '行（刪除', lines.length - unique.length, '筆重複）');
} catch (e) {
  if (e.code === 'EBUSY' || e.code === 'EPERM') {
    fs.writeFileSync(altPath, out, 'utf8');
    console.log('原檔被占用，已另存為：三重區門牌位置數值資料_已去重.csv');
    console.log('原本', lines.length, '行 → 現在', unique.length, '行（刪除', lines.length - unique.length, '筆重複）。請關閉原檔後將此檔覆蓋回原檔名。');
  } else throw e;
}