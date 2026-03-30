#!/usr/bin/env node
/**
 * 电子签章 - 完整流程脚本
 * 
 * 用法:
 * node scripts/sign/workflow.js --file signers.json
 * 
 * signers.json 格式:
 * {
 *   "signers": [
 *     {
 *       "signerNo": "甲方",
 *       "type": "enterprise",
 *       "enterpriseName": "公司名称",
 *       "creditCode": "统一社会信用代码",
 *       "contactName": "联系人姓名",
 *       "contactIdCard": "联系人身份证",
 *       "contactMobile": "联系人手机"
 *     },
 *     {
 *       "signerNo": "乙方",
 *       "type": "person",
 *       "name": "姓名",
 *       "idCard": "身份证号",
 *       "mobile": "手机号"
 *     }
 *   ],
 *   "contractFile": "合同文件路径"
 * }
 */

const path = require('path');
const fs = require('fs');
const crypto = require('crypto');

const libPath = path.resolve(__dirname, '../../lib');
const configPath = path.resolve(__dirname, '../../config.json');

const { init, request } = require(path.join(libPath, 'client'));
const sign = require(path.join(libPath, 'modules/sign'));

const config = require(configPath);
init(config);

/**
 * 信息校验
 * 检查签署方是否存在，并验证信息一致性
 */
async function validateSigners(signers) {
  const errors = [];
  const existingEntities = [];

  for (const s of signers) {
    if (s.type === 'enterprise') {
      // 企业校验
      const listResult = await sign.enterprise.list(s.enterpriseName, s.creditCode);
      const enterpriseList = listResult && listResult.data ? listResult.data : (listResult || []);
      
      if (enterpriseList.length > 0) {
        const existing = enterpriseList[0];
        
        // 检查企业名称是否一致
        if (existing.principalName !== s.enterpriseName) {
          errors.push({
            signerNo: s.signerNo,
            type: 'enterprise',
            field: 'enterpriseName',
            provided: s.enterpriseName,
            systemValue: existing.principalName,
            creditCode: s.creditCode
          });
        } else {
          existingEntities.push({
            signerNo: s.signerNo,
            type: 'enterprise',
            userId: existing.userId,
            exists: true
          });
        }
      } else {
        existingEntities.push({
          signerNo: s.signerNo,
          type: 'enterprise',
          exists: false
        });
      }
    } else if (s.type === 'person') {
      // 个人校验
      const listResult = await sign.person.list(s.name, s.idCard);
      const personList = listResult && listResult.data ? listResult.data : (listResult || []);
      
      if (personList.length > 0) {
        const existing = personList[0];
        
        // 检查姓名是否一致
        if (existing.name !== s.name) {
          errors.push({
            signerNo: s.signerNo,
            type: 'person',
            field: 'name',
            provided: s.name,
            systemValue: existing.name,
            idCard: s.idCard
          });
        } else {
          existingEntities.push({
            signerNo: s.signerNo,
            type: 'person',
            userId: existing.userId,
            exists: true
          });
        }
      } else {
        existingEntities.push({
          signerNo: s.signerNo,
          type: 'person',
          exists: false
        });
      }
    }
  }

  return { errors, existingEntities };
}

/**
 * 格式化校验错误信息
 */
function formatValidationErrors(errors) {
  let message = '❌ 信息校验失败\n\n';
  
  for (const err of errors) {
    if (err.type === 'enterprise') {
      message += `【${err.signerNo}】企业信息不一致：\n`;
      message += `- 提供的企业名称：${err.provided}\n`;
      message += `- 系统中该信用代码对应的企业名称：${err.systemValue}\n`;
      message += `- 统一社会信用代码：${err.creditCode}\n\n`;
    } else {
      message += `【${err.signerNo}】个人信息不一致：\n`;
      message += `- 提供的姓名：${err.provided}\n`;
      message += `- 系统中该身份证对应的姓名：${err.systemValue}\n`;
      message += `- 身份证号：${err.idCard}\n\n`;
    }
  }
  
  message += '请确认信息是否正确，或联系管理员处理。';
  return message;
}

/**
 * 创建主体（企业或个人）
 */
