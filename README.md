# 新化一中全景

在线浏览：**https://zenghaolinz.github.io/xinhua-panorama/**

八个场景，支持拖动环顾、滚轮/双指缩放、场景热点、三档画质、截图和全景 JPG 下载。

六面立方体切片已修复贴图朝向，l2/l3/l4 图像均保留。最高画质的每面尺寸为 5696 或 5760 像素；导出的等距柱状全景 JPG 为 8192×4096。只加载当前场景所选画质，无需一次下载全部资源。

静态网站位于 `site/`。推送 `main` 后由 GitHub Actions 检查资源完整性并自动发布到 GitHub Pages。

## 影像来源

影像原作 © DREAMFY 影像工作室，来源：[湖南省新化县第一中学全景](https://www.720yun.com/vr/a0920csgmca)。本项目为个人学习展示，非学校或原平台官方网站，与原平台及影像作者无关联。影像权利归原作者所有。

## 本地预览

```sh
python -m http.server 8737 --directory site
```

打开 http://127.0.0.1:8737/ 。
