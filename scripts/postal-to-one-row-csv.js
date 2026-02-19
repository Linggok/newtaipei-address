/**
 * 將 103.12.25-臺灣地區郵遞區號前3碼一覽表.csv 從多欄表格轉成「一列一筆」格式
 * 輸出：行政區,郵遞區號（每列一筆）
 */
const fs = require('fs');
const path = require('path');

const inputPath = path.join(__dirname, '..', '103.12.25-臺灣地區郵遞區號前3碼一覽表.csv');
const outputPath = path.join(__dirname, '..', '103.12.25-臺灣地區郵遞區號前3碼一覽表.csv');

if (!fs.existsSync(inputPath)) {
  console.error('找不到檔案：103.12.25-臺灣地區郵遞區號前3碼一覽表.csv');
  process.exit(1);
}

const raw = fs.readFileSync(inputPath, 'utf8').replace(/\r\n/g, '\n').replace(/\r/g, '\n');
const lines = raw.split('\n').filter((l) => l.trim());
if (lines.length < 2) {
  console.error('檔案行數不足');
  process.exit(1);
}

const seen = new Set();
const rows = [];

for (let r = 1; r < lines.length; r++) {
  const cols = lines[r].split(',');
  for (let i = 1; i < cols.length; i++) {
    const cell = (cols[i] || '').trim();
    const zip3 = cell.replace(/\D/g, '').slice(0, 3);
    if (zip3.length !== 3 || parseInt(zip3, 10) < 100) continue;
    let name = '';
    for (let j = i - 1; j >= 0; j--) {
      const prev = (cols[j] || '').trim().replace(/\s+/g, '');
      if (prev && !/^\d+$/.test(prev)) {
        name = (cols[j] || '').trim().replace(/\s+/g, ' ');
        break;
      }
    }
    if (!name) continue;
    const key = name + '|' + zip3;
    if (seen.has(key)) continue;
    seen.add(key);
    rows.push({ 行政區: name, 郵遞區號: zip3 });
  }
}

rows.sort((a, b) => {
  const za = parseInt(a.郵遞區號, 10);
  const zb = parseInt(b.郵遞區號, 10);
  if (za !== zb) return za - zb;
  return (a.行政區 || '').localeCompare(b.行政區 || '', 'zh-TW');
});

const header = '行政區,郵遞區號';
const body = rows.map((x) => `${x.行政區},${x.郵遞區號}`).join('\n');
const out = '\uFEFF' + header + '\n' + body;

fs.writeFileSync(outputPath, out, 'utf8');
console.log('已轉成「一列一筆」格式，共', rows.length, '筆');
console.log('檔案已覆寫：103.12.25-臺灣地區郵遞區號前3碼一覽表.csv');
console.log('表頭：行政區,郵遞區號');
