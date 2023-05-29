from django.shortcuts import render
from django.http import HttpResponse
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from customers.models import Customers
from customers.serializers import CustomerSerializer
from customers.serializers import CustomersBulkSerializer
from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view
from django.contrib.auth import logout


import logging
logger = logging.getLogger("django")

@api_view(['POST'])
def logout_view(request):
    logout(request)
    return JsonResponse({'message': 'Logout successful'})


# Login
from django.http import HttpRequest
from django.contrib.auth import authenticate, login
from rest_framework.decorators import api_view
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie, requires_csrf_token
from django.core.exceptions import PermissionDenied
import requests
from django.core.exceptions import SuspiciousOperation

# @csrf_protect
# @require_POST
# @api_view(['POST'])
# def check_sessions(request):
#     if request.method == 'POST':
#         csrf_token = request.META.get('HTTP_X_CSRFTOKEN')
#         print("MY CSRF TOKEN", csrf_token)
#         if not csrf_token :
#             print("The token is missing")
#             raise PermissionDenied("CSRF token missing")    
#         elif csrf_token is None or csrf_token == 'null':
#             print("The token is missing!!!")
#             raise PermissionDenied("CSRF token missing")

#         if csrf_token != request.META.get('HTTP_X_CSRFTOKEN'):
#             raise PermissionDenied("CSRF token invalid")

#         return JsonResponse({'message': 'CSRF token is valid', 'csrftoken': csrf_token})
from rest_framework_simplejwt.authentication import JWTAuthentication


@api_view(['GET'])
def my_protected_view(request):
    jwt_authentication = JWTAuthentication()
    try:
        user, _ = jwt_authentication.authenticate(request)
        # print(request.META.get())
        if user is not None:
            # User is logged in
            return JsonResponse({'loggedin': True, 'message': 'User is logged in'})
        else:
            # User is not logged in
            
            return JsonResponse({'loggedin': False, 'message': 'User is not logged in'})
    except Exception:
        # Error occurred during authentication
        return JsonResponse({'loggedin': False, 'message': 'Authentication error'})

from rest_framework.permissions import BasePermission


from rest_framework_simplejwt.tokens import RefreshToken
####LOGIN####
@require_POST
@api_view(['POST'])
def login_view(request):
    # if request.method == 'POST':
    username= request.POST['username']
    password= request.POST['password']
    user = authenticate(request, username=username, password=password) 
    if user is not None:
        login(request, user)
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        print("Access",access_token)
        return JsonResponse({'message': 'Login successful','access_token': access_token})
    else:
        return JsonResponse({'message': 'Invalid credentials'}, status=401)


from django.middleware.csrf import CsrfViewMiddleware
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

#Finding All Customers, Post Single Customer
@authentication_classes([JWTAuthentication,SessionAuthentication, BasicAuthentication])  # Apply JWT authentication
@permission_classes([IsAuthenticated])
@api_view(['GET','POST'])
def customer_list(request):
    if request.method == 'GET':
        try:
            print("Hello beeeeps passed")
            customers = Customers.objects.all()
            id = request.GET.get('index', None)
            if id is not None:
                customers = customers.filter(id__icontains=id)
            customers_serializer = CustomerSerializer(customers, many=True)
            return JsonResponse(customers_serializer.data, safe=False) # 'safe=False' for objects serialization
        except Exception as e:
         response= JsonResponse({"message":"Unable to retrieve customers table."})
         response.status_code=500 #for internal server error
         return response
    if request.method == 'POST': #Post Single Customer
        try:
            user = request.user
            # jwt_authentication = JWTAuthentication()
            # user, _ = jwt_authentication.authenticate(request)
            print("going into jwt!!")
            if user is not None:
            # User is logged in
                print("user is logged in, can perform operations")
                try:
                    logger.info("POST API has been executed")
                    customers_data = JSONParser().parse(request)
                    customers_serializer = CustomersBulkSerializer(data=customers_data)
                    if customers_serializer.is_valid():
                        customers_serializer.save()
                        return JsonResponse(customers_serializer.data, status=status.HTTP_201_CREATED) 
                    else:
                        print(customers_serializer)
                        return JsonResponse(customers_serializer.errors, status=400) 
                except Exception as e:
                    print(e)
                    return JsonResponse({"message":"Registration of Customer failed.", "theerror":e.args}, status = 400)
            else:
                return JsonResponse({'loggedin': False, 'message': 'User is not logged in!'},status=401)
        except Exception as e:
        # Error occurred during authentication
            return JsonResponse({'loggedin': False, 'message': 'Authentication error', 'theerror':e.args},status=401)
    
    
