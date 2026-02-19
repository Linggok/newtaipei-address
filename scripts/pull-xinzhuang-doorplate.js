/**
 * 拉取「新北市新莊區」門牌資料 from 新北市政府資料開放平台
 * 1. 若設定 NTPC_DOORPLATE_OID：從 API 拉取，篩選 新莊區，存成 CSV
 * 2. 若平台僅提供 CSV：將手動下載的 CSV 放到 data/ntpc-doorplate.csv，腳本會篩選新莊區並轉存
 *
 * 執行：npm run pull-xinzhuang
 * 或：node scripts/pull-xinzhuang-doorplate.js
 */

require('dotenv').config();
const https = require('https');
const fs = require('fs');
const path = require('path');

const NTPC_BASE = 'https://data.ntpc.gov.tw';
const OID = process.env.NTPC_DOORPLATE_OID || process.env.NTPC_DATASET_OID || '';
const OUT_DIR = path.join(__dirname, '..', 'data');
const OUT_CSV = path.join(__dirname, '..', '新北市門牌位置數值資料_with_area.csv');
const LOCAL_CSV = path.join(OUT_DIR, 'ntpc-doorplate.csv');
const PAGE_SIZE = 5000;
const TARGET_DISTRICT = '新莊區';

function getField(r, keys) {
  for (const k of keys) {
    const v = r[k];
    if (v !== undefined && v !== null && String(v).trim() !== '') return String(v).trim();
  }
  return '';
}

function isXinzhuang(r) {
  const area = getField(r, ['area', 'Area', '行政區', 'district', 'District', '區']);
  return area === TARGET_DISTRICT || area.includes(TARGET_DISTRICT);
}

function toCsvRow(r) {
  const area = getField(r, ['area', 'Area', '行政區', 'district', 'District']) || TARGET_DISTRICT;
  const road = getField(r, ['road', 'Road', '路名', '道路', 'roadname']);
  const lane = getField(r, ['lane', 'Lane', '巷', '巷弄']);
  const alley = getField(r, ['alley', 'Alley', '弄']);
  const number = getField(r, ['number', 'Number', '號', '門牌號']);
  return [area, road, lane, alley, number].map((c) => (c || '').replace(/,/g, '，')).join(',');
}

function fetchWithStatus(url) {
  return new Promise((resolve, reject) => {
    https.get(url, (res) => {
      let data = '';
      res.on('data', (chunk) => { data += chunk; });
      res.on('end', () => {
        if (res.statusCode !== 200) {
          const err = new Error(`HTTP ${res.statusCode}`);
          err.statusCode = res.statusCode;
          err.body = data;
          return reject(err);
        }
        try {
          resolve(JSON.parse(data));
        } catch (e) {
          reject(new Error('回應不是有效 JSON'));
        }
      });
    }).on('error', reject);
  });
}

function extractRecords(json) {
  if (!json || typeof json !== 'object') return [];
  if (Array.isArray(json)) return json;
  return json?.data ?? json?.result?.records ?? json?.records ?? json?.results ?? json?.value ?? [];
}

async function fetchFromApi() {
  const all = [];
  let page = 0;
  for (;;) {
    const url = `${NTPC_BASE}/api/datasets/${OID}/json?page=${page}&size=${PAGE_SIZE}`;
    const json = await fetchWithStatus(url);
    const records = extractRecords(json);
    if (records.length === 0) break;
    all.push(...records);
    console.log(`  第 ${page + 1} 頁，取得 ${records.length} 筆，累計 ${all.length}`);
    if (records.length < PAGE_SIZE) break;
    page += 1;
  }
  if (all.length === 0) {
    const fullUrl = `${NTPC_BASE}/api/datasets/${OID}/json/file`;
    try {
      const fullJson = await fetchWithStatus(fullUrl);
      all.push(...extractRecords(fullJson));
    } catch (_) {}
  }
  return all;
}

async function main() {
  let records = [];

  if (fs.existsSync(LOCAL_CSV)) {
    console.log('從本地 CSV 讀取:', LOCAL_CSV);
    const raw = fs.readFileSync(LOCAL_CSV, 'utf8').replace(/\r\n/g, '\n');
    const lines = raw.split('\n').filter((l) => l.trim());
    const headers = lines[0].split(',');
    for (let i = 1; i < lines.length; i++) {
      const cols = lines[i].split(',');
      const row = {};
      headers.forEach((h, j) => { row[h.trim()] = (cols[j] || '').trim(); });
      row.行政區 = row.行政區 || row.area || row.Area || row.district || '';
      row.路名 = row.路名 || row.road || row.Road || '';
      row.巷 = row.巷 || row.lane || row.Lane || '';
      row.弄 = row.弄 || row.alley || row.Alley || '';
      row.號 = row.號 || row.number || row.Number || '';
      records.push(row);
    }
  } else if (OID.trim()) {
    console.log('從新北市開放平台 API 拉取，OID:', OID);
    records = await fetchFromApi();
  } else {
    console.error('請擇一方式：');
    console.error('1. 設定 NTPC_DOORPLATE_OID 於 .env，從 API 拉取');
    console.error('2. 將平台下載的 CSV 放到 data/ntpc-doorplate.csv');
    process.exit(1);
  }

  const xinzhuang = records.filter(isXinzhuang);
  console.log('篩選 新莊區：', records.length, '→', xinzhuang.length, '筆');

  if (xinzhuang.length === 0) {
    console.error('無新莊區資料。請確認來源或欄位名稱。');
    process.exit(1);
  }

  const header = 'area,road,lane,alley,number';
  const body = xinzhuang.map(toCsvRow).join('\n');
  fs.writeFileSync(OUT_CSV, header + '\n' + body, 'utf8');
  console.log('已儲存至', OUT_CSV, '，共', xinzhuang.length, '筆（新莊區）');
}

main().catch((err) => {
  console.error('拉取失敗:', err.message);
  process.exit(1);
});
