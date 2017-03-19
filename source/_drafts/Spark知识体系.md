title: Spark相关知识体系大纲
date: 2017-01-15 16:28:53
categories:
- 技术

tags: 
- 大数据分析
- Spark
---

数据分析的两个基本方向：工程架构与策略算法。本篇文章从工程架构角度分解一下Spark的学习路径。Spark的学习又可以分为两个分支：批量计算与流式计算。但是这两者不是独立的。他们有着共同的技术，相似的API，只是在应用常见与具体的实施上有些不同，往往流式比批量面临更多的问题。



* 基础准备
  * Scala语言基础
  * Java语言基础
  * Hadoop基础知识
* 入门
  * Spark配置&&开发环境
  * 基本API
    * RDD
      * partition问题
      * input/output
      * cache
    * 共享变量的应用
      * 广播变量
      * 累加器
  * Spark SQL
    * DataFrame
    * DataSet
  * Spark Streaming
    * 可靠性问题-精确一次
    * 时间窗口问题
* 基本原理（spark internals）
  * 运行模型分析：Driver && Executor
* 源码分析（待细分）
* 性能调优
* 工程实践
  * 使用场景&&案例分析
    * 批量
    * 流式
* 应用扩展
  * 基于Yarn开发分布式程序—Spark源码分析扩展
  * 机器学习模型的实现

