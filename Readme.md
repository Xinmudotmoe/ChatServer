# 仿[A站](http://www.acfun.cn)的AC水聊版。
因为无需过高的并发，并且为减少连接数据库造成的大量IO访问（实际是减少sqlite被锁而导致访问进程堆积进而引发的停滞），而使用内部HttpServer替换Apache。~~实际上应该使用MySQL而不是sqlite了~~
