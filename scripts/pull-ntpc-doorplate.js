/**
 * 拉取「新北市門牌位置數值資料」 from 新北市政府資料開放平台
 * 使用方式：設定環境變數 NTPC_DOORPLATE_OID 後執行 node scripts/pull-ntpc-doorplate.js
 * 或：npm run pull-doorplate
 *
 * OID 取得：至 https://data.ntpc.gov.tw 搜尋「門牌位置數值」，
 * 點進資料集，網址最後一段即為 OID（例如 .../datasets/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx）
 */

require('dotenv').config();
const https = require('https');
const fs = require('fs');
const path = require('path');

const NTPC_BASE = 'https://data.ntpc.gov.tw';
const OID = process.env.NTPC_DOORPLATE_OID || process.env.NTPC_DATASET_OID || '';
const OUT_DIR = path.join(__dirname, '..', 'data');
const OUT_RAW = path.join(OUT_DIR, 'ntpc-doorplate-raw.json');
const PAGE_SIZE = 5000;

// 若平台僅提供 CSV，可改為用 CSV 網址手動下載後放到 data/ntpc-doorplate.csv，腳本會讀取並轉成 JSON
const LOCAL_CSV = path.join(OUT_DIR, 'ntpc-doorplate.csv');

function fetchWithStatus(url) {
  return new Promise((resolve, reject) => {
    https.get(url, (res) => {
      let data = '';
      res.on('data', (chunk) => { data += chunk; });
      res.on('end', () => {
        if (res.statusCode !== 200) {
          const err = new Error(`HTTP ${res.statusCode}: ${url}`);
          err.statusCode = res.statusCode;
          err.body = data;
          return reject(err);
        }
        try {
          resolve(JSON.parse(data));
        } catch (e) {
          const err = new Error('回應不是有效 JSON: ' + e.message);
          err.body = data.slice(0, 500);
          reject(err);
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

async function main() {
  // 若已有手動下載的 CSV，可直接轉成 JSON
  if (fs.existsSync(LOCAL_CSV)) {
    console.log('發現本地 CSV，轉成 JSON:', LOCAL_CSV);
    const csvText = fs.readFileSync(LOCAL_CSV, 'utf8');
    const lines = csvText.split(/\r?\n/).filter((l) => l.trim());
    const headers = lines[0].split(',').map((h) => h.trim().replace(/^"|"$/g, ''));
    const records = [];
    for (let i = 1; i < lines.length; i++) {
      const vals = lines[i].split(',').map((v) => v.trim().replace(/^"|"$/g, ''));
      const row = {};
      headers.forEach((h, j) => { row[h] = vals[j] ?? ''; });
      records.push(row);
    }
    const out = { source: '新北市政府資料開放平台（本地 CSV）', fetchedAt: new Date().toISOString(), total: records.length, records };
    fs.writeFileSync(OUT_RAW, JSON.stringify(out, null, 2), 'utf8');
    console.log('已儲存至', OUT_RAW, '，共', records.length, '筆');
    return;
  }

  if (!OID.trim()) {
    console.error('請設定環境變數 NTPC_DOORPLATE_OID（或 NTPC_DATASET_OID）');
    console.error('至 https://data.ntpc.gov.tw 搜尋「門牌位置數值」，取得資料集 OID 後填入 .env');
    console.error('或將平台下載的 CSV 檔命名為 ntpc-doorplate.csv 放到 data/ 目錄後再執行本腳本。');
    process.exit(1);
  }

  if (!fs.existsSync(OUT_DIR)) {
    fs.mkdirSync(OUT_DIR, { recursive: true });
  }

  const all = [];
  let page = 0;

  console.log('開始拉取新北市門牌位置數值資料，OID:', OID);

  try {
    // 先嘗試分頁（最常見）
    const pageUrl = `${NTPC_BASE}/api/datasets/${OID}/json?page=0&size=${PAGE_SIZE}`;
    console.log('請求:', pageUrl);

    let firstJson;
    try {
      firstJson = await fetchWithStatus(pageUrl);
    } catch (e) {
      if (e.statusCode) {
        console.error('API 回傳狀態碼:', e.statusCode);
        if (e.body) console.error('回應內容（前 500 字）:', String(e.body).slice(0, 500));
      }
      throw e;
    }

    const firstRecords = extractRecords(firstJson);
    if (firstRecords.length > 0) {
      all.push(...firstRecords);
      console.log('第 1 頁，取得', firstRecords.length, '筆');
    }

    // 若第一頁就滿頁，繼續分頁
    if (firstRecords.length >= PAGE_SIZE) {
      page = 1;
      for (;;) {
        const url = `${NTPC_BASE}/api/datasets/${OID}/json?page=${page}&size=${PAGE_SIZE}`;
        const json = await fetchWithStatus(url);
        const records = extractRecords(json);
        if (records.length === 0) break;
        all.push(...records);
        console.log(`  第 ${page + 1} 頁，取得 ${records.length} 筆，累計 ${all.length} 筆`);
        if (records.length < PAGE_SIZE) break;
        page += 1;
      }
    }

    // 若分頁無資料，再試整份下載
    if (all.length === 0) {
      const fullUrl = `${NTPC_BASE}/api/datasets/${OID}/json/file`;
      console.log('分頁無資料，嘗試整份下載:', fullUrl);
      try {
        const fullJson = await fetchWithStatus(fullUrl);
        const fullRecords = extractRecords(fullJson);
        if (fullRecords.length > 0) {
          all.push(...fullRecords);
          console.log('以整份下載取得', fullRecords.length, '筆');
        }
      } catch (e2) {
        console.error('整份下載也失敗:', e2.message);
      }
    }

    if (all.length === 0) {
      console.error('無法取得任何筆數。請確認：');
      console.error('1. OID 是否正確（至 https://data.ntpc.gov.tw 搜尋「門牌位置數值」取得）');
      console.error('2. 該資料集是否提供 JSON API（部分僅提供 ZIP/CSV）');
      console.error('若平台回傳結構不同，可將上述請求 URL 貼到瀏覽器查看實際回應。');
      process.exit(1);
    }

    const out = {
      source: '新北市政府資料開放平台 - 新北市門牌位置數值資料',
      datasetOid: OID,
      fetchedAt: new Date().toISOString(),
      total: all.length,
      records: all
    };

    fs.writeFileSync(OUT_RAW, JSON.stringify(out, null, 2), 'utf8');
    console.log('已儲存至', OUT_RAW, '，共', all.length, '筆');
  } catch (err) {
    console.error('拉取失敗:', err.message);
    if (err.body) console.error('回應片段:', err.body);
    process.exit(1);
  }
}

main();
