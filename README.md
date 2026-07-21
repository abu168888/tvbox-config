# TVBox 全自动监控系统 — v2.0 4K 专版

## 系统架构

```
┌───────────────────────────────────────────┐
│            本机 (192.167.0.147)           │
│                                           │
│  tvbox-monitor/                           │
│  ├── monitor.py       # 健康检测 + 评分    │
│  ├── auto_replace.py  # 失效自动替换       │
│  ├── watchdog.py      # 服务自启守护       │
│  ├── server.py        # HTTP 服务 (8080)   │
│  └── sources.json     # 当前片源列表       │
│                                           │
│  tvbox-github/                              │
│  └── tvbox.json     # 公网配置 (GitHub)    │
│                                           │
│  tvbox-package/                           │
│  └── config.json    # TVBox 配置文件       │
└───────────────────────────────────────────┘
         │ Git Push          │
         ▼                   ▼
┌──────────────────┐  ┌────────────────────┐
│ GitHub Pages      │  │ jsdelivr CDN       │
│ 直连访问          │  │ 加速访问            │
└──────────────────┘  └────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────┐
│  电视盒子 (TVBox)                            │
│  配置地址: http://192.167.0.147:8080/tvbox  │
│  或 GitHub: xxx.github.io/xxx/tvbox.json    │
│  或 CDN:    jsdelivr.net/gh/.../tvbox.json  │
└─────────────────────────────────────────────┘
```

## 使用方式

### 方式一：局域网直连（推荐，最快）
```
在 TVBox 设置 → 配置中心 → 配置地址:
http://192.167.0.147:8080/tvbox
```

### 方式二：公网访问
```
GitHub Pages 地址:
https://abu168888.github.io/tvbox-config/tvbox.json

CDN 加速地址:
https://cdn.jsdelivr.net/gh/abu168888/tvbox-config@main/tvbox.json
```

## 功能特性

| 功能 | 说明 |
|------|------|
| 4K 片源优先 | 玩偶哥哥/立播/米搜 4K 云盘源置顶 |
| 健康检测 | 响应时间/内容大小/内容有效性 三维评分 |
| 失效替换 | 内置 100+ 备用源，失效自动替换 |
| 自动采集 | 从 liucn.cc 等公开源采集新片源 |
| 服务守护 | watchdog.py 监控 server.py，崩溃自动重启 |
| 定时监控 | Windows 计划任务每日凌晨 2:00 自动检测 |
| 开机自启 | 启动批处理加入系统启动文件夹 |
| 备份机制 | 每次修改前自动备份到 backups/ |
| 日志系统 | monitor.log + server.log + errors.log |

## 运维命令

| 命令 | 说明 |
|------|------|
| `python server.py` | 启动 HTTP 服务 |
| `python monitor.py` | 执行一次健康检测+替换 |
| `python auto_replace.py` | 执行自动替换 |
| `python watchdog.py` | 启动守护进程 |
| `netstat -ano \| findstr :8080` | 查看端口占用 |
| `schtasks /query /tn TVBox_Monitor_Daily` | 查看定时任务 |

## 维护说明

1. **电脑保持开机** — 电视盒子需要局域网访问
2. **防火墙允许 8080 端口** — 确保局域网可访问
3. **建议路由器设置静态 IP** — 避免 IP 变化
4. **片源失效属正常** — 系统每日凌晨自动检测替换
5. **GitHub 推送** — 需要 GitHub 账号和 token
