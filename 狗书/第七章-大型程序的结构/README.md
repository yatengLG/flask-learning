# 第七章 大型程序的结构

尽管在单一脚本中编写小型 Web 程序很方便，但这种方法并不能广泛使用。程序变复杂后，使用单个大型源码文件会导致很多问题.

在本章，我们将介绍一种使用包和模块组织大型程序的方式。

## 7.1 项目结构

Flask程序的基本结构如下所示：

```text
|- flasky
    |-app 
        |-templates
        |-static
        |-main
            |-__init__.py
            |-errors.py
            |-forms.py
            |-views.py
        |-__init__.py
        |-email.py
        |-models.py
    |-migrations/
    |-tests/
        |-__init__.py
        |-test*.py
    |-venv/
    |-requirements.txt
    |-config.py
    |-manage.py
```

有四个顶级文件夹：
* Falsk程序一般保存在app文件夹下
* migrations包含数据库迁移脚本
* tests文件夹中保存单元测试
* venv中包含了python环境

* manage.py用于启动程序以及其他的程序任务。
* requirements.txt 依赖项
* config.py配置

