title: Android图片库--Glide Wiki中文翻译
date: 2016-01-24 10:32:54
description: Glide Wiki中文翻译 Version 0.1。Glide是一个Android图片库，确切地说应当叫『媒体框架』。支持图片、Gif、原生视频的加载。使用简单，性能优异，Google推荐。
categories:
- 技术
tags:
- Android
- 主框架
---
## 序
最近，一直在捣鼓Glide这个图片库，确切地说应当叫『媒体框架』。为了支持Gif播放，项目中使用Glide代替了Universal Image Loader。起初我们打算使用的是Fresco方案，最终因为Lib体积的问题放弃。万万没想到apk的size这么敏感，国外很多推广服务是更具apk体积收费的，3M一个门槛，5M一个门槛。fresco引入之后即使使用proguard、7zip，apk的大小也增加的1m，多平台的os库是个大头，第三世界的应用市场还不支持按平台分发😓。。
Glide的使用还不深入，仅仅停留在Api的范畴，为了解决bug，跟踪了代码，也是云里雾里。不得不说，Glide源码的设计十分NB，面向接口的理念贯彻的很彻底，是一个学习设计的好demo。
GitHub的README作为最简单的入门足够了，但是遇到具体问题还是要理解一些设计思想的，GitHub上的Wiki有一份不错的文档，可惜木有中文，正好学习的过程中翻译一下。（2016-1-24日）
两篇中文入门可以参考

