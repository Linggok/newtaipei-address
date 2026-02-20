/**
 * 台灣地址欠祥查詢系統 - 後端
 * 優先使用專案內「新北市門牌位置數值資料_with_area.csv」當資料庫。
 */

require('dotenv').config();
const express = require('express');
const cors = require('cors');
const path = require('path');
const fs = require('fs');
const http = require('http');
const https = require('https');
const iconv = require('iconv-lite');

const app = express();
const PORT = process.env.PORT || 3000;

// 是否使用任何資料來源（false = 不載入資料，查詢結果為空）
const USE_DATA_SOURCES = true;

// 本地門牌資料（都會載入並合併使用）
const DOORPLATE_CSV_PATH = path.join(__dirname, '新北市門牌位置數值資料_with_area.csv');
const XINZHUANG_CSV_PATH = path.join(__dirname, '新莊區.csv');
const XINZHUANG_XLSX_PATH = path.join(__dirname, '新莊區門牌路巷弄資料.xlsx');
const XINZHUANG_DOORPLATE_CSV_PATH = path.join(__dirname, '新莊區門牌路巷弄資料.csv');
const BANQIAO_DOORPLATE_CSV_PATH = path.join(__dirname, '板橋區門牌路巷弄資料.csv');
const BANQIAO_REAL_DATA_PATH = path.join(__dirname, 'banqiao_real_data.csv');
const ZHONGHE_REAL_DATA_PATH = path.join(__dirname, 'zhonghe_real_data.csv');
const SANCHONG_REAL_DATA_PATH = path.join(__dirname, 'sanchong_real_data.csv');
const YONGHE_REAL_DATA_PATH = path.join(__dirname, 'yonghe_real_data.csv');
const YONGHE_DOORPLATE_CSV_PATH = path.join(__dirname, '永和區門牌位置數值資料.csv');
const XINDIAN_DOORPLATE_CSV_PATH = path.join(__dirname, '新店區門牌位置數值資料.csv');
const SHULIN_DOORPLATE_CSV_PATH = path.join(__dirname, '樹林區門牌位置數值資料.csv');
const YINGGE_DOORPLATE_CSV_PATH = path.join(__dirname, '鶯歌區門牌位置數值資料.csv');
const SANXIA_DOORPLATE_CSV_PATH = path.join(__dirname, '三峽區門牌位置數值資料.csv');
const TAMSUI_DOORPLATE_CSV_PATH = path.join(__dirname, '淡水區門牌位置數值資料.csv');
const XIZHI_DOORPLATE_CSV_PATH = path.join(__dirname, '汐止區門牌位置數值資料.csv');
const RUIFANG_DOORPLATE_CSV_PATH = path.join(__dirname, '瑞芳區門牌位置數值資料.csv');
const TUCHENG_DOORPLATE_CSV_PATH = path.join(__dirname, '土城區門牌位置數值資料.csv');
const LUZHOU_DOORPLATE_CSV_PATH = path.join(__dirname, '蘆洲區門牌位置數值資料.csv');
const WUGU_DOORPLATE_CSV_PATH = path.join(__dirname, '五股區門牌位置數值資料.csv');
const TAISHAN_DOORPLATE_CSV_PATH = path.join(__dirname, '泰山區門牌位置數值資料.csv');
const LINKOU_DOORPLATE_CSV_PATH = path.join(__dirname, '林口區門牌位置數值資料.csv');
const SHENKENG_DOORPLATE_CSV_PATH = path.join(__dirname, '深坑區門牌位置數值資料.csv');
const SHIDING_DOORPLATE_CSV_PATH = path.join(__dirname, '石碇區門牌位置數值資料.csv');
const PINGLIN_DOORPLATE_CSV_PATH = path.join(__dirname, '坪林區門牌位置數值資料.csv');
const SANZHI_DOORPLATE_CSV_PATH = path.join(__dirname, '三芝區門牌位置數值資料.csv');
const SHIMEN_DOORPLATE_CSV_PATH = path.join(__dirname, '石門區門牌位置數值資料.csv');
const BALI_DOORPLATE_CSV_PATH = path.join(__dirname, '八里區門牌位置數值資料.csv');
const PINGXI_DOORPLATE_CSV_PATH = path.join(__dirname, '平溪區門牌位置數值資料.csv');
const SHUANGXI_DOORPLATE_CSV_PATH = path.join(__dirname, '雙溪區門牌位置數值資料.csv');
const GONGLIAO_DOORPLATE_CSV_PATH = path.join(__dirname, '貢寮區門牌位置數值資料.csv');
const WANLI_DOORPLATE_CSV_PATH = path.join(__dirname, '萬里區門牌位置數值資料.csv');
const WULAI_DOORPLATE_CSV_PATH = path.join(__dirname, '烏來區門牌位置數值資料.csv');
// 台北市門牌資料
const ZHONGZHENG_DOORPLATE_CSV_PATH = path.join(__dirname, '中正區門牌位置數值資料.CSV');
const ZHONGSHAN_DOORPLATE_CSV_PATH = path.join(__dirname, '中山區門牌位置數值資料.CSV');
const DATONG_DOORPLATE_CSV_PATH = path.join(__dirname, '大同區門牌位置數值資料_utf8.CSV');
const SONGSHAN_DOORPLATE_CSV_PATH = path.join(__dirname, '松山區門牌位置數值資料.CSV');
const DAAN_DOORPLATE_CSV_PATH = path.join(__dirname, '大安區門牌位置數值資料.CSV');
const WANHUA_DOORPLATE_CSV_PATH = path.join(__dirname, '萬華區門牌位置數值資料.CSV');
const XINYI_DOORPLATE_CSV_PATH = path.join(__dirname, '信義區門牌位置數值資料.CSV');
const SHILIN_DOORPLATE_CSV_PATH = path.join(__dirname, '士林區門牌位置數值資料.CSV');
const BEITOU_DOORPLATE_CSV_PATH = path.join(__dirname, '北投區門牌位置數值資料.CSV');
const NEIHU_DOORPLATE_CSV_PATH = path.join(__dirname, '內湖區門牌位置數值資料.CSV');
const NANGANG_DOORPLATE_CSV_PATH = path.join(__dirname, '南港區門牌位置數值資料.CSV');
const WENSHAN_DOORPLATE_CSV_PATH = path.join(__dirname, '文山區門牌位置數值資料.CSV');
// 新北市政府資料開放平台（門牌/路名資料集 OID，可選）
const NTPC_OPEN_DATA_BASE = 'https://data.ntpc.gov.tw';
const NTPC_DATASET_OID = process.env.NTPC_DATASET_OID || '';
const FALLBACK_PATH = path.join(__dirname, 'data', 'fallback-roads.json');

