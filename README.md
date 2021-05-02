#### FLASK RESTFUL API HOMEWORK

### Terminal commands
Note: make sure you have `python3` and `pip` installed. Then change current directory to the project directory

    1. Install virtual environment: 
        python -m venv venv
    
    2. Activate the virtual environment: 
        . venv/bin/activate      # Ubuntu
        . venv/Scripts/activate  # Window
        
    3. Install third-party libraries:
        pip install -r requirements.txt
        
    4. To run test: 
        python test.py

    5. To run application: 
        python app.py
        

### APIs information ####
    1. Save a pool object
        Method: POST
        URL: http://127.0.0.1:5000/api/1
        Content-Type: application/json
        Body:
            {
              "poolId": 5,
              "percentile": 5
            }
    2. Calculate quantile and count number of elements in a pool
        Method: POST
        URL: http://127.0.0.1:5000/api/2
        Content-Type: application/json
        Body:
            {
              "poolId": 5,
              "percentile": 99
            }
