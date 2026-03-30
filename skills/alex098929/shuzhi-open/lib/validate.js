/**
 * 配置校验模块
 */

/**
 * 校验配置是否完整
 * @param {object} config - 配置对象
 * @returns {boolean} 校验通过返回 true
 * @throws {Error} 配置不完整时抛出错误（包含详细的配置指导）
 */
function validateConfig(config) {
  const errors = [];
  const warnings = [];
  
  // 检查基础配置 - baseUrl
  if (!config.baseUrl) {
    errors.push({
      field: 'baseUrl',
      message: 'baseUrl 未配置',
      guide: '请配置接口地址，测试环境: https://test-apisix-gateway.shuzhi.shuqinkeji.cn'
    });
  }
  
  // appKey 和 appSecret 检查（作为警告，不阻止运行）
  if (!config.appKey) {
    warnings.push({
      field: 'appKey',
      message: 'appKey 未配置',
      guide: '请在 config.json 中填入数秦开放平台提供的 appKey'
    });
  }
  if (!config.appSecret) {
    warnings.push({
      field: 'appSecret',
      message: 'appSecret 未配置',
      guide: '请在 config.json 中填入数秦开放平台提供的 appSecret'
    });
  }
  
  // 检查各产品配置
  if (!config.products) {
    errors.push({
      field: 'products',
      message: 'products 未配置',
      guide: '请在 config.json 中配置 products 对象'
    });
  } else {
    // 区块链API服务 - upload 和 queryResult 是必须的
    if (config.products.chain) {
      const chainEndpoints = config.products.chain.endpoints || {};
      
      // 必须配置的端点
      const requiredEndpoints = ['upload', 'queryResult'];
      for (const endpointKey of requiredEndpoints) {
        const endpoint = chainEndpoints[endpointKey];
        if (!endpoint || !endpoint.productId) {
          errors.push({
            field: `products.chain.endpoints.${endpointKey}.productId`,
            message: `区块链API服务「${endpoint?.description || endpointKey}」的产品标识未配置`,
            guide: `请向数秦开放平台获取「${endpoint?.description || endpointKey}」接口的应用产品标识，并填入 config.json`
          });
        }
      }
    }
    
    // 自动化取证（可选）
    if (config.products.evidence && !config.products.evidence.productId) {
      warnings.push({
        field: 'products.evidence.productId',
        message: '自动化取证的产品标识未配置',
        guide: '如需使用自动化取证功能，请配置产品标识'
      });
    }
    
    // 保管单组件（可选）
    if (config.products.certificate && !config.products.certificate.productId) {
      warnings.push({
        field: 'products.certificate.productId',
        message: '保管单组件的产品标识未配置',
        guide: '如需使用保管单功能，请配置产品标识'
      });
    }
    
    // 电子签章（可选）
    if (config.products.sign && !config.products.sign.productId) {
      warnings.push({
        field: 'products.sign.productId',
        message: '电子签章的产品标识未配置',
        guide: '如需使用电子签章功能，请配置产品标识'
      });
    }
  }
  
  // 生成错误消息
  if (errors.length > 0) {
    const errorLines = ['\n❌ 配置错误，请按以下指导完成配置：\n'];
    
    errors.forEach((err, index) => {
      errorLines.push(`${index + 1}. ${err.message}`);
      errorLines.push(`   → ${err.guide}`);
      errorLines.push(`   配置路径: config.json → ${err.field}`);
      errorLines.push('');
    });
    
    if (warnings.length > 0) {
      errorLines.push('\n⚠️  以下配置项未完成：\n');
      warnings.forEach((warn) => {
        errorLines.push(`   - ${warn.message}`);
      });
    }
    
    errorLines.push('\n📖 详细配置说明请参考 SKILL.md 或 references/ 目录下的 API 文档\n');
    
    throw new Error(errorLines.join('\n'));
  }
  
  return true;
}

/**
 * 获取端点配置
 * @param {object} config - 配置对象
 * @param {string} product - 产品名称
 * @param {string} endpoint - 端点名称
 * @returns {object} { path, productId }
 */
function getEndpointConfig(config, product, endpoint) {
  const productConfig = config.products[product];
  if (!productConfig) {
    throw new Error(`产品 "${product}" 不存在`);
  }
  
  const endpointConfig = productConfig.endpoints[endpoint];
  if (!endpointConfig) {
    throw new Error(`端点 "${product}.${endpoint}" 不存在`);
  }
  
  // 端点级 productId（区块链API服务）
  if (endpointConfig.productId !== undefined) {
    if (!endpointConfig.productId) {
      throw new Error(`\n❌ 配置错误：区块链API服务「${endpoint}」的产品标识未配置\n   → 请在 config.json 中配置 products.chain.endpoints.${endpoint}.productId\n`);
    }
    return {
      path: endpointConfig.path,
      productId: endpointConfig.productId
    };
  }
  
  // 产品级 productId
  if (!productConfig.productId) {
    throw new Error(`\n❌ 配置错误：${productConfig.name || product} 的产品标识未配置\n   → 请在 config.json 中配置 products.${product}.productId\n`);
  }
  
  return {
    path: typeof endpointConfig === 'string' ? endpointConfig : endpointConfig.path,
    productId: productConfig.productId
  };
}

/**
 * 获取产品配置
 * @param {object} config - 配置对象
 * @param {string} product - 产品名称
 * @returns {object} 产品配置
 */
function getProductConfig(config, product) {
  const productConfig = config.products[product];
  if (!productConfig) {
    throw new Error(`产品 "${product}" 不存在`);
  }
  return productConfig;
}

module.exports = {
  validateConfig,
  getEndpointConfig,
  getProductConfig
};