// 郵遞區號前 3 碼一覽表（先找專案目錄，再找桌面）
const POSTAL_BASENAME = '103.12.25-臺灣地區郵遞區號前3碼一覽表';
function getPostalPath() {
  const exts = ['.csv', '.xlsx', '.xls'];
  for (const ext of exts) {
    const p = path.join(__dirname, POSTAL_BASENAME + ext);
    if (fs.existsSync(p)) return p;
  }
  const desktop = process.env.USERPROFILE ? path.join(process.env.USERPROFILE, 'Desktop') : '';
  if (desktop) {
    const taipeiDir = path.join(desktop, 'taipei');
    for (const ext of exts) {
      const p = path.join(taipeiDir, POSTAL_BASENAME + ext);
      if (fs.existsSync(p)) return p;
    }
    for (const ext of exts) {
      const p = path.join(desktop, POSTAL_BASENAME + ext);
      if (fs.existsSync(p)) return p;
    }
  }
  return null;
}

let cachePostal = null;

app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

/** 快取：路名 -> 行政區；行政區 -> 路名；資料來源標記 */
let cacheNtpcRoads = null;
let cacheByDistrict = null; // 行政區 -> 路名[]
let cacheTime = 0;
let cacheSource = ''; // 'local_csv' | 'ntpc' | 'fallback'
const CACHE_MS = 1000 * 60 * 60; // 1 小時

function buildByDistrict(byRoad) {
  const byDistrict = {};
  for (const [road, info] of Object.entries(byRoad || {})) {
    for (const d of info.districts || []) {
      if (!byDistrict[d]) byDistrict[d] = [];
      if (!byDistrict[d].includes(road)) byDistrict[d].push(road);
    }
  }
  return byDistrict;
}

function fetchJson(url) {
  return new Promise((resolve, reject) => {
    const lib = url.startsWith('https') ? https : http;
    lib.get(url, (res) => {
      let data = '';
      res.on('data', (chunk) => { data += chunk; });
      res.on('end', () => {
        try {
          resolve(JSON.parse(data));
        } catch (e) {
          reject(e);
        }
      });
    }).on('error', reject);
  });
}

/** 從單筆資料取出欄位（支援中英文欄位名） */
function getField(r, keys) {
  for (const k of keys) {
    const v = r[k];
    if (v !== undefined && v !== null && String(v).trim() !== '') return String(v).trim();
  }
  return '';
}

/** 載入台北市格式的 CSV（格式：省市縣市代碼,鄉鎮市區代碼,區名,村里,鄰,街路段,地區,巷,弄,號,橫座標,縱座標） */
function loadTaipeiCsv(filePath) {
  if (!fs.existsSync(filePath)) return null;
  const byRoad = {};
  try {
    // 嘗試不同編碼讀取
    const buffer = fs.readFileSync(filePath);
    let raw;
    let encodingFound = false;
    
    // 嘗試的編碼順序（針對大同區檔案特別處理）
    const encodings = ['utf8', 'big5', 'cp950', 'gb2312', 'gbk', 'gb18030'];
    
    // 檢查是否為大同區檔案（可能需要特殊處理）
    const isDatongFile = filePath.includes('大同區');
    
    for (const encoding of encodings) {
      try {
        if (encoding === 'utf8') {
          raw = buffer.toString('utf8');
        } else {
          raw = iconv.decode(buffer, encoding);
        }
        
        // 檢查是否成功解碼
        // 對於大同區，可能需要更寬鬆的檢查
        const hasChinese = /[\u4e00-\u9fa5]/.test(raw);
        const hasKeywords = raw.includes('區名') || raw.includes('街路段') || 
                           raw.includes('大同區') || raw.includes('中正區') || 
                           raw.includes('中山區');
        
        // 如果包含中文字且（有關鍵字 或 是大同區檔案）
        if (hasChinese && (hasKeywords || isDatongFile)) {
          encodingFound = true;
          break;
        }
      } catch (e) {
        // 繼續嘗試下一個編碼
        continue;
      }
    }
    
    if (!encodingFound) {
      // 如果都失敗，嘗試直接使用 utf8
      raw = buffer.toString('utf8');
      console.warn('無法確定編碼，使用 UTF-8:', filePath);
    }
    
    raw = raw.replace(/\r\n/g, '\n').replace(/\r/g, '\n');
    const lines = raw.split('\n').filter((l) => l.trim());
    if (lines.length < 2) return null;
    
    const headerRow = lines[0].replace(/^\uFEFF/, '').trim();
    
    // 判斷分隔符：先嘗試 Tab，再嘗試逗號
    let delimiter = '\t';
    let headers = headerRow.split('\t').map((h) => h.trim());
    if (headers.length < 3) {
      delimiter = ',';
      headers = headerRow.split(',').map((h) => h.trim());
    }
    
    // 台北市格式欄位索引（支援多種可能的欄位名稱）
    const idxDistrict = headers.findIndex((h) => {
      const hLower = h.toLowerCase();
      return h === '區名' || h === '鄉鎮市區' || h.includes('區名') || h.includes('鄉鎮') || 
             hLower.includes('district') || hLower.includes('區');
    });
    const idxRoad = headers.findIndex((h) => {
      const hLower = h.toLowerCase();
      return h === '街路段' || h === '路名' || h.includes('街路') || h.includes('路段') ||
             hLower.includes('road') || hLower.includes('street') || hLower.includes('路');
    });
    const idxLane = headers.findIndex((h) => {
      const hLower = h.toLowerCase();
      return h === '巷' || h.includes('巷') || hLower.includes('lane');
    });
    const idxAlley = headers.findIndex((h) => {
      const hLower = h.toLowerCase();
      return h === '弄' || h.includes('弄') || hLower.includes('alley');
    });
    const idxNumber = headers.findIndex((h) => {
      const hLower = h.toLowerCase();
      return h === '號' || h.includes('號') || hLower.includes('number') || hLower.includes('號');
    });
    
    // 如果找不到標準欄位，嘗試根據位置推斷（Tab 分隔通常是：省市,鄉鎮,區名,村里,鄰,街路段,地區,巷,弄,號,橫座標,縱座標）
    let finalIdxDistrict = idxDistrict;
    let finalIdxRoad = idxRoad;
    
    if (finalIdxDistrict < 0 || finalIdxRoad < 0) {
      // 根據位置推斷（通常區名在第 3 欄，街路段在第 6 欄）
      if (headers.length >= 6) {
        if (finalIdxDistrict < 0) finalIdxDistrict = 2; // 第 3 欄（索引 2）
        if (finalIdxRoad < 0) finalIdxRoad = 5; // 第 6 欄（索引 5）
        console.warn('使用位置推斷欄位:', filePath, '區名索引:', finalIdxDistrict, '路名索引:', finalIdxRoad);
      } else {
        console.error('台北市 CSV 格式不符:', filePath, 'headers:', headers, '欄位數:', headers.length);
        return null;
      }
    }
    
    for (let i = 1; i < lines.length; i++) {
      const cols = lines[i].split(delimiter);
      const district = (cols[finalIdxDistrict] || '').trim();
      const road = (cols[finalIdxRoad] || '').trim();
      
      // 如果欄位為空或看起來像亂碼，跳過
      if (!road || !district || road.length === 0 || district.length === 0) continue;
      
      // 檢查是否為有效的中文字（至少包含一個中文字）
      if (!/[\u4e00-\u9fa5]/.test(district) || !/[\u4e00-\u9fa5]/.test(road)) {
        // 如果不是中文字，可能是編碼問題，跳過這筆資料
        continue;
      }
      
      if (!byRoad[road]) byRoad[road] = { districts: [], raw: [] };
      if (district && !byRoad[road].districts.includes(district)) {
        byRoad[road].districts.push(district);
      }
      
      const laneVal = idxLane >= 0 ? (cols[idxLane] || '').trim() : '';
      const alleyVal = idxAlley >= 0 ? (cols[idxAlley] || '').trim() : '';
      const numVal = idxNumber >= 0 ? (cols[idxNumber] || '').trim() : '';
      
      // 只加入有巷、弄或號的資料到 raw（避免資料過大）
      if (laneVal || alleyVal || numVal) {
        byRoad[road].raw.push({
          road,
          site: district,
          lane: laneVal ? (laneVal.includes('巷') ? laneVal : laneVal + '巷') : '',
          alley: alleyVal ? (alleyVal.includes('弄') ? alleyVal : alleyVal + '弄') : '',
          number: numVal
        });
      }
    }
    return Object.keys(byRoad).length > 0 ? byRoad : null;
  } catch (e) {
    console.error('台北市 CSV 讀取失敗:', filePath, e.message);
    return null;
  }
}

