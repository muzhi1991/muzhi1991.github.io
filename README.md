TODO:
* 404 not find 页面展示问题
* 把文件名字换成gitment支持的样子（优先级低）
* 关注这个issue，看看bug解决没[查看issue](https://github.com/imsun/gitment/issues/16)
* https域名验证（coding过期怎么办？github没开启强制https）


注意点：
**hexo是node 6.x支持的，其他版本编译失败。**

## 更新日志
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



