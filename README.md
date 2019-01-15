1. 运行Django环境，执行数据库迁移

   ```
   $ python manage.py makemigrations blog
   $ python manage.py migrate
   ```

2. 在数据库USER表中手动创建管理员用户，记得设置权限（role）为2

3. 注意留言过滤，不要说脏话

4. 富文本编辑和分页懒得写了

5. 运行开发服务器

   ```
   $ python manage.py runserver
   ```

   

   