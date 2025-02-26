# views.py
import os
from django.http import HttpResponse
import tempfile
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Document, PreviewRequest
from django.shortcuts import render, redirect, get_object_or_404
from .models import PaymentTerm
import datetime
from docx2pdf import convert


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')

        else:
            messages.error(request, '帐号或者密码错误')
    else:
        form = AuthenticationForm()

    return render(request, 'doc_management/login.html', {'form': form})


def home(request):
    documents = Document.objects.order_by('-uploaded_at')  # 以上传时间降序排序
    paginator = Paginator(documents, 17)
    page_number = request.GET.get('page')
    page_documents = paginator.get_page(page_number)

    for document in page_documents:
        if document.previewrequest_set.filter(requester=request.user, is_approved=True).exists():
            document.is_approved_for_preview = True
            document.is_waiting_approval = False
        elif document.previewrequest_set.filter(requester=request.user, is_approved=False).exists():
            document.is_approved_for_preview = False
            document.is_waiting_approval = True
        else:
            document.is_approved_for_preview = False
            document.is_waiting_approval = False

    return render(request, 'doc_management/home.html', {'page_documents': page_documents})


def upload_document(request):
    existing_payment_terms = PaymentTerm.objects.all()  # 获取所有现有的对应系统

    if request.method == 'POST':
        document = request.FILES.get('document')
        if document:
            document_name = document.name
            uploader = request.user

            if Document.objects.filter(document_name=document_name).exists():
                message = "已上传过相同名称的文件，请修改文件名称后重新上传。"
                return redirect('home')

            # 获取用户输入的新字段值
            contract_category = request.POST.get('contract_category')
            contract_signature_date = request.POST.get('contract_signature_date')
            contract_expiry_date = request.POST.get('contract_expiry_date')
            contract_amount_with_tax = request.POST.get('contract_amount_with_tax')
            contract_amount_without_tax = request.POST.get('contract_amount_without_tax')
            payment_terms_id = request.POST.get('payment_terms')  # 获取用户选择的对应系统的 ID

            # 根据付款条件的 ID 获取对应的 PaymentTerm 对象
            payment_terms = PaymentTerm.objects.get(pk=payment_terms_id)

            doc = Document.objects.create(
                document_type=document.content_type,
                document_name=document_name,
                uploader=uploader,
                document_file=document,
                contract_category=contract_category,
                contract_signature_date=contract_signature_date,
                contract_expiry_date=contract_expiry_date,
                contract_amount_with_tax=contract_amount_with_tax,
                contract_amount_without_tax=contract_amount_without_tax,
                payment_terms=payment_terms  # 保存付款条件对象
            )
            return redirect('upload_document')

    return render(request, 'doc_management/upload_document.html', {'existing_payment_terms': existing_payment_terms})


def batch_upload_document(request):
    if request.method == 'POST':
        documents = request.FILES.getlist('document')

        uploaded_count = 0
        for document in documents:
            try:
                document_name = document.name
                uploader = request.user

                if Document.objects.filter(document_name=document_name).exists():
                    message = f"已上传过相同名称的文件: {document_name}"
                    return render(request, 'doc_management/batch_upload_document.html', {'message': message})

                # 获取用户输入的新字段值
                contract_category = request.POST.get('contract_category')

                Document.objects.create(
                    document_type=document.content_type,
                    document_name=document_name,
                    uploader=uploader,
                    document_file=document,
                    contract_category=contract_category
                )
                uploaded_count += 1
            except Exception as e:
                print(f"上传文件 {document_name} 时出现异常: {str(e)}")

        message = f"成功上传了 {uploaded_count} 个文件。"
        return redirect('home')

    return render(request, 'doc_management/batch_upload_document.html')


