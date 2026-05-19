git pull origin dev  
pip install -r requirements.txt
python manage.py makemigrations app_profile app_main app_user app_vehicle app_branch app_gas_consumption app_billing app_insurance app_vehicle_registation
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py password_expiration
supervisorctl restart fms