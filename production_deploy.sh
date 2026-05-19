git pull origin master  
python manage.py makemigrations app_profile app_main app_user app_vehicle app_branch app_gas_consumption app_billing app_insurance app_vehicle_registation
python manage.py migrate
python manage.py collectstatic --noinput 
python manage.py setup_user_role_permission
supervisorctl restart fms