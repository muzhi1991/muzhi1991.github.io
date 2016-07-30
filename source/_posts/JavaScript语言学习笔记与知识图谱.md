title: JavaScript语言学习笔记与知识图谱
date: 2016-07-17 16:14:44
categories:
- 技术
- 全栈

tags:
- javascript
- web开发
---

## 概述

js是网页的脚本语言，学习的过程中才发现内容其实很多，甚至感觉难以上手，可能是因为他与我们遇到的大部分语言都不太一样，如C Java甚至是Python。

还好在学习的过程中做了笔记，有些知识点很难接受。

一些重要的点：

* 原型模式
* 静态方法，实例方法，内部方法。
* 单线程，异步特点，事件循环
* this变量，与坑
* 闭包的概念与应用（核心：记住函数上下文变量）
* 设计的不严谨的地方，如null，undefined，变量提升
* 很多ES6新特性，可以用在node上面

建议：**使用严格模式**

参考文章：

* [廖雪峰的JavaScript教程](http://www.liaoxuefeng.com/wiki/001434446689867b27157e896e74d51a89c25cc8b43bdb3000)：建议学习这一篇，简单易懂，忽略细节，尤其是关于原型的部分。
* [阮一峰的JavaScript标准参考教程ES5](http://javascript.ruanyifeng.com/)：十分详尽，可以当做参考资料。

其他书籍：

* JavaScript语言精粹，听说不错。

知识图谱：
[这里下载JavaScript知识图谱](files/JavaScript知识图谱.mindnode)

## 变量

* 如果只是声明变量而没有赋值，则该变量的值是`undefined`。`undefined`是一个JavaScript关键字，表示“无定义”。如果一个变量没有声明就直接使用，JavaScript会报错，告诉你变量未定义。`ReferenceError: x is not defined`


* 严格地说，`var a = 1` 与 `a = 1`，这两条语句的效果不完全一样，主要体现在`delete`命令无法删除前者。不过，绝大多数情况下，这种差异是可以忽略的。**建议总是使用`var`命令声明变量。**


* 变量`x`声明了两次，第二次声明是无效的(赋值的话就有效了)


* 变量提升：JavaScript引擎的工作方式是，先解析代码，获取所有被声明的变量，然后再一行一行地运行。这造成的结果，就是所有的变量的声明语句，都会被提升到代码的头部，这就叫做变量提升（hoisting）。函数内部也是这样。

  ```javascript
  var a;
  console.log(a); // undefined,表示变量a已声明，但还未赋值。
  a = 1;
  ```

> 变量提升只对`var`命令声明的变量有效，如果一个变量不是用`var`命令声明的，就不会发生变量提升。

* 合法：`arg0` `_tmp` **`$elem`** `π` 中文变量 ；不合法: `1a` `***` `a+b` `-d`

* 作用域：只有两种作用域：函数作用域和全局作用域。**变量没有块作用域**：区块中的变量与区块外的变量，属于同一个作用域。只有函数中声明的变量是局部的。因此特别注意`for`、`if`、`while`.

  ```javascript
  if (true) {
    var x = 5;
  }
  console.log(x);  // 5
  ```

  ​

## if while for switch等注意点

* if while for的条件语句中使用`=`不会报错，因而要注意
* `if(undefined){}` `if(0){}` `if(false){}` `if(null)` `if("")` `if('')` `if(NaN）`都不进入语句
* `if([ ]){}` `if({}){}`都是true，**js的语法参考的是java，与python不同**
* `switch`语句后面的表达式与`case`语句后面的表示式，在比较运行结果时，采用的是严格相等运算符（`===`），而不是相等运算符（`==`）


* label的使用，可以`break label` `continue label`跳出多层循环

  ```javascript
  top:
     for (var i = 0; i < 3; i++){
      for (var j = 0; j < 3; j++){
        if (i === 1 && j === 1) break top;
        console.log('i=' + i + ', j=' + j);
      }
    }
  ```

## 数据类型

- 数值（number）：整数和小数（比如1和3.14）**原始类型**

- 字符串（string）：字符组成的文本（比如”Hello World”）**原始类型**

- 布尔值（boolean）：`true`（真）和`false`（假）两个特定值 **原始类型**

- `undefined`：表示“未定义”或不存在，即此处目前没有任何值 **特殊值**

- `null`：表示空缺，即此处应该有一个值，但目前为空 **特殊值**

- 对象（object）：各种值组成的集合 **合成类型**

  - 狭义的对象（object）

  - 数组（array）

  - 函数（function）

    > JavaScript把函数当成一种数据类型，**可以像其他类型的数据一样，进行赋值和传递**，这为编程带来了很大的灵活性，体现了JavaScript作为**“函数式语言”**的本质。

> JavaScript的所有数据，都可以视为**广义的对象**。不仅数组和函数属于对象，就连原始类型的数据（数值、字符串、布尔值）也可以用对象方式调用。为了避免混淆，此后除非特别声明，本教程的”对象“都特指**狭义的对象。**

* 判断一个值是什么类型

  * `typeof`运算符：区别数据类型，注意返回值是**字符串**，加引号了。

    ```javascript
    typeof undefined // "undefined"
    typeof v // "undefined" v是一个没声明的变量不会报错

    typeof window // "object"
    typeof {} // "object"
    typeof [] // "object"
    typeof null // "object" 注意这个instanceof Object false
    typeof 123 // "number"
    typeof '123' // "string"
    typeof false // "boolean"

    function f() {}
    typeof f // "function"
    ```

  * `instanceof`运算符：区分**对象**object的类型???

    ```javascript
    var o = {};
    var a = [];
    o instanceof Array // false
    a instanceof Array // true
    a instanceof Object // true
    ```

  * `Object.prototype.toString`方法


* `undefined`和`null`等价理解(undefined==null)，按下面含义使用：

  * `null`表示空值，即该处的值现在为空。比如，调用函数时，不需要传入某个参数，这时就可以传入`null`。

  * `undefined`表示“未定义”，下面是返回`undefined`的典型场景

    ```javascript
    // 变量声明了，但没有赋值
    var i;
    i // undefined

    // 调用函数时，应该提供的参数没有提供，该参数等于undefined
    function f(x) {
      return x;
    }
    f() // undefined

    // 对象没有赋值的属性
    var  o = new Object();
    o.p // undefined

    // 函数没有返回值时，默认返回undefined
    function f() {}
    f() // undefined
    ```
  >  `undefined`和`null`不同于`Undefined`和`Null`（或者其他仅仅大小写不同的词形），后者只是普通的变量名。


* 布尔型：除了下面六个值被转为`false`，其他值都视为`true`
  * `undefined`
  * `null`
  * `false`
  * `0`
  * `NaN`
  * `""`或`''`（空字符串）



## 数值

* js中所有数都是64bit的浮点数（包括整数）

* 最大值，最小值 `Number.MAX_VALUE` // 1.7976931348623157e+308
  `Number.MIN_VALUE` // 5e-324

* `NaN`是JavaScript的特殊值，表示“非数字”（Not a Number）,主要出现在将字符串解析成数字出错的场合。如：`5 - 'x'` `Math.acos(2)` `0/0`。

  * `typeof NaN` // 'number' NaN不是一种独立的数据类型，而是一种特殊数值

  * `NaN === NaN` // false `NaN`不等于任何值，包括它本身

  * `Boolean(NaN) `// false

  * `NaN + 32` // NaN `NaN`与任何数（包括它自己）的运算，得到的都是`NaN`

  * `isNaN(NaN) ` // true `isNaN`方法可以用来判断一个值是否为`NaN` ；isNaN('Hello') ==》true； isNaN([12]) ==》false，它会先尝试参数类型转换。

  * 因此isNaN并不可靠可靠的判断 是不是 NaN的方法：利用`NaN`是JavaScript之中唯一不等于自身的值这个特点

    ```javascript
    function myIsNaN(value) {
      return value !== value;
    }
    ```


* `Infinity`表示“无穷”，用来表示两种场景。一种是一个正的数值太大，或一个负的数值太小。**正向溢出（overflow）、负向溢出（underflow）和被`0`除，JavaScript都不报错**

  ```javascript
  Infinity === -Infinity // false
  Math.pow(2, Math.pow(2, 100))  // Infinity
  0 / 0 // NaN
  1 / -0 // -Infinity
  -1 / -0 // Infinity
  ```

  一堆奇葩的运算，从数学无穷角度理解

  ```javascript
  5 * Infinity // Infinity
  5 - Infinity // -Infinity
  Infinity / 5 // Infinity
  5 / Infinity // 0
  0 * Infinity // NaN
  0 / Infinity // 0
  Infinity / 0 // Infinity
  null * Infinity // NaN // null相当于0
  null / Infinity // 0
  Infinity / null // Infinity
  undefined + Infinity // NaN
  undefined - Infinity // NaN
  undefined / Infinity // NaN
  Infinity / undefined // NaN
  Infinity + Infinity // Infinity
  Infinity - Infinity // NaN
  Infinity / Infinity // NaN
  ```

  * **isFinite函数**

* 与数值相关的全局方法：字符串转换成数字和进制转换，有些蛋疼的细节

  * parseInt
  * parseFloat


## 字符串

* 单引号和双引号都可以，但是**建议单引号**。由于HTML语言的属性值使用双引号
* 单引号内部可以用双引号，反之亦然
* unicode utf16，有坑？
* 其他方法，参考标准库

## 对象

定义：所谓对象，就是一种无序的数据集合，由若干个“键值对”（key-value）构成。因此**对象的key都是字符串，可以是任意字符（不符合变量命名规范也行）**。但是引用时使用**`o[key]`**（优先）、`o['key']`（可能有歧义），不能用`o.key`。

```javascript
var o ={
  1: 'a',
  3.2: 'b',
  1e-2: true,
  .234: true,
  0xFF: true,
  p: "helloworld",
};
```

* 对象的生成方法，通常有三种方法

  ```javascript
  var o1 = {}; // 推荐
  var o2 = new Object();
  var o3 = Object.create(null); // 继承用？？
  ```

* ~~定义的一个注意点~~(一般情况不用管)

  ```javascript
  var o = {
    p: 'Hello World'
  };
  // 尽量不要这样，有歧义，可能任务是语句快
  var o = {p: 'Hello World'};
  ```

* 查看本身的所有属性(不含继承) Object.keys(o);

  ```javascript
  var o = {
    key1: 1,
    key2: 2
  };
  Object.keys(o); // ['key1', 'key2']
  ```

* 添加属性： `o.p=1` || `o['p']=1`

* **删除属性**：

  * `delete`命令只能删除对象本身的属性，**无法删除继承的属性**


* `delete`命令**不能删除`var`命令声明的变量**，只能用来删除属性。因为**`var`声明的全局变量都是顶层对象（浏览器的顶层对象就是`window`对象）的属性**，而且默认不得删除。

```javascript
  var o = {};
  delete o.p // true
```

  注意：`o`对象并没有`p`属性，但是`delete`命令照样返回`true`。只有一种情况，`delete`命令会返回`false`，那就是该属性存在，且不得删除。

```javascript
  // defineProperty定义的属性不能删除！
  var o = Object.defineProperty({}, 'p', {
    value: 123,
    configurable: false
  });

  o.p // 123
  delete o.p // false
```

* in运算符：`in`运算符用于检查对象是否包含某个属性

  * `for...in`：循环用来遍历一个对象的全部属性

    ```javascript
    var o = {a: 1, b: 2, c: 3};

    for (var i in o) {
      console.log(o[i]);
    }
    ```

    > - 它遍历的是对象所有可遍历（enumberable）的属性，**会跳过不可遍历的属性**，比如`toString`属性不会被`for...in`循环遍历到，因为它默认设置为“不可遍历”
    > - 它不仅遍历对象自身的属性，**还遍历继承的属性**

* ~~with语句~~（**不建议使用！**用在模板引擎的实现）：操作同一个对象的多个属性时，提供一些书写的方便。`with`区块内部的变量，**必须是当前对象已经存在的属性，否则会创造一个当前作用域的全局变量**。

  ```javascript
  // 例一
  with (o) {
    p1 = 1;
    p2 = 2;
  }
  // 等同于
  o.p1 = 1;
  o.p2 = 2;

  // 例二
  with (document.links[0]){
    console.log(href);
    console.log(title);
    console.log(style);
  }
  // 等同于
  console.log(document.links[0].href);
  console.log(document.links[0].title);
  console.log(document.links[0].style);
  ```


## 数组

定义：数组是一个key（属性名）为0，1，2...的对象，它的类型是Array，原型是Object。`Object.keys()`可返回。与其他任何对象类似，可用`a[0]`，`a['0']`取值，

* 定义：`var arr = ['a', 'b'];`

* 重要方法：`arr.push(element) ` `arr.pop()`

* *请注意*，`for ... in`对`Array`的循环得到的是`String`而不是`Number`。

* 长度： `arr.length` 

  * 值可以修改
    * 如果比实际的length小，会删除多余元素
    * 如果比实际的length大，这种结果[1, undefined × 2]
  * `length`属性的值就是等于最大的**数字键**加1

* 添加：

  ```javascript
  arr[1000] = 'e'; // 不一定要连续
  arr.length // 1001 注意，很特别
  arr[999] // undefined 注意，很特别
  Object.keys(arr) // ["0", "1", "1000"]
  arr.length=3 
  arr //["a", "b", undefined × 1]
  arr[4] // undefined
  ```

* 遍历：

  ```javascript
  var a = [1, ,2,3]; // 一个含有空位的数组
  // for in 不推荐，可能会遍历非数组属性，自动忽略空位
  for (var i in a) {
    console.log(a[i]); // 注意与python区别，i只是key，不是value
  }

  // 循环,可能遇到空位
  for(var i = 0; i < a.length; i++) {
    console.log(a[i]);
  }

  // for each，自动忽略空位
  a.forEach(function (color) {
    console.log(color);
  });
  ```

* 清空:

  ```javascript
  arr.length = 0;
  ```

* 删除任意一个值：`delete a[1]`不影响`length`，被删除的成为`undefined`,成为***空位***。

* 可以添加其他属性 `a['p'] = 'abc';`

* 注意：**由于数组本质上是对象的一种，所以我们可以为数组添加属性，但是这不影响`length`属性的值。**

* 数组类似对象：给普通Object对象加上length属性，如**string，arguments就是**。



## 函数

一等公民

* 三种声明方式

  ```javascript
  // 方法一
  function print(s) {
    console.log(s);
  }
  // 方法二
  var print = function(s) {
    console.log(s);
  };
  // 方法二，注意func只在函数体内可访问
  // 最好  var f = function f() {};
  var print = function func(s) {
    console.log(s);
  };
  // 方法三 函数的本质是对象，最后一句是返回值，前面是n个参数
  var add = new Function( //new 可以不写，但是不建议！
    'x',
    'y',
    'return (x + y)'
  );
  ```

* 函数重复声明，之前的会失效（对比变量）

* 函数提升：只有第一种方式声明的会提升。

* 函数对象的属性：

  * `name` 函数名

    ```javascript
    function f1() {}
    f1.name // 'f1'

    var f2 = function () {};
    f2.name // '' 测试发现，返回"f2".....

    var f3 = function myName() {};
    f3.name // 'myName'
    ```

  * `length` 函数参数个数，可以区分实际传入的个数，实现面向对象编程的”方法重载“（overload）。

  * `toString()` 返回函数的源码，函数内部的注释也可以返回。

* 允许调用时省略参数

  ```javascript
  function f(a, b) {
    return a;
  }

  f(1, 2, 3) // 1
  f(1) // 1
  f() // undefined
  f(undefined, 1)  // 省略第一个参数，不能f(,1)语法错误
  f.length // 2 注意length是f定义的本身的属性
  ```

* **为函数参数设置默认值**：参考code snippet

* 值传递，引用传递，与java类似

* **`arguments`对象**：代表所有参数，由于JavaScript允许函数有不定数目的参数，所以我们需要一种机制，可以在函数体内部读取所有参数。这就是`arguments`对象的由来。**这个对象只有在函数体内部，才可以使用**。

  * 它不是数组，虽然很像，`arguments[0]`取值，`arguments.length`获取参数个数，`arguments[0]=1`赋值(不建议)。	

  * 不能使用数组的方法forEach/slice等，可以转化为数组后再用。

  * 常用的地方是`myfunction.apply(obj, arguments)`

  * ~~callee属性~~：arguments对应的原函数，严格模式里面是禁用的，因此不建议使用。

  * 应用：

    ```javascript
    // 判断个数
    function foo(a, b, c) {
        if (arguments.length === 2) {
            // 实际拿到的参数是a和b，c为undefined
        }
    }
    //  即使不定义参数也能拿到参数
    function abs() {
        if (arguments.length === 0) {
            return 0;
        }
        var x = arguments[0];
        return x >= 0 ? x : -x;
    }
    abs(-9); // 9
    ```

    ​

* ~~立即调用的函数表达式（IIFE）~~

  * 一对圆括号`()`是一种运算符，跟在函数名之后，表示调用该函数

    ```javascript
    // 避免歧义，必须要外层的括号，以表达式解释，而不是语句。
    // 如果function在行首js引擎认为是语句。
    (function(){ /* code */ }());
    // 或者 更好理解
    (function(){ /* code */ })();
    ```

  * 用处：

    * 一是不必为函数命名，避免了污染全局变量；

    * 二是IIFE内部形成了一个单独的作用域，可以封装一些外部无法读取的私有变量。

      ```javascript
      // 写法一
      var tmp = newData;
      processData(tmp);
      storeData(tmp);

      // 写法二,更好，避免tmp污染全局作用域
      (function (){
        var tmp = newData;
        processData(tmp);
        storeData(tmp);
      }());
      ```



* ~~eval命令~~：相当于其他语言的exe命令，**将字符串当作语句执行**

  * `eval`没有自己的作用域，都在当前作用域内执行

  * `eval`的使用分成两种情况，像上面这样的调用，就叫做“直接使用”，这种情况下`eval`的作用域就是当前作用域（即全局作用域或函数作用域）。另一种情况是，`eval`不是直接调用，而是“间接调用”，此时eval的作用域总是全局作用域。

    ```javascript
    var a = 1;

    function f(){
      var a = 2;
      var e = eval;
      e('console.log(a)');
    }

    f() // 1
    ```

  * 同样的功能：`Function`构造函数也可以让字符串执行。


* 不要在if，while语句中声明函数，但是可以在函数内部声明函数。(闭包)
* 高阶函数：将函数作为参数传入一个函数。

## 函数闭包

* 定义：把闭包简单理解成“定义在一个函数内部的函数”。在本质上，闭包就是将函数内部和函数外部连接起来的一座桥梁。

* 作用：

  * 可以读取函数内部的变量，
  * 让这些变量始终保持在内存中，即闭包可以使得它诞生环境一直存在

* 用法举例：

  * 保持变量到内存：

    ```javascript
    function createIncrementor(start) {
      // 或者var start =0;
      return function () {
        return start++;
      };
    }

    var inc = createIncrementor(5);

    inc() // 5
    inc() // 6
    inc() // 7
    ```

  * 封装私有变量和方法

    ```javascript
    function Person(name) {
      var _age;
      function setAge(n) {
        _age = n;
      }
      function getAge() {
        return _age;
      }
      // 注意：如果new Person 实际生成的是这个对象
      return {
        name: name,
        getAge: getAge,
        setAge: setAge
      };
    }

    var p1 = person('张三');
    p1.setAge(25);
    p1.getAge() // 25
    ```

## 运算符

* 比较方法：

  * 如果运算子是对象，先自动转成原始类型的值（即先执行该对象的`valueOf`方法，如果结果还不是原始类型的值，再执行`toString`方法）。
  * 如果两个运算子都是字符串，则按照字典顺序比较（实际上是比较Unicode码点）。
  * 否则，将两个运算子都转成数值，再进行比较。

* `==`和`===`：如果两个值不是同一类型，严格相等运算符（`===`）直接返回`false`，而**相等运算符（`==`）会将它们转化成同一个类型**，再用严格相等运算符进行比较

  ```javascript
  '' == 0 // 等同于 Number('') === 0 

  1 === "1" // false
  1 == "1" // true
  // 对象是比较内存地址
  ({} === {}) // false
  ({} == {}) // false

  null === null // true
  null === undefined // false
  null == undefined // true
  0 == null // false
  0 == undefined // false
  ```

* `!=`和`!==`：同上

* 最佳实践：**不要使用相等运算符（`==`），最好只使用严格相等运算符（`===`）。**因为`==`会有很多违反直觉的例子：

  ```javascript
  '' == '0'           // false
  0 == ''             // true
  0 == '0'            // true
  ```

* 取反运算：下面的6个值取反是true，但是不代表本身==false

  * `undefined`
  * `null`
  * `false`
  * `0`（包括`+0`和`-0`）
  * `NaN`
  * 空字符串（`''`）

* void 运算符：执行一个表达式，然后不返回任何值，或者说返回`undefined`。

  * 示例

    ```javascript
    x = 5 // 5
    void (x = 5); // // undefined

    function f() {return 1}
    f(); // 1
    void f(); // undefined
    ```

  * 应用：在超级链接中插入代码，目的是返回`undefined`可以防止网页跳转

    ```html
    <!--点击某个link，运行某个方法-->
    <!-- 会运行f函数，并跳转到example.com网页-->
    <a href="http://example.com" onclick="f();">文字</a>
    <!-- onclick返回false，不跳转-->
    <a href="http://example.com" onclick="f();return false;">文字</a>
    <!-- 用void，实现点击不调不跳转-->
    <a href="javascript: void(f())">文字</a>

    <!-- 不会在当前页面跳转，而是打开新窗口-->
    <a href="javascript:void window.open('http://example.com/')">
      点击打开新窗口
    </a>
    <!--提交表单-->
    <a href="javascript: void(document.form.submit())">
    文字</a>
    ```

## 数据类型转换

变量本身的类型是动态的。但是**运算时**是有类型的。理解上面各种运算符（如`1 == '1'`,`'4' - '3'`）就是数据转换的过程。

* 强制转换：使用`Number`、`String`和`Boolean`三个构造函数，手动将各种类型的值，转换成数字、字符串或者布尔值。

  * Number

    ```javascript
    Number('') // 0
    Number(undefined) // NaN
    Number(null) // 0
    Number({}) // NaN

    // 区分Number与parseInt
    Number('42 cats') // NaN
    parseInt('42 cats') // 42
    ```

    > `Number`函数会自动过滤一个字符串前导和后缀的空格。
    >
    > `Number`方法的参数是对象(字符串除外)时，将返回`NaN`。

  * String

  * Boolean 除了下面6个，都是true

    - `undefined`
    - `null`
    - `-0`
    - `0`或`+0`
    - `NaN`
    - `''`（空字符串）

* 自动转换：

  * 时机：

    *  不同类型的数据互相运算 如 `123+'abc'`
    *  对非布尔值类型的数据求布尔值 如` if("abc")`
    *  对非数值类型的数据使用一元运算符（即“+”和“-”）如- [1, 2, 3] // NaN

  * 规则：

    预期什么类型的值，就调用该类型的转换函数

    * 转化为String：加法运算
    * 转化为Number：除了加法运算

* 建议：**全部使用`Boolean`、`Number`和`String`函数进行显式转换。**
* 坑：

  * +"123"-->number(123)  
  * 1+"123"-->String("1123")
  * i+1，导致结果不确定！可以使用+i+1;

## 错误处理

类似于java的throw catch机制，这里都叫Error或者xxxError。

* 内置异常：Error的子类

  * **SyntaxError**:解析代码时发生的语法错误。
  * **ReferenceError**：引用一个不存在的变量时发生的错误。
  * **RangeError**：一是数组长度为负数，二是Number对象的方法参数超出范围
  * **TypeError**：变量或参数不是预期类型时发生的错误，如：调用对象不存在的方法
  * **URIError**：`URIError`是URI相关函数的参数不正确时抛出的错误，主要涉及`encodeURI()`、`decodeURI()`、`encodeURIComponent()`、`decodeURIComponent()`、`escape()`和`unescape()`
  * ~~**EvalError**~~

* 自定义错误：Error的子类

  ```javascript
  function UserError(message) {
     this.message = message || "默认信息";
     this.name = "UserError";
  }

  UserError.prototype = new Error();
  UserError.prototype.constructor = UserError;
  // 使用
  new UserError("这是自定义的错误！");
  ```

* throw 可以抛出任何对象，当然包括Error对象

  ```javascript
  // 一般使用
  throw new Error('出错了!');

  // 抛出一个字符串
  try {
    throw "Error！";
  }catch(e){
    console.log(e);
  }

  // 抛出一个数值
  throw 42;
  // 抛出一个布尔值
  throw true;
  ```

* try catch示例

  ```javascript
  try {
    foo.bar();
  } catch (e) {
    if (e instanceof EvalError) {
      console.log(e.name + ": " + e.message);
    } else if (e instanceof RangeError) {
      console.log(e.name + ": " + e.message);
    }
    // ...
  }
  ```

* finally

  ```javascript
  try {
    writeFile(Data);
  } catch(e) {
    handleError(e);
  } finally {
    closeFile();
  }
  ```

* try catch finally return 之间的trick。。。

## 标准库

调用对象方法的两种方式：

* 正常：o.func(arg1,arg2)

* call/apply `对象名.func.call(o,arg1,arg2 )`或者 `对象名.func.apply(o,args)`，

  * 应用：实例对象可能会自定义`toString`方法，覆盖掉`Object.prototype.toString`方法。通过函数的`call`方法，可以在任意值上调用`Object.prototype.toString`方法，帮助我们判断这个值的类型。如果不想创建实例，只是想单纯调用这些方法

    ​

    ```javascript
    Object.prototype.toString.call(value)
    // 
    // Array.prototype.method.call(调用对象，参数)
    ```

### Object

**重点**：对象的方法一般定义在`Object.prototype`（**实例方法**）和`Object`（**静态方法，不能被Object实例对象调用**）中。

> 除此之外，还有内部方法，在Object的构造函数中定义，外部无法修改，这种定义方法耗内存。ex:this.func=function(){};

* 给Object添加方法的两种方式（其他对象也是）：

  * 添加到`Object`中
  * 添加到`Object.prototype`中

  ```javascript
  // 静态方法,区别，这里不是构造函数里面this.print(内部方法)
  Object.print = function(o){ console.log(o) };
  // 静态方法，只能这样调用
  Object.print(o);

  // 实例方法
  Object.prototype.print = function(){ console.log(this)};
  // 两种调用方式
  o.print();
  Object.prototype.print.call(o);
  ```

  ​


* 静态方法
  * **Object.keys()**，~~Object.getOwnPropertyNames()~~作用以及区别
  * **对象属性模型的相关方法**
  * **控制对象状态的方法**
  * **原型链相关方法**
    * Object.create()：生成一个新对象，并该对象的原型。
    * Object.getPrototypeOf()：获取对象的Prototype对象
* 实例方法
  * `valueOf()`：返回当前对象对应的值。
  * `toString()`：返回当前对象对应的字符串形式。
  * `hasOwnProperty()`：判断某个属性是否为当前对象自身的属性，还是继承自原型对象的属性。
  * `isPrototypeOf()`：判断当前对象是否为另一个对象的原型。
  * `propertyIsEnumerable()`：判断某个属性是否可枚举。
  * `toLocaleString()`：返回当前对象对应的本地字符串形式。

### Array

Object的子类，建议使用`var arr=[];`方式定义

* 静态方法

  * `isArray()`：一个值是否为数组。它可以弥补typeof运算符的不足

* 实例方法

  * Object继承的 valueOf、toString等
  * push pop
  * join 它把当前`Array`的每个元素都用指定的字符串连接起来，然后返回连接后的字符串
  * concat
  * shift unshift
  * reverse
  * **slice**:方法用于提取原数组的一部分，返回一个新数组，还能用作把非数组**转为真正的数组**。
  * splice`splice()`方法是修改`Array`的“万能方法”，它可以从指定的索引开始删除若干元素，然后再从该位置添加若干元素.
  * `sort()`：默认把所有元素先转换为String再排序，结果`'10'`排在了`'2'`的前面。用默认排序规则，直接对数字排序，绝对栽进坑里！`sort()`方法会直接对`Array`进行修改，它返回的结果仍是当前`Array`

* 新增方法：大部分是函数式操作方法

  * map forEach filter
  * some every
  * reduce reduceRight
  * indexOf lastIndexOf

* **链式使用**：demo

  ```javascript
  var users = [{name:"tom", email:"tom@example.com"},
  			 {name:"peter", email:"peter@example.com"}];

  users
  .map(function (user){ return user.email; })
  .filter(function (email) { return /^t/.test(email); })
  .forEach(alert);
  ```

### 其他标准库对象

包装对象（Boolean、Number、String）、Math、Date、RegExp、JSON

* 正则

  * 构造

    ```javascript
    // /xyz/构造了一个正则表达式
    var regex = /xyz/;
    var regex = new RegExp('xyz');
    ```

  * 应用

    * 分割字符串

      ```javascript
      // 正确分割空格，n个空格
      'a b   c'.split(/\s+/); // ['a', 'b', 'c']
      ```

      ​


* 包装类型：

  * `new String(true)` 不是String` (true)`
  * `new String("str") === "str";` `Boolean(true) === true;`**是false**
  * **不要使用包装对象**！

* Date：

  * 坑：**月份是0–11**，不是1–12

  * 为了方便时区转换，统一用**时间戳**表示时间，显示的时候再转换

    ```javascript
    var d = new Date(1435146562875);
    d.toLocaleString(); // '2015/6/24 下午7:49:22'，本地时间（北京时区+8:00），显示的字符串与操作系统设定的格式有关
    d.toUTCString();
    ```

* Json:

  * 序列化（都是UTF8）

    ```javascript
    // 
    var xiaoming = {
        name: '小明',
        age: 14,
        skills: ['JavaScript', 'Java', 'Python', 'Lisp'],
        // 给对象添加toJSON方法，会按照下面的输出
        // toJSON: function () {
        //     return { // 只输出name和age，并且改变了key：
        //         'Name': this.name,
        //         'Age': this.age
        //     };
        // }
    };

    JSON.stringify(xiaoming); 
    // 控制缩进，比较好看
    JSON.stringify(xiaoming, null, '  ');
    // 过滤
    JSON.stringify(xiaoming, ['name', 'skills'], '  ');
    // 处理函数后输出
    function convert(key, value) {
        if (typeof value === 'string') {
            return value.toUpperCase();
        }
        return value;
    }
    JSON.stringify(xiaoming, convert, '  ');
    ```

  * 反序列化

    ```javascript
    JSON.parse('[1,2,3,true]'); // [1, 2, 3, true]
    JSON.parse('{"name":"小明","age":14}'); // Object {name: '小明', age: 14}
    // 处理函数
    JSON.parse('{"name":"小明","age":14}', function (key, value) {
        // 把number * 2:
        if (key === 'name') {
            return value + '同学';
        }
        return value;
    }); // Object {name: '小明同学', age: 14}
    ```



### 属性描述对象（了解）

描述一个对象的属性的行为。**对象的每个属性都有自己对应的属性描述对象，保存该属性的一些元信息。**比如是否可以修改（writable），是否可以被遍历enumerable。

```javascript
{
  // 存放该属性的属性值,默认为undefined
  value: 123, 
  // boolean，是否可改变，默认为true
  writable: false, 
  //是否可枚举，默认true,影响for in/Object.keys
  enumerable: true, 
  // “可配置性”，默认为true,false后这其他描述值不可修改
  configurable: false,
  // 保持属性的get，set方法
  get: undefined,
  set: undefined
}
```

## 面向对象编程

### 基本概念

* **没有类**。不是基于“类”的，而是基于构造函数（constructor）和原型链（prototype）。

* 用构造函数生成对象模板

  ```javascript
  // Vehicle就是构造函数，它提供模板
  var Vehicle = function () {
    // 'use strict'; //可以添加，使用严格模式
    this.price = 1000;
  };
  ```

  >  注意：
  >
  >  * 遵守构造函数名**首字母大写**的编码规范
  >  * ~~尽量使用上面的方法定义构造函数，避免使用`function Vehicle(){}`定义构造函数，向外暴露成了函数。~~

* 生成对象

  ```javascript
  var v = new Vehicle(); // 有参数传参 new Vehicle(100)
  var v = new Vehicle; // 没参数的话也可以
  // 错误！容易忘记new，使用严格模式时会报错
  // var v = Vehicle();
  ```

* new的原理

  1. 创建一个空对象，作为将要返回的对象实例
  2. 将这个空对象的原型，指向构造函数的`prototype`属性
  3. **将这个空对象赋值给函数内部的`this`关键字**
  4. 开始执行构造函数内部的代码

  ```javascript
   // 超级简化，var a = new A('hehe') =>
   var a = new Object();
   a.__proto__ = A.prototype; (proto)
   A.call(a, 'hehe');
  ```

  ​

* 坑：

  * *如果构造函数内部有`return`语句**，而且`return`后面跟着一个对象，`new`命令会返回`return`语句指定的对象；否则，就会不管`return`语句，返回`this`对象。
  * ~~如果对普通函数（**内部没有`this`关键字的函数**）使用`new`命令，则会返回一个空对象。~~(chrome测试，不是这样的)

  ```javascript
  var Vehicle = function (){
    this.price = 1000;
    return { price: 2000 };
  };
  (new Vehicle()).price

  //function getMessage() {
  //  return 'this is a message';
  //}
  //var msg = new getMessage();
  //msg // {}
  //typeof msg // "Object"
  ```

* 一个可以参考的new命令流程

  ```javascript
  function _new(/* 构造函数 */ constructor, /* 构造函数参数 */ param1) {
    // 将 arguments 对象转为数组
    var args = [].slice.call(arguments);
    // 取出构造函数
    var constructor = args.shift();
    // 创建一个空对象，继承构造函数的 prototype 属性
    var context = Object.create(constructor.prototype);
    // 执行构造函数
    var result = constructor.apply(context, args);
    // 如果返回结果是对象，就直接返回，则返回 context 对象
    return (typeof result === 'object' && result != null) ? result : context;
  }

  // 实例
  var actor = _new(Person, '张三', 28);
  ```

* instanceof：判断对象的类型（根据原型判断），区别typeof，也是typeof的补充。

  ```javascript
  // 对原始类型无效，用typeof判断
  var s = 'hello';
  s instanceof String // false

  var s = new String('hello');
  s instanceof String // true
  // undefined和null不是对象
  undefined instanceof Object // false
  null instanceof Object // false
  ```

### this关键字

* 核心：
  * 每个函数都说有this，这个隐藏的参数
  * this是随时变换的，**函数被赋值给谁（对象），this就指向谁（对象）**。
  * 全局的函数this指向window。


* 阅读：http://javascript.ruanyifeng.com/oop/this.html

* 一个常见的错误：

  ```javascript
  var log = console.log;
  // 调用call并传入console对象作为this:
  log("test"); // error!
  ```


* 注意点：
  * 避免嵌套this，解决办法：**使用一个变量锁定this**（如`var that = this;`）然后内层函数调用这个变量，是非常常见的做法，有大量应用，<u>请务必掌握</u>。
  * **避免数组处理方法中的this**，数组的`map`和`foreach`方法，允许提供一个函数作为参数。**解决办法同上**。或者**将`this`当作`foreach`方法的第二个参数**，固定它的运行环境。也可使用bind方法。
  * **避免回调函数中的this**，可使用bind方法。
  * 对普通函数调用，我们通常把`this`绑定为`null`。


* 固定this：JavaScript提供了`call`、`apply`、`bind`这三个方法，来切换/固定`this`的指向。他们都是**function的方法**

  * `function.prototype.call()`、`function.prototype.apply()`：指定this&&调用函数，不同是参数列表。一个应用：调用原生方法，见标准库Object节

  * `function.prototype.bind()`：绑定函数到某个对象，保存返回值，以后调用该函数，this都是指向这个对象。

    ```javascript
    var obj = {
      count: 100
    };
    // 注意保持func
    var func = counter.inc.bind(obj);
    // 不是直接调用counter.inc
    func();
    obj.count // 101

    // 数组的例子，多调用bind，来绑定this
    obj.print = function () {
      this.times.forEach(function (n) {
        console.log(this.name);
      }.bind(this));
    };
    ```

    ​

    * 还可以绑定参数
    * 传null，表示绑定全局的window

  * <u>**bind结合call使用**，一定要理解！！！！！很有意思</u>

    ```javascript
    //Array.prototype.push函数本身是个对象
    // 一个绑定了push函数的call，call参数是(调用者,调用参数)
    var push = Function.prototype.call.bind(Array.prototype.push);
    var pop = Function.prototype.call.bind(Array.prototype.pop);

    var a = [1 ,2 ,3];
    push(a, 4)
    a // [1, 2, 3, 4]

    pop(a)
    a // [1, 2, 3]
    ```

### 原型prototype与继承

* 原型机制的出发点：构造函数生成的方法每个实例都有一个，浪费内存，有什么机制能公用这些方法。

* 实质：**构造函数通过原型链记录了继承关系。记录的方法是：通过函数的`prototype`把关系串联起来。**至于原型链中分配的对象即**原型对象**,**一个构造函数对应一个原型对象**。（好好理解为什么不能直接把构造函数串起来）

* 基本设计：原型对象上的所有属性和方法，都能被派生对象共享。<u>通过构造函数生成实例对象时，会自动为实例对象分配原型对象</u>。**每一个构造函数都有一个`prototype`属性**，这个属性就是实例对象的**原型对象**。

  * 当实例对象本身没有某个属性或方法的时候，它会到构造函数的`prototype`属性指向的对象，去寻找该属性或方法。这就是原型对象的特殊之处。
  * 如果实例对象自身就有某个属性或方法，它就不会再去原型对象寻找这个属性或方法。
  * 当修改某个属性时，会在实例对象本身上加入该属性，从而覆盖(override)原型对象的属性。以后修改的都是实例对象本身的属性。

  > 注意：`prototype`只有构造**函数**（Function）有！普通对象（Object）没有！普通对象只有`__proto__`


* JavaScript的所有对象都有构造函数，而所有构造函数都有`prototype`属性（其实是所有函数都有`prototype`属性），所以所有对象都有自己的原型对象。

* 原型链：**原型链的尽头是一个`__proto__`值为null的Object实体**。所有对象的原型最终都可以上溯到`Object.prototype`，即`Object`构造函数的`prototype`属性指向的那个**对象**。那么，`Object.prototype`对象有没有它的原型呢？回答可以是有的，就是没有任何属性和方法的`null`对象，而`null`对象没有自己的原型。

* constructor属性：`prototype`对象有一个`constructor`属性，默认指向`prototype`对象所在的构造函数。(`constructor`是`Object`的属性,指向构造自身的构造函数Function)

  * `constructor`属性的作用，是分辨原型对象到底属于哪个构造函数。

  * 有了`constructor`属性，就可以从实例新建另一个实例。

    ```javascript
    var y = new x.constructor();
    // 一个应用，创建一个copy函数
    Constr.prototype.createCopy = function () {
      return new this.constructor();
    };
    // 一个应用，获取某个对象的构造函数名
    function Foo() {}
    var f = new Foo();
    f.constructor.name // "Foo"
    ```

  * instanceof 的判断和constructor和prototype有关。

    ```javascript
    mine instanceof Array
    // 等同于
    (Array === MyArray.prototype.constructor) ||
    (Array === Array.prototype.constructor) ||
    (Array === Object.prototype.constructor )
    ```

  * constructor实际用处不大，但是所有如果设置了函数对象的prototype属性加一句：(因为.constructor是Object的属性)

    ```javascript
    o.prototype.constructor = o;
    ```

* `Object.getPrototypeOf`方法返回一个对象的原型。

  ```javascript
  Object.getPrototypeOf({}) === Object.prototype
  // 函数的原型是Function.prototype
  function f() {}
  Object.getPrototypeOf(f) === Function.prototype // true
  Object.getPrototypeOf(f) === f.__proto__ // true
  // f 为 F 的实例对象，则 f 的原型是 F.prototype
  var f = new F();
  Object.getPrototypeOf(f) === F.prototype // true
  ```

* `Object.setPrototypeOf`方法可以为现有对象设置原型，**返回一个新对象**。

  ```javascript
  var a = {x: 1};
  var b = Object.setPrototypeOf({}, a);
  // 等同于
  // var b = {__proto__: a};
  ```

* `Object.create`方法用于从**原型对象**生成新的**实例对象**，可以替代`new`命令。

  ```javascript
  var A = {
   print: function () {
     console.log('hello');
   }
  };
  // 注意参数，是原型对象
  var B = Object.create(A);
  var C = Object.create(null)

  B.print // hello
  B.print === A.print // true
  ```

  * `var b =Object.create(a) `会导致类型判断不方便，使用`isPrototypeOf`方法即可。

    ```javascript
    var o1 = {};
    var o2 = Object.create(o1);
    var o3 = Object.create(o2);

    o2.isPrototypeOf(o3) // true
    o1.isPrototypeOf(o3) // true
    ```

  * Object.create(null) 不继承任何属性，不含有Object.ptototype的方法如valueOf,可以使用下面方式

    ```javascript
    var o1 = Object.create({});
    var o2 = Object.create(Object.prototype);
    var o3 = new Object();
    ```

* `__proto__`:记录对象的原型，可以读写，来改变对象原型对象，但是不建议这么做，而是通过`Object.getPrototypeof()`（读取）和`Object.setPrototypeOf()`（设置）。

  * 获取当前对象的原型对象
    * `obj.__proto__` 不推荐，有些浏览器没有
    * `obj.constructor.prototype` 不推荐，有些继承修改忘了改constructor。
    * `Object.getPrototypeOf(obj)` 推荐

## 模块化

使用trick模块化js代码

### 方式一

方法放入prototype，私有变量放入实例对象中。问题是私有变量暴露出去了。

```javascript
function StringBuilder() {
  this._buffer = [];
}

StringBuilder.prototype = {
  constructor: StringBuilder,
  add: function (str) {
    this._buffer.push(str);
  },
  toString: function () {
    return this._buffer.join('');
  }
};
```

### 方式二

封装私有变量：立即执行函数的写法

```javascript
// 立即执行函数确保全局只生成一个实例。
var module1 = (function($, window, document) {
  var _count = 0;
  function go(num) {
  }

  function handleEvents() {
  }

  function initialize() {
  }

  function dieCouraselDie() {
  }

  // 放入全局作用域，也可不放
  window.finalCarousel = {
    // 暴露出去的方法
    init : initialize,
    destroy : dieCouraselDie
  }
  return window.finalCarousel;
  // 依赖的其他模块，因为网络异步加载可能为undefined，可以使用宽松放大模式，确保内部访问jQuery.xxx不会Error。
  // (jQuery|| {});
})( jQuery, window, document );
```

## 线程模型

### 单线程+队列+异步

一个例子:

```javascript
var start = new Date;
setTimeout(function(){
    var end = new Date;
    console.log('Time elapsed:', end - start, 'ms');
}, 500);
while (new Date - start < 1000) {};
// 最后输出>1000.setTimeout立即返回到线程队列里面等待
```

### 事件循环

* [参考这篇文章](http://www.ruanyifeng.com/blog/2014/10/event-loop.html)

## ES6有用新特性

### 字符串

* 多行字符串 

  ```javascript
  alert(`多行
  字符串
  测试`);
  ```

### 数据结构

* `Map` `Set`

  * 与普通对象{}区别：

    * `Map`的key可以是任意类型`{}`只能是String
    * 很容易的得到一个`Map的键值对个数`,而只能跟踪一个对象的键值对个数

  * 使用：

    ```javascript
    var m = new Map(); // 空Map
    // var m = new Map([['Michael', 95], ['Bob', 75], ['Tracy', 85]]);
    m.set('Adam', 67); // 添加新的key-value
    m.has('Adam'); // 是否存在key 'Adam': true
    m.get('Adam'); // 67
    m.delete('Adam'); // 删除key 'Adam'

    var s = new Set([1, 2, 3, 3, '3']);
    s.add(4);
    s.delete(3);
    s.has(3);
    ```

* iterable与遍历：**Array、Map和Set都属于iterable类型**。遍历Array可以采用下标循环，遍历Map和Set就无法使用下标。为了统一集合类型，ES6标准引入了新的iterable类型。

  * `for .. of ..`

    ```javascript
    var a = ['A', 'B', 'C'];
    var s = new Set(['A', 'B', 'C']);
    var m = new Map([[1, 'x'], [2, 'y'], [3, 'z']]);
    for (var x of a) { // 遍历Array
        alert(x);
    }
    for (var x of s) { // 遍历Set
        alert(x);
    }
    for (var x of m) { // 遍历Map
        alert(x[0] + '=' + x[1]);
    }
    ```

  * `forEach`

    ```javascript
    // 数组，如果对某些参数不感兴趣，由于JavaScript的函数调用不要求参数必须一致，因此可以忽略它们。例如，只需要获得Array的element：
    var a = ['A', 'B', 'C'];
    a.forEach(function (element) {
        alert(element);
    });
    // 集合，前两个元素相同
    var s = new Set(['A', 'B', 'C']);
    s.forEach(function (element, sameElement, set) {
        alert(element);
    });
    // map,
    var m = new Map([[1, 'x'], [2, 'y'], [3, 'z']]);
    m.forEach(function (value, key, map) {
        alert(value);
    });
    ```

### 函数

* rest参数：不定个数参数时使用，代替arguments

  ```javascript
  function foo(a, b, ...rest) {
      console.log('a = ' + a);
      console.log('b = ' + b);
      console.log(rest);
  }
  foo(1, 2, 3, 4, 5); // 1 2 [3,4,5]
  foo() // undefined undefined []
  ```


* 箭头函数：修正了this问题

  ```javascript
  x => x * x
  x => {
      if (x > 0) {
          return x * x;
      }
      else {
          return - x * x;
      }
  }

  // 两个参数:
  (x, y) => x * x + y * y
  // 修正this指向
  var obj = {
      birth: 1990,
      getAge: function () {
          var b = this.birth; // 1990
          var fn = () => new Date().getFullYear() - this.birth; // this指向obj对象
          return fn();
      }
  };
  obj.getAge(); // 25
  ```

  * generator函数 ：一个函数返回多次值

    ```javascript
    function* foo(x) {
        yield x + 1;
        yield x + 2;
        return x + 3;
    }
    var f= foo(1); // 没有开始运行
    f.next(); // {value: 2, done: false}
    f.next(); // {value: 3, done: false}
    f.next(); // {value: 4, done: true}
    ```

    * 应用：异步回调代码变成“同步”代码???

### 变量

* 块作用域变量

  ```javascript
  function foo() {
      var sum = 0;
    // 使用let代替var
      for (let i=0; i<100; i++) {
          sum += i;
      }
      i += 1; // SyntaxError
  }
  ```

* 常量const

  ```javascript
  const PI = 3.14;
  ```

### 面向对象

* class关键字：实现继承的语法糖

  ```javascript
  class Student {
      constructor(name) {
          this.name = name;
      }

      hello() {
          alert('Hello, ' + this.name + '!');
      }
  }
  // class extends关键字隐含了原型的处理
  class PrimaryStudent extends Student {
      constructor(name, grade) {
        // 类似与apply与call的功能
          super(name); // 记得用super调用父类的构造方法!
          this.grade = grade;
      }

      // 添加到PrimaryStudent的原型中
      myGrade() {
          alert('I am at grade ' + this.grade);
      }
  }
  ```



### 库

* Promise：

  * 链式调用 `job1.then(handleSuccess).catch(handleError);`

    ```javascript
    // 执行函数，两个参数，一个成功的回调，一个失败的回调
    function test(resolve, reject) {
        var timeOut = Math.random() * 2;
        console.log('set timeout to: ' + timeOut + ' seconds.');
        setTimeout(function () {
            if (timeOut < 1) {
                console.log('call resolve()...');
                resolve('200 OK');
            }
            else {
                console.log('call reject()...');
                reject('timeout in ' + timeOut + ' seconds.');
            }
        }, timeOut * 1000);
    }
    // 链式调用
    new Promise(test).then(function (result) {
        console.log('成功：' + result);
    }).catch(function (reason) {
        console.log('失败：' + reason);
    });
    ```

  * 链式调用 `job1.then(job2).then(job3).catch(handleError);`其中，**`job1`、`job2`和`job3`都是返回Promise对象的函数**。即会自动执行函数返回的Promise对象，然后把结果传递给下一个then/catch。

    ```javascript
    function log(s) {
        console.log(s);
    }
    function multiply(input) {
      // 注意返回的是promise对象
        return new Promise(function (resolve, reject) {
            log('calculating ' + input + ' x ' + input + '...');
            setTimeout(resolve, 500, input * input);
        });
    }

    // 0.5秒后返回input+input的计算结果:
    function add(input) {
        return new Promise(function (resolve, reject) {
            log('calculating ' + input + ' + ' + input + '...');
            setTimeout(resolve, 500, input + input);
        });
    }

    var p = new Promise(function (resolve, reject) {
        log('start new Promise...');
        resolve(123);
    });

    p.then(multiply)
     .then(add)
     .then(multiply)
     .then(add)
     .then(function (result) {
        log('Got value: ' + result);
    });
    ```


* 并行调用

  ```javascript
    var p1 = new Promise(function (resolve, reject) {
        setTimeout(resolve, 500, 'P1');
    });
    var p2 = new Promise(function (resolve, reject) {
        setTimeout(resolve, 600, 'P2');
    });
    // 同时执行p1和p2，并在它们都完成后执行then:
    Promise.all([p1, p2]).then(function (results) {
        console.log(results); // 获得一个Array: ['P1', 'P2']
    });
  ```

* 并行竞争调用，常用于容错设计，获得先返回的结果。

  ```javascript
      var p1 = new Promise(function (resolve, reject) {
          setTimeout(resolve, 500, 'P1');
      });
      var p2 = new Promise(function (resolve, reject) {
          setTimeout(resolve, 600, 'P2');
      });
      Promise.race([p1, p2]).then(function (result) {
          console.log(result); // 'P1'
      });
  ```

  ​


## 理解点

1. 为什么访问`o.xx`，即使xx没有定义，也会返回undefined，不会报错Error，但是直接访问变量xx，会报错。

   答：o对象的本质是hashmap，`o.xx`理解成`o[xx]`，既没有查找到key值。但是，直接访问xx，本质上他是root（window）的属性window[xx]，但是编译器特殊处理了，返回error。当然你访问`this.xx`（当然要看作用域）或者`window.xx`就可以避免了。

2. 理解静态方法，实例方法，内部方法。

3. 理解this，理解call，apply，bind，以及混合使用。

4. 理解原型，原型实体，原型实体与构造函数的关系。为什么是1：1的关系？

5. typeof 与 instanceOf 与 Object.prototype.isPrototypeOf()

   答：

   * typeof，返回类型的字符串,只有这几个值 "undefined" "number" "string" "boolean" "function" "object",其中null也是"object"
   * instanceof，通过原型链，判断对象是不是某个模板生成的。注意null instanof Object 是false。(xxx === Object.prototype.constructor）
   * Object.prototype.isPrototypeOf() 功能与instanceof类似。但是参数不同o1.isPrototTypeOf(o2)

6. 原型链是什么，存放在哪里？原型链中存放的是什么，继承为什么通过原型链实现？

## 最佳实践

- 括号使用java风格的：

  ```javascript
  return {
    key : value
  };
  // 不要这样
  return // 相当于这里会自动加上分号
  {
    key: value
  };
  ```


- **建议不省略行尾分号。**js会自动添加分号，如果下一行会和上一行连起来就不自动添加了

  ```javascript
  // 等同于 3 * 2 + 10 * (27 / 6)
  3 * 2
  +
  10 * (27 / 6)
  ```

- 避免使用全局变量。如果不得不使用，用大写字母表示变量名，比如`UPPER_CASE`。减少冲突的一个方法是把自己的所有变量和函数全部绑定到一个全局变量中。

  ```javascript
  // 唯一的全局变量MYAPP:把自己的代码全部放入唯一的名字空间MYAPP中，会大大减少全局变量冲突的可能。
  var MYAPP = {};

  // 其他变量:
  MYAPP.name = 'myapp';
  MYAPP.version = 1.0;

  // 其他函数:
  MYAPP.foo = function () {
      return 'foo';
  };
  ```

- 最好把变量声明都放在代码块的头部。为了避免声明”提升”

  ```javascript
  for (var i = 0; i < 10; i++) {
    // ...
  }

  // 写成

  var i;
  for (i = 0; i < 10; i++) {
    // ...
  }
  ```

- 建议使用let代替var定义布局变量，使用const定义常量（ES6特性，Nodejs上使用）

- 关于数据类型

  - 不要使用`new Number()`、`new Boolean()`、`new String()`创建包装对象；
  - 用`parseInt()`或`parseFloat()`来转换任意类型到`number`；
  - 用`String()`来转换任意类型到`string`，或者直接调用某个对象的`toString()`方法；
  - 通常不必把任意类型转换为`boolean`再判断，因为可以直接写`if (myVar) {...}`；
  - `typeof`操作符可以判断出`number`、`boolean`、`string`、`function`和`undefined`；
  - 判断`Array`要使用`Array.isArray(arr)`；
  - 判断`null`请使用`myVar === null`；
  - 判断某个全局变量是否存在用`typeof window.myVar === 'undefined'`；
  - 函数内部判断某个变量是否存在用`typeof myVar === 'undefined'`。

- 建议使用`Object.create(null/prototype)`命令，替代`new`命令。如果不得不使用`new`，为了防止出错，最好在视觉上把构造函数与其他函数区分开来。比如，构造函数的函数名，采用首字母大写（InitialCap），其他函数名一律首字母小写。

  ```javascript
  // 忘了加上new，myObject()内部的this关键字就会指向全局对象，导致所有绑定在this上面的变量，都变成全局变量。
  var o = new myObject();
  ```

- 不要使用“相等”（`==`）运算符，只使用“严格相等”（`===`）运算符。

- 装饰器：替换某个对象中某个方法默认实现，添加自己的功能

  ```javascript
  var count = 0;
  var oldParseInt = parseInt; 
  window.parseInt = function () {
      count += 1;
      return window.apply(null, arguments); // 调用原函数
  };

  // 测试:
  parseInt('10');
  parseInt('20');
  parseInt('30');
  count; // 3
  ```

- 高阶函数的使用

  - map/reduce/filter/sort处理数组

- 闭包使用：封装私有变量、模块化



## 疑问

http://cnodejs.org/topic/5056e007433135ca35034e8d

## code snippet

*  判断一个变量是否声明

   ```javascript
        // 检查a变量是否被声明
        if (a) {...} // 报错
        // 写法1
        if (typeof a === "undefined") { // 注意引号
          // ...
        }

        // 写法2 浏览器环境，所有全局变量都是window对象的属性。
        if (window.a === undefined) { // 注意没有引号
          // ...
        }

        // 写法3
        if ('a' in window) {
          // ...
        }
        // 下面方法有漏洞，a=""是可能声明过
        // if (window.a) {...} // 不报错
        // if (window['a']) {...} // 不报错
   ```

*  base64：编解码url参数用

   ```javascript
        function b64Encode(str) {
          // encodeURIComponent支持中文，但是对url的斜杠也会编码
          return btoa(encodeURIComponent(str));
        }

        function b64Decode(str) {
          return decodeURIComponent(atob(str));
        }

        b64Encode('你好') // "JUU0JUJEJUEwJUU1JUE1JUJE"
        b64Decode('JUU0JUJEJUEwJUU1JUE1JUJE') // "你好"
   ```

*  对象属性遍历

   * 遍历自身对象（可枚举），不含继承

     ```javascript
     // for test
     function Person(name) {
       this.name = name;
     }
     // describe是Person.prototype的属性
     Person.prototype.describe = function () {
       return 'Name: '+this.name;
     };
     var person = new Person('Jane');

     // 方法1
     var allkeys=Object.keys(person);
     for (index in allkeys) {
       console.log(allkeys[index]);
     }
     // 方法2
     for (var key in person) {
       if (person.hasOwnProperty(key)) {
         console.log(key);
       }
     }
     ```

   * 遍历所有对象（可枚举），包括继承

     ```javascript
     for (var key in person) {
       console.log(key);
     }
     ```

   * 遍历所有属性（包括不可枚举），不包括继承

     ```javascript
     Object.getOwnPropertyNames(Date)
     ```

   * 获得对象的所有属性（不管是自身的还是继承的，以及是否可枚举）

     ```javascript
           function inheritedPropertyNames(obj) {
             var props = {};
             while(obj) {
               Object.getOwnPropertyNames(obj).forEach(function(p) {
                 props[p] = true;
               });
               obj = Object.getPrototypeOf(obj);
             }
             return Object.getOwnPropertyNames(props);
           }
     ```

*  模板引擎

   ```javascript
        var str = 'Hello <%= name %>!';

        var o = {
          name: 'Alice'
        };
        function parser(str){
          // 'Hello <%= name %>!'--> '"Hello ", name, "!"'
        }
        function tmpl(str, obj) {
          str = 'var p = [];' +
            'with (obj) {p.push(' + parser(str) + ')};' +
            'return p;'
          var r = (new Function('obj', str))(obj);
          return r.join('');
        }

        tmpl(str, o)
   ```

*  为函数参数设置默认值

   ```javascript
        // 方法一：简单，但是0，false会误判，如果默认值是0，用这个方法不错
        function f(a){
          a = a || 1; //  这句话
          return a;
        }
        // 方法二：更完善一些
        function f(a) {
          (a !== undefined && a !== null) ? a = a : a = 1;
          return a;
        }
   ```

*  类似数组与数组的转化：

   ```javascript
        var args = Array.prototype.slice.call(arguments);

        // or

        var args = [];
        for (var i = 0; i < arguments.length; i++) {
          args.push(arguments[i]);
        }
   ```

*  asset方法：规范化异常抛出

   ```javascript
        // 没必要自己实现
        function assert(expression, message) {
          if (!expression)
            throw {name: 'Assertion Exception', message: message};
        }
        // 建议
        console.assert(typeof myVar != 'undefined', 'myVar is undefined!');
   ```

*  定义构造函数的一个模板代码，避免忘记new引起全局变量污染

   ```javascript
        function Fubar (foo, bar) {
          if (this instanceof Fubar) {
            this._foo = foo;
            this._bar = bar;
          }
          else {
            return new Fubar(foo, bar);
          }
        }
   ```

*  深拷贝对象：1.确保拷贝后的对象，与原对象具有同样的prototype原型对象。2.确保拷贝后的对象，与原对象具有同样的属性。
   ```javascript
        function copyObject(orig) {
          var copy = Object.create(Object.getPrototypeOf(orig));
          copyOwnPropertiesFrom(copy, orig);
          return copy;
        }

        function copyOwnPropertiesFrom(target, source) {
          Object
          .getOwnPropertyNames(source)
          .forEach(function(propKey) {
            var desc = Object.getOwnPropertyDescriptor(source, propKey);
            Object.defineProperty(target, propKey, desc);
          });
          return target;
        }
   ```

*  继承的例子：方法共享，属性私有（除非模拟静态变量）

   ```javascript
       function Shape() {
         this.x = 0;
         this.y = 0;
       }

       Shape.prototype.move = function (x, y) {
         this.x += x;
         this.y += y;
         console.info('Shape moved.');
       };

       function Rectangle() {
         // 第一步：调用父类构造函数，动态构造属性
         Shape.call(this); 
       }
       // 另一种写法
       function Rectangle() {
         this.base = Shape;
         this.base();
       }

       // 第二步:
       // 子类继承父类的方法，继承的核心 对比这两种写法，下面的更好
       // Rectangle.prototype =  new Shape()
       Rectangle.prototype = Object.create(Shape.prototype);
       Rectangle.prototype.constructor = Rectangle;

       var rect = new Rectangle();
   ```



* 封装继承的工具方法

  ```javascript
  // 处理原型链
  function inherits(Child, Parent) {
      // 构造原型
      Child.prototype = Object.create(Parent.prototype)
      // var F = function () {};
      // F.prototype = Parent.prototype;
      // Child.prototype = new F();
      Child.prototype.constructor = Child;
  }
  // 处理属性，别忘了调用call
  ```
