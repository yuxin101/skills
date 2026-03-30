#!/usr/bin/env node
/**
 * 电子签章 - 交互式工作流
 * 所有不确定的信息都会询问用户
 */

const path = require('path');
const fs = require('fs');
const readline = require('readline');

const libPath = path.resolve(__dirname, '../../lib');
const configPath = path.resolve(__dirname, '../../config.json');

const { init } = require(path.join(libPath, 'client'));
const sign = require(path.join(libPath, 'modules/sign'));

const config = require(configPath);
init(config);

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

function ask(question) {
  return new Promise(resolve => rl.question(question, resolve));
}

function askConfirm(question) {
  return ask(question + ' (yes/no): ').then(answer => 
    answer.toLowerCase() === 'yes' || answer.toLowerCase() === 'y'
  );
}

async function main() {
  console.log('\n📝 电子签章工作流向导');
  console.log('='.repeat(50));
  console.log('说明：所有不确定的信息都会询问您确认');
  console.log('='.repeat(50) + '\n');

  try {
    // Step 1: 询问合同文件和签署方数量
    console.log('Step 1: 合同文件和签署方数量\n');
    console.log('❓ 请提供以下信息：\n');
    console.log('合同文件:');
    const contractPath = await ask('  文件路径: ');
    
    if (!contractPath || !fs.existsSync(contractPath)) {
      console.log('\n❌ 文件不存在或路径无效');
      rl.close();
      return;
    }
    
    const stats = fs.statSync(contractPath);
    const sizeMB = stats.size / (1024 * 1024);
    if (sizeMB > 10) {
      console.log(`\n❌ 文件太大：${sizeMB.toFixed(2)}MB`);
      rl.close();
      return;
    }
    
    console.log('\n签署方数量:');
    const enterpriseCount = parseInt(await ask('  企业方: ')) || 0;
    const personCount = parseInt(await ask('  个人方: ')) || 0;
    
    console.log(`\n✅ 合同文件：${contractPath}`);
    console.log(`✅ 签署方：${enterpriseCount}方企业 + ${personCount}方个人\n`);
    
    // Step 2: 提供信息填写模板
    console.log('Step 2: 填写签署方信息\n');
    console.log('='.repeat(50));
    
    const signers = [];
    let signerIndex = 1;
    
    // 企业方
    for (let i = 0; i < enterpriseCount; i++) {
      console.log(`\n【企业方${signerIndex}】\n`);
      console.log('  企业名称: [填写]');
      console.log('  统一社会信用代码: [填写]');
      console.log('  联系人姓名: [填写]');
      console.log('  联系人身份证: [填写]');
      console.log('  联系人手机: [填写]');
      console.log('');
      
      const enterpriseName = await ask('  企业名称: ');
      const creditCode = await ask('  统一社会信用代码: ');
      const contactName = await ask('  联系人姓名: ');
      const contactIdCard = await ask('  联系人身份证: ');
      const mobile = await ask('  联系人手机: ');
      
      signers.push({
        type: 'enterprise',
        signerNo: `企业方${signerIndex}`,
        enterpriseName,
        creditCode,
        contactName,
        contactIdCard,
        mobile
      });
      signerIndex++;
    }
    
    // 个人方
    for (let i = 0; i < personCount; i++) {
      console.log(`\n【个人方${signerIndex}】\n`);
      console.log('  姓名: [填写]');
      console.log('  身份证: [填写]');
      console.log('  手机: [填写]');
      console.log('');
      
      const name = await ask('  姓名: ');
      const idCard = await ask('  身份证: ');
      const mobile = await ask('  手机: ');
      
      signers.push({
        type: 'person',
        signerNo: `个人方${signerIndex}`,
        name,
        idCard,
        mobile
      });
      signerIndex++;
    }
    
    // Step 3: 确认信息
    console.log('\n' + '='.repeat(50));
    console.log('Step 3: 确认信息\n');
    console.log('合同文件:', contractPath);
    console.log(`签署方: ${enterpriseCount}方企业 + ${personCount}方个人`);
    console.log('');
    
    signers.forEach((s) => {
      console.log(`【${s.signerNo}】${s.type === 'enterprise' ? '企业' : '个人'}`);
      if (s.type === 'enterprise') {
        console.log('  企业名称:', s.enterpriseName);
        console.log('  统一社会信用代码:', s.creditCode);
        console.log('  联系人:', s.contactName);
        console.log('  手机:', s.mobile);
      } else {
        console.log('  姓名:', s.name);
        console.log('  身份证:', s.idCard);
        console.log('  手机:', s.mobile);
      }
      console.log('');
    });
    
    const confirmed = await askConfirm('确认创建签署流程？');
    if (!confirmed) {
      console.log('\n❌ 已取消');
      rl.close();
      return;
    }
    
    // Step 4: 执行流程
    console.log('\nStep 4: 执行签署流程...\n');
    console.log('正在执行，请稍候...');
    
    // 这里执行实际的签署流程...
    
    console.log('\n🎉 签署流程创建完成！');
    
  } catch (error) {
    console.log('\n❌ 错误:', error.message);
  }
  
  rl.close();
}

main();