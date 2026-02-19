/**
 * 從 永和區門牌位置數值資料.csv 刪除欄位 A,C,D,F,I,J,K
 * 以 Big5 讀取（避免中文亂碼），寫出為 UTF-8
 * 使用前請先還原原始 CSV 檔（若已亂碼請從備份或來源重新取得）
 */
const fs = require('fs');
const path = require('path');
const iconv = require('iconv-lite');

const filePath = path.join(__dirname, '..', '永和區門牌位置數值資料.csv');
const REMOVE_INDICES = new Set([0, 2, 3, 5, 8, 9, 10]); // A, C, D, F, I, J, K

if (!fs.existsSync(filePath)) {
  console.error('找不到檔案：永和區門牌位置數值資料.csv');
  process.exit(1);
}

const buf = fs.readFileSync(filePath);
const decoded = iconv.decode(buf, 'big5');
const lines = decoded.replace(/\r\n/g, '\n').replace(/\r/g, '\n').split('\n');

const out = lines
  .map((line) => {
    const cols = line.split(',');
    return cols.filter((_, i) => !REMOVE_INDICES.has(i)).join(',');
  })
  .join('\n');

fs.writeFileSync(filePath, '\uFEFF' + out, 'utf8');
console.log('已刪除欄位 A,C,D,F,I,J,K，並以 UTF-8 儲存（含 BOM）');
console.log('共處理', lines.length, '行');
console.log('若仍見亂碼，表示原始檔可能為 UTF-8，請告知。');
