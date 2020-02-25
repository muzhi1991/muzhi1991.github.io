# readme

20200225
* 升级node版本到12.xx 安装新的hexo
* next主题更新为7.x
* 替换新浪图床连接 所有 ws1 ws2 ws3 ws4 ww1 ww2 ww3 ws1 开头的链接改成 tva1 开头，**以后请迁移图片**:`pic_need_migrate.txt`
* 修复codding pages的升级
* [valine评论系统](https://leancloud.cn/)不变（同20190615）
* 手动修改（同20190615）
  * `themes/next/_config.yml`的配置
  * `themes/next/languages/zh-CN.yml` 中文添加自定义内容
  * 修复math显示, [官方连接](https://theme-next.org/docs/third-party-services/math-equations.html)安装后可以部分显示，但是公式里有下划线就不行,参考[连接](https://blog.csdn.net/yexiaohhjk/article/details/82526604)修改部分文件可以解决
    * `node_modules/kramed/lib/rules/inline.js` 修改部分内容

```bash
# nvm ls -- Node.js 版本需不低于 8.10，建议使用 Node.js 10.0 及以上版本
# 安装hexo
npm install -g hexo-cli 
# 升级&&安装所有依赖（package.json）
npm update 
# 不升级只安装
# npm install
# 下载主题
git clone https://github.com/theme-next/hexo-theme-next themes/next

# 修改themes/next/_config.yml 修改配置
# 修改themes/next/languages/zh-CN.yml 增加中文

# 修复math问题
cp bac/bac_20190615/node_modules/kramed/lib/rules/inline.js node_modules/kramed/lib/rules/inline.js
```
