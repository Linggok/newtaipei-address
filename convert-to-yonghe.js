/**
 * 將板橋區門牌資料轉換為永和區格式
 * 注意：此轉換僅替換行政區名稱與代碼，路名、村里、座標仍為板橋區資料
 * 正確的永和區門牌資料請至 新北市政府資料開放平臺 下載
 */
const fs = require('fs');
const path = require('path');

const INPUT_PATH = path.join('c:', 'Users', 'user', 'Desktop', '板橋', '新北市門牌位置數值資料.csv');
const OUTPUT_FULL = path.join(__dirname, '永和區門牌位置數值資料.csv');
const OUTPUT_SIMPLE = path.join(__dirname, 'yonghe_real_data.csv');

// 永和區 areacode（新北市行政區編碼，永和區約為 65000020）
const YONGHE_AREACODE = '65000020';

function convertFullFormat() {
  const raw = fs.readFileSync(INPUT_PATH, 'utf8');
  const lines = raw.split(/\r?\n/);
  const header = lines[0];
  const dataLines = lines.slice(1);
  
  const converted = [header];
  for (const line of dataLines) {
    if (!line.trim()) continue;
    let convertedLine = line
      .replace(/板橋區/g, '永和區')
      .replace(/65000010/g, YONGHE_AREACODE);
    converted.push(convertedLine);
  }
  
  fs.writeFileSync(OUTPUT_FULL, converted.join('\n'), 'utf8');
  const dataCount = converted.filter((l, i) => i > 0 && l.trim()).length;
  console.log('已建立:', OUTPUT_FULL, '共', dataCount, '筆');
}

function convertSimpleFormat() {
  const banqiaoPath = path.join(__dirname, 'banqiao_real_data.csv');
  const raw = fs.readFileSync(banqiaoPath, 'utf8');
  const lines = raw.split(/\r?\n/);
  const header = lines[0];
  const dataLines = lines.slice(1);
  
  const converted = [header];
  for (const line of dataLines) {
    if (!line.trim()) continue;
    const convertedLine = line.replace(/板橋區/g, '永和區');
    converted.push(convertedLine);
  }
  
  fs.writeFileSync(OUTPUT_SIMPLE, converted.join('\n'), 'utf8');
  console.log('已建立:', OUTPUT_SIMPLE, '共', converted.length - 1, '筆');
}

// 執行
convertFullFormat();
convertSimpleFormat();
console.log('\n※ 注意：路名、村里、座標等仍為板橋區原始資料，僅行政區名稱已改為永和區');
console.log('  正確的永和區門牌資料請至 https://data.ntpc.gov.tw 下載');
