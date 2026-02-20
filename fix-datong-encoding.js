/**
 * 修正大同區檔案編碼
 * 嘗試多種編碼讀取並轉換為 UTF-8
 */

const fs = require('fs');
const path = require('path');
const iconv = require('iconv-lite');

const inputFile = path.join(__dirname, '大同區門牌位置數值資料.CSV');
const outputFile = path.join(__dirname, '大同區門牌位置數值資料_utf8.CSV');

// 嘗試的編碼列表
const encodings = ['big5', 'cp950', 'gb2312', 'gbk', 'gb18030', 'utf8'];

console.log('正在嘗試讀取大同區檔案...');

let success = false;
let usedEncoding = '';

for (const encoding of encodings) {
  try {
    console.log(`嘗試編碼: ${encoding}...`);
    const buffer = fs.readFileSync(inputFile);
    let content;
    
    if (encoding === 'utf8') {
      content = buffer.toString('utf8');
    } else {
      content = iconv.decode(buffer, encoding);
    }
    
    // 檢查是否成功解碼（檢查是否包含中文字或關鍵字）
    if (content.includes('區名') || content.includes('街路段') || content.includes('大同區') || 
        content.includes('中正區') || /[\u4e00-\u9fa5]/.test(content)) {
      console.log(`✓ 成功使用編碼: ${encoding}`);
      usedEncoding = encoding;
      
      // 轉換為 UTF-8 並儲存
      fs.writeFileSync(outputFile, content, 'utf8');
      console.log(`✓ 已轉換為 UTF-8 並儲存為: 大同區門牌位置數值資料_utf8.CSV`);
      success = true;
      break;
    }
  } catch (e) {
    console.log(`✗ 編碼 ${encoding} 失敗:`, e.message);
  }
}

if (!success) {
  console.log('\n無法自動偵測編碼，嘗試手動讀取...');
  try {
    const buffer = fs.readFileSync(inputFile);
    // 嘗試直接讀取前幾行看看
    const sample = buffer.slice(0, 500);
    console.log('檔案開頭（hex）:', sample.toString('hex').substring(0, 100));
  } catch (e) {
    console.error('讀取失敗:', e.message);
  }
}

if (success) {
  console.log('\n完成！請將 server.js 中的檔案路徑改為: 大同區門牌位置數值資料_utf8.CSV');
  console.log('或直接覆蓋原檔案。');
} else {
  console.log('\n無法自動修正，請手動檢查檔案編碼。');
}
