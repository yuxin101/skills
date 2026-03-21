/**
 * Configuration Manager
 * 配置管理模块
 */

const fs = require('fs');
const path = require('path');

class Config {
    constructor() {
        this.config = {};
        this.load();
    }

    /**
     * 加载配置
     */
    load() {
        // 从环境变量加载
        this.config.github = {
            token: process.env.GITHUB_TOKEN || '',
            owner: process.env.GITHUB_OWNER || 'default-owner'
        };

        this.config.agents = {
            dev_count: parseInt(process.env.DEV_AGENT_COUNT) || 2,
            test_count: parseInt(process.env.TEST_AGENT_COUNT) || 1,
            review_count: parseInt(process.env.REVIEW_AGENT_COUNT) || 1
        };

        this.config.logging = {
            level: process.env.LOG_LEVEL || 'info',
            file: process.env.LOG_FILE || 'github-collab.log'
        };

        this.config.qq = {
            enabled: process.env.QQ_ENABLED === 'true',
            token: process.env.QQ_TOKEN || '',
            target: process.env.QQ_TARGET || 'qqbot:c2c:3512D704E5667F4DF660228B731965C2'
        };

        // 从配置文件加载（如果存在）
        const configPath = path.join(__dirname, '.github-collab-config.json');
        if (fs.existsSync(configPath)) {
            try {
                const fileConfig = JSON.parse(fs.readFileSync(configPath, 'utf8'));
                this.config = { ...this.config, ...fileConfig };
            } catch (error) {
                console.warn('Failed to load config file:', error.message);
            }
        }

        console.log('[Config] Configuration loaded:', JSON.stringify(this.config, null, 2));
    }

    /**
     * 获取配置
     * @param {string} key - 配置键（支持点号分隔）
     * @returns {any} - 配置值
     */
    get(key) {
        const keys = key.split('.');
        let value = this.config;
        for (const k of keys) {
            value = value?.[k];
        }
        return value;
    }

    /**
     * 设置配置
     * @param {string} key - 配置键
     * @param {any} value - 配置值
     */
    set(key, value) {
        const keys = key.split('.');
        let config = this.config;
        for (let i = 0; i < keys.length - 1; i++) {
            if (!config[keys[i]]) {
                config[keys[i]] = {};
            }
            config = config[keys[i]];
        }
        config[keys[keys.length - 1]] = value;
    }

    /**
     * 保存配置到文件
     */
    save() {
        const configPath = path.join(__dirname, '.github-collab-config.json');
        fs.writeFileSync(configPath, JSON.stringify(this.config, null, 2));
        console.log('[Config] Configuration saved to:', configPath);
    }

    /**
     * 重新加载配置
     */
    reload() {
        this.load();
    }
}

module.exports = { Config };