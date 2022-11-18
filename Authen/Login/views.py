from django.shortcuts import render,HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,decorators,logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from .forms import PostForm,DocumentForm
from .models import Document
from django.db import connection
import pandas as pd
import csv
import json
import datetime
from datetime import date, timedelta
from django.core.paginator import Paginator
# Create your views here.
class IndexClass(LoginRequiredMixin ,View):
    login_url='login'                                                                                                            
    def get(self,  request):
            date_object = datetime.date.today()
            print(date_object)
            ngay = ''.join(char for char in str(date_object) if char.isalnum())
            print(ngay)
            thang = str(ngay)[0:6]
            print(thang)
            month=ngay[0:6]
            sqla="SELECT * FROM simbox_log where start_date >= '"+str(date_object)+"'"
            df = pd.read_sql(sqla,connection)
            df['start_date'] = df['start_date'].astype('str')
            df['answer_date'] = df['answer_date'].astype('str')
            json_records = df.reset_index().to_json(orient ='records')
            data = []
            data = json.loads(json_records)
            paginator = Paginator(data, 25)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            # context = {'d': data,'startdate':startdate,'enddate':str(enddate),'phone':phone}
            return render(request,'Login/index.html',{'page_obj': page_obj,'startdate':str(date_object),'enddate':str(date_object)})
class forgotmk(View):
    def get(self,  request):
        return render(request,'Login/forgotmk.html')
    def post(self,  request):
        try :
            email = request.POST.get('email')
            cursor = connection.cursor()
            sqlcheckemail = "SELECT count(*) 'sl' FROM Login_user where email= '"+email+"'"
            df = pd.read_sql(sqlcheckemail,connection)
            sl = df.iloc[0,0]
            print(sl)
            if sl == 0:
                messages.success(request, 'Email không tồn tại !!!')
                return redirect('forgotmk')
            else :
                sqlreset = "update Login_user set password ='pbkdf2_sha256$120000$trSM0EIAz8nr$dxcGr9KOM3qVwDyEgNt30AveoCH4TJGiXY+3aK3dvGk=' where email = '"+email+"'"
                cursor.execute(sqlreset)
                messages.success(request, 'Đã reser mật khẩu về : 123456 !!!')
                return redirect('login')
        except:
            return HttpResponse('Lỗi')
def logout_request(request):
    logout(request)
    # messages.info(request, "Logged out successfully!")
    return redirect('login')
class LoginClass(View):
    def get(self,  request):
        return render(request,'Login/login.html')
    def post(self,  request):
        username = request.POST.get('uname')
        password = request.POST.get('psw')
        my_user = authenticate(username=username,password=password)
        if my_user is None :
            messages.success(request, 'Đăng nhập thất bại ,kiểm tra lại user và mật khẩu')
            return redirect('login')
        login(request,my_user)
        return redirect('IndexClass')
class ViewUser(LoginRequiredMixin ,View):
    login_url='login'
    def get(self,  request):
        return HttpResponse('OK')
@decorators.login_required(login_url='login')
def ViewProduct(View):
    return HttpResponse('OK')

class Register(View):
    def get(self,  request):
        return render(request,'Login/register.html')
    def post(self,  request):
        username = request.POST.get('uname')
        password = request.POST.get('psw')
        email = request.POST.get('email')
        hash_password = make_password(password)
        print(hash_password)
        try:
            sqlcheckemail = "SELECT count(*) 'sl' FROM Login_user where email= '"+email+"'"
            df = pd.read_sql(sqlcheckemail,connections['default'])
            sl = df.iloc[0,0]
            print(sl)
            if str(sl) == "0" :
                sql="insert into Login_user(password,is_superuser,username,first_name,last_name,email,is_staff,is_active,date_joined,age,gender,address) value ('"+hash_password+"','0','"+username+"','','','"+email+"','1','1',now(),'0','0','')"
                cursor = connections['default'].cursor()
                cursor.execute(sql)       
                messages.success(request, 'Tạo tài khoản thành công !!!')
                return redirect('login')
            else :
                messages.success(request, 'Email đã tồn tại !!!')
                return redirect('register')
        except:
            messages.success(request, 'Username đã tồn tại !!!')
            return redirect('register')
def download_csv(request):
    startdate = request.POST.get('startdate')
    print(startdate)
    enddate = request.POST.get('enddate')
    enddates =str(enddate)+" 23:59:59"
    month = str(startdate)[0:7].replace("-","")
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="{filename}.csv"'.format(filename='cdr')
    writer = csv.writer(response)
    sqla="select * from simbox_log where start_date >= '"+str(startdate)+"' and start_date < '"+str(enddates)+"'"
    df = pd.read_sql(sqla,connection)
    df['start_date'] = df['start_date'].astype('str')
    df['answer_date'] = df['answer_date'].astype('str')
    writer.writerow([column for column in df.columns])
    writer.writerows(df.values.tolist())
    return response
def csv_search(request):
    if request.method == 'POST':
        startdate = request.POST.get('startdate')
        print(startdate)
        enddate = request.POST.get('enddate')
    else :
        startdate = request.GET.get('startdate')
        print(startdate)
        enddate = request.GET.get('enddate')
    enddates =str(enddate)+" 23:59:59"
    month = str(startdate)[0:7].replace("-","")
    sqla="select * from simbox_log where start_date >= '"+str(startdate)+"' and start_date < '"+str(enddates)+"'"
    df = pd.read_sql(sqla,connection)
    df['start_date'] = df['start_date'].astype('str')
    df['answer_date'] = df['answer_date'].astype('str')
    json_records = df.reset_index().to_json(orient ='records')
    data = []
    data = json.loads(json_records)
    paginator = Paginator(data, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    print(page_obj)
    context = {'page_obj': page_obj,'startdate':startdate,'enddate':str(enddate)}
    return render(request,'Login/cdr.html',context)


