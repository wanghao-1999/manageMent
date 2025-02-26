def user_login(request):
    if request.method == 'POST':  # 检查请求方法是否为POST，表示用户提交了登录表单
        form = AuthenticationForm(request, request.POST)  # 创建一个身份验证表单实例，传入请求和POST数据
        if form.is_valid():  # 验证表单数据的合法性
            username = form.cleaned_data.get('username')  # 获取用户名
            password = form.cleaned_data.get('password')  # 获取密码
            user = authenticate(username=username, password=password)  # 调用authenticate函数进行用户身份验证
            if user is not None:  # 如果用户验证成功
                login(request, user)  # 使用login函数将用户登录状态保存在会话中
                return redirect('home')  # 重定向到主页（'home'是URL的名称）
            else:
                # 如果用户验证不成功，根据表单中的错误信息判断是帐号错误还是密码错误
                error_message = '帐号不存在' if not form.errors.get('username') else '密码错误'
                messages.error(request, error_message)  # 添加错误消息到消息队列，用于显示给用户
                return render(request, 'doc_management/login.html', {'form': form})
    else:
        form = AuthenticationForm()  # 创建一个空的身份验证表单实例

    return render(request, 'doc_management/login.html', {'form': form})
