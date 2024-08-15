# MuYaHo

An app for students of Dongguk Univ. `MuYaHo` provides notices of the univ.

## Run

```
python3 -m venv env
source ./env/bin/activate
pip3 install -r requirements.txt
python3 src/manage.py makemigrate
python3 src/manage.py migrate
python3 src/manage.py runserver
```
