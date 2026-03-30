/**
 * 雅思复盘笔记 PDF 生成脚本
 * 用法：node generate-pdf.js <HTML文件路径>
 * 示例：node generate-pdf.js 剑5-Test1-Passage1-XXX复盘.html
 */
const puppeteer = require('puppeteer-core');
const path = require('path');
const fs = require('fs');

const htmlFile = process.argv[2];
if (!htmlFile) {
  console.error('❌ 请提供 HTML 文件路径，例如：node generate-pdf.js 复盘笔记.html');
  process.exit(1);
}

const absPath = path.resolve(htmlFile);
if (!fs.existsSync(absPath)) {
  console.error(`❌ 文件不存在：${absPath}`);
  process.exit(1);
}

const pdfPath = absPath.replace(/\.html$/, '.pdf');

(async () => {
  const browser = await puppeteer.launch({
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    headless: true
  });
  const page = await browser.newPage();
  await page.goto('file://' + absPath, { waitUntil: 'networkidle0' });
  await page.pdf({
    path: pdfPath,
    format: 'A4',
    margin: { top: '2cm', right: '2cm', bottom: '2cm', left: '2cm' },
    printBackground: true,
    displayHeaderFooter: false
  });
  await browser.close();
  console.log(`✅ PDF 已生成：${pdfPath}`);
})();
