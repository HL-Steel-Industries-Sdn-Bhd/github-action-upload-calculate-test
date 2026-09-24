# GitHub Action Upload Calculate Test

用 GAS 定时触发 GitHub Actions，跑完 9 个模块的贡献分计算，结果写到目标 Google Sheet。

## ⚠️ 安全须知

- 本仓库是 **Public**，用于实验。
- **绝对不要** commit 任何 `*.json` key 文件。
- SA 的 JSON key 只存在 GitHub Secret `GOOGLE_SA_JSON`。
- GAS 触发器里的 GitHub PAT 只存在 script.google.com，不进仓库。

## 运行方式

- GAS 每天定时 → 打 `repository_dispatch` → Actions 跑 `scripts/main.py`
- 也可在 Actions 页面手动 `Run workflow`

## 目标表

`1P8-PVmRWDjgPGZ5HjpzHNXEelPWnpDhnXEupaMxnFxI`