/** 從單一 CSV 檔載入並轉成 byRoad（支援 area/行政區、road/路名、lane/巷、alley/弄、number/號） */
function loadOneCsv(filePath) {
  if (!fs.existsSync(filePath)) return null;
  const byRoad = {};
  try {
    const raw = fs.readFileSync(filePath, 'utf8').replace(/\r\n/g, '\n');
    const lines = raw.split('\n').filter((l) => l.trim());
    if (lines.length < 2) return null;
    const headerRow = lines[0].replace(/^\uFEFF/, '').trim();
    const headers = headerRow.split(',').map((h) => h.trim());
    const col = (names, fallback) => { for (const n of names) { const i = headers.findIndex((h) => h.toLowerCase() === String(n).toLowerCase() || h === n); if (i >= 0) return i; } return fallback; };
    const idxArea = col(['area', '行政區'], 0);
    const idxRoad = col(['road', '路名', 'street、road、section'], 1);
    const idxLane = col(['lane', '巷'], 2);
    const idxAlley = col(['alley', '弄'], 3);
    const idxNumber = col(['number', '號'], 4);
    for (let i = 1; i < lines.length; i++) {
      const cols = lines[i].split(',');
      const area = (cols[idxArea] || '').trim();
      const road = (cols[idxRoad] || '').trim();
      if (!road) continue;
      if (!byRoad[road]) byRoad[road] = { districts: [], raw: [] };
      if (area && !byRoad[road].districts.includes(area)) byRoad[road].districts.push(area);
      const laneVal = (cols[idxLane] || '').trim();
      const alleyVal = (cols[idxAlley] || '').trim();
      const numVal = (cols[idxNumber] || '').trim();
      byRoad[road].raw.push({
        road,
        site: area || '',
        lane: laneVal ? (laneVal.includes('巷') ? laneVal : laneVal + '巷') : '',
        alley: alleyVal ? (alleyVal.includes('弄') ? alleyVal : alleyVal + '弄') : '',
        number: numVal
      });
    }
    return Object.keys(byRoad).length > 0 ? byRoad : null;
  } catch (e) {
    console.error('CSV 讀取失敗:', filePath, e.message);
    return null;
  }
}

/** 從 新莊區門牌路巷弄資料.xlsx 載入 */
function loadFromXinzhuangXlsx() {
  if (!fs.existsSync(XINZHUANG_XLSX_PATH)) return null;
  try {
    const XLSX = require('xlsx');
    const wb = XLSX.readFile(XINZHUANG_XLSX_PATH);
    const ws = wb.Sheets[wb.SheetNames[0]];
    const rows = XLSX.utils.sheet_to_json(ws, { header: 1, defval: '' });
    if (rows.length < 2) return null;
    const headers = rows[0].map((h) => String(h || '').trim());
    const col = (names, fallback) => { for (const n of names) { const i = headers.findIndex((h) => h.toLowerCase() === String(n).toLowerCase() || h === n); if (i >= 0) return i; } return fallback; };
    const idxArea = col(['area', '行政區', '區'], 0);
    const idxRoad = col(['road', '路名', '路'], 1);
    const idxLane = col(['lane', '巷'], 2);
    const idxAlley = col(['alley', '弄'], 3);
    const idxNumber = col(['number', '號'], 4);
    const byRoad = {};
    for (let i = 1; i < rows.length; i++) {
      const cols = rows[i];
      const area = (cols[idxArea] !== undefined ? String(cols[idxArea]) : '').trim() || '新莊區';
      const road = (cols[idxRoad] !== undefined ? String(cols[idxRoad]) : '').trim();
      if (!road) continue;
      if (!byRoad[road]) byRoad[road] = { districts: [], raw: [] };
      if (area && !byRoad[road].districts.includes(area)) {
        byRoad[road].districts.push(area);
        const laneVal = (cols[idxLane] !== undefined ? String(cols[idxLane]) : '').trim();
        const alleyVal = (cols[idxAlley] !== undefined ? String(cols[idxAlley]) : '').trim();
        const numVal = (cols[idxNumber] !== undefined ? String(cols[idxNumber]) : '').trim();
        byRoad[road].raw.push({
          road,
          site: area,
          lane: laneVal ? (laneVal.includes('巷') ? laneVal : laneVal + '巷') : '',
          alley: alleyVal ? (alleyVal.includes('弄') ? alleyVal : alleyVal + '弄') : '',
          number: numVal
        });
      }
    }
    return Object.keys(byRoad).length > 0 ? byRoad : null;
  } catch (e) {
    console.error('新莊區門牌路巷弄資料.xlsx 讀取失敗:', e.message);
    return null;
  }
}

