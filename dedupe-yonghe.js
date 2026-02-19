/**
 * 將 yonghe_real_data.csv 去重並依 路名、巷、弄 從小到大排序
 */
const fs = require('fs');
const path = require('path');

const FILE_PATH = path.join(__dirname, 'yonghe_real_data.csv');

// 全形數字轉半形
function toHalfWidth(s) {
  return String(s || '').replace(/[０-９]/g, (c) =>
    String.fromCharCode(c.charCodeAt(0) - 0xfee0)
  );
}

// 從巷/弄字串取出數字用於排序，例如 "７０巷" -> 70
function extractNum(str) {
  if (!str || !str.trim()) return 0;
  const s = toHalfWidth(str).replace(/[巷弄號\s]/g, '').trim();
  const m = s.match(/^\d+/);
  return m ? parseInt(m[0], 10) : 0;
}

// 排序用：先路名，再巷數字，再弄數字
function sortKey(row) {
  const [area, road, lane, alley] = row;
  return [
    road || '',
    extractNum(lane),
    extractNum(alley),
    (lane || '').trim(),
    (alley || '').trim()
  ];
}

function compareRows(a, b) {
  const ka = sortKey(a);
  const kb = sortKey(b);
  if (ka[0] !== kb[0]) return ka[0].localeCompare(kb[0], 'zh-TW');
  if (ka[1] !== kb[1]) return ka[1] - kb[1];
  if (ka[2] !== kb[2]) return ka[2] - kb[2];
  if (ka[3] !== kb[3]) return ka[3].localeCompare(kb[3], 'zh-TW');
  return ka[4].localeCompare(kb[4], 'zh-TW');
}

const raw = fs.readFileSync(FILE_PATH, 'utf8').replace(/\r\n/g, '\n');
const lines = raw.split('\n').filter((l) => l.trim());
const header = lines[0];
const rows = lines.slice(1).map((line) => line.split(',').map((c) => (c || '').trim()));

// 去重：以 行政區,路名,巷,弄 為 key
const seen = new Set();
const unique = [];
for (const row of rows) {
  const key = row.join('|');
  if (seen.has(key)) continue;
  seen.add(key);
  unique.push(row);
}

// 排序
unique.sort(compareRows);

const output = [header, ...unique.map((r) => r.join(','))].join('\n');
fs.writeFileSync(FILE_PATH, output, 'utf8');
console.log('原筆數:', rows.length, '去重後:', unique.length, '已排序並儲存');
