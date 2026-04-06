# 微信公众号题图生成 Prompt

## 图片主题
OAuth2/OIDC 会话超时与三层令牌边界

## 视觉风格
极简主义、专业科技感、扁平化设计

## 画面构图
- 中心：三个不同大小的同心圆或递进式卡片，代表三层令牌（Access Token、Refresh Token、SSO Session）
- 外层：用细线圆环表示时间边界，带有时钟指针元素
- 底部：简洁的流动线条，象征认证流程和数据交换

## 色彩方案
- 主色：深蓝色 (#1a365d) - 代表安全、专业
- 辅助色：青色 (#38b2ac) - 代表技术、信任
- 点缀色：橙色 (#ed8936) - 少量使用，突出关键节点
- 背景：浅灰白色 (#f7fafc) 或纯白，保持干净

## 设计细节
1. **三层门票可视化**：
   - 内层：小圆，标记 "AT"（Access Token）
   - 中层：中圆，标记 "RT"（Refresh Token）
   - 外层：大圆，标记 "SSO"（Session）

2. **时间元素**：
   - 外围添加虚线圆环，表示时间流逝
   - 右上角添加简洁的时钟图标
   - 用渐变色表示从有效到过期的过渡

3. **连接元素**：
   - 各层之间用细箭头或虚线连接
   - 表示层级关系和续期流程

## 文字要求
- 图片底部留白，避免放置文字（公众号标题会覆盖）
- 图内只保留简短的技术标识（AT/RT/SSO）

## 尺寸规格
- 宽高比：16:9 或 2.35:1（适合微信封面）
- 分辨率：900x383 或 1080x460

## 避免元素
- 避免过于复杂的认证流程图
- 避免过多文字说明
- 避免花哨的装饰元素
- 避免暗黑风格（保持清新专业）

## 情绪基调
- 专业、可信、清晰
- 技术感但不晦涩
- 简约但不失深度

## 推荐生成工具
- Midjourney: `/imagine prompt: minimalist illustration of OAuth2 token layers, three concentric circles representing access token refresh token and SSO session, clean tech style, blue and teal color scheme, white background, flat design, professional --style raw --ar 16:9`

- DALL-E: "A minimalist tech illustration showing three layered circles representing OAuth2 tokens. Inner circle labeled 'AT', middle 'RT', outer 'SSO'. Clean flat design with blue and teal colors on white background. Thin arrows connecting layers. Clock elements showing time boundaries. Professional, simple, modern."

- Stable Diffusion: "minimalist infographic, three concentric circles, OAuth2 tokens, access token refresh token SSO session, blue teal color scheme, white background, flat design, tech illustration, clean lines, professional, high quality"

---

## 使用建议

### 方案一：直接使用 AI 工具
复制上述 prompt 到 Midjourney/DALL-E/Stable Diffusion 生成

### 方案二：本地生成
如果使用 ImageMagick 或其他工具，可以参考以下配色：
```bash
# 核心配色
主色: #1a365d (深蓝)
辅助色: #38b2ac (青色)
点缀色: #ed8936 (橙色)
背景色: #f7fafc (浅灰白)
```

### 方案三：设计软件手动制作
在 Figma/Sketch/Illustrator 中：
1. 创建 900x383 画布
2. 绘制三个同心圆（半径 60/100/140）
3. 添加细线圆环表示时间边界
4. 添加简短标签 AT/RT/SSO
5. 保持大量留白，避免拥挤

---

## 预期效果
生成后的图片应该：
- 一眼能看出是关于认证/令牌主题
- 视觉层次清晰，不过载
- 适合作为技术文章的封面
- 与微信公众号排版风格协调
