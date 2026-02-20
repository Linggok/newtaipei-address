/**
 * 修正大同區檔案編碼 - 版本 2
 * 嘗試更多編碼方式
 */

const fs = require('fs');
const path = require('path');
const iconv = require('iconv-lite');

const inputFile = path.join(__dirname, '大同區門牌位置數值資料.CSV');

console.log('正在讀取大同區檔案...');

const buffer = fs.readFileSync(inputFile);
console.log('檔案大小:', buffer.length, 'bytes');

// 嘗試更多編碼
const encodings = [
  'big5',
  'cp950', 
  'gb2312',
  'gbk',
  'gb18030',
  'utf8',
  'utf16le',
  'utf16be'
];

let bestMatch = null;
let bestScore = 0;

for (const encoding of encodings) {
  try {
    let content;
    if (encoding === 'utf8') {
      content = buffer.toString('utf8');
    } else if (encoding === 'utf16le' || encoding === 'utf16be') {
      // UTF-16 需要特殊處理
      try {
        content = buffer.toString(encoding === 'utf16le' ? 'utf16le' : 'utf16be');
      } catch (e) {
        continue;
      }
    } else {
      content = iconv.decode(buffer, encoding);
    }
    
    // 計算中文字符數量
    const chineseChars = (content.match(/[\u4e00-\u9fa5]/g) || []).length;
    const hasKeywords = content.includes('區名') || content.includes('街路段') || 
                        content.includes('大同區') || content.includes('中正區');
    
    const score = chineseChars + (hasKeywords ? 1000 : 0);
    
    console.log(`編碼 ${encoding}: 中文字 ${chineseChars} 個, 關鍵字: ${hasKeywords}, 分數: ${score}`);
    
    if (score > bestScore) {
      bestScore = score;
      bestMatch = { encoding, content };
    }
    
    // 顯示前 200 個字符
    if (chineseChars > 0) {
      console.log(`  前 200 字符:`, content.substring(0, 200));
    }
  } catch (e) {
    console.log(`編碼 ${encoding} 失敗:`, e.message);
  }
}

if (bestMatch && bestMatch.content) {
  console.log(`\n最佳編碼: ${bestMatch.encoding}`);
  console.log(`前 500 字符:\n${bestMatch.content.substring(0, 500)}`);
  
  // 儲存轉換後的檔案
  const outputFile = path.join(__dirname, '大同區門牌位置數值資料_utf8.CSV');
  fs.writeFileSync(outputFile, bestMatch.content, 'utf8');
  console.log(`\n已儲存為: 大同區門牌位置數值資料_utf8.CSV`);
} else {
  console.log('\n無法找到合適的編碼');
}
