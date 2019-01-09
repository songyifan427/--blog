from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import User,Article,Comment,Category

def index(request):
    cate = Category.objects.filter(state=1)
    article = Article.objects.filter(a_state=1).order_by('-articleid')[:5]
    for i in range(len(article)):
        username = User.objects.get(userid=article[i].userid).username
        article[i].username = username
        commentnum = Comment.objects.filter(articleid=article[i].articleid).count
        article[i].commentnum=commentnum
    userid = request.session.get('userid','')
    username = request.session.get('username','')
    role=request.session.get('role','')
    return render(request,'index/index.html',{'cate':cate,'article':article,'userid':userid,'username':username,'role':role})

def login(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        url = request.POST['url']
        if not username or not password:
            return redirect(url)
        isLogin = User.objects.filter(username=username,password=password).first()
        if isLogin:
            request.session['userid'] = isLogin.userid
            request.session['username'] = isLogin.username
            request.session['role'] = isLogin.role
        return redirect(url)
    else:
        url = request.POST['url']
        return redirect(url)

def logout(request):
    try:
        del request.session['userid']
        del request.session['username']
        del request.session['role']
    except KeyError:
        pass
    return redirect('/')

def register(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        repassword = request.POST['repassword']
        url = request.POST['url']
        if password != repassword or not username or not password:
            return redirect(url)
        if User.objects.filter(username=username):
            return redirect(url)
        User(username=username, password=password).save()
        return redirect(url)

def list(request,categoryname):
    cate = Category.objects.filter(state=1)
    article = Article.objects.filter(categoryname=categoryname).exclude(a_state=0).order_by('-articleid')[:5]
    for i in range(len(article)):
        username = User.objects.get(userid=article[i].userid).username
        article[i].username = username
        commentnum = Comment.objects.filter(articleid=article[i].articleid).count
        article[i].commentnum = commentnum
    userid = request.session.get('userid', '')
    username = request.session.get('username', '')
    role = request.session.get('role', '')
    return render(request, 'index/list.html',{'cate': cate, 'article': article, 'userid': userid, 'username': username,
                                              'role': role,'categoryname':categoryname})

def article(request,articleid):
    cate = Category.objects.all()
    article = Article.objects.filter(articleid=articleid).first()
    if not article or article.a_state==0:
        return redirect('/')
    article.readnum+=1
    article.save()
    comment = Comment.objects.filter(articleid=articleid).exclude(c_state=0)
    for i in range(len(comment)):
        comment[i].username = User.objects.get(userid=comment[i].userid).username
    userid = request.session.get('userid', '')
    username = request.session.get('username', '')
    role = request.session.get('role', '')
    return render(request, 'index/article.html',{'cate': cate, 'article': article, 'userid': userid,'comment': comment ,
                                                 'username': username, 'role': role})

def comment(request,articleid):
    if request.POST:
        c_content = request.POST['c_content']
        userid = request.session.get('userid', '')
        Comment(userid=userid,articleid=articleid, c_content=c_content).save()
        url = request.POST['url']
        return redirect(url)

def admin(request):
    role=request.session.get('role','')
    if role==2:
        userid = request.session.get('userid', '')
        username = request.session.get('username', '')
        user = User.objects.all()
        article = Article.objects.all()
        for i in range(len(article)):
            article[i].username = User.objects.get(userid=article[i].userid).username
        category = Category.objects.all()
        return render(request,'index/admin.html',{'userid':userid,'username':username,'role':role,'user':user,
                                                  'article':article,'category':category})
    return redirect('/')

def adminsetting(request):
    if request.POST:
        Category(categoryname=request.POST['categoryname']).save()
        return redirect('/admin/')
    elif request.GET:
        family = request.GET['family']
        id = int(request.GET['attr'])
        value = int(request.GET['value'])
        if family=='user':
            obj = User.objects.get(userid=id)
            obj.role=value
            obj.save()
        elif family=='article':
            obj = Article.objects.get(articleid=id)
            obj.a_state = value
            obj.save()
        elif family=='cate':
            obj = Category.objects.get(categoryid=id)
            obj.state = value
            obj.save()
        return HttpResponse('done')

def homepage(request,userName):
    username = request.session.get('username', '')
    if username and username==userName:
        userid = request.session.get('userid', '')
        role = request.session.get('role', '')
        article = Article.objects.filter(userid=userid).exclude(a_state=0).order_by('-articleid')
        for i in range(len(article)):
            username = User.objects.get(userid=article[i].userid).username
            article[i].username = username
            commentnum = Comment.objects.filter(articleid=article[i].articleid).count
            article[i].commentnum = commentnum
        return render(request, 'index/homepage.html',{'userid':userid,'username':username,'role':role,'article':article})
    return redirect('/')

def addarticle(request,userName):
    username = request.session.get('username', '')
    if username and username==userName:
        role = request.session.get('role', '')
        if role == 0:
            return redirect('/'+username)
        userid = request.session.get('userid', '')
        if request.POST:
            title = request.POST['title']
            abstract = request.POST['abstract']
            a_content = request.POST['a_content']
            categoryname = request.POST['categoryname']
            if title == '' or a_content == '':
                category = Category.objects.filter(state=1)
                return render(request, 'index/write.html',{'userid': userid, 'username': username, 'role': role,
                                                           'category': category,'categoryname':categoryname,'title':title,
                                                           'abstract':abstract,'a_content':a_content,'isDone':'no'})
            Article(title=title,userid=userid,abstract=abstract,categoryname=categoryname,a_content=a_content).save()
            return redirect('/' + username)
        else:
            category = Category.objects.filter(state=1)
            return render(request, 'index/write.html',{'userid':userid,'username':username,'role':role,'category':category})
    return redirect('/')

def updarticle(request,userName,articleid):
    username = request.session.get('username', '')
    if username and username == userName:
        role = request.session.get('role', '')
        if role == 0:
            return redirect('/' + username)
        userid = request.session.get('userid', '')
        if request.POST:
            title = request.POST['title']
            abstract = request.POST['abstract']
            a_content = request.POST['a_content']
            categoryname = request.POST['categoryname']
            if title == '' or a_content == '':
                category = Category.objects.filter(state=1)
                return render(request, 'index/write.html',
                              {'userid': userid, 'username': username, 'role': role, 'category': category,
                               'categoryname': categoryname, 'title': title, 'abstract': abstract,
                               'a_content': a_content, 'isDone': 'no'})
            obj = Article.objects.get(articleid=articleid)
            obj.title = title
            obj.abstract = abstract
            obj.categoryname = categoryname
            obj.a_content = a_content
            obj.save()
            return redirect('/' + username)
        else:
            article = Article.objects.filter(articleid=articleid).first()
            if not article or article.a_state == 0:
                return redirect('/' + username)
            category = Category.objects.filter(state=1)
            return render(request, 'index/write.html',
                          {'userid': userid, 'username': username, 'role': role, 'category': category,'article':article})
    return redirect('/')

def delarticle(request,userName,articleid):
    username = request.session.get('username', '')
    if username and username == userName:
        article = Article.objects.filter(articleid=articleid).first()
        if not article:
            return redirect('/' + username)
        article.a_state = 0
        article.save()
        return redirect('/' + username)
    return redirect('/')

