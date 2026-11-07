# 如何恢复 QQ 小号

> 适用：小号被风控、NapCat 起不来、二维码刷不出、想让小号重新上线。
> 前提：**只用小号**；主号永远只走官方 QQ Bot。

## 风控后的正确姿势

1. **立即停掉协议端**，别反复重试：
   ```powershell
   fish\qq-life\start-napcat.ps1 -Stop
   ```
2. 手机用**官方 QQ** 正常登录小号，按提示完成安全验证（如有）；
3. **养号 3–7 天**：正常聊天、别频繁改资料/发说说/换设备；
4. 期间大肥鱼聊天走官方 QQ Bot 与微信，不受影响；
5. 恢复后先只登协议端、不立刻做写操作，观察 1–2 天。

## 重新上线的步骤

1. 确认没有 QQ/QQEX 残留进程：
   ```powershell
   Get-Process QQ,QQEX,NapCatWinBootMain -ErrorAction SilentlyContinue
   ```
2. 启动（脚本已带 `NAPCAT_DISABLE_MULTI_PROCESS=1` 与 `--disable-gpu`）：
   ```powershell
   fish\qq-life\start-napcat.ps1
   ```
3. 打开 WebUI：`http://127.0.0.1:6099/webui?token=<token>`；
4. **用小号扫码**；二维码约 2 分钟过期，过期就：
   ```powershell
   python fish\qq-life\qq_life.py qr --refresh --save out\qrcode-now.png
   ```
5. 验证：
   ```powershell
   python fish\qq-life\qq_life.py status      # isLogin=True / coreReady=True
   ```
   并确认 3000 端口出现、AstrBot 日志「适配器已连接」。

## 常见故障

| 现象 | 处理 |
|---|---|
| 6099 不监听 | NapCat 没起；检查日志 `fish\qq-life\out\napcat-*.log` |
| 二维码刷新超时 | 清 `%APPDATA%\QQ\GPUCache`、`Code Cache`、`GrShaderCache`、`DawnGraphiteCache`、`DawnWebGPUCache`，再起 |
| QQ 窗口黑屏 | 同上；不要用主号测试 |
| login rate limit | 调高 `napcat\shell\config\webui.json` 的 `loginRate` |
| 主号误扫 | 立刻停协议端；手机主号做安全验证/改密/删异常设备；以后只扫小号 |
| 3000 不通 | QQ 未登录成功（二维码没扫/过期） |

## 不要做

- ❌ 主号扫码；
- ❌ 风控期反复重启注入；
- ❌ 刚恢复就批量改头像/发说说/加好友；
- ❌ 把二维码截图外传。

## 相关

- [端口与路径](../reference/端口与路径.md)
- [排障](排障.md)
- [配置项](../reference/配置项.md)
