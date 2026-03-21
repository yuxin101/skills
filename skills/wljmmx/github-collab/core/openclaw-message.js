/**
 * OpenClaw Message Tool Integration
 * 集成 OpenClaw message 工具接口调用能力
 */

/**
 * 发送消息到 OpenClaw 通道
 * @param {object} options - 消息选项
 * @param {string} options.channel - 目标通道（qqbot, telegram 等）
 * @param {string} options.target - 目标用户/群聊 ID
 * @param {string} options.message - 消息内容
 * @param {string} [options.media] - 媒体 URL 或本地路径
 * @param {string} [options.filename] - 文件名
 * @param {string} [options.contentType] - 内容类型
 * @returns {Promise<object>} - 消息发送结果
 */
async function sendMessage(options) {
    const {
        channel,
        target,
        message,
        media,
        filename,
        contentType
    } = options;

    // 构建消息参数
    const messageParams = {
        action: 'send',
        channel,
        target,
        message
    };

    if (media) {
        messageParams.media = media;
        if (filename) messageParams.filename = filename;
        if (contentType) messageParams.contentType = contentType;
    }

    // 调用 OpenClaw message 工具
    try {
        const result = await message(messageParams);
        return {
            success: true,
            result
        };
    } catch (error) {
        return {
            success: false,
            error: error.message
        };
    }
}

/**
 * 发送进度更新
 * @param {object} options - 进度更新选项
 * @param {string} options.channel - 目标通道
 * @param {string} options.target - 目标用户/群聊 ID
 * @param {number} options.taskId - 任务 ID
 * @param {number} options.progress - 进度百分比
 * @param {string} options.status - 状态
 * @returns {Promise<object>} - 发送结果
 */
async function sendProgressUpdate(options) {
    const { channel, target, taskId, progress, status } = options;

    const message = `📊 任务进度更新
任务 ID: ${taskId}
进度：${progress}%
状态：${status}
时间：${new Date().toLocaleString('zh-CN')}`;

    return await sendMessage({
        channel,
        target,
        message
    });
}

/**
 * 发送任务完成通知
 * @param {object} options - 通知选项
 * @param {string} options.channel - 目标通道
 * @param {string} options.target - 目标用户/群聊 ID
 * @param {number} options.taskId - 任务 ID
 * @param {string} options.taskName - 任务名称
 * @param {string} options.agentName - Agent 名称
 * @param {string} [options.result] - 任务结果
 * @returns {Promise<object>} - 发送结果
 */
async function sendTaskCompletion(options) {
    const { channel, target, taskId, taskName, agentName, result } = options;

    const message = `✅ 任务完成
任务 ID: ${taskId}
任务名称：${taskName}
执行 Agent: ${agentName}
结果：${result || '成功'}
时间：${new Date().toLocaleString('zh-CN')}`;

    return await sendMessage({
        channel,
        target,
        message
    });
}

/**
 * 发送错误通知
 * @param {object} options - 错误选项
 * @param {string} options.channel - 目标通道
 * @param {string} options.target - 目标用户/群聊 ID
 * @param {number} options.taskId - 任务 ID
 * @param {string} options.taskName - 任务名称
 * @param {string} options.error - 错误信息
 * @returns {Promise<object>} - 发送结果
 */
async function sendErrorNotification(options) {
    const { channel, target, taskId, taskName, error } = options;

    const message = `❌ 任务失败
任务 ID: ${taskId}
任务名称：${taskName}
错误：${error}
时间：${new Date().toLocaleString('zh-CN')}`;

    return await sendMessage({
        channel,
        target,
        message
    });
}

/**
 * 发送项目报告
 * @param {object} options - 报告选项
 * @param {string} options.channel - 目标通道
 * @param {string} options.target - 目标用户/群聊 ID
 * @param {string} options.report - 报告内容
 * @returns {Promise<object>} - 发送结果
 */
async function sendProjectReport(options) {
    const { channel, target, report } = options;

    // 将报告作为文件发送
    const filename = `project-report-${Date.now()}.md`;
    
    return await sendMessage({
        channel,
        target,
        message: `📋 项目报告已生成`,
        media: report,
        filename,
        contentType: 'text/markdown'
    });
}

/**
 * 发送图片
 * @param {object} options - 图片选项
 * @param {string} options.channel - 目标通道
 * @param {string} options.target - 目标用户/群聊 ID
 * @param {string} options.imageUrl - 图片 URL 或本地路径
 * @param {string} [options.caption] - 图片说明
 * @returns {Promise<object>} - 发送结果
 */
async function sendImage(options) {
    const { channel, target, imageUrl, caption = '' } = options;

    return await sendMessage({
        channel,
        target,
        message: caption,
        media: imageUrl,
        contentType: 'image'
    });
}

/**
 * 发送语音
 * @param {object} options - 语音选项
 * @param {string} options.channel - 目标通道
 * @param {string} options.target - 目标用户/群聊 ID
 * @param {string} options.audioPath - 音频文件路径
 * @returns {Promise<object>} - 发送结果
 */
async function sendVoice(options) {
    const { channel, target, audioPath } = options;

    return await sendMessage({
        channel,
        target,
        message: '',
        media: audioPath,
        contentType: 'audio'
    });
}

/**
 * 发送文件
 * @param {object} options - 文件选项
 * @param {string} options.channel - 目标通道
 * @param {string} options.target - 目标用户/群聊 ID
 * @param {string} options.filePath - 文件路径或 URL
 * @param {string} [options.filename] - 文件名
 * @returns {Promise<object>} - 发送结果
 */
async function sendFile(options) {
    const { channel, target, filePath, filename } = options;

    return await sendMessage({
        channel,
        target,
        message: `📎 文件：${filename || path.basename(filePath)}`,
        media: filePath,
        filename: filename || path.basename(filePath),
        contentType: 'file'
    });
}

// 导出所有消息发送函数
module.exports = {
    sendMessage,
    sendProgressUpdate,
    sendTaskCompletion,
    sendErrorNotification,
    sendProjectReport,
    sendImage,
    sendVoice,
    sendFile
};