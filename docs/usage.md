# 直接使用

Windows 11 下双击即可运行。_**适合所有人**_

# 源码编译

下载[C++源码](https://github.com/Pfolg/WindowsWaterMark/tree/main/src/C%2B%2B)，理论上在有Qt环境的系统可以直接编译运行。_**不推荐**_

下载[Python源码](https://github.com/Pfolg/WindowsWaterMark/tree/main/src/Python)，需要Python环境，需要安装PySide6库。_**不推荐小白**_

# 配置

程序第一次运行后会生成一个`.json`文件，里面有一些配置信息，可以根据自己的需要进行修改：

```json
{
    "line1": "激活 Windows",
    "line2": "转到\"设置\"以激活 Windows。",
    "port": 20520,
    "ratio": {
        "down": 1,
        "left": 20,
        "right": 1,
        "up": 8
    }
}
```
+ `line1`和`line2`是水印文字 _(用半角引号包裹)_，可以修改为自己喜欢的文字。
+ `port`_(整数)_ 是程序运行的端口，默认是`20520`，可以修改为自己喜欢的端口。（**端口占用时可以修改为其他端口**）
+ `ratio`_(整数)_ 是水印文字的位置比例，可以修改`down`、`left`、`right`、`up`的值来调整水印文字的位置。

> 为什么有端口配置？
> 
> 程序运行时需要监听一个端口，防止其他程序占用这个端口，所以需要配置端口。
>
> 如果您**不信任此程序请不要运行！**

如果您想更加个性化可以使用Python源码进行修改。

大佬随意（C++、Python）。

# 关闭

您需要**在任务管理器中关闭程序**，按下`Alt+F4`无效。

![](..\assets\image1.png)

关闭程序后，水印文字会自动消失。

