from django.db import models

# 用户表
class User(models.Model):
    userid = models.AutoField(primary_key=True,max_length=9,verbose_name='用户id')
    password = models.CharField(max_length=20,verbose_name='用户密码')
    username = models.CharField(max_length=18,unique=True,verbose_name='用户名')
    role = models.IntegerField(
    	choices=(
    		(0,'禁言用户'),
    		(1,'普通用户'),
            (2, '管理员用户'),
    	),
        default='0',
        verbose_name='用户权限'
    )

# 文章表
class Article(models.Model):
    articleid = models.AutoField(primary_key=True, max_length=12, verbose_name='文章id')
    title = models.CharField(max_length=20, verbose_name='文章标题')
    date = models.DateTimeField(auto_now_add=True,verbose_name='文章添加时间')
    userid = models.IntegerField(verbose_name='文章用户id')
    abstract = models.CharField(max_length=40, verbose_name='文章简介',default='尚无简介')
    categoryname = models.CharField(max_length=20, verbose_name='文章标签')
    a_content = models.CharField(max_length=20000, verbose_name='文章内容',default='尚无内容')
    a_state = models.IntegerField(
    	choices=(
    		(1,'正常'),
    		(0,'删除'),
    	),
        default='1',
        verbose_name='文章状态'
    )
    readnum = models.IntegerField(default='0',verbose_name='文章阅读量')

# 评论表
class Comment(models.Model):
    commentid = models.AutoField(primary_key=True, max_length=12, verbose_name='评论id')
    userid = models.IntegerField(verbose_name='评论用户id')
    date = models.DateTimeField(auto_now_add=True,verbose_name='评论添加时间')
    articleid = models.IntegerField(verbose_name='评论文章id')
    c_content = models.CharField(max_length=200, verbose_name='评论内容',default='尚无内容')
    c_state = models.IntegerField(
        choices=(
            (1, '正常'),
            (0, '删除'),
        ),
        default='1',
        verbose_name='评论状态'
    )

# 标签表
class Category(models.Model):
    categoryid = models.AutoField(primary_key=True, max_length=2, verbose_name='标签id')
    categoryname = models.CharField(max_length=18,unique=True,verbose_name='标签名')
    state = models.IntegerField(
        choices=(
            (1, '正常'),
            (0, '删除'),
        ),
        default='1',
        verbose_name='标签状态'
    )