/** banqiao_real_data.csv 專用載入（格式：行政區,路名,巷,弄，確保行政區正確對應） */
function loadBanqiaoRealData(filePath) {
  if (!fs.existsSync(filePath)) return null;
  const byRoad = {};
  try {
    const raw = fs.readFileSync(filePath, 'utf8').replace(/\r\n/g, '\n');
    const lines = raw.split('\n').filter((l) => l.trim());
    if (lines.length < 2) return null;
    const headers = lines[0].replace(/^\uFEFF/, '').trim().split(',').map((h) => h.trim());
    const idxArea = headers.findIndex((h) => h === '行政區' || h.toLowerCase() === 'area');
    const idxRoad = headers.findIndex((h) => h === '路名' || h === 'street、road、section' || h.toLowerCase() === 'road');
    const idxLane = headers.findIndex((h) => h === '巷' || h.toLowerCase() === 'lane');
    const idxAlley = headers.findIndex((h) => h === '弄' || h.toLowerCase() === 'alley');
    if (idxArea < 0 || idxRoad < 0) return null;
    for (let i = 1; i < lines.length; i++) {
      const cols = lines[i].split(',');
      const area = (cols[idxArea] || '').trim();
      const road = (cols[idxRoad] || '').trim();
      if (!road) continue;
      if (!byRoad[road]) byRoad[road] = { districts: [], raw: [] };
      if (area && !byRoad[road].districts.includes(area)) byRoad[road].districts.push(area);
      const laneVal = idxLane >= 0 ? (cols[idxLane] || '').trim() : '';
      const alleyVal = idxAlley >= 0 ? (cols[idxAlley] || '').trim() : '';
      byRoad[road].raw.push({
        road,
        site: area || '',
        lane: laneVal ? (laneVal.includes('巷') ? laneVal : laneVal + '巷') : '',
        alley: alleyVal ? (alleyVal.includes('弄') ? alleyVal : alleyVal + '弄') : '',
        number: ''
      });
    }
    return Object.keys(byRoad).length > 0 ? byRoad : null;
  } catch (e) {
    console.error('banqiao_real_data 讀取失敗:', filePath, e.message);
    return null;
  }
}

/** 永和區門牌位置數值資料.csv 專用載入（格式：street、road、section, lane, alley, number，無行政區欄位，固定為永和區） */
function loadYongheDoorplateCsv(filePath) {
  if (!fs.existsSync(filePath)) return null;
  const SITE = '永和區';
  const byRoad = {};
  try {
    const raw = fs.readFileSync(filePath, 'utf8').replace(/\r\n/g, '\n');
    const lines = raw.split('\n').filter((l) => l.trim());
    if (lines.length < 2) return null;
    const headers = lines[0].replace(/^\uFEFF/, '').trim().split(',').map((h) => h.trim());
    const idxRoad = headers.findIndex((h) => h === 'street、road、section' || h === '路名' || h.toLowerCase() === 'road');
    const idxLane = headers.findIndex((h) => h === 'lane' || h === '巷');
    const idxAlley = headers.findIndex((h) => h === 'alley' || h === '弄');
    const idxNumber = headers.findIndex((h) => h === 'number' || h === '號');
    if (idxRoad < 0) return null;
    for (let i = 1; i < lines.length; i++) {
      const cols = lines[i].split(',');
      const road = (cols[idxRoad] || '').trim();
      if (!road) continue;
      if (!byRoad[road]) byRoad[road] = { districts: [SITE], raw: [] };
      const laneVal = idxLane >= 0 ? (cols[idxLane] || '').trim() : '';
      const alleyVal = idxAlley >= 0 ? (cols[idxAlley] || '').trim() : '';
      const numVal = idxNumber >= 0 ? (cols[idxNumber] || '').trim() : '';
      byRoad[road].raw.push({
        road,
        site: SITE,
        lane: laneVal ? (laneVal.includes('巷') ? laneVal : laneVal + '巷') : '',
        alley: alleyVal ? (alleyVal.includes('弄') ? alleyVal : alleyVal + '弄') : '',
        number: numVal
      });
    }
    return Object.keys(byRoad).length > 0 ? byRoad : null;
  } catch (e) {
    console.error('永和區門牌位置數值資料 讀取失敗:', filePath, e.message);
    return null;
  }
}

/** 合併兩個 byRoad，將 b 的資料併入 a（同路名會合併行政區與 raw） */
function mergeByRoad(a, b) {
  if (!b) return a;
  if (!a) a = {};
  
  // 使用 Set 和 Map 來加速去重
  for (const [road, info] of Object.entries(b)) {
    if (!a[road]) {
      a[road] = { 
        districts: [...(info.districts || [])], 
        raw: [...(info.raw || [])] 
      };
      continue;
    }
    
    // 合併行政區（使用 Set 去重）
    const districtSet = new Set(a[road].districts);
    for (const d of info.districts || []) {
      districtSet.add(d);
    }
    a[road].districts = Array.from(districtSet);
    
    // 合併 raw 資料（使用 Map 去重）
    const rawMap = new Map();
    for (const r of a[road].raw || []) {
      const key = [r.site, r.road, r.lane || '', r.alley || '', r.number || ''].join('|');
      rawMap.set(key, r);
    }
    for (const r of info.raw || []) {
      const key = [r.site, r.road, r.lane || '', r.alley || '', r.number || ''].join('|');
      if (!rawMap.has(key)) {
        rawMap.set(key, r);
      }
    }
    a[road].raw = Array.from(rawMap.values());
  }
  return a;
}

