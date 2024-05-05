
# Vendor Management System with Performance Metrics

This project is a Vendor Management System developed using Django and Django REST Framework. The system allows to manage vendor profiles, track purchase orders, and calculate vendor performance metrics such as on-time delivery rate, quality rating average, response time, and fulfillment rate.




## Features

- Vendor Profile Management: Create, retrieve, update, and delete vendor profiles. Each vendor profile includes essential information such as name, contact details, address, and a unique vendor code.
- Purchase Order Tracking: Track purchase orders with details including PO number, vendor reference, order date, items, quantity, and status.

- Vendor Performance Evaluation: Calculate and display performance metrics for vendors, including on-time delivery rate, quality rating average, response time, and fulfillment rate.


## Installation
1.Clone the repository:
```bash
https://github.com/s1999-alt/Vendor-Management.git
```


2.Path to Project File

```bash
 cd .\vendor_management_system\        
```



3.Create and activate Environment:
```bash
python3 -m venv env

windows : .env\Scripts\activate
Linux   :  source env/bin/activate
```

4.Install dependencies:

```bash
pip install -r requirements.txt
```

5.Apply database migrations:

```bash
python manage.py migrate
```

6.Run the development server:

```bash
python manage.py runserver

```






## Authentication
To access the API endpoints, authentication is required.Use this token as Bearer Token.

1.Create a superuser:

```bash
python manage.py createsuperuser
```
Use Superuser Username and Password for Login.

## API Reference

### Login

```http
  POST /api/login/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `username` | `string` | **Required**. SuperUser's username|
| `password` | `string` | **Required**. SuperUser's password|

After Login , We got an access token and refresh token, access token is required for all other endpoints


### Vendor Endpoints

#### 1. Create a new vendor.

```http
  POST /api/vendors/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `name` | `string` | **Required**. Vendor name|
| `contact_details ` | `string` | **Required**. Vendor's contact details |
| `address` | `string` | **Required**. address |
| `vendor_code` | `string` | **Required**. vendor_code |



#### 2. List all vendors

```http
  GET /api/vendors/
```


#### 3. Retrieve a specific vendor's details.

```http
  GET /api/vendors/<vendor_id>/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `vendor_id`      | `integer` | **Required**. ID of the vendor whose details are to be retrieved.|


#### 4. Update a vendor's details. 

```http
  PUT /api/vendors/<vendor_id>/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `vendor_id`      | `integer` | **Required**. ID of the vendor.|
| `name` | `string` | **Required**. Vendor name |
| `contact_details ` | `string` | **Required**. Vendor's contact details |
| `address` | `string` | **Required**. address |
| `vendor_code` | `string` | **Required**. vendor_code |


#### 5. Delete a vendor.

```http
  DELETE /api/vendors/<vendor_id>/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `vendor_id`      | `integer` | **Required**. ID of the vendor.|




### Purchase Order Endpoints

#### 1. Create a purchase order.

```http
  POST /api/purchase_orders/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `po_number` | `string` | **Required**. Purchase order number(It Generates Automatically) |
| `vendor` | `integer` | **Required**. Vendor ID |
| `order_date` | `string` | **Required**. Order date (YYYY-MM-DD) |
| `delivery_date` | `string` | **Required**. delivery_date (YYYY-MM-DD) |
| `items` | `json` | **Required**.  Items in the purchase order |
| `quantity` | `integer` | **Required**. Total quantity of items|
| `status` | `string` | **Required**. Status of the purchase order |
| `quality_rating` | `integer` |  Rating given to the vendor |
| `issue_date` | `string` | **Required**. issue_date (YYYY-MM-DD) (issue date automatically generates with the current date and time, give order date less than the issue date and delivery date greater than than issue date(+7 days from order date)) |
| `acknowledgment_date` | `string` | acknowledgment_date (YYYY-MM-DD) (acknowledge date is greater than the issue date and less than the delivery date ) |


#### 2. List all Purchase Orders

```http
  GET /api/purchase_orders/
```

#### 3. Retrieve purchase orders by vendor.

```http
  GET /api/purchase_orders/by_vendor/<int:vendor_id>/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `vendor_id` | `integer` | **Required**. Vendor Id|


#### 4. Retrieve details of a specific purchase order.

```http
  GET /api/purchase_orders/<po_id>/:
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `po_id` | `integer` | **Required**. Purchase Order ID |



#### 5. Update a purchase order.

```http
  PUT /api/purchase_orders/<po_id>/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `po_id` | `integer` | **Required**. Purchase Order ID |
| `po_number` | `string` | **Required**. Purchase order number(It Generates Automatically) |
| `vendor` | `integer` | **Required**. Vendor ID |
| `order_date` | `string` | **Required**. Order date (YYYY-MM-DD) |
| `delivery_date` | `string` | **Required**. delivery_date (YYYY-MM-DD) |
| `items` | `json` | **Required**.  Items in the purchase order |
| `quantity` | `integer` | **Required**. Total quantity of items|
| `status` | `string` | **Required**. Status of the purchase order |
| `quality_rating` | `integer` | Rating given to the vendor |
| `issue_date` | `string` | **Required**. issue_date (YYYY-MM-DD) |
| `acknowledgment_date` | `string` | **Required**. acknowledgment_date (YYYY-MM-DD) |


#### 6. Delete a Purchase Order

```http
  DELETE /api/purchase_orders/<po_id>/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `po_id` | `integer` | **Required**. Purchase Order ID |



### Retrieve Vendor Performance Metrics Endpoint

```http
  GET /api/vendors/<vendor_id>/performance/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `vendor_id` | `integer` | **Required**. Vendor ID|


### Update Acknowledgment Endpoint:

```http
  PUT purchase_orders/<po_id>/acknowledge/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `po_id` | `integer` | **Required**. Purchase Order ID|




## Running Tests

Run unit tests to validate the functionality of API endpoints:

```bash
  python manage.py test vendors
```

