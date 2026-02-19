/**
 * 在 永和區門牌位置數值資料.csv 的 area 欄（第 6 欄，index 5）填入「永和區」
 */
const fs = require('fs');
const path = require('path');

const filePath = path.join(__dirname, '..', '永和區門牌位置數值資料.csv');
const AREA_COL = 5;
const VALUE = '永和區';

if (!fs.existsSync(filePath)) {
  console.error('找不到檔案：永和區門牌位置數值資料.csv');
  process.exit(1);
}

const raw = fs.readFileSync(filePath, 'utf8').replace(/\r\n/g, '\n').replace(/\r/g, '\n');
const lines = raw.split('\n');

const out = lines.map((line, i) => {
  if (i === 0) return line;
  const cols = line.split(',');
  while (cols.length <= AREA_COL) cols.push('');
  cols[AREA_COL] = VALUE;
  return cols.join(',');
}).join('\n');

try {
  fs.writeFileSync(filePath, '\uFEFF' + out, 'utf8');
  console.log('已在 area 欄填入「永和區」，共', lines.length - 1, '筆資料列');
} catch (e) {
  if (e.code === 'EBUSY' || e.code === 'EPERM') {
    const altPath = path.join(__dirname, '..', '永和區門牌位置數值資料_含區.csv');
    fs.writeFileSync(altPath, '\uFEFF' + out, 'utf8');
    console.log('原檔被占用，已另存為：永和區門牌位置數值資料_含區.csv');
    console.log('共', lines.length - 1, '筆資料列，area 欄已填「永和區」。關閉原檔後可將此檔覆蓋回原檔名。');
  } else throw e;
}