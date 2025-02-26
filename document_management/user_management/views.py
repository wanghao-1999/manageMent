from django.core.paginator import Paginator
from django.shortcuts import render
from .forms import DepartmentForm  # 导入部门表单
from .forms import UserForm
from django.shortcuts import get_object_or_404, redirect
from .models import CustomUser
from .forms import EditUserForm
from django.contrib.auth.hashers import make_password
from .models import Department


def user_list(request):
    users = CustomUser.objects.order_by('id')  # 以id字段升序排序
    paginator = Paginator(users, 10)  # 每页显示 10 条记录
    page_number = request.GET.get('page')
    page_users = paginator.get_page(page_number)

    if request.method == 'POST':
        # 如果是 POST 请求，可能是新增用户后刷新页面，重新查询数据库
        page_users = paginator.get_page(page_number)

    return render(request, 'user_management/user_list.html', {'page_users': page_users})


# 部门设置添加视图函数
def department_settings(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            # 处理表单提交逻辑，保存部门信息等
            form.save()
            return redirect('department_list')  # 重定向到用户列表页面
    else:
        form = DepartmentForm()

    return render(request, 'user_management/department_settings.html', {'form': form})


def department_list(request):
    departments = Department.objects.all()
    return render(request, 'user_management/department_list.html', {'departments': departments})


def delete_department(request, department_id):
    department = get_object_or_404(Department, pk=department_id)
    department.delete()
    return redirect('department_list')


# 添加用户视图函数
def add_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            # 查询更新后的用户列表并传递给用户列表页面
            users = CustomUser.objects.order_by('id')
            paginator = Paginator(users, 10)
            page_number = request.GET.get('page')
            page_users = paginator.get_page(page_number)
            return redirect('add_user')  # 重定向到用户列表页面
            return render(request, 'user_management/user_list.html', {'page_users': page_users})
    else:
        form = UserForm()
    return render(request, 'user_management/add_user.html', {'form': form})


# 删除用户视图函数
def delete_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.delete()
    return redirect('user_list')


# 编辑用户视图函数
def edit_user(request, user_id):
    user = CustomUser.objects.get(pk=user_id)

    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=user)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            if new_password:
                user.password = make_password(new_password)  # Hash the new password
            form.save()  # Save the form data to the user model
            return redirect('user_list')
    else:
        form = EditUserForm(instance=user)

    return render(request, 'user_management/edit_user.html', {'form': form, 'user': user})


