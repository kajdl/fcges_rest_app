# Stock Trading Rest App

## Installation

```bash
# Download the zip file and extract it on your local machine

# Navigate to the project directory or open with your IDE(VS Code) of choice
cd fcges_rest_app-master

# Install dependencies
pip install  django djangorestframework

# Use command makemigrations
python manage.py makemigrations api
python manage.py migrate

# Create a superuser(admin) using the the command below
python manage.py createsuperuser

# If you'd like to use the GUI to create stocks, please use http://localhost:8000/admin
# Login using the credentials you created and navigate to the stocks page on the api section

# Alternatively you can also use the stocks API to send a post request with your superuser token
# Just send a JSON body with the id, name and current price to the link below:
http://localhost:8000/api/stocks/

# Once you're done creating the test stocks
# If you're using VS Code, I recommend using the Rest Client Extension and use the test.rest file
# You can also use Postman to test the code

```

## Available API General Info

```bash
# Signup
# Using POST, you can register a username, password, and an optional email in order to login
http://localhost:8000/api/signup/

# Login
# Also using POST, you can login with the credentials you created from signup and use the token
# generated in order to use the other APIs available for this project
http://localhost:8000/api/login/

# Stocks
# This API can show the available stocks that can be bought
http://localhost:8000/api/stocks/

# Orders
# This API can let you buy stocks, please refer to the test.rest file for the sample JSON
http://localhost:8000/api/orders/

# Orders List
# Shows the user's purchase and selling history
http://localhost:8000/api/orders/list/

# Portfolio
# Shows the user's current portfolios
http://localhost:8000/api/portfolio/

# Specific Portfolio
# Shows the user's specific portfolio, please refer to the test.rest file for the sample JSON
http://localhost:8000/api/portfolio/<str:stock_id>/
