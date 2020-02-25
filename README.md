TODO:
* 图床迁移，需要迁移的文件在`pic_need_migrate.txt`中
* 404 not find 页面展示问题
* https域名验证（coding过期怎么办？github没开启强制https）
* 百度爬虫问题（优先级低）:https://ziyuan.baidu.com/https/index?site=http://www.limuzhi.com/


注意点：
**新版本hexo是node 12.x(8.x以上)**

## 更新日志

20200225:

* 见[说明](bac/bac_20200225/README.md)


20190615:

* update hexo: 
	* npm install -g hexo-cli (可能需要修改某些目录权限）
	* npm update
	* hexo version 查看版本
* update next-theme，作者已换，新地址：https://theme-next.org/
	* [安装最新release](https://github.com/theme-next/hexo-theme-next/blob/master/docs/INSTALLATION.md)：
	* `curl -s https://api.github.com/repos/theme-next/hexo-theme-next/releases/latest | grep tarball_url | cut -d '"' -f 4 | wget -i - -O- | tar -zx -C themes/next --strip-components=1`
* 使用新的评论系统，valine，支持非登录评论，评论可以登录[leancloud官网](https://leancloud.cn)上的存储的`comment`库直接看到
* 手动修改部分：
	* `themes/next/_config.yml`的配置
	* `themes/next/languages/zh-CN.yml` 中文添加自定义内容
	* **修复math显示**, [官方连接](https://theme-next.org/docs/third-party-services/math-equations.html)安装后可以部分显示，但是公式里有下划线就不行,参考[连接](https://blog.csdn.net/yexiaohhjk/article/details/82526604)修改部分文件可以解决
		* `node_modules/kramed/lib/rules/inline.js` 修改部分内容
	* **微博防盗链问题修复**，[参考](https://www.playpi.org/2019042701.html)
		* `themes/next/layout/_partials/head/head.swig` 添加header
	

20180508:

* 升级到next 6.0 `git clone https://github.com/theme-next/hexo-theme-next themes/next-reloaded`
* 修改根目录`_confgi.yml`: 使用next-reloaded的theme（保留了旧的next，测试没问题后，以后可以还是用next作为主题名，修改theme下的目录名就行）。修改了language为zh-CN（因为next6.0中中文改了名字）
* 加入 hostedby coding（next6.0原生支持），去广告
* 解决数学公式问题，只需要在需要显示公式的文档上加入`mathjax: true`
* image路径问题修改，现在的本地图片应用用`/images/xxx.pn`，文件引用`/files/xxx.zip`。（以前是相对路径）

20180507: 

* 升级了 hexo-cli (`npm install -g hexo-cli`), next(`npm install`)，gitment已经加进去，但是bug不少，注意
    * 写的文章在`source/_post/`里面的文件名必须为英文&&没有空格冒号，可以有-
    * 新的文章必须手动打开网站，点击初始化，才能打开文档
    * 有个新依赖`npm install highlight.js --save`
* coding网站强制https，参考[文章](https://www.hi-linux.com/posts/45911.html)，可能证书过期后有问题，因为外国的letsencrypt，按域名解析不到coding那里。

20170903：

* 多说被关闭了，使用gitment代替，由于现在主题next中还没有集成这个功能所有现在手动加入了很多文件（参考bac目录）,[具体方法](https://zonghongyan.github.io/2017/06/29/201706292034/) 。
* 后续关注这个PR：https://github.com/iissnan/hexo-theme-next/pull/1634 ~~


## 使用说明:
1. 第一次下载，执行 sh ./init.sh ，该脚本执行了下面这些操作
    next主题没有下载 在站点根目录下使用 
    git clone https://github.com/iissnan/hexo-theme-next themes/next
    如果hexo命令没有用，尝试 npm install
    使用bac/themes/next/ 覆盖到themes/next下

2. 部署时候，执行 sh ./delpoy.sh

3. 写作
    hexo n [layout] title // n--new title--文章名称 ,layout--默认post
    基本：https://hexo.io/zh-cn/docs/writing.html
    文章头部：https://hexo.io/zh-cn/docs/front-matter.html


4. debug
hexo s // s--server

5. 其他命令
hexo clean
hexo generate 
hexo deploy

6. 一些知识
    source目录下面是写的文章

7. 不错的参考文章
http://ibruce.info/2013/11/22/hexo-your-blog/
http://www.selfrebuild.net/2015/06/24/Github-Hexo-Next%E4%B8%BB%E9%A2%98%E4%B8%AA%E6%80%A7%E5%8C%96%E5%AE%9A%E5%88%B6/



