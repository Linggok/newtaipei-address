/**
 * 從桌面 新北市/新北市門牌位置數值資料.csv 篩選永和區（areacode=65000040）
 * 輸出：專案目錄/永和區門牌位置數值資料.csv
 */
const fs = require('fs');
const path = require('path');

const desktop = process.env.USERPROFILE ? path.join(process.env.USERPROFILE, 'Desktop') : '';
const inputPath = path.join(desktop, '新北市', '新北市門牌位置數值資料.csv');
const outputPath = path.join(__dirname, '..', '永和區門牌位置數值資料.csv');
const YONGHE_AREACODE = '65000040';

if (!fs.existsSync(inputPath)) {
  console.error('找不到檔案：', inputPath);
  console.error('請確認桌面上有 新北市 資料夾，且內含 新北市門牌位置數值資料.csv');
  process.exit(1);
}

const raw = fs.readFileSync(inputPath, 'utf8').replace(/\r\n/g, '\n').replace(/\r/g, '\n');
const lines = raw.split('\n');
if (lines.length < 2) {
  console.error('檔案無資料');
  process.exit(1);
}

const header = lines[0].replace(/^\uFEFF/, '').trim();
const cols = header.split(',');
const idxAreacode = cols.findIndex((h) => h.toLowerCase() === 'areacode' || h === '區碼');
const areacodeCol = idxAreacode >= 0 ? idxAreacode : 1;

const outLines = [header];
let count = 0;
for (let i = 1; i < lines.length; i++) {
  const row = lines[i];
  if (!row.trim()) continue;
  const parts = row.split(',');
  const code = (parts[areacodeCol] || '').trim();
  if (code === YONGHE_AREACODE) {
    outLines.push(row);
    count++;
  }
}

fs.writeFileSync(outputPath, '\uFEFF' + outLines.join('\n'), 'utf8');
console.log('已篩選永和區（areacode=65000040）門牌資料');
console.log('輸出檔案：', outputPath);
console.log('共', count, '筆');
