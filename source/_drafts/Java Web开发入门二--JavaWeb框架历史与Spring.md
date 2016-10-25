title: Java Web开发入门二--JavaWeb框架历史与Spring
date: 2016-10-15 12:17:00
categories:
- 技术

tags:
- JavaWeb
- 后端
---

本章先务虚地介绍一下JavaWeb技术的发展历史，由此引出当前使用的一些技术的来龙去脉。比如Spring技术就是在JavaWeb发展的过程中形成的。由此，我们可以更好的体会这些技术要解决的问题和意义。参考资料如下：

* [Web MVC简介](http://jinnianshilongnian.iteye.com/blog/1593441)
* [Java帝国之Java bean上](http://mp.weixin.qq.com/s?__biz=MzAxOTc0NzExNg==&mid=2665513115&idx=1&sn=da30cf3d3f163d478748fcdf721b6414#rd) 
* [Java帝国之Java bean下](http://mp.weixin.qq.com/s?__biz=MzAxOTc0NzExNg==&mid=2665513118&idx=1&sn=487fefb8fa7efd59de6f37043eb21799#rd)

## JavaWeb技术的发展历史

### JavaWeb框架的发展历史

JavaWeb框架的的发展基本遵循从简答到复杂的过程，复杂的框架带来的好处是清晰的业务逻辑、明确的分层、更可扩展可维护的代码。基本遵循这么一个过程：**从简单的Servlet&&JSP技术（无分层），到Model1模型（两层），到Model2模型（MVC三层）**。最后到SpringMVC的**服务到工作者模型**（更细的分层，基于MVC）。

#### 第零步：纯Servlet编程（无框架时代）

最先有的Servlet技术，正如我们在简单的Servlet例子中看到的，单纯地处理request，调用业务逻辑，输出html的数据流。所有过程都在sevice函数中（或者doGEt等），以字符串形式拼接并输出HTML语句也十分低效。这是最原始的方式，也是所有的技术基础，当我们不使用框架时，可以使用基本的设计模式知识实现简单的框架（如命令模式）。

优势：

* 理解简单，没有框架知识
* 高性能

劣势：

* 直接output html语句十分低效
* view的代码与业务逻辑代码都在service一个函数中，无法复用。
* 没有框架导致基本的功能都要手动实现，如路由分发

#### 第一步：JSP编程（无框架时代）

为了改进Servlet技术的问题：直接用字符串输出view层的代码（HTML代码的拼接）太低效了。为此人们**基于Servlet开发了JSP技术**。JSP技术的目的在于使用`*.jsp`文件代替`*.html`，在jsp中不仅有HTML代码，还有java代码。最后由一个处理工具将*.jsp**转换成**一个Servlet类（这样就回到了上面一步，Servlet中有输出HTML的语句，**这里面的HTML的输入语句自动生成**）。该技术的实质是对Servlet技术的优化，解决了上面提到的第一个问题。

![纯JSP技术]()

优势：

* 不需要写一堆output方法了
* jsp标签库加入了很多便捷方法
* 理解相对简单，没有框架（jsp的使用方法要学习）
* 复杂度不算高，性能可以

劣势：

* **没有解决view层与业务逻辑混合的问题，只是现在所有代码都到了jsp文件中了**
* 这种混合引入了复杂性，jsp还是比较恶心的。一堆html中插着java代码还有一堆符号，头晕。

#### 第二步：Model1模型（2层模型框架）

为了解决上述问题，人们**基于JSP技术，进一步改进**。为了把复杂的业务逻辑分离出去，开发了Model模型。JSP文件负责View层和调用业务逻辑，独立出去的业务逻辑形成JavaBean实体作为Model层。**JavaBean实体是一个满足一定规则的Java类**（如必须要属性的get set方法，复杂的EJB即企业级JavaBean规则更多）。

![Model1模型](http://sishuok.com/forum/upload/2012/7/1/d3b5b2ec88706fff7ef4b98d110837d1__9.JPG)

优势：

* 保留了之前JSP开发的基本优势
* 解决了业务逻辑混合的问题，JavaBean负责数据处理与数据持久化（数据库操作）操作，JSP文件相对清晰。

劣势：

* JSP文件除了有**View层代码还有很多判断逻辑代码**，主要是对Model的操作（大量if else的java代码）。View依然不可复用。
* 除了简单的JavaBean规范。其他规范发展了越来越复杂，尤其是EJB。
* JSP混合的那些java代码和符号一如既往的恶心。维护jsp文件依旧心累。

#### Model2模型（经典的MVC三层模型）

#### 服务到工作者模型（SpringMVC的Model2方案）

### JavaBean的发展历史

可以说伴随这JavaWeb框架的发展，他们的具体实现也在发生变化，最显著的就是框架中的**对象实体**的变化：**从普通的Java对象到JavaBean，再到复杂的EJB，最后返璞归真到POJO**，这一系列变化很有启示意义。





