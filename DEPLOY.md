# 段永平智慧库 - Cloudflare Pages 部署指南

## 📦 已完成准备工作

- [x] Git仓库已初始化
- [x] 代码已提交（104个文件）

---

## 🚀 部署步骤

### 步骤1：创建GitHub仓库

1. 打开 https://github.com/new
2. 填写信息：
   - Repository name: `duanyongping-wisdom`
   - Description: `段永平投资智慧知识库`
   - 选择 **Public**
   - **不要**勾选 "Add a README file"
3. 点击 **Create repository**

### 步骤2：推送到GitHub

创建仓库后，GitHub会显示命令，或者在本地执行：

```bash
cd "C:\Users\Charlie\Desktop\段永平智慧库"
git remote add origin https://github.com/YOUR_USERNAME/duanyongping-wisdom.git
git branch -M main
git push -u origin main
```

**注意：** 把 `YOUR_USERNAME` 替换成你的GitHub用户名

### 步骤3：连接Cloudflare Pages

1. 打开 https://dash.cloudflare.com/
2. 点击左侧 **Workers & Pages**
3. 点击 **Create application**
4. 选择 **Pages** 标签
5. 点击 **Connect to Git**
6. 选择 **GitHub**，授权连接
7. 选择你的 `duanyongping-wisdom` 仓库
8. 配置构建设置：
   - Project name: `duanyongping` （或其他名称）
   - Production branch: `main`
   - Build command: 留空
   - Build output directory: `/` 或留空
9. 点击 **Save and Deploy**

### 步骤4：获取网站地址

部署完成后，你会获得一个免费域名：
- `https://duanyongping.pages.dev`

你也可以绑定自定义域名（如 `duanyongping.fangcunbiji.cn`）

---

## 🔄 后续更新流程

当你有新内容时：

```bash
# 1. 同步HTML（双击 sync.py 或运行）
python sync.py

# 2. 提交并推送到GitHub
cd "C:\Users\Charlie\Desktop\段永平智慧库"
git add .
git commit -m "更新内容"
git push

# 3. Cloudflare Pages 会自动部署！
```

---

## 📝 注意事项

1. **首次推送需要GitHub登录**
   - 如果使用HTTPS，需要输入用户名和密码（或Personal Access Token）
   - 推荐使用SSH密钥

2. **Cloudflare Pages自动部署**
   - 每次push到main分支，Cloudflare会自动重新部署
   - 通常1-2分钟完成

3. **自定义域名**（可选）
   - 在Cloudflare Pages项目设置中添加
   - 需要在域名DNS中添加CNAME记录

---

## 🔗 相关链接

- GitHub: https://github.com/
- Cloudflare Dashboard: https://dash.cloudflare.com/
- 巴菲特知识库参考: http://101.43.0.238/buffett/
