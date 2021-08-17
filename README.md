# technotesplus

Recommended OS ubuntu

1. install python venv
    for linux:
    install:          python3 -m pip install virtualenv
    create venv:      python3 -m venv <any name for env>
    active(bash/zsh): source env/bin/activate

2. Install requirment apps by using below commands
    
    sudo apt-get install redis
    sudo apt-get install rabbitmq-server
    sudo systemctl enable rabbitmq-server
    sudo systemctl start rabbitmq-server

3. Install file from requiements.txt 
        pip3 install -r requirements.txt
  
4. Run web the application by 
    python manage.py runserver
 
  and 
  in another terminal with activated same venv run
    celery -A Tech_Note.celery beat -l info




