async function createEntity(signer, existingEntity) {
  if (existingEntity.exists) {
    return { userId: existingEntity.userId, existed: true };
  }

  if (signer.type === 'enterprise') {
    try {
      const result = await sign.enterprise.create(signer.enterpriseName, signer.creditCode);
      return { userId: result.userId, existed: false };
    } catch (error) {
      // 如果创建失败（可能是因为已存在），尝试查询现有记录
      if (error.message && error.message.includes('重复')) {
        console.log('    ⚠️ 企业已存在，使用现有记录...');
        const listResult = await sign.enterprise.list(signer.enterpriseName, signer.creditCode);
        if (listResult && listResult.length > 0) {
          return { userId: listResult[0].userId, existed: true };
        }
      }
      throw error;
    }
  } else {
    try {
      const result = await sign.person.create(signer.name, signer.idCard);
      return { userId: result.userId, existed: false };
    } catch (error) {
      // 如果创建失败（可能是因为已存在），尝试查询现有记录
      if (error.message && error.message.includes('重复')) {
        console.log('    ⚠️ 个人已存在，使用现有记录...');
        const listResult = await sign.person.list(signer.name, signer.idCard);
        if (listResult && listResult.length > 0) {
          return { userId: listResult[0].userId, existed: true };
        }
      }
      throw error;
    }
  }
}

/**
 * 创建印章
 * 企业印章：enterpriseSealType: 1, sealMode: 2
 * 个人签名：sealMode: 2
 */
async function createSeal(signer, userId) {
  if (signer.type === 'enterprise') {
    // 检查是否已有印章
    const sealList = await sign.enterpriseSeal.list({ principalName: signer.enterpriseName });
    if (sealList && sealList.data && sealList.data.length > 0) {
      return { sealId: sealList.data[0].sealId, existed: true };
    }

    // 创建企业印章 - enterpriseSealType: 1, sealMode: 2
    const sealResult = await sign.enterpriseSeal.create({
      userId: userId,
      sealName: signer.enterpriseName + '印章',
      enterpriseSealType: 1,  // 自定义印章
      sealMode: 2             // 印章样式
    });
    
    return { sealId: sealResult.sealId, existed: false };
  } else {
    // 检查是否已有签名
    const sealList = await sign.personSeal.list(signer.name, signer.idCard);
    if (sealList && sealList.data && sealList.data.length > 0) {
      return { sealId: sealList.data[0].sealId, existed: true };
    }

    // 创建个人签名 - sealMode: 2
    const sealResult = await sign.personSeal.create({
      userId: userId,
      sealName: signer.name + '签名',
      sealMode: 2  // 签名样式
    });
    
    return { sealId: sealResult.sealId, existed: false };
  }
}

/**
 * 完整流程
 */
