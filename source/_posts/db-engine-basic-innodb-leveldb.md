title: 数据库引擎InnoDB vs LevelDB
date: 2018-06-22 18:40:01
mathjax: true
categories:

- 技术

tags: 

- 数据库

---

## Overview
常见的存储引擎：
* innodb：https://draveness.me/mysql-innodb
* MyISAM
* levelDB
* rocksdb
这里我们主要分析最常用的：一个是Mysql中常用的innodb，一个是分布式数据库常用的levelDB

## InnodDB

存储结构
* 所有的数据都被逻辑地存放在表空间中，表空间（tablespace）是存储引擎中最高的存储逻辑单位，在表空间的下面又包括段（segment）、区（extent）、页（page）
* 最小存储单元page，默认情况下，表空间中的页大小都为 16KB
![](https://ws3.sinaimg.cn/large/006tNbRwgy1fy66767bznj31o00u0768.jpg)

如何存储
* `.frm` 表结构，不管什么存储引擎通用的
* `.ibd` 索引+数据

存储Record
* 常见的格式：Antelope 是 InnoDB 最开始支持的文件格式，它包含两种行格式 Compact 和 Redundant，Barracuda 的出现引入了两种新的行格式 Compressed 和 Dynamic；
![](https://ws3.sinaimg.cn/large/006tNbRwgy1fy667j7fvkj31iz0u0gmn.jpg)
* 对比Compact 和 Redundant：前者节约空间20%
![](https://ws1.sinaimg.cn/large/006tNbRwgy1fy667pylwbj31uo0h8t9n.jpg)
* 行溢出，对于可变长度的col，如VARCHAR 或者 BLOB 。不会直接将所有的内容都存放在数据页节点中，而是将行数据中的前 768 个字节存储在数据页中，后面会通过偏移量指向溢出页。但是当我们使用新的行记录格式 Compressed 或者 Dynamic 时都只会在行记录中保存 20 个字节的指针，实际的数据都会存放在溢出页面中。对比如下
![](https://ws2.sinaimg.cn/large/006tNbRwgy1fy6683l0gjj31uo0f0t92.jpg)
![](https://ws4.sinaimg.cn/large/006tNbRwgy1fy668a2lczj31uo0f03yv.jpg)

存储page
* 存储格式如下：
![](https://ws4.sinaimg.cn/large/006tNbRwgy1fy668id3mij31uo0c8wez.jpg)
* 页是 InnoDB 存储引擎管理数据的**最小磁盘单位**，而 **B-Tree 节点**就是实际存放表中数据的页面（B+树的节点只能定位到page）。
* Infimum 记录是比该页中任何主键值都要小的值，Supremum 是该页中的最大值：
* Page Directory 保持了页内部的定位信息
* User Records 就是整个页面中**真正用于存放行记录**的部分。（Free是空闲部分）
  * 整个页面并不会按照主键顺序对所有记录进行排序
  * 它会自动从左侧向右寻找空白节点进行插入，行记录在物理存储上并不是按照顺序的，
  * 它们之间的顺序是由 next_record 这一指针控制的。
* 通过B+树取出page数据后，通过 Page Directory 中存储的稀疏索引和 n_owned、next_record 属性取出对应的记录，不过因为这一操作是在内存中进行的

索引
![](https://ws1.sinaimg.cn/large/006tNbRwgy1fy668qk2ogj31je0u0q59.jpg)
* 使用B+树，特点：平衡树，查找任意节点所耗费的时间都是完全相同
![](https://ws3.sinaimg.cn/large/006tNbRwgy1fy668zbe5jj31uo0p0q3z.jpg)
* 索引的分类
  * 主键：聚集索引--构建的b树的叶子节点存放的是真正的page数据--得到整条行记录
  * 其他：辅助索引--它的叶节点并不包含行记录的全部数据，仅包含索引中的所有键和一个用于查找对应行记录的『书签』,就是他还要**二次查找主键的聚集索引**去获得真正的记录
* 如何设计表的索引？？

锁
* 按并发控制分类
  * 乐观锁：不是真正的锁
  * 悲观锁：真正的锁，可能引发死锁，**innodb使用**的是他！
* innodb中的锁
  * 锁的种类
    * 共享锁（读锁）
    * 互斥锁（写锁）
  * 锁的粒度
    * 行锁
    * 表锁--意向锁，分为意向共享锁，意向互斥锁
* 锁算法
  * Record Lock：最普通的锁，行锁**必须通过索引**查找对应的行，再加锁。
  * Gap Lock：对某个范围的行加锁
  * Next-Key Lock：它是记录锁和记录前的间隙锁的结合，部分解决幻读问题
* 死锁发生
![](https://ws2.sinaimg.cn/large/006tNbRwgy1fy669he43tj31sj0u0tap.jpg)

事务
* innodb支持事务，ACID
* 隔离级别
  * RAED UNCOMMITED：当前事务中能读到别人**没提交**的事务行为--脏读（dirty read）
  ![](https://ws4.sinaimg.cn/large/006tNbRwgy1fy66axglv2j31uo0ssgmy.jpg)
  * READ COMMITED：当前事务中能多次读到别人**提交的**事务的不一致数据--不可重复读（unrepeatable read）
    ![](https://ws1.sinaimg.cn/large/006tNbRwgy1fy669wq8ifj31lm0u0dhk.jpg)
  * REPEATABLE READ：**默认级别**，多次读取同一范围的数据会返回第一次查询的快照，不会返回不同的数据行，--幻读（Phantom Read）
  ![](https://ws3.sinaimg.cn/large/006tNbRwgy1fy66a3sq9cj31gy0u076a.jpg)
  * SERIALIZABLE：InnoDB 隐式地将全部的查询语句加上共享锁，直到事务结束。解决了幻读的问题
    
总结如下：

![](https://ws2.sinaimg.cn/large/006tNbRwgy1fy66bfab0wj31uo0rs3zz.jpg)
使用Next-Key 锁的效果：
![](https://ws3.sinaimg.cn/large/006tNbRwgy1fy66bkr0ttj31n10u0abo.jpg)

## LevelDB
java使用：https://medium.com/@wishmithasmendis/leveldb-from-scratch-in-java-c300e21c7445

levelDB是可以理解为BigTable的单机版本，看做，bigTable中的tablet的一个实例，tablet中有sstable。

Bigtable基本架构
* master+n个tablet server架构
* tablet使用metadata-tablet支持多层架构，支持大量数据存储--每一个 metadata-tablet 包括根节点上的 tablet 都存储了 tablet 的位置和该 tablet 中 key 的最小值和最大值；每一个 METADATA 行大约在内存中存储了 1KB 的数据，如果每一个 METADATA tablet 的大小都为 128MB，那么整个三层结构可以存储 2^61 字节的数据。
  ![](https://ws3.sinaimg.cn/large/006tNbRwgy1fy66bu9y2gj30rs0dwq37.jpg)
* master存储所有Server（Tablet）的位置信息
* Client启动时会去master获取server信息，以后去写不需要再取了


基于SSTable的存储引擎可以这样Run起来：

* 当一条数据写入时，我们将其插入到基于内存的平衡树中（Red-black tree，为了有序）。 内存中的树我们称之为Memtable。
* 当Memtable的大小超过一定阈值时，我们将Memtable Flush到磁盘，转为SSTable。我们称为Minor-Compaction
  ![](https://ws1.sinaimg.cn/large/006tNbRwgy1fy66c39l88j30rs084aa4.jpg)
* 周期性的在后台进行异步的Merge和Compaction操作。我们称为Major-Compaction，为了保证有序，需要进行sort merge
  ![](https://ws2.sinaimg.cn/large/006tNbRwgy1fy66c8salpj30rs0bldg0.jpg)
* 当我们查询时，需要同时查询内存中的Memtable和磁盘中的SSTable。
* 为了防止Memtable在Flush到磁盘前机器故障导致数据丢失，我们可以在磁盘上维护一个只追加写的log文件，称之为Write-Ahead-Log,当集群故障后可以从log中恢复出Memtable。 所以我们在**每次写入Memtable，需要先写入WAL**。当Memtable flush到磁盘后，对应的WAL文件就可以删除。

读/写过程如下：
![](https://ws4.sinaimg.cn/large/006tNbRwgy1fy66cl6gbqj30rs0b6dg3.jpg)
注:上图中`tablet log`理解为WAL


LevelDB，RocksDB，Cassandra，HBase
kafka是对lsm tree的极端应用么，key天然自增，绕过了Memtable直接落磁盘

## rocksdb
RocksDB是facebook基于LevelDB实现的，目前为facebook内部大量业务提供服务。经过facebook大量工作，将RocksDB作为MySQL的一个存储引擎移植到MySQL，称之为[MyRocks](http://mysql.taobao.org/monthly/2016/08/03/)

## 相关算法

SkipList：对比红黑树、AVL：[参考](https://blog.csdn.net/Wj741238436/article/details/73565163)