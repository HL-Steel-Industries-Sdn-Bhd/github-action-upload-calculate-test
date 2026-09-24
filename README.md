# GitHub Action Upload Calculate Test

用 GAS 定时触发 GitHub Actions，跑完贡献分计算，结果写到目标 Google Sheet。

## 架构
- GAS 每天定时 → 打 repository_dispatch → Actions 跑 scripts/main.py
- Actions 用 Drive API 导出 XLSX 到 /tmp，本地 pandas 计算，写回目标表
- 全程只用 10 次网络请求，不撞配额

## ⚠️ 安全
- 本仓库是 Public，用于实验。
- 绝不 commit 任何 *.json key。
- SA JSON 只存在 GitHub Secret `GOOGLE_SA_JSON`。
- GAS 里的 GitHub PAT 只存在 script.google.com，不进仓库。

## 目标表
1P8-PVmRWDjgPGZ5HjpzHNXEelPWnpDhnXEupaMxnFxI
