# CustomerManagementBackend
CustomerManagementSystem
This is the backend for the Customer Management System. It requires the frontend Vue for it to work. This Customers' Data Management System was created for users to view, add and manage customer’s data. 
  The end-to-end prototype(using vuejs as UI, Django as the ORM to Postgres) includes:  
Allowing a user to upload a csv file for bulk record data ingestion as well as a simple table that allows fuzzy query to customers dataset and an export function to export that selected dataset out to csv.
![image](https://github.com/anabellechan/CustomerManagementVue/assets/97331839/9d7c314e-9fe1-4ad8-b243-861e1369c63c)
![image](https://github.com/anabellechan/CustomerManagementVue/assets/97331839/1a3e5061-81ad-4191-87d4-fe950ebc6b22)
![image](https://github.com/anabellechan/CustomerManagementVue/assets/97331839/52072203-721d-40ba-9ae0-ffe8e3a8a88d)
![image](https://github.com/anabellechan/CustomerManagementVue/assets/97331839/ddea5839-b1b8-4894-b2ae-bf7c7f683d28)
![image](https://github.com/anabellechan/CustomerManagementVue/assets/97331839/bab8356d-7c5d-40a1-a66a-106356ea8b90)
![image](https://github.com/anabellechan/CustomerManagementVue/assets/97331839/90e81246-517a-4fef-a6de-883c3906208a)

Database Changes  
<img width="506" alt="image" src="https://github.com/anabellechan/CustomerManagementVue/assets/97331839/5c1eb07e-be91-4bae-b559-9e8c3af975dd">


Error Handling:  

<img width="559" alt="image" src="https://github.com/anabellechan/CustomerManagementVue/assets/97331839/e945a655-b3a1-4898-9e99-672d37d11e6d">
<img width="560" alt="image" src="https://github.com/anabellechan/CustomerManagementVue/assets/97331839/89900710-5f34-41dd-be7c-c70e99195cef">
<img width="563" alt="image" src="https://github.com/anabellechan/CustomerManagementVue/assets/97331839/a600e1c1-644d-4ca7-9081-95084a3dcd2f">
<img width="472" alt="image" src="https://github.com/anabellechan/CustomerManagementVue/assets/97331839/4d0c78a8-48d1-4aae-8221-819e7560334b">


Webapp Security Measures  
<img width="466" alt="image" src="https://github.com/anabellechan/CustomerManagementVue/assets/97331839/b626cd9a-0948-4d0e-97ea-d450eb1df285">  
-Token Expiration (Access=15mins, Refresh=1day)  
Program’s Secret Credentials from settings into .env  
	- Secret key  
	- Whitelist CORS  
	- Database Username and Password  

![image](https://github.com/anabellechan/CustomerManagementVue/assets/97331839/69fd6675-8d06-4f96-aa1b-e2339e17b1be)
![image](https://github.com/anabellechan/CustomerManagementVue/assets/97331839/fd629e37-1f0b-4c33-b74a-89eb87fb0ba0)
![image](https://github.com/anabellechan/CustomerManagementVue/assets/97331839/f12fea0d-58da-4286-b63f-c87b757310cf)


Future Improvements  
<img width="446" alt="image" src="https://github.com/anabellechan/CustomerManagementVue/assets/97331839/35bdb6ae-23e3-49c7-8b0c-fe54c43f52c6">