def delete_document(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    document_path = document.document_file.path

    try:
        if os.path.exists(document_path):
            os.remove(document_path)
    except:
        pass

    document.delete()

    return redirect('home')


@login_required
def preview_document(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    file_path = document.document_file.path
    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".pdf":
        try:
            with open(file_path, 'rb') as file:
                content = file.read()
                response = HttpResponse(content, content_type='application/pdf')
                response['Content-Disposition'] = f'inline; filename="{document.document_name}"'
                return response
        except FileNotFoundError:
            return HttpResponse("找不到文件。")
    elif extension in [".docx", ".doc", ".xlsx", ".xls", ".pptx", ".ppt"]:
        try:
            # Convert the document to PDF using docx2pdf
            pdf_content = convert_to_pdf(file_path)
            response = HttpResponse(pdf_content, content_type='application/pdf')
            response['Content-Disposition'] = f'inline; filename="{document.document_name}.pdf"'
            return response
        except Exception as e:
            return HttpResponse(f"预览失败：{str(e)}")
    else:
        return HttpResponse("不支持的文件类型。")


def convert_to_pdf(input_file_path):
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_pdf_file:
        temp_pdf_path = temp_pdf_file.name
    convert(input_file_path, temp_pdf_path)  # Use docx2pdf to convert
    with open(temp_pdf_path, 'rb') as pdf_file:
        pdf_content = pdf_file.read()
    os.remove(temp_pdf_path)
    return pdf_content


def request_preview(request, document_id):
    document = get_object_or_404(Document, id=document_id)

    if request.user != document.uploader and not PreviewRequest.objects.filter(requester=request.user,
                                                                               document=document).exists():
        preview_request = PreviewRequest.objects.create(
            requester=request.user,
            document=document,
            approved_by=None,
            is_approved=False,
            created_at=timezone.now(),
        )

        document.requested_for_preview = True
        document.save()

    return redirect('home')


def edit_document(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    existing_payment_terms = PaymentTerm.objects.all()

    if request.method == 'POST':
        contract_category = request.POST.get('contract_category')
        contract_signature_date = request.POST.get('contract_signature_date')
        contract_expiry_date = request.POST.get('contract_expiry_date')
        contract_amount_with_tax = request.POST.get('contract_amount_with_tax')
        contract_amount_without_tax = request.POST.get('contract_amount_without_tax')
        payment_terms_id = request.POST.get('payment_terms')

        payment_terms = PaymentTerm.objects.get(pk=payment_terms_id)

        document.contract_category = contract_category
        document.contract_signature_date = contract_signature_date
        document.contract_expiry_date = contract_expiry_date
        document.contract_amount_with_tax = contract_amount_with_tax
        document.contract_amount_without_tax = contract_amount_without_tax
        document.payment_terms = payment_terms
        document.save()

        return redirect('home')
    else:
        # 如果日期字段为None，则设置一个适当的默认值
        if document.contract_signature_date is None:
            document.contract_signature_date = datetime.date.today()

        if document.contract_expiry_date is None:
            document.contract_expiry_date = datetime.date.today()

        return render(request, 'doc_management/edit_document.html', {
            'document': document,
            'existing_payment_terms': existing_payment_terms
        })


def payment_terms_list(request):
    payment_terms = PaymentTerm.objects.all()
    return render(request, 'doc_management/payment_terms_list.html', {'payment_terms': payment_terms})


def add_payment_term(request):
    if request.method == 'POST':
        abbreviation = request.POST.get('abbreviation')
        description = request.POST.get('description')
        PaymentTerm.objects.create(abbreviation=abbreviation, description=description)
        return redirect('payment_terms_list')
    return render(request, 'doc_management/add_payment_term.html')


def edit_payment_term(request, payment_term_id):
    payment_term = get_object_or_404(PaymentTerm, id=payment_term_id)
    if request.method == 'POST':
        abbreviation = request.POST.get('abbreviation')
        description = request.POST.get('description')
        payment_term.abbreviation = abbreviation
        payment_term.description = description
        payment_term.save()
        return redirect('payment_terms_list')
    return render(request, 'doc_management/edit_payment_term.html', {'payment_term': payment_term})


def delete_payment_term(request, payment_term_id):
    payment_term = get_object_or_404(PaymentTerm, id=payment_term_id)
    if request.method == 'POST':
        payment_term.delete()
        return redirect('payment_terms_list')
    return render(request, 'doc_management/delete_payment_term.html', {'payment_term': payment_term})