/** 從本地載入（新莊區 + 板橋區 + 中和區 + 永和區 + 新店區 + 樹林區 + 鶯歌區 + 三峽區 + 淡水區 + 汐止區 + 瑞芳區 + 土城區 + 蘆洲區 + 五股區 + 泰山區 + 林口區 + 深坑區 + 石碇區 + 坪林區 + 三芝區 + 石門區 + 八里區 + 平溪區 + 雙溪區 + 貢寮區 + 萬里區 + 中正區 + 中山區 + 大同區 + 松山區 + 大安區 + 萬華區 + 信義區 + 士林區 + 北投區 + 內湖區 + 南港區 + 文山區門牌資料，合併使用） */
async function loadFromLocalDoorplateCsv() {
  const startTime = Date.now();
  
  // 定義所有要載入的檔案（並行載入）
  const loadTasks = [
    { loader: () => loadOneCsv(XINZHUANG_DOORPLATE_CSV_PATH), name: '新莊區' },
    { loader: () => loadOneCsv(BANQIAO_DOORPLATE_CSV_PATH), name: '板橋區' },
    { loader: () => loadBanqiaoRealData(BANQIAO_REAL_DATA_PATH), name: '板橋區(real)' },
    { loader: () => loadBanqiaoRealData(ZHONGHE_REAL_DATA_PATH), name: '中和區' },
    { loader: () => loadBanqiaoRealData(SANCHONG_REAL_DATA_PATH), name: '三重區' },
    { loader: () => loadOneCsv(YONGHE_DOORPLATE_CSV_PATH), name: '永和區' },
    { loader: () => loadOneCsv(XINDIAN_DOORPLATE_CSV_PATH), name: '新店區' },
    { loader: () => loadOneCsv(SHULIN_DOORPLATE_CSV_PATH), name: '樹林區' },
    { loader: () => loadOneCsv(YINGGE_DOORPLATE_CSV_PATH), name: '鶯歌區' },
    { loader: () => loadOneCsv(SANXIA_DOORPLATE_CSV_PATH), name: '三峽區' },
    { loader: () => loadOneCsv(TAMSUI_DOORPLATE_CSV_PATH), name: '淡水區' },
    { loader: () => loadOneCsv(XIZHI_DOORPLATE_CSV_PATH), name: '汐止區' },
    { loader: () => loadOneCsv(RUIFANG_DOORPLATE_CSV_PATH), name: '瑞芳區' },
    { loader: () => loadOneCsv(TUCHENG_DOORPLATE_CSV_PATH), name: '土城區' },
    { loader: () => loadOneCsv(LUZHOU_DOORPLATE_CSV_PATH), name: '蘆洲區' },
    { loader: () => loadOneCsv(WUGU_DOORPLATE_CSV_PATH), name: '五股區' },
    { loader: () => loadOneCsv(TAISHAN_DOORPLATE_CSV_PATH), name: '泰山區' },
    { loader: () => loadOneCsv(LINKOU_DOORPLATE_CSV_PATH), name: '林口區' },
    { loader: () => loadOneCsv(SHENKENG_DOORPLATE_CSV_PATH), name: '深坑區' },
    { loader: () => loadOneCsv(SHIDING_DOORPLATE_CSV_PATH), name: '石碇區' },
    { loader: () => loadOneCsv(PINGLIN_DOORPLATE_CSV_PATH), name: '坪林區' },
    { loader: () => loadOneCsv(SANZHI_DOORPLATE_CSV_PATH), name: '三芝區' },
    { loader: () => loadOneCsv(SHIMEN_DOORPLATE_CSV_PATH), name: '石門區' },
    { loader: () => loadOneCsv(BALI_DOORPLATE_CSV_PATH), name: '八里區' },
    { loader: () => loadOneCsv(PINGXI_DOORPLATE_CSV_PATH), name: '平溪區' },
    { loader: () => loadOneCsv(SHUANGXI_DOORPLATE_CSV_PATH), name: '雙溪區' },
    { loader: () => loadOneCsv(GONGLIAO_DOORPLATE_CSV_PATH), name: '貢寮區' },
    { loader: () => loadOneCsv(WANLI_DOORPLATE_CSV_PATH), name: '萬里區' },
    { loader: () => loadOneCsv(WULAI_DOORPLATE_CSV_PATH), name: '烏來區' },
    { loader: () => loadOneCsv(ZHONGZHENG_DOORPLATE_CSV_PATH), name: '中正區' },
    { loader: () => loadOneCsv(ZHONGSHAN_DOORPLATE_CSV_PATH), name: '中山區' },
    { loader: () => loadTaipeiCsv(DATONG_DOORPLATE_CSV_PATH), name: '大同區' },
    { loader: () => loadOneCsv(SONGSHAN_DOORPLATE_CSV_PATH), name: '松山區' },
    { loader: () => loadOneCsv(DAAN_DOORPLATE_CSV_PATH), name: '大安區' },
    { loader: () => loadOneCsv(WANHUA_DOORPLATE_CSV_PATH), name: '萬華區' },
    { loader: () => loadOneCsv(XINYI_DOORPLATE_CSV_PATH), name: '信義區' },
    { loader: () => loadOneCsv(SHILIN_DOORPLATE_CSV_PATH), name: '士林區' },
    { loader: () => loadOneCsv(BEITOU_DOORPLATE_CSV_PATH), name: '北投區' },
    { loader: () => loadOneCsv(NEIHU_DOORPLATE_CSV_PATH), name: '內湖區' },
    { loader: () => loadOneCsv(NANGANG_DOORPLATE_CSV_PATH), name: '南港區' },
    { loader: () => loadOneCsv(WENSHAN_DOORPLATE_CSV_PATH), name: '文山區' }
  ];

  // 並行載入所有檔案
  const results = await Promise.all(
    loadTasks.map(async (task) => {
      try {
        const data = await Promise.resolve(task.loader());
        return { data, name: task.name };
      } catch (e) {
        console.error(`載入 ${task.name} 失敗:`, e.message);
        return { data: null, name: task.name };
      }
    })
  );

  // 合併所有結果
  let byRoad = null;
  const loadedDistricts = [];
  for (const result of results) {
    if (result.data) {
      byRoad = mergeByRoad(byRoad || {}, result.data);
      loadedDistricts.push(result.name);
    }
  }

  const loadTime = Date.now() - startTime;
  console.log(`已並行載入 ${loadedDistricts.length} 個行政區資料，耗時 ${loadTime}ms`);
  if (loadedDistricts.length > 0) {
    console.log('已載入的行政區:', loadedDistricts.join(', '));
  }

  if (byRoad && Object.keys(byRoad).length > 0) return { byRoad, source: 'local_csv' };
  return null;
}