async function workflow(signersData) {
  const { signers, contractFile } = signersData;

  // 检查签署方数量
  if (signers.length > 6) {
    throw new Error('签署方数量超过限制，最多支持6个签署方');
  }

  console.log('='.repeat(60));
  console.log('电子签章流程');
  console.log('='.repeat(60));
  console.log(`\n签署方数量: ${signers.length}`);

  // Step 0: 信息校验
  console.log('\n【Step 0】信息校验...');
  const { errors, existingEntities } = await validateSigners(signers);
  
  if (errors.length > 0) {
    console.log(formatValidationErrors(errors));
    return { success: false, errors };
  }
  console.log('✅ 信息校验通过');

  // 准备签署方信息
  const preparedSigners = [];

  // Step 1: 创建主体
  console.log('\n【Step 1】创建主体...');
  for (let i = 0; i < signers.length; i++) {
    const s = signers[i];
    const existing = existingEntities[i];
    
    console.log(`  ${s.signerNo}: ${s.type === 'enterprise' ? s.enterpriseName : s.name}`);
    
    const entityResult = await createEntity(s, existing);
    console.log(`    userId: ${entityResult.userId} ${entityResult.existed ? '(已存在)' : '(新建)'}`);
    
    preparedSigners.push({
      ...s,
      userId: entityResult.userId
    });
  }

  // Step 2: 创建印章
  console.log('\n【Step 2】创建印章...');
  for (const s of preparedSigners) {
    console.log(`  ${s.signerNo}: ${s.type === 'enterprise' ? s.enterpriseName : s.name}`);
    
    const sealResult = await createSeal(s, s.userId);
    s.sealId = sealResult.sealId;
    console.log(`    sealId: ${s.sealId} ${sealResult.existed ? '(已存在)' : '(新建)'}`);
  }

  // Step 3: 上传合同文件
  console.log('\n【Step 3】上传合同文件...');
  const fileBuffer = fs.readFileSync(contractFile);
  const base64 = fileBuffer.toString('base64');
  console.log(`  文件: ${contractFile}`);
  console.log(`  大小: ${(fileBuffer.length / 1024).toFixed(2)} KB`);

  const uploadResult = await sign.file.upload(base64, path.basename(contractFile), '.pdf');
  // 兼容两种返回格式: { fileId } 或 { code, data: { fileId } }
  const fileId = uploadResult.fileId || (uploadResult.data && uploadResult.data.fileId);
  console.log(`  ✅ fileId: ${fileId}`);

  // Step 4: 创建合同模板
  console.log('\n【Step 4】创建合同模板...');
  const templateName = `合同模板_${Date.now()}`;
  const signerNoList = preparedSigners.map(s => s.signerNo);
  
  const templateResult = await sign.template.create({
    templateName: templateName,
    fileList: [{
      fileId: fileId,
      fileName: path.basename(contractFile),
      signerList: signerNoList,
      controlList: [
        { controlName: '签署日期', controlKey: 'sign_date', controlKeyType: 'text', allowEdit: 1, isRequired: 1 }
      ]
    }]
  });

  // 兼容两种返回格式
  const templateId = templateResult.templateId || (templateResult.data && templateResult.data.templateId);
  const templatePreviewUrl = templateResult.previewUrl || (templateResult.data && templateResult.data.previewUrl);
  console.log(`  ✅ templateId: ${templateId}`);
  console.log(`  模板预览链接: ${templatePreviewUrl}`);

  // 返回结果
  return {
    success: true,
    signers: preparedSigners.map(s => ({
      signerNo: s.signerNo,
      type: s.type,
      userId: s.userId,
      sealId: s.sealId,
      name: s.type === 'enterprise' ? s.enterpriseName : s.name
    })),
    template: {
      templateId: templateId,
      templateName: templateName,
      previewUrl: templatePreviewUrl
    },
    fileId: fileId,
    nextStep: '请打开模板预览链接配置签署位置，配置完成后调用创建签署流程接口'
  };
}

// CLI 入口
function parseArgs() {
  const args = process.argv.slice(2);
  const params = {};

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg.startsWith('--')) {
      const key = arg.slice(2);
      const value = args[i + 1];
      if (value && !value.startsWith('--')) {
        params[key] = value;
        i++;
      }
    }
  }

  return params;
}

async function main() {
  const params = parseArgs();

  if (!params.file) {
    console.error('用法: node workflow.js --file signers.json');
    console.error('\nsigners.json 格式:');
    console.error(JSON.stringify({
      signers: [
        {
          signerNo: '甲方',
          type: 'enterprise',
          enterpriseName: '公司名称',
          creditCode: '统一社会信用代码',
          contactName: '联系人姓名',
          contactIdCard: '联系人身份证',
          contactMobile: '联系人手机'
        },
        {
          signerNo: '乙方',
          type: 'person',
          name: '姓名',
          idCard: '身份证号',
          mobile: '手机号'
        }
      ],
      contractFile: '合同文件路径'
    }, null, 2));
    process.exit(1);
  }

  const signersData = JSON.parse(fs.readFileSync(params.file, 'utf-8'));

  try {
    const result = await workflow(signersData);
    console.log('\n' + '='.repeat(60));
    console.log('【结果】');
    console.log('='.repeat(60));
    console.log(JSON.stringify(result, null, 2));
  } catch (error) {
    console.error('\n❌ 执行失败:', error.message);
    process.exit(1);
  }
}

main();