# 【1Panel】1、安装 1Panel

#### 1、1Panel 介绍

[1Panel](https://1panel.cn/) 提供了一个直观的 Web 界面，帮助用户轻松管理 Linux 服务器中的应用、网站、文件、数据库以及大语言模型（LLMs）等。

- 高效管理：用户可以通过 Web 图形界面轻松管理 Linux 服务器，实现主机监控、文件管理、数据库管理、容器管理等功能
- 快速建站：深度集成开源建站软件 WordPress 和 Halo，域名绑定、SSL 证书配置等操作一键搞定
- 应用商店：精选上架各类高质量的开源工具和应用软件，协助用户轻松安装并升级
- 安全可靠：基于容器管理并部署应用，实现最小的漏洞暴露面，同时提供防火墙和日志审计等功能
- 一键备份：支持一键备份和恢复，用户可以将数据备份到各类云端存储介质，永不丢失

#### 2、安装 1Panel

[在线安装](https://1panel.cn/docs/v2/installation/online_installation/)，需要您的系统可以访问互联网，是内网环境，推荐实现 [离线安装包](https://1panel.cn/docs/v2/installation/package_installation/) 方式进行部署。

在线安装，执行如下命令：

```bash
bash -c "$(curl -sSL https://resource.fit2cloud.com/1panel/package/v2/quick_start.sh)"
```

会有如下提示：

- 安装语言

 Select a language:

- English
- Chinese 中文 (简体)
- Persian
- Português (Brasil)
- Русский Enter the number corresponding to your language choice: 2

选择 2，中文简体即可
 2. 安装目录：/opt
 3. 是否安装 docker，选择 n，暂时不安装
 4. 面板端口，默认 39602，可以输入自定义端口号
 5. 安全入口，访问面板路径后面跟的参数，可以默认生成
 6. 用户名/密码，随机生成即可

安装完成后，会在控制台输出 1Panel 的访问地址及用户名/密码，访问地址即可打开 1Panel 的控制面板

http://<你的公网 IP>:面板端口/<安全入口>

也可以通过命令获取安全入口

```bash
1pctl user-info
```

#### 3、面板加固

- 面板设置

| 位置 | 路径 | 建议值 |
|------|------|--------|
| 端口 | 面板设置 → 服务端口 | 改成 5 位随机，如 35210 |
| 安全入口 | 面板设置 → 安全 → 安全入口 | 把 /abc123 改成 /star_xxx，我这边改成自己好记的。 |
| 授权 IP | 面板设置 → 安全 → 授权 IP | 如果有固定公网 IP，填入你的，则更安全 |
| 面板域名 | 面板设置 → 安全 → 面板 SSL | 有域名就上传证书，强制 HTTPS |

- 安装 Fail2ban

在左侧菜单找到：计划任务 --> 安装 Fail2ban
在左侧菜单找到：工具箱 --> Fail2ban

开启 SSH 防护，暴力破解 5 次就封 IP。

#### 4、修改系统信息

- 修改面板用户

```bash
1pctl update username
```

- 修改面板密码

```bash
1pctl update password
```

根据提示输入两次密码即可

- 修改面板端口

```bash
1pctl update port
```

#### 5、获取更多帮助

获取更多帮助，输入命令：

```bash
1pctl help
```

如您在阅读中发现不足，欢迎留言！！！