/** 載入郵遞區號前 3 碼一覽表，回傳 { zip3 -> [{ county, district }] } */
function loadPostalTable() {
  if (cachePostal) return cachePostal;
  const filePath = getPostalPath();
  if (!filePath) {
    cachePostal = {};
    return cachePostal;
  }
  const byZip = {};
  try {
    const ext = path.extname(filePath).toLowerCase();
    if (ext === '.csv') {
      const raw = fs.readFileSync(filePath, 'utf8').replace(/\r\n/g, '\n').replace(/\r/g, '\n');
      const lines = raw.split('\n').filter((l) => l.trim());
      if (lines.length < 2) return (cachePostal = byZip);
      const firstRow = lines[0].replace(/^\uFEFF/, '').trim();
      const isGridFormat = firstRow.includes('一覽表') || !firstRow.includes('郵遞區號');
      if (isGridFormat) {
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
            if (!byZip[zip3]) byZip[zip3] = [];
            if (!byZip[zip3].some((x) => (x.district || '') === name)) {
              const isCounty = /[縣市]$/.test(name);
              byZip[zip3].push({ county: isCounty ? name : '', district: isCounty ? '' : name });
            }
          }
        }
      } else {
        const headers = firstRow.split(',').map((h) => h.trim());
        const col = (names) => {
          for (const n of names) {
            const i = headers.findIndex((h) => h === n || (h && h.toLowerCase && h.toLowerCase().includes(n)));
            if (i >= 0) return i;
          }
          return -1;
        };
        const idxZip = col(['郵遞區號', '區號', '3碼', 'zip', '前3碼']);
        const idxCounty = col(['縣市', '縣市別', '縣市名稱']);
        const idxDistrict = col(['鄉鎮市區', '行政區', '區鄉鎮', '鄉鎮區']);
        if (idxZip < 0) return (cachePostal = byZip);
        for (let i = 1; i < lines.length; i++) {
          const cols = lines[i].split(',');
          const zipRaw = (cols[idxZip] || '').trim();
          const zip3 = String(zipRaw).replace(/\D/g, '').slice(0, 3);
          if (!zip3) continue;
          const county = idxCounty >= 0 ? (cols[idxCounty] || '').trim() : '';
          const district = idxDistrict >= 0 ? (cols[idxDistrict] || '').trim() : '';
          if (!byZip[zip3]) byZip[zip3] = [];
          const key = county + '|' + district;
          if (!byZip[zip3].some((x) => (x.county || '') + '|' + (x.district || '') === key)) {
            byZip[zip3].push({ county, district });
          }
        }
      }
    } else {
      const XLSX = require('xlsx');
      const wb = XLSX.readFile(filePath);
      const ws = wb.Sheets[wb.SheetNames[0]];
      const rows = XLSX.utils.sheet_to_json(ws, { header: 1, defval: '' });
      if (rows.length < 2) return (cachePostal = byZip);
      const headers = (rows[0] || []).map((h) => String(h || '').trim());
      const col = (names) => {
        for (const n of names) {
          const i = headers.findIndex((h) => h === n || (h && h.toLowerCase && h.toLowerCase().includes(n)));
          if (i >= 0) return i;
        }
        return -1;
      };
      const idxZip = col(['郵遞區號', '區號', '3碼', 'zip', '前3碼']);
      const idxCounty = col(['縣市', '縣市別', '縣市名稱']);
      const idxDistrict = col(['鄉鎮市區', '行政區', '區鄉鎮', '鄉鎮區']);
      if (idxZip < 0) return (cachePostal = byZip);
      for (let i = 1; i < rows.length; i++) {
        const row = rows[i] || [];
        const zipRaw = (row[idxZip] !== undefined ? String(row[idxZip]) : '').trim();
        const zip3 = String(zipRaw).replace(/\D/g, '').slice(0, 3);
        if (!zip3) continue;
        const county = idxCounty >= 0 ? String(row[idxCounty] || '').trim() : '';
        const district = idxDistrict >= 0 ? String(row[idxDistrict] || '').trim() : '';
        if (!byZip[zip3]) byZip[zip3] = [];
        const key = county + '|' + district;
        if (!byZip[zip3].some((x) => (x.county || '') + '|' + (x.district || '') === key)) {
          byZip[zip3].push({ county, district });
        }
      }
    }
    cachePostal = byZip;
    if (Object.keys(byZip).length > 0) {
      console.log('已載入郵遞區號前3碼一覽表：', filePath);
    }
  } catch (e) {
    console.error('郵遞區號一覽表讀取失敗:', filePath, e.message);
    cachePostal = {};
  }
  return cachePostal;
}

/** 從新北市政府資料開放平台取得資料並轉成 byRoad */
async function loadFromNtpcOpenData() {
  const oid = NTPC_DATASET_OID.trim();
  if (!oid) return null;
  const byRoad = {};
  let page = 0;
  const size = 5000;
  try {
    for (;;) {
      const url = `${NTPC_OPEN_DATA_BASE}/api/datasets/${oid}/json?page=${page}&size=${size}`;
      const json = await fetchJson(url);
      const records = Array.isArray(json) ? json : json?.data ?? json?.result?.records ?? json?.records ?? [];
      if (records.length === 0) break;
      for (const r of records) {
        const road = getField(r, ['road', 'Road', '路名', '道路', 'roadname', '街路']);
        const site = getField(r, ['site_id', 'Site_id', 'district', 'District', '行政區', '行政區域名稱', '區', '鄉鎮市區']);
        if (!road) continue;
        if (!byRoad[road]) byRoad[road] = { districts: [], raw: [] };
        const districtName = site || '新北市';
        if (districtName && !byRoad[road].districts.includes(districtName)) {
          byRoad[road].districts.push(districtName);
          byRoad[road].raw.push({
            road,
            site: districtName,
            lane: getField(r, ['lane', '巷', '巷弄']),
            alley: getField(r, ['alley', '弄']),
            number: getField(r, ['number', '號', '門牌號'])
          });
        }
      }
      if (records.length < size) break;
      page += 1;
    }
    if (Object.keys(byRoad).length > 0) return { byRoad, source: 'ntpc' };
  } catch (err) {
    console.error('新北市開放平台 API 取得失敗:', err.message);
  }
  return null;
}

