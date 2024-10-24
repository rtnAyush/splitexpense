# Expense Sharing Web Application
## Overview
- This web application allows users to add expenses and split them based on three different methods: exact amounts, percentages, and equal splits. The web application manages user details, validates inputs, and generates downloadable balance CSV sheets.

## Framework
- Django
  
## Installation
  1. Clone the repository: `git clone https://github.com/rtnAyush/splitexpense.git`
  2. cd splitwise
  3. Make sure you have Django installed globally

## Running the application
  `python manage.py runserver`
  
## Endpoints
- The following endpoints are available in this expense sharing application:

- BASEURL: http://localhost:8000
## 1. User Endpoints:

  ### 1.1 POST user/create
  - Description: Create a new user

Example Request:

![image](https://github.com/user-attachments/assets/f91f6291-d879-4606-b66a-c4a548c74a80)

Example Response:

![image](https://github.com/user-attachments/assets/c0dd4683-e348-43cf-aea0-d6d7e7c00703)

Example Validations:
- if User exists:

![image](https://github.com/user-attachments/assets/d3821354-0fbc-4d69-8916-82d0a0b8b50b)

- if Phone key is not given(checks for all fields):
  
![image](https://github.com/user-attachments/assets/9ac849b0-4de5-405e-9d77-bf88b966ad4d)

- If user send invalid JSON:
  
![image](https://github.com/user-attachments/assets/9f6d1e79-875d-4000-a9c5-f1ae3151d3f8)

### 1.2 GET user/get/:userId
- Description: Retrieve user details by id

Example Response:

![image](https://github.com/user-attachments/assets/f733f1d4-b246-47d8-9407-c55d7f46ca53)

## 2. Expense Endpoints:
### 2.1 POST expense/add
- Description: Add an expense with its participants

Example Request:

![image](https://github.com/user-attachments/assets/4bb9fbad-7c4a-4c1f-83ac-056763c85a68)

Example Response:

![image](https://github.com/user-attachments/assets/308395fd-008c-4a67-adc0-0febfa0cc04a)

### 2.2 GET expense/list/:userId
- Description: Get individual user expenses which include entire expense payment and as a participant in an expense

Example Response:

![image](https://github.com/user-attachments/assets/0cd7a600-a5e0-46b8-b28d-25618448b00c)

### 2.3 GET expense/overall
- Description: Retrieves overall expenses for all users

Example Response:

![image](https://github.com/user-attachments/assets/d5fb2194-7292-4c31-a923-1d0c449229f4)

### 2.4 GET expense/download/balance-sheet/<userId>
- Description: Downloads balance Excel sheet for a user which contains individual expenses as well as overall expenses for all users

Example Response:

| Type       | Expense ID | Description      | Amount | Date       | Payer  | Payment Type | Amount Owed | Amount Paid | Individual ID | Username | Amount Owed |
|------------|------------|------------------|--------|------------|--------|--------------|--------------|-------------|---------------|----------|--------------|
| Expense    | 1          | Ice Cream Party   | 100.0  | 2024-07-28 | Ayush  | percentage    | 50.0         | 0           | 3             | Pranshu  | 50.0        |
| Expense    | 1          | Ice Cream Party   | 100.0  | 2024-07-28 | Ayush  | percentage    | 25.0         | 0           | 4             | Vaidik   | 25.0        |
| Expense    | 1          | Ice Cream Party   | 100.0  | 2024-07-28 | Ayush  | percentage    | 25.0         | 0           | 5             | Aman     | 25.0        |
