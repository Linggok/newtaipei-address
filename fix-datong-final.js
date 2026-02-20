/**
 * 最終修正大同區檔案編碼
 */

const fs = require('fs');
const path = require('path');
const iconv = require('iconv-lite');

const inputFile = path.join(__dirname, '大同區門牌位置數值資料.CSV');
const outputFile = path.join(__dirname, '大同區門牌位置數值資料_utf8.CSV');

console.log('讀取大同區檔案...');

const buffer = fs.readFileSync(inputFile);

// 從 hex 分析：99bd96bc 看起來像是 UTF-8 編碼的中文字節
// 嘗試直接以 UTF-8 讀取（沒有 BOM）
let content = buffer.toString('utf8');

// 檢查是否包含正確的中文字
if (!content.includes('區名') && !content.includes('街路段')) {
  // 如果 UTF-8 不行，嘗試其他編碼
  console.log('UTF-8 無法正確解碼，嘗試其他編碼...');
  
  // 嘗試 Big5
  try {
    const big5Content = iconv.decode(buffer, 'big5');
    if (big5Content.includes('區名') || big5Content.includes('街路段') || /[\u4e00-\u9fa5]{3,}/.test(big5Content)) {
      content = big5Content;
      console.log('使用 Big5 編碼');
    }
  } catch (e) {
    // 繼續
  }
  
  // 嘗試 GB2312
  try {
    const gbContent = iconv.decode(buffer, 'gb2312');
    if (gbContent.includes('區名') || gbContent.includes('街路段') || /[\u4e00-\u9fa5]{3,}/.test(gbContent)) {
      content = gbContent;
      console.log('使用 GB2312 編碼');
    }
  } catch (e) {
    // 繼續
  }
}

// 檢查內容
const firstLine = content.split('\n')[0];
console.log('第一行:', firstLine.substring(0, 200));

// 如果還是亂碼，嘗試手動解析
if (!content.includes('區名') && !content.includes('街路段')) {
  console.log('\n檔案可能是 Tab 分隔，嘗試解析...');
  
  // 嘗試用 Tab 分隔
  const lines = content.split('\n').filter(l => l.trim());
  if (lines.length > 0) {
    const firstLineCols = lines[0].split('\t');
    console.log('第一行欄位數:', firstLineCols.length);
    console.log('第一行欄位:', firstLineCols.slice(0, 6).map(c => c.substring(0, 20)));
  }
}

// 儲存（無論如何都儲存，讓用戶檢查）
fs.writeFileSync(outputFile, content, 'utf8');
console.log(`\n已儲存為: 大同區門牌位置數值資料_utf8.CSV`);
