1. 运行Django环境，执行数据库迁移，注意在setting中配置数据库

   ```
   $ python manage.py makemigrations blog
   $ python manage.py migrate
   ```

2. 在数据库USER表中手动创建管理员用户，记得设置权限（role）为2

3. 留言过滤负面评论会被过滤

4. 运行开发服务器

   ```
   $ python manage.py runserver
   ```

   

   
