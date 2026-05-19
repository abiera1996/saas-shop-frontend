find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete
pip install --upgrade --force-reinstall  Django==4.2.2