/**
 * 將 板橋區門牌路巷弄資料.csv 內同路名的地址依巷、弄從小到大排序
 * 執行：node scripts/sort-banqiao-csv.js
 */

const fs = require('fs');
const path = require('path');

const CSV_PATH = path.join(__dirname, '..', '板橋區門牌路巷弄資料.csv');

if (!fs.existsSync(CSV_PATH)) {
  console.error('找不到 板橋區門牌路巷弄資料.csv，請先將檔案放到 newtaipei 資料夾內。');
  process.exit(1);
}

function toNum(s) {
  if (!s || typeof s !== 'string') return 0;
  const n = String(s).replace(/[０-９]/g, (c) => String.fromCharCode(c.charCodeAt(0) - 0xfee0)).replace(/[^\d]/g, '');
  return n ? parseInt(n, 10) : 0;
}

const raw = fs.readFileSync(CSV_PATH, 'utf8').replace(/\r\n/g, '\n');
const lines = raw.split('\n').filter((l) => l.trim());
const header = lines[0];
const rows = lines.slice(1).map((line) => {
  const cols = line.split(',');
  return { area: cols[0] || '', road: cols[1] || '', lane: cols[2] || '', alley: cols[3] || '' };
});

rows.sort((a, b) => {
  if (a.road !== b.road) return (a.road || '').localeCompare(b.road || '', 'zh-TW');
  const laneA = toNum(a.lane);
  const laneB = toNum(b.lane);
  if (laneA !== laneB) return laneA - laneB;
  return toNum(a.alley) - toNum(b.alley);
});

const out = [header, ...rows.map((r) => [r.area, r.road, r.lane, r.alley].join(','))].join('\n');
const tmpPath = CSV_PATH + '.tmp';
fs.writeFileSync(tmpPath, out, 'utf8');
try {
  fs.renameSync(tmpPath, CSV_PATH);
  console.log('已排序 板橋區門牌路巷弄資料.csv，共', rows.length, '筆');
} catch (e) {
  fs.copyFileSync(tmpPath, CSV_PATH);
  fs.unlinkSync(tmpPath);
  console.log('已排序 板橋區門牌路巷弄資料.csv，共', rows.length, '筆');
}
