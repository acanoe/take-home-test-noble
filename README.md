# solve-this

## Rules

1. Cannot alter the field and table names of existing models
2. Use Bearer Token based as API Authentication
3. Push your answer on your public repo and send the url link to jefri.arbi@noble-software.com

## Issues

1. Solve the circular dependency and migration issues
2. Create API for owner sign-up
3. Create API for user login
4. Create API for company creation (This API can be accessed after user login)
5. Create API for registered new employee (Only Owner of company has access to it)
6. Create django admin for User and Company models
7. Create django command to filled the Authentication and Authorization Group in the django admin that all staff can only add and view all models
8. If employee created from django admin, add validation for the company must not be null
9. Use OpenAPI schema based to showed all of the API endpoint
10. Use SQLlite3 as DB that already migrated with the models (put it in the project as POC)

## User credentials

- Admin:
  - email: `admin@admin.com`, password: `admin`
- Company owners:
  - email: `owner@trusted.company`, password: `trust`
  - email: `jeff@amazon.com`, password: `atoz`
  - email: `bill@micro.soft`, password: `msft`
- Employees:
  - email: `employee.1@trusted.company`, password: `trust1`
  - email: `employee.2@trusted.company`, password: `trust2`
  - email: `adam@amazon.com`, password: `atoz1`
  - email: `bryan@amazon.com`, password: `atoz2`
  - email: `alef@micro.soft`, password: `msft1`
  - email: `bet@micro.soft`, password: `msft2`

## Django management commands

- run `./manage.py set_permissions` to give all new company owner permission to view and add a new company and employees in the django admin page. You can also specify users to give permissions to, e.g. `./manage.py set_permissions jeff@amazon.com bill@micro.soft`