#Get for a Single Customer
@api_view(['GET'])
def customer_getbyid(request, pk):
    # Find Single Customer by ID
    try: 
        customer = Customers.objects.filter(pk=pk)
        if not customer:
            customer = Customers.objects.get(pk=pk)
    except Customers.DoesNotExist: 
        return JsonResponse({'message':'Customer with the company does not exist'}, status=status.HTTP_404_NOT_FOUND) 
    if request.method == 'GET': 
        customer_serializer = CustomerSerializer(customer, many=True) 
        return JsonResponse(customer_serializer.data, safe=False) 
    return JsonResponse(customer_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 



# Put/Delete for a Single Customer
@api_view(['PUT', 'DELETE'])
def customer_detail(request, pk):
    # Find Single Customer by ID first
      try: 
        print(pk)
        customer = Customers.objects.get(pk=pk) 
      except Customers.DoesNotExist: 
        return JsonResponse({'message': 'The customer does not exist'}, status=status.HTTP_404_NOT_FOUND) 
    #Put Request to Update a Tutorial Works
      if request.method == 'PUT': 
        logger.info("Update by ID has been executed")
        customer_data = JSONParser().parse(request) 
        customer_serializer = CustomerSerializer(customer, data=customer_data) 
        print(customer_serializer)
        if customer_serializer.is_valid(): 
            customer_serializer.save() 
            return JsonResponse(customer_serializer.data, safe=False) 
        return JsonResponse(customer_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    #Delete Single Customer
      elif request.method == 'DELETE':
        logger.info("Delete by ID has been executed") 
        customer.delete() 
        return JsonResponse({'message': 'Customers Details was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
      else:
        return JsonResponse(customer_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
   
   
#Delete All in Table and Reset PK Number
@api_view(['GET'])
def customers_deleteall(request):
    from django.core.management.color import no_style
    from django.db import connection
    from customers.models import Customers
    logger.info("Delete All has been executed")
    customers = Customers.objects.all()
    if not customers: #if queryset has no results
        return JsonResponse({'message': 'Table is empty.'}, status=status.HTTP_400_BAD_REQUEST)
    else: #queryset has results
        Customers.objects.all().delete()
        sequence_sql = connection.ops.sequence_reset_sql(no_style(), [Customers])
        with connection.cursor() as cursor:
            for sql in sequence_sql:
                cursor.execute(sql)
        return JsonResponse({'message': 'Customers are deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


#Finding a Customer by Company Name
@api_view(['GET'])
def customer_company(request, company):
    try: 
        mycompany = Customers.objects.filter(company=company)
        if not mycompany:
            mycompany = Customers.objects.get(company=company)
    except Customers.DoesNotExist: 
        return JsonResponse({'message': 'Customer with the company does not exist'}, status=status.HTTP_404_NOT_FOUND) 
    if request.method == 'GET': 
        customer_serializer = CustomerSerializer(mycompany, many=True) 
        return JsonResponse(customer_serializer.data, safe=False) 
    
    
#Find all Companies Exclude Empty
@api_view(['GET'])
def company_list(request):
    if request.method == 'GET':
        companies = Customers.objects.all().values('company')
        companies=companies.exclude(company__exact='')
    customers_serializer = CustomerSerializer(companies, many=True)
    return JsonResponse(customers_serializer.data, safe=False)


#For Import of CSV into table
import time
import numpy as np
import pandas as pd
@api_view(['POST'])
def customer_listcsv(request):
    file = request.FILES['file']
    csvname= request.POST['csvname']
    start_time = time.time()
    try:
        colnames=['Customer Id', 'First Name', 'Last Name', 'Company', 'City','Country','Phone 1','Phone 2','Email','Subscription Date','Website','Index'] 
        data=pd.read_csv(file,sep=',', usecols=colnames)
    except pd.errors.EmptyDataError: #if file is not chosen its empty
        return JsonResponse({'message': 'Error: Either no file was uploaded or there is an error with system receiving the file. Check the headers and columns.'}, safe=False,  status=400) 
    data.rename({'Customer Id': 'customerid', 'First Name': 'firstname', 'Last Name': 'lastname', 'Company': 'company','City': 'city', 'Country':'country', 'Phone 1':'phone1', 'Phone 2':'phone2','Email':'email', 'Subscription Date': 'subscriptiondate', 'Website':'website', 'Index':'filename_index' }, axis=1, inplace=True)
    #create filename_index
    thecsvname= csvname[:-4]
    data['filename_index'] = thecsvname + '_' + data['filename_index'].astype(str)
    #Do cleaning of PH first before duplicates checking
    dfa=data['phone1'].str.replace('.','')
    dfa=dfa.str.replace('+','')
    dfa=dfa.str.replace('-','')
    dfb=data['phone2'].str.replace('.','')
    dfb=dfb.str.replace('+','')
    dfb=dfb.str.replace('-','')
    data=data.drop(columns=['phone1','phone2']) #drop existing 2 phone columns, concat the new ones
    df = pd.concat([data, dfa, dfb] , axis="columns")

    #Catch incorrect date-time from imported csv
    try:
        pd.to_datetime(df['subscriptiondate'], errors='raise')
    except ValueError as e:
        print("Caught Error!", e.args)
        return JsonResponse({'message': 'There are invalid date format within the CSV.', 'dateerrors': e.args}, safe=False,  status=422) 
        
    #to display the duplicate rows in a new dataframe
    #1. Remove the duplicates in the csv
    duplicateRows = df[df.duplicated()] #Don't Rlly NEED, checks for entire row if there is duplicates
    duplicateCustID = df[df.duplicated(subset=['customerid'])]
    df1=df.drop_duplicates() #drops if entire row is a duplicate
    df2=df1.drop_duplicates(subset=['customerid']).fillna("") #drops row if customer id is a duplicate
    
    #2. Remove the duplicate by checking in db
    #2.1 Get data from db, compare with csv dataframe for duplicates
    customers = Customers.objects.all()
    cust_ser = CustomerSerializer(customers, many=True)
    custdf=pd.DataFrame(cust_ser.data)
    
    # if DB custdf.empty: then you can just save your current df2
    if custdf.empty:
        result = df2.to_dict('records')
        customers_serializer = CustomersBulkSerializer(data=result, many=True)
        if customers_serializer.is_valid():
            customers_serializer.save()
            end_time = time.time()
            times = end_time - start_time
            print("Total Time Taken", times, "seconds")
        return JsonResponse(customers_serializer.data, safe=False, status=status.HTTP_201_CREATED) 
        # else:
        #     print("There are errors")
        #     return JsonResponse(customers_serializer.errors, safe=False, status=400)
        
        
    #if not empty you need to compare all the data, excluding id
    #this removes the duplicated items between db and current csv
    cond = df2['customerid'].isin(custdf['customerid']) #if customerid is the same
    df3=df2[df2['customerid'].isin(custdf['customerid'])] #df3 is for storing
    df2.drop(df2[cond].index, inplace = True) #drop the same data from df2
    #concat all records of duplicates within CSV and comparison of CSV and DB
    duplicates= pd.concat([duplicateRows,duplicateCustID,df3],ignore_index=True)
    print("duplicates are present", duplicates)
    #final records of csv without duplicates
    result = df2.to_dict('records')
    # print(result)
    if df2.shape[0]==0: #Nothing to save to database, all data in csv is a duplicate
        print("IM IN HEREEEEE", df2, duplicates)
        dupes=duplicates.to_dict('records')
        dupes_serializer = CustomersBulkSerializer(data=dupes, many=True, validate=False)
        print("DUPE OR NOT?", dupes)
        # dupes_serializer.is_valid()
        # if dupes_serializer.is_valid():
        end_time = time.time()
        times = end_time - start_time
        print("Total Time Taken", times, "seconds")
        return JsonResponse({'message': 'The CSV already exists in the database.', 'duplicates':dupes_serializer.data}, safe=False,  status=400) 
        # else:
            # end_time = time.time()
            # times = end_time - start_time
            # print("Total Time Taken", times, "seconds")
            # return JsonResponse({'message': 'The CSV already exists in the database.', 'duplicates':dupes_serializer.data}, safe=False,  status=400) 
    elif not duplicates.empty: #if duplicates not empty, means only some can be saved to DB.
        customers_serializer = CustomersBulkSerializer(data=result, many=True)
        if customers_serializer.is_valid():
            customers_serializer.save()
        dupes=duplicates.to_dict('records')
        dupes_serializer = CustomersBulkSerializer(data=dupes, many=True,validate=False)
        # print(customers_serializer.data)
        # dupes_serializer.is_valid()
        end_time = time.time()
        times = end_time - start_time
        print("Total Time Taken", times, "seconds")
        return JsonResponse({'message': 'Some duplicates already exists in the CSV or Database.','customers':customers_serializer.data, 'duplicates':dupes_serializer.data}, safe=False,  status=400) 
    else:
        try:
            customers_serializer = CustomersBulkSerializer(data=result, many=True)
            if customers_serializer.is_valid():
                customers_serializer.save()
                end_time = time.time()
                times = end_time - start_time
                print("Total Time Taken", times, "seconds")
                return JsonResponse(customers_serializer.data, safe=False, status=status.HTTP_201_CREATED) 
            else:
                return JsonResponse({'message': 'There is invalid data within CSV. Please check the fields.','therrors': e.args}, safe=False,  status=400) 
        except Exception as e:
            return JsonResponse({'message': 'There are invalid data or format within the CSV.', 'therrors': e.args}, safe=False,  status=400) 
        
        

# Fuzzy Search TrigramSimilarity
@api_view(['GET'])
def companies_fuzzysearch(request,company):
    from django.contrib.postgres.search import TrigramSimilarity
    searchcompany=company
    results = Customers.objects.annotate(similarity=TrigramSimilarity('company',searchcompany),).filter(similarity__gte=0.2).order_by('-similarity')
    customers_serializer = CustomerSerializer(results, many=True)
    return JsonResponse(customers_serializer.data, safe=False)
