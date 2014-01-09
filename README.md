btc
===

A Navigation Site For BTC

### [FreeBTC123](http://freebtc123.com/)（[HereBTC](http://herebtc.com/)）

* 免费获取比特币网址导航，同时也囊括比特币、山寨币网址导航，后续也会推出其他比特币相关服务
* 执行命令运行服务

  >执行： python manage.py syncdb （PS： 请按照提示设置登录后台管理界面的帐户和密码）
  
  >执行： python manage.py collectstatic
  
  >执行： python manage.py runserver 0.0.0.0:80

* 本机通过IP访问 或者 通过127.0.0.1访问，IP/admin 或者 127.0.0.1/admin访问后台管理界面
* 如果线上运行的话，推荐使用[Nginx](http://nginx.org/)或者使用[Apache](http://httpd.apache.org/)等HTTP服务器 + [uwsgi](https://uwsgi.readthedocs.org/en/latest/tutorials/Django_and_nginx.html)

### TODO:

* 前端页面优化
* 表格按列排序        √
* 取消赞和收藏        √
* 密码修改/找回
* 比特币相关服务
