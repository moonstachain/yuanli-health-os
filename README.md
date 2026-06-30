# 原力健康 OS｜Public Site

AI Agent Native 的个人健康操作系统：把健康数据转化为每日决策、每周复盘、季度实验和医生沟通包。

## 仓库定位

这是 **Public 外显仓库**，只放：

- 产品官网与公开 Demo
- PC Desktop HTML 原型
- 数据 schema 与 demo data
- Codex 接入任务与战略规划文档

不要把真实体检报告、Apple Health 导出、真实 `health.json`、身份证明、手机号、就诊报告等敏感数据提交到 public 仓库。

## 推荐仓库名

`yuanli-health-os`

## 页面

- `index.html`：公开网站首页
- `app.html`：PC Agent Demo
- `docs/STRATEGY.md`：战略规划
- `docs/CODEX_TASKS.md`：Codex 接入任务
- `data/demo-health.json`：公开示例数据

## GitHub Pages 发布

推荐：Settings → Pages → Build and deployment → Source: Deploy from a branch → Branch: `main` → Folder: `/root` → Save。

发布后地址通常为：

`https://<github-username>.github.io/yuanli-health-os/`

## 本地预览

直接双击 `index.html` 或启动一个静态服务：

```bash
python -m http.server 8080
```

然后打开：

`http://localhost:8080`
