# TimerTask
定时任务系统(暂时缺个任务监控)

0. 支持按照时间间隔，日期，时，分，星期组合定时规则

1. 动态新增定时任务
将新增的任务模块名称和定时规则添加到 tasks.py 中，系统会读取新增的任务模块名称，并加载该任务

2. 动态修改定时规则
修改 tasks.py 中任务的定时规则，系统会读取新的规则然后在下次执行的时候生效

3. 动态修改定时任务
通过 view 命令查询任务模块对应Id，然后 stop Id 暂停该任务， 然后 start Id 重新加载启动该任务
如果该模块引用了其他修改的模块，需要重写父类的 reload_modules 方法，将引用的模块重新加载，否则不会生效

4. 动态生成日志配置
根据任务名称，动态生成日志配置

5. 查看任务状态
在命令窗口输入：view 
 
 `==================================================================================================== `
 
 ` TaskId  Running      Stop          Start time               Task name `
 
 `---------------------------------------------------------------------------------------------------- `
 
 `-   0    False        False     2017-07-25 17:44:53          task_test1 `
 
 `-   1    False        True      2017-07-25 17:45:01          task_test2 `
 
 `-   2    False        False     2017-07-25 17:45:07          task_test3 `
 
 `==================================================================================================== `
 
TaskId：任务对应 Id，用来启动或者暂停
Running：该任务当前是否正在运行
Stop： 该任务是否暂停
Start time：该次（正在运行时）/下次任务运行的时间
Task name：任务模块名称·
 
6. 暂停任务
在命令窗口输入：stop TaskId
当该任务正在运行时，会在任务结束后暂停

7. 启动任务
在命令窗口输入：start TaskId

8. 所有定时任务必须继承 timer.timer.Timer 类

9. 启动任务 python manager.py


