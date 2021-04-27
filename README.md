# **Fliprfantasy**
### Flipr Hackathon 8.0-2021.
--------------------------
## Setup instructions
### **Server**
* **Step 1 (optional but recommended)**

    Create a python virtual environment by using virtualenv or conda
    
        conda create -n environment python3.6

    or

        python -m venv environment && source environment/bin/activate
* **Step 2**

    Clone this repo
    
        git clone https://github.com/Harendra8095/flipr_backend.git && cd flipr_backend

* **Step 3**

    Install the dependencies
        
        pip install -r requirements.txt

    Install the docker

        Refer: https://docs.docker.com/compose/install

    Install the redis

        Refer: https://redis.io/topics/quickstart

* **Step 4**

    Create the .env file with following key-values
    Copy same .env in the matchupdater folder
    
        SECRET_KEY=DefaultSecretKey
        DB_DIALECT=postgresql
        DB_HOST=postgres
        DB_PORT=5432
        DB_USER=postgres
        DB_PASS=postgres
        DB_NAME=flipr
        REDIS_HOST=redis
        REDIS_PORT=6379

* **Step 5**

    Create your localdatabase with localhost postgres and populate data
    
        python migrations.py db migrate
        python migrations.py db upgrade
        python manage.py testdb
* **Step 6**

    To run server
    
        sudo docker-compose up --build --remove-orphans

### **Use app in browser**

    Go to the address your console show

        * Backend Running on http://localhost:5000
        * Api-Docs Running on http://localhost:8080
        * Frontend Running on http://localhost:80