/** 取得路名資料：優先本地門牌 CSV → 新北市 API → 備援 JSON */
async function loadNtpcRoads() {
  if (!USE_DATA_SOURCES) {
    cacheSource = '';
    return {};
  }
  if (cacheNtpcRoads !== null && Date.now() - cacheTime < CACHE_MS) {
    return cacheNtpcRoads;
  }
  cacheByDistrict = null;
  let result = await loadFromLocalDoorplateCsv();
  if (result) {
    cacheNtpcRoads = result.byRoad;
    cacheByDistrict = buildByDistrict(cacheNtpcRoads);
    cacheSource = result.source;
    cacheTime = Date.now();
    return cacheNtpcRoads;
  }
  result = await loadFromNtpcOpenData();
  if (result) {
    cacheNtpcRoads = result.byRoad;
    cacheByDistrict = buildByDistrict(cacheNtpcRoads);
    cacheSource = result.source;
    cacheTime = Date.now();
    console.log('已從新北市政府資料開放平台載入路名資料，OID:', NTPC_DATASET_OID);
    return cacheNtpcRoads;
  }
  cacheNtpcRoads = loadFallbackRoads();
  cacheByDistrict = buildByDistrict(cacheNtpcRoads);
  cacheSource = 'fallback';
  if (cacheNtpcRoads && Object.keys(cacheNtpcRoads).length > 0) {
    cacheTime = Date.now();
    console.log('已使用備援路名資料（新北市部分範例）');
  }
  return cacheNtpcRoads || {};
}

/** API 不可用時使用本地備援資料 */
function loadFallbackRoads() {
  try {
    const raw = fs.readFileSync(FALLBACK_PATH, 'utf8');
    const records = JSON.parse(raw);
    const byRoad = {};
    for (const r of records) {
      const road = (r.road || '').trim();
      const site = (r.site_id || '').trim();
      if (!road) continue;
      if (!byRoad[road]) byRoad[road] = { districts: [], raw: [] };
      if (site && !byRoad[road].districts.includes(site)) {
        byRoad[road].districts.push(site);
        byRoad[road].raw.push({ road, site });
      }
    }
    if (cacheNtpcRoads === null) {
      cacheNtpcRoads = byRoad;
      cacheTime = Date.now();
      console.log('已使用備援路名資料（新北市部分範例）');
    }
    return byRoad;
  } catch (e) {
    console.error('備援資料讀取失敗:', e.message);
    return {};
  }
}

/** 模糊匹配路名（包含關鍵字即算） */
function matchRoad(inputRoad, roadName) {
  if (!inputRoad || !roadName) return false;
  const a = String(inputRoad).trim();
  const b = String(roadName).trim();
  if (a === b) return true;
  return b.includes(a) || a.includes(b);
}

/** 全形數字轉半形，方便「88巷」對應資料中的「８８巷」 */
function normalizeNum(s) {
  return String(s).replace(/[０-９]/g, (c) => String.fromCharCode(c.charCodeAt(0) - 0xfee0));
}

/** 取出巷/弄/號的「數字部分」用於精準比對，例如 "１１６巷" -> "116", "2弄" -> "2" */
function extractNumPart(s) {
  const n = normalizeNum(String(s).trim()).replace(/[巷弄號]$/, '').trim();
  return n;
}

/**
 * 巷、弄、號欄位比對：輸入為空則符合。
 * 若輸入與資料都是「數字+巷/弄/號」，則必須數字完全一致（打 1 巷只對 1巷，不對 116巷、291巷）。
 * 其餘用包含比對。
 */
function matchField(input, value) {
  if (!input) return true;
  if (!value) return false;
  const a = normalizeNum(String(input).trim());
  const b = normalizeNum(String(value).trim());
  if (a === b) return true;
  const numA = extractNumPart(input);
  const numB = extractNumPart(value);
  if (numA && numB && /^\d+$/.test(numA) && /^\d+$/.test(numB)) return numA === numB;
  return b.includes(a) || a.includes(b);
}

/**
 * GET /api/search?road=&district=板橋&lane=&alley=&number=5
 * 路名可留空；至少填一項即可查詢可能行政區。
 */