* [Google推荐的图片加载库Glide介绍](http://www.jcodecraeer.com/a/anzhuokaifa/androidkaifa/2015/0327/2650.html)
* [Glide 一个专注于平滑滚动的图片加载和缓存库](http://www.jianshu.com/p/4a3177b57949)

### 名词解释
Target
Model
Signature

## 目录
* 主目录
* 缓存机制与缓存失效
* Glide配置
* 自定义Target
* 调试与错误处理
* 使用Glide下载自定义大小图片
* 与其他库的整合
* 后台线程的加载与缓存
* Glide中的资源复用
* 快照（Snapshots）
* 图形变换（Transformations）

## 主目录
### 提问
如果你有任何问题，可以在Github上提出或者发送email到我们的邮件列表，也可以在IRC(Internet Relay Chat 网络中继聊天？)频道上联系我们。
### 3.0版本的新特性
* 支持Gif动画播放解码 - 与加载图片相同，只有调用Glide.with(...).load(...)，如果你加载的是动画Gif，Glide会自动加载它并把gif显示在一个自定义的Drawable上（注：GifDrawable）。此外，你还可以控制的更多，比如

```java
// 你想加载Gif为一张静态图片
Glide.with(context).load(...).asBitmap()。
// 或者你想只有加载对象是Gif时才能加载成功
Glide.with(context).load(...).asGif()。
```

* 本地视频播放技术 - 除了解码Gif，Glide也能解码你设备上的视频（video）。使用方法和加载gif相同，Glide支持所有Android可以直接解码的视频。
* 支持缩略图加载 - 有时我们希望减少用户等待的时间又不想牺牲图片的质量，我们可以同时加载多张图片到一个View中，先加载缩略图（只有view的1/10大小），然后再加载一个完整的图像覆盖在上面。使用下面的代码

```java
Glide.with(yourFragment).load(yourUrl).thumbnail(0.1f).into(yourView)
```

当然，你也可以传入一个request到`.thumbnail()`函数中作为参数。

* 与生命周期相整合 - 加载请求现在会自动在onStop中暂停在，onStart中重新开始。为了节约电量，Gif动画也会在onStop中自动暂停。此外，当设备的连接状态改变时，所有失败的请求会自动重试，确保Glide不会因为临时性的连接问题，导致请求永远失败。
* 转码 - 除了解码资源，Glide的`.toBytes()`和`.transcode()`方法允许你在后台正常地获取、解码、变换一张图片。而且，在这些调用中，你可以把图片转码成更有用的格式，比如，上传一张大小为250*250像素的用户头像的图片bytes数据，代码如下

```java
Glide.with(context)
    .load(“/user/profile/photo/path”)
    .asBitmap()
    .toBytes()
    .centerCrop()
    .into(new SimpleTarget<byte[]>(250, 250) {
        @Override
        public void onResourceReady(byte[] data, GlideAnimation anim) {
            // 在此处，将bytes数据传入后台线程，再上传他们
        }
    });
```

* 动画 - Glide3.x支持cross fades动画（`.crossFade()`）和view的属性动画(`.animate(ViewPropertyAnimation.Animator)`)。此外，还有Glide2.0就支持的view动画。
* 支持 OkHttp 和 Volley - 现在你可以选择用OkHttp、Volley或者默认的HttpUrlConnection作为网络栈。OkHttp和Volley可以通过添加对应的整合库(integration library)和注册相应的`ModelLoaderFactory`来引入。具体查看ReadMe文件。
* 其他

### 从2.0迁移到3.0
* 将所有的`Glide.load()`替换为`Glide.with([fragment/activity/context]).load()`。
* 将所有的自定义目标的加载调用`Glide.load(url).into(new SimpleTarget(){ ... }).with(context)`替换成`Glide.with(context).load(url).into(new SimpleTarget(width, height) { ... })`。

### 特性
除了3.0引入的新功能，Glide继承了2.0的所有功能：

* 后台图片加载
* 如果你使用了listview的复用机制，那么Glide会自动取消作业（job）
* 内存和磁盘缓存
* Bitmap和资源池来减少内存抖动
* 支持任意的图像变换

## 缓存机制与缓存失效
缓存失效是一个比较复杂的话题，理想情况下，你尽可能不要考虑这个问题。这一节主要是让你粗略的了解一下Glide中cache的key是如何生成，以及给你一些关于如何合理利用缓存的提示。
### 缓存的key
`DiskCacheStrategy.RESULT`磁盘缓存策略（注：配置的一种磁盘缓存策略）使用的key由以下四个主要部分组成：

* DataFetcher的方法`getId()`返回的字符。典型地，DataFetcher仅仅返回由数据Model的`toString()`方法得到的值。所以，如果Model是一个**URL**，那么会返回URL的字符串，如果Model是是一个文件，那么会返回文件的**路径**。。。
* 宽和高。如果你调用过override(width,height)方法，那么就是是它传入的值。没有调用过，默认是通过**Target**的`getSize()`方法获得这个值。
* 各种编码器、解码器的`getId()`方法返回的字符串。这些编码器、解码器用于加载和缓存你的图片。仅有哪些堆bytes数据有影响的编码器、解码器才会有这些`id`值。比如，你只有一个将bytes数据写入磁盘的编码器，那么它就没有id值，因为不管怎样它都不会修改数据。
* 可选地，你可以为图片加载提供签名(Signature),请看下面的缓存失效部分。

所有的这些key，以特定的顺序计算出hash值，并将这个值作为保存图片到磁盘上的唯一且安全的文件名。

### 自定义缓存失效
通常情况下改版缓存的标志（key）是困难的。Glide提供了`signature()`API来混入其他数据，帮助你控制缓存的key。签名（Signature）对于多媒体内容以及你可以维护版本信息的任何内容来说都很有用。

* 媒体库内容 - 对于媒体库内容，你可以使用Glide的`MediaStoreSignature`类作为签名， MediaStoreSignature类允许你混入文件修改时间、mime类型、媒体库的方向(orientation?)这些值作为缓存的key，这三个值足以让你可靠的捕捉到任何修改和更新，使你可以缓存媒体库的缩略图.?
* 文件 - 你可以使用`StringSignature`混入文件修改时间
* url - 虽然是url失效最好的方式是当内容变化时，服务器修改url并更新客户端，但是你也可以用`StringSignature`混入任意的元数据（如版本号）来使缓存失效。

使用String Signature加载数据很简单：

```java
Glide.with(yourFragment)
    .load(yourFileDataModel)
    .signature(new StringSignature(yourVersionMetadata))
    .into(yourImageView);
```

媒体库Signature可以直接使用从MeidaStore(注：一个android api）获得的数据

```java
Glide.with(fragment)
    .load(mediaStoreUri)
    .signature(new MediaStoreSignature(mimeType, dateModified, orientation))
    .into(view);
```

你还可以通过实现`key`接口来自定义签名，确保实现了`equals()`, `hashCode()`和`updateDiskCacheKey()`这几个方法

```java
public class IntegerVersionSignature implements Key {
    private int currentVersion;
 
    public IntegerVersionSignature(int currentVersion) {
         this.currentVersion = currentVersion;
    } 
 
    @Override 
    public boolean equals(Object o) {
        if (o instanceof IntegerVersionSignature) {
            IntegerVersionSignature other = (IntegerVersionSignature) o;
            return currentVersion = other.currentVersion;
        } 
        return false; 
    } 
 
    @Override 
    public int hashCode() { 
        return currentVersion;
    } 
 
    @Override 
    public void updateDiskCacheKey(MessageDigest md) {
        messageDigest.update(ByteBuffer.allocate(Integer.SIZE).putInt(signature).array());
    } 
} 
```
请牢记：为了避免性能下降，请在后台线程中批量加载版本元数据(metaData,注：一般查询数据库获得),只有这样，才能确保当你想加载图片的时候，这些值是可用的。
如果这些方法都失败了，比如，你不能改变标识符，也不能跟踪一个合理的版本号。你还可以使用`diskCacheStrategy()`和`DiskCacheStrategy.NONE.`来完全关闭磁盘缓存。

## 配置
### 懒加载配置
从Glide3.5开始，你可以使用`GlideModule`接口来懒加载配置Glide以及注册组件（如`ModelLoaders`),这些配置将会在第一个Glide请求发起的时候被调用。

### 创建一个GlideModule
为了使用和注册GlideModule，首先需要实现该接口，加入你的配置和组件。

```java
package com.mypackage; 
 
public class MyGlideModule implements GlideModule { 
    @Override public void applyOptions(Context context, GlideBuilder builder) {
        // Apply options to the builder here. 
    } 
 
    @Override public void registerComponents(Context context, Glide glide) {
        // register ModelLoaders here. 
    } 
} 
```

然后，添加你的实现类到`proguard.cfg`文件中，让你的module可以被反射调用到。这个性能开支很少，因为每个module只会在Glide第一次请求的时候实例化一次。

```xml
-keepnames class com.mypackage.MyGlideModule
# or more generally:
#-keep public class * implements com.bumptech.glide.module.GlideModule
```

最后，添加meta-data标记到`AndroidManifest.xml`，那有Glide才能找到它。

```xml
<manifest ...>
    <!-- ... permissions -->
    <application ...>
        <meta-data
            android:name="com.mypackage.MyGlideModule"
            android:value="GlideModule" />
        <!-- ... activities and other components -->
    </application>
</manifest>
```

你可以实现任意个`GlideModule`，但是每一个都要添加到`proguard.cfg`，而且每一个都要在manifest有自己的meta-data标记。

### Library工程
Library工程可能含有一个或多个`GlideModule`。当我们使用Gradle（或者任何支持manifest合并的构建工具）构建app时，如果我们所依赖的Library工程的manifest中含有module，那么这些module会自动加入到app中。如果构建工具不支持manifest合并，那么这些library工程中的module必须手动添加到你app的manifest中。

### GlideModule冲突
虽然Glide允许每个app注册多个`Glidemodule`,但是不会以某种特定的顺序调用这些module。所以，如果你的app中多个`GlideModules`或者依赖的library工程中有多个`GlideModules`，你必须负责避免他们之间的冲突。
如果冲突不可避免，app应该定义自己的默认module，这个module需要手动解决这些冲突，提供所有Library工程所需要的依赖。Gradle的使用者，或者使用manifest合并的用户，可以通过下面的标签来排除冲突的module。

```xml
<meta-data android:name=”com.mypackage.MyGlideModule” tools:node=”remove” />
```

### 全局配置
你可以配置一些作用于所有请求的全局性配置项。请使用`GlideModule#applyOptions`方法中（作为参数）提供给你的`GlideBuilder`来配置。本节代码示例中的`builder`就是GlideModule。

### 磁盘缓存
你可以使用`GlideBuilder`的`setDiskCache()`方法设置磁盘缓存的位置、大小（最大值）。你也可以使用`DiskCacheAdapter`彻底关闭缓存,或者自己实现`DiskCache`接口来换掉默认实现。磁盘缓存由`DiskCache.Factory`接口的实例在后台线程中创建，使用后台线程可以避免在严格模式中出现问题。
Glide默认使用`InternalCacheDiskCacheFactory`类建立磁盘缓存。这个内部缓存工厂（internal cache factory）会把磁盘缓存放到应用程序的内部缓存目录中，并且设置最大空间是250MB，使用内部缓存的目录而不是SD卡的外部目录意味着其他应用程序无法访问到你下载的图片。具体请查看Android的[存储选项相关文档](http://developer.android.com/intl/zh-cn/guide/topics/data/data-storage.html#filesInternal)。
#### 大小
使用`InternalCacheDiskCacheFactory`设置磁盘缓存大小

```java
builder.setDiskCache(
  new InternalCacheDiskCacheFactory(context, yourSizeInBytes));
```
#### 位置
也可以设置磁盘缓存位置
你可以使用`InternalCacheDiskCacheFactory `来把你的磁盘缓存放到应用程序私有的内部存储目录中：

```java
builder.setDiskCache(
  new InternalCacheDiskCacheFactory(context, cacheDirectoryName, yourSizeInBytes));
```
你也可以用`ExternalCacheDiskCacheFactory `来把你的磁盘缓存放到sd卡的公共缓存目录上。

```java
builder.setDiskCache(
  new ExternalCacheDiskCacheFactory(context, cacheDirectoryName, yourSizeInBytes));
```
如果你想用其他自定义的路径，可以用`DiskLruCacheFactory`类的构造函数来实现。

```java
// If you can figure out the folder without I/O: 
// Calling Context and Environment class methods usually do I/O. 
builder.setDiskCache( 
  new DiskLruCacheFactory(getMyCacheLocationWithoutIO(), yourSizeInBytes)); 
 
// In case you want to specify a cache folder ("glide"): 
builder.setDiskCache( 
  new DiskLruCacheFactory(getMyCacheLocationWithoutIO(), "glide", yourSizeInBytes)); 
 
// In case you need to query the file system while determining the folder: 
builder.setDiskCache(new DiskLruCacheFactory(new CacheDirectoryGetter() { 
    @Override public File getCacheDirectory() {
        return getMyCacheLocationBlockingIO(); 
    } 
}), yourSizeInBytes); 
```
注意：请牢记，写死任何值都不是个好主意，尤其是目录的路径，因为自Android4.2开始，支持单设备多用户。

如果你想完全控制缓存的创建，可以自己实现`DiskCache.Factory `接口，使用`DiskLruCacheWrapper`可以在你想要的位置创建一个新的缓存。

```java
builder.setDiskCache(new DiskCache.Factory() { 
    @Override public DiskCache build() { 
        File cacheLocation = getMyCacheLocationBlockingIO();
        cacheLocation.mkdirs();
        return DiskLruCacheWrapper.get(cacheLocation, yourSizeInBytes);
    } 
}); 
```

### 内存缓存和缓存池
`GlideBuilder`类允许你设置内存缓存大小，而且可以实现自定义的`MemoryCache`和`BitmapPool`。
#### 大小
默认大小是由`MemorySizeCalculator`类决定的。MemorySizeCalculator类会考虑该设备的屏幕大小，可用内存来计算出一个合理的默认值。如果你想调整这个默认值，请构建自己的实例。

```java
MemorySizeCalculator calculator = new MemorySizeCalculator(context);
int defaultMemoryCacheSize = calculator.getMemoryCacheSize();
int defaultBitmapPoolSize = calculator.getBitmapPoolSize();
```
如果你想在应用的某个阶段动态调整Glide的内存占用，你可以选择一个`MemoryCategory`并使用`setMemoryCategory()`方法传入Glide中：

```java
Glide.get(context).setMemoryCategory(MemoryCategory.HIGH);
```

#### 内存缓存
Glide的内存缓存会在内存中持有资源，它的作用是，我们可以不进行IO操作而快速获得可用资源。
你可以使用`GlideBuilder`的`setMemoryCache()`方法设置大小，或者设置你关于内存缓存的自定义实现（自定义类）。`LruResourceCache`类是Glide的默认实现。你可以通过`LruResourceCache`的构造函数配置内存占用的bytes的最大值。

```java
builder.setMemoryCache(new LruResourceCache(yourSizeInBytes));
```

#### Bitmap池
Glide的bitmap池主要作用是，可以让各种尺寸的Bitmap被复用，可以可观的减少由垃圾回收引起的内存抖动。在解码图片时，需要给像素数组分配空间，这会触发垃圾回收。
你可以使用`GlideBuilder`的`setBitmapPool()`方法设置大小，或者设置你关于Bitmap池的自定义实现，`LruBitmapPool`类是Glide的默认实现。LruBitmapPool类使用了LRU算法维护最近最多使用的Bitmap的尺寸。你可以通过`LruBitmapPool`的构造函数配置内存占用的bytes的最大值。

```java
builder.setBitmapPool(new LruBitmapPool(sizeInBytes));
```
### Bitmap格式
`GlideBuilder` 类也允许你设置一个App全局使用的Bitmap的Config属性的配置。
Glide默认使用RGB_565，因为它每个像素只需要2bytes（16bit）的空间，只需要高质量图片（既系统默认的`ARGB_8888 `）一半的内存空间。但是，这对于某些图片这可能会出现『条带』的问题，而且它也不支持透明度。
如果在你的应用中『条带』是一个问题，或者你需要尽可能好的图片质量，你可以使用`GlideBuilder`的`setDecodeFormat`方法设置DecodeFormat.ALWAYS_ARGB_8888作为首选配置。

```java
builder.setDecodeFormat(DecodeFormat.ALWAYS_ARGB_8888);
```

## 自定义目标（Targets）
除了可以加载图像，视频剧照，gif动画到View中，你还可以加载他们到实现了Target接口的自定义目标中。

### SimpleTarget
如果你只是想加载一个Bitmap，并不想直接展示给用户而是有一些特殊用途，比如在通知中显示或者用作头像上传。
Glide也可以做到。
SimpleTarget为Target接口提供了大部分的默认实现。你可以专注于处理加载的结果。
为了使用SimpleTarget，你需要在它的构造函数中提供你要加载的资源的宽和高（单位像素），你还需要实现` onResourceReady(T resource, GlideAnimation animation)`方法。
一个典型的使用SimpleTarget的例子如下:

```java
int myWidth = 512;
int myHeight = 384;
 
Glide.with(yourApplicationContext)) 
    .load(youUrl) 
    .asBitmap() 
    .into(new SimpleTarget<Bitmap>(myWidth, myHeight) {
        @Override 
        public void onResourceReady(Bitmap bitmap, GlideAnimation anim) {
            // Do something with bitmap here. 
        } 
    }; 
```

#### 一些警告
正常情况下，你加载一个资源会把他们放到view中。当你的Activity或者Fragment被pause或者destroy时，Glide会暂停或取消加载，确保你不会加载那些根本不会显示的资源。
可是当我们使用SimpleTarget的时候，这可能并不是我们希望的行为。所有，当你调用`Glide.with(context)`的时候，你可以传入Application的context，而不是传入Activity或者Fragment。
此外，考虑到长时间的加载操作可能导致内存泄漏，请考虑使用静态内部类，而不是匿名内部类。

### ViewTarget
如果你想加载一个图片到View中，但是你想观察或者覆盖Glide的默认行为。你可以覆盖ViewTarget或者它的子类。
当你想让Glide来获取view的的大小，但是想你自己来启动动画和设置资源到view中，ViewTarget是个不错的选择。如果你要加载一个图片到ImageView之外的自定义view中，那么ImageViewTarget或者它的子类就不能满足你的要求，此时继承ViewTarget就特别合适。
你可以静态的定义一个ViewTarget的子类，或者传递一个匿名内部类到你的加载调用里：

```java
Glide.with(yourFragment)
    .load(yourUrl)
    .into(new ViewTarget<YourViewClass, GlideDrawable>(yourViewObject) {
        @Override
        public void onResourceReady(GlideDrawable resource, GlideAnimation anim) {
            YourViewClass myView = this.view;
            // Set your resource on myView and/or start your animation here.
        }
    });
```
注意，如果你想指定加载Bitmap还是GifDrawable，请在`.load(yourUrl)`调用后面直接添加`.asBitmap()`或者`asGif()`，同时将ViewTarget的类型参数`GlideDrawable`换成对应加载的类型。
为了更多控制，你也可以在Target实现`LifecycleListener`回调，`onStart()`, `onStop()`, 或者`onDestroy()`会和你view所在的fragment的生命周期同步。
### 覆盖默认行为
如果你只想观察不想修改Glide的默认行为，你可以继承任何一个Glide对ImageViewTargets的默认实现。

* GlideDrawableImageViewTarget - 默认的Target，用做正常的加载，和`asGif()`。
* BitmapImageViewTarget - 当使用`asBitmap()`加载时，使用的默认Target。

只有你在每个方法里面调用super()，将会保留默认的行为，同时还可以添加一些你希望的功能。

例如，想要生成一个[调色板](http://chris.banes.me/2014/07/04/palette-preview/)，你可以这样做。

```java
Glide.with(yourFragment) 
    .load(yourUrl) 
    .asBitmap() 
    .into(new BitmapImageViewTarget(yourImageView)) { 
        @Override 
        public void onResourceReady(Bitmap bitmap, GlideAnimation anim) {
            super.onResourceReady(bitmap, anim);
            Palette.generateAsync(bitmap, new Palette.PaletteAsyncListener() {  
                @Override 
                public void onGenerated(Palette palette) {
                    // Here's your generated palette 
                } 
            }); 
        } 
    }); 
```
虽然这个例子还不错，但是，通常情况下，我不推荐用这个方式生成调色板。请查看Glide的 `ResourceTranscoder` 接口和`.transcode()`方法，考虑返回一个包含Bitmap和调色板的自定义资源。调色板可在在后台线程生成。？？？？？更多内容会在以后推出。。。

## 调试和错误处理
Glide在加载过程中出现异常默认情况下不会打日志。Glide为你提供了两种方式查看和处理这些异常。
### 调试
仅仅为了查看异常的话，你可以为`GenericRequest`类打开Debug日志。这个类处理所有媒体资源的加载响应（response）。你可以在命令行里运行：

```xml
adb shell setprop log.tag.GenericRequest DEBUG
```
想要包括详细的请求时序信息，你可以把`DEBUG`缓存`VERBOSE`。

关闭日志使用：

```xml
adb shell setprop log.tag.GenericRequest ERROR
```
### 调试[工作流](https://docs.google.com/drawings/d/1KyOJkNd5Dlm8_awZpftzW7KtqgNR6GURvuF6RfB210g/edit)
为了查看内部引擎（engine）如何以及何时查找到资源，你可以打开日志：

```xml
adb shell setprop log.tag.Engine VERBOSE
adb shell setprop log.tag.EngineJob VERBOSE
adb shell setprop log.tag.DecodeJob VERBOSE
```
打开这个有助于你找出为什么某个资源没有从内存缓存中加载，为什么请求再次从外部的url下载数据。这也可以帮助你了解：如果想命中磁盘缓存，什么样的参数需要匹配。启用`DecodeJob`日志也可以帮助你找去自定义transformation/decoder/encoder相关的问题。

### 监听请求-RequestListener
虽然启用debug日志很简单，但是只有在你可以连接到设备时才能这样干。为了把Glide整合进已有的更专业的错误日志系统。你可以使用`RequestListener`类的`onException()`。当请求失败时，该方法会告知你导致失败的`异常`(Exception),如果解码器（Decoder）不能从数据中解析出任何有用的信息。Exception也可能传`null`。你可以使用`listener()`API传一个你的监听器（listener）到每一个请求中。
请确保`onException()`返回`false`。以免覆盖了Glide的默认错误处理行为。（例如，通知`Target`这个error）
这是一个快速调试的例子：

```java
// example usage: .listener(new LoggingListener<String, GlideDrawable>()) 
public class LoggingListener<T, R> implements RequestListener<T, R> {
    @Override public boolean onException(Exception e, Object model, Target target, boolean isFirstResource) {
        android.util.Log.d("GLIDE", String.format(Locale.ROOT,
                "onException(%s, %s, %s, %s)", e, model, target, isFirstResource), e);
        return false; 
    } 
    @Override public boolean onResourceReady(Object resource, Object model, Target target, boolean isFromMemoryCache, boolean isFirstResource) {
        android.util.Log.d("GLIDE", String.format(Locale.ROOT,
                "onResourceReady(%s, %s, %s, %s, %s)", resource, model, target, isFromMemoryCache, isFirstResource));
        return false; 
    } 
} 
```
**确保发版前移除所有使用这个类的地方**

### 更多日志
这个列表是给3.6.0版本用的，可能不完整。

```xml
cd .../android-sdk/platform-tools
adb shell setprop log.tag.AnimatedGifEncoder VERBOSE
adb shell setprop log.tag.AssetUriFetcher VERBOSE
adb shell setprop log.tag.BitmapEncoder VERBOSE
adb shell setprop log.tag.BufferedIs VERBOSE
adb shell setprop log.tag.ByteArrayPool VERBOSE
adb shell setprop log.tag.CacheLoader VERBOSE
adb shell setprop log.tag.ContentLengthStream VERBOSE
adb shell setprop log.tag.DecodeJob VERBOSE
adb shell setprop log.tag.DiskLruCacheWrapper VERBOSE
adb shell setprop log.tag.Downsampler VERBOSE
adb shell setprop log.tag.Engine VERBOSE
adb shell setprop log.tag.EngineRunnable VERBOSE
adb shell setprop log.tag.GenericRequest VERBOSE
adb shell setprop log.tag.GifDecoder VERBOSE
adb shell setprop log.tag.GifEncoder VERBOSE
adb shell setprop log.tag.GifHeaderParser VERBOSE
adb shell setprop log.tag.GifResourceDecoder VERBOSE
adb shell setprop log.tag.Glide VERBOSE
adb shell setprop log.tag.ImageHeaderParser VERBOSE
adb shell setprop log.tag.ImageVideoDecoder VERBOSE
adb shell setprop log.tag.IVML VERBOSE
adb shell setprop log.tag.LocalUriFetcher VERBOSE
adb shell setprop log.tag.LruBitmapPool VERBOSE
adb shell setprop log.tag.MediaStoreThumbFetcher VERBOSE
adb shell setprop log.tag.MemorySizeCalculator VERBOSE
adb shell setprop log.tag.PreFillRunner VERBOSE
adb shell setprop log.tag.ResourceLoader VERBOSE
adb shell setprop log.tag.RMRetriever VERBOSE
adb shell setprop log.tag.StreamEncoder VERBOSE
adb shell setprop log.tag.TransformationUtils VERBOSE
```