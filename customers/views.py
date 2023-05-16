from django.shortcuts import render
from django.http import HttpResponse
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from customers.models import Customers
from customers.serializers import CustomerSerializer
from customers.serializers import CustomersBulkSerializer
from rest_framework.decorators import api_view
# from thesite.settings import GLOBAL_VAR_X

import logging
logger = logging.getLogger("django")


#Finding All Customers, Post Single Customer
@api_view(['GET','POST'])
def customer_list(request):
    if request.method == 'GET':
     try:
        customers = Customers.objects.all()
        id = request.GET.get('id', None)
        if id is not None:
            customers = customers.filter(id__icontains=id)
        customers_serializer = CustomerSerializer(customers, many=True)
        return JsonResponse(customers_serializer.data, safe=False) # 'safe=False' for objects serialization
     except Exception as e:
         response= JsonResponse({"message":"Unable to retrieve customers table."})
         response.status_code=500 #for internal server error
         return response
    elif request.method == 'POST': #Post Single Customer
     logger.info("POST API has been executed")
     try:
        customers_data = JSONParser().parse(request)
        print("going into customers bulk serializer!!!!")
        customers_serializer = CustomersBulkSerializer(data=customers_data)
        if customers_serializer.is_valid():
            customers_serializer.save()
            return JsonResponse(customers_serializer.data, status=status.HTTP_201_CREATED) 
     except Exception as e:
         print(e)
         return JsonResponse({"message":"Registration of Customer failed.", "theerror":e.args}, status = 400)


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
    start_time = time.time()
   # #1. Remove the duplicates in the csv
    try:
        df=pd.read_csv(request,sep=',')
    except pd.errors.EmptyDataError: #if file is not chosen its empty
        return JsonResponse({'message': 'No file was chosen. Please insert a CSV.'}, safe=False,  status=400) 
    df.drop(columns=['Index'], inplace=True)
    df.rename({'Customer Id': 'customerid', 'First Name': 'firstname', 'Last Name': 'lastname', 'Company': 'company','City': 'city', 'Country':'country', 'Phone 1':'phone1', 'Phone 2':'phone2','Email':'email', 'Subscription Date': 'subscriptiondate', 'Website':'website', 'Cleaned Phone 1':'cleanedphone1', 'Cleaned Phone 2':'cleanedphone2' }, axis=1, inplace=True)
    # headers_to_keep = ['Name', 'Country']
    # headers_to_delete = [header for header in df.columns if header not in headers_to_keep]
    # df.drop(headers_to_delete, axis=1, inplace=True)
    #to display the duplicate rows in a new dataframe
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
            print("reached heereeeeeeee")
            end_time = time.time()
            times = end_time - start_time
            print("Total Time Taken", times, "seconds")
            return JsonResponse(customers_serializer.data, safe=False, status=status.HTTP_201_CREATED) 
        else:
            print("There are errors")
            return JsonResponse(customers_serializer.errors, safe=False, status=400)
    #if not empty you need to compare all the data, excluding id
    #this removes the duplicated items between db and current csv
    cond = df2['customerid'].isin(custdf['customerid']) #if customerid is the same
    df3=df2[df2['customerid'].isin(custdf['customerid'])] #df3 is for storing
    df2.drop(df2[cond].index, inplace = True) #drop the same data from df2
    #concat all records of duplicates within CSV and comparison of CSV and DB
    duplicates= pd.concat([duplicateRows,duplicateCustID,df3],ignore_index=True)
    #final records of csv without duplicates
    result = df2.to_dict('records')
    if df2.shape[0]==0: #Nothing to save to database, all data in csv is a duplicate
        dupes=duplicates.to_dict('records')
        dupes_serializer = CustomerSerializer(data=dupes, many=True)
        if dupes_serializer.is_valid():
            end_time = time.time()
            times = end_time - start_time
            print("Total Time Taken", times, "seconds", "the dupes are", dupes_serializer.data)
            return JsonResponse({'message': 'The CSV already exists in the database.', 'duplicates':dupes_serializer.data}, safe=False,  status=400) 
    elif not duplicates.empty: #only some have been saved to DB.
        customers_serializer = CustomerSerializer(data=result, many=True)
        if customers_serializer.is_valid():
            customers_serializer.save()
        dupes=duplicates.to_dict('records')
        dupes_serializer = CustomerSerializer(data=dupes, many=True)
        if dupes_serializer.is_valid():
            end_time = time.time()
            times = end_time - start_time
            print("Total Time Taken", times, "seconds")
            return JsonResponse({'message': 'Some duplicates already exists in the CSV or Database.','customers':customers_serializer.data, 'duplicates':dupes_serializer.data}, safe=False,  status=400) 
    else:
        try:
            customers_serializer = CustomerSerializer(data=result, many=True)
            if customers_serializer.is_valid():
                customers_serializer.save()
                end_time = time.time()
                times = end_time - start_time
                print("Total Time Taken", times, "seconds")
                return JsonResponse(customers_serializer.data, safe=False, status=status.HTTP_201_CREATED) 
            else:
                return JsonResponse({'message': 'There is invalid data within CSV. Please check the dates.'}, safe=False,  status=400) 

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