app.get('/api/search', async (req, res) => {
  const road = (req.query.road || '').trim();
  const district = (req.query.district || '').trim();
  const lane = (req.query.lane || '').trim();
  const alley = (req.query.alley || '').trim();
  const number = (req.query.number || '').trim();

  const hasAny = road || district || lane || alley || number;
  if (!hasAny) {
    return res.json({
      ok: false,
      message: '請至少輸入一項（行政區、路名、巷、弄、號任一）',
      possibleDistricts: [],
      query: { road, district, lane, alley, number }
    });
  }

  try {
    const byRoad = await loadNtpcRoads();
    let districts = [];
    let matchedRoads = [];
    const possibleAddresses = []; // { district, road, lane, alley, number } 完整地址，用於顯示多種可能性
    const seenKey = new Set(); // 去重用
    const MAX_ADDRESSES = 200;

    function addAddress(x) {
      const key = [x.site, x.road, x.lane || '', x.alley || ''].join('|');
      if (seenKey.has(key) || possibleAddresses.length >= MAX_ADDRESSES) return;
      seenKey.add(key);
      possibleAddresses.push({
        district: x.site,
        road: x.road,
        lane: x.lane || '',
        alley: x.alley || '',
        number: x.number || ''
      });
    }

    if (road) {
      if (byRoad[road]) {
        districts = [...byRoad[road].districts];
        matchedRoads.push({ road, districts: byRoad[road].districts });
        if (lane || alley || number) {
          for (const x of byRoad[road].raw || []) {
            if (matchField(lane, x.lane) && matchField(alley, x.alley) && matchField(number, x.number))
              addAddress(x);
          }
        }
      } else {
        for (const [r, info] of Object.entries(byRoad)) {
          if (matchRoad(road, r)) {
            matchedRoads.push({ road: r, districts: info.districts });
            for (const d of info.districts) {
              if (!districts.includes(d)) districts.push(d);
            }
            if (lane || alley || number) {
              for (const x of info.raw || []) {
                if (matchField(lane, x.lane) && matchField(alley, x.alley) && matchField(number, x.number))
                  addAddress(x);
              }
            }
          }
        }
      }
      if (district) districts = districts.filter((d) => d.includes(district) || district.includes(d));
      // 有填巷/弄/號時，只顯示「實際有該路+巷弄」的行政區，避免誤顯示其他區（例：大勇街29巷只應顯示中和區）
      if (lane || alley || number) {
        if (possibleAddresses.length > 0) {
          districts = [...new Set(possibleAddresses.map((a) => a.district).filter(Boolean))];
          if (district) districts = districts.filter((d) => d.includes(district) || district.includes(d));
        } else {
        const filteredDistricts = new Set();
        for (const m of matchedRoads) {
          const info = byRoad[m.road];
          if (!info || !info.raw) continue;
          for (const x of info.raw) {
            if (matchField(lane, x.lane) && matchField(alley, x.alley) && matchField(number, x.number)) {
              filteredDistricts.add(x.site);
              addAddress(x);
            }
          }
        }
        if (filteredDistricts.size > 0) districts = [...filteredDistricts];
        }
      }
      // 僅依路名查詢時，也加入具行政區的代表性地址（確保 banqiao_real_data 等來源的行政區能顯示）
      if (road && !(lane || alley || number) && possibleAddresses.length === 0) {
        const addedPair = new Set();
        for (const m of matchedRoads) {
          const info = byRoad[m.road];
          if (!info || !info.raw) continue;
          for (const x of info.raw) {
            if (!x.site) continue;
            const pair = x.site + '|' + x.road;
            if (addedPair.has(pair) || possibleAddresses.length >= MAX_ADDRESSES) continue;
            addedPair.add(pair);
            addAddress(x);
          }
        }
      }
    } else {
      if (district && cacheByDistrict) {
        const matchingDistricts = Object.keys(cacheByDistrict).filter(
          (d) => d.includes(district) || district.includes(d)
        );
        for (const d of matchingDistricts) {
          if (!districts.includes(d)) districts.push(d);
          const roads = cacheByDistrict[d] || [];
          matchedRoads.push({ road: roads.slice(0, 30).join('、'), districts: [d] });
        }
      }
      if ((lane || alley || number) && Object.keys(byRoad).length > 0) {
        const fromRaw = new Set();
        for (const [r, info] of Object.entries(byRoad)) {
          for (const x of info.raw || []) {
            if (matchField(lane, x.lane) && matchField(alley, x.alley) && matchField(number, x.number)) {
              fromRaw.add(x.site);
              addAddress({ site: x.site, road: r, lane: x.lane, alley: x.alley, number: x.number });
              if (!matchedRoads.some((m) => m.road === r && m.districts && m.districts[0] === x.site))
                matchedRoads.push({ road: r, districts: [x.site] });
            }
          }
        }
        if (fromRaw.size > 0) districts = [...new Set([...districts, ...fromRaw])];
      }
    }

    // 若只填巷/弄/號時有符合的地址但 districts 仍空，從 possibleAddresses 補上（確保「可能所在行政區」有顯示）
    if (districts.length === 0 && possibleAddresses.length > 0) {
      districts = [...new Set(possibleAddresses.map((a) => a.district).filter(Boolean))];
    }

    // 使用者有填行政區時，可能所在行政區與多種可能性都只保留該行政區
    if (district) {
      districts = districts.filter((d) => d.includes(district) || district.includes(d));
    }
    let outAddresses = possibleAddresses;
    if (district) {
      outAddresses = possibleAddresses.filter(
        (a) => a.district && (a.district.includes(district) || district.includes(a.district))
      );
    }

    const sourceText = !USE_DATA_SOURCES || !cacheSource
      ? '（目前未使用任何資料來源）'
      : cacheSource === 'local_csv'
        ? '新北市門牌位置數值資料_with_area.csv（本地）'
        : cacheSource === 'ntpc'
          ? '新北市政府資料開放平台門牌/地址資料'
          : '本地備援路名資料（新北市範例）';
    res.json({
      ok: true,
      possibleDistricts: districts.sort(),
      matchedRoads: matchedRoads.slice(0, 30),
      possibleAddresses: outAddresses,
      query: { road, district, lane, alley, number },
      source: sourceText,
      note: '巷、弄、號為您填寫之參考；實際門牌請以戶政門牌系統或當地戶所為準。'
    });
  } catch (err) {
    console.error(err);
    res.status(500).json({
      ok: false,
      message: '查詢失敗',
      possibleDistricts: [],
      query: { road, district, lane, alley, number }
    });
  }
});

/** 依郵遞區號（前 3 碼）查詢對應行政區，例：GET /api/postal?zip=220 */
app.get('/api/postal', (req, res) => {
  const zip = (req.query.zip || req.query.postal || '').trim().replace(/\D/g, '').slice(0, 3);
  if (!zip) {
    return res.json({ ok: false, message: '請輸入郵遞區號（前 3 碼）', areas: [] });
  }
  const byZip = loadPostalTable();
  const areas = byZip[zip] || [];
  res.json({
    ok: true,
    zip3: zip,
    areas,
    source: getPostalPath() ? '103.12.25-臺灣地區郵遞區號前3碼一覽表' : null
  });
});

/** 列出所有新北市路名（可選：依行政區過濾） */
app.get('/api/roads', async (req, res) => {
  const district = (req.query.district || '').trim();
  try {
    const byRoad = await loadNtpcRoads();
    let list = [];
    for (const [road, info] of Object.entries(byRoad)) {
      if (district) {
        const inDistrict = info.districts.some((d) => d.includes(district));
        if (inDistrict) list.push({ road, districts: info.districts });
      } else {
        list.push({ road, districts: info.districts });
      }
    }
    list.sort((a, b) => a.road.localeCompare(b.road, 'zh-TW'));
    res.json({ ok: true, roads: list });
  } catch (err) {
    res.status(500).json({ ok: false, roads: [] });
  }
});

app.listen(PORT, () => {
  console.log(`台灣地址欠祥查詢服務: http://localhost:${PORT}`);
});
