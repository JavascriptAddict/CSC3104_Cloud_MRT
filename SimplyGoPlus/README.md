
## Features
- Account Service:
    - User Auth
    - Access account to retrieve account details
    - Top up wallet
- Transaction Service:
    - Post transactions
    - Retrieve transactions
- Trip Service:
    - Create trip
    - End trip
    - Get trips
- Vision Service:
    - Training model weights
    - Storing user's face for training
    - Return latest weights

## Project Root
- SimplyGoPlus folder is the project/package root
- To run any modules within, start from outside the root folder

## Create virtual environment
```shell
cd .\SimplyGoPlus\
python -m venv myenv
cd ..
```
#### Activate the Virtual Environment
- .\SimplyGoPlus\myenv\Scripts\activate

## Install Dependencies
```sh
.\myenv\Scripts\activate
pip install -r requirements.txt
```

## To run the API Gateway Service
uvicorn SimplyGoPlus.apiGateway.main:app --host 0.0.0.0 --port 80

## To compile protobuf
- Script automation work in progress
- Will have to shift the files manually into generated folder for now
#### Codes for generating pb2 files
From inside the SimplyGoPlus folder, invoke this code and change trip to whatever you're generating
```sh
python -m grpc_tools.protoc -I protos --python_out=./generated --pyi_out=./generated --grpc_python_out=./generated protos/trip.proto
```
- Make sure to change _pb2_grpc.py files to "from . import account_pb2 as account__pb2" to fix not found error (remove this? I don't even see this)

## To run individual services or API Gateway
#### Activate virtual environment
- .\SimplyGoPlus\myenv\Scripts\activate

#### Run the codes in 3 separate powershells all in virtual environment
- Run as a module from package 
- python -m SimplyGoPlus.accountService.main
- python -m SimplyGoPlus.transactionService.main
- python -m SimplyGoPlus.tripService.main
- uvicorn SimplyGoPlus.apiGateway.main:app --host 0.0.0.0 --port 80

#### To kill a port in cmd
- netstat -ano | findstr :<port number>
- taskkill /PID <pid> /F
- Hope we never have to use this

## Database
- Initial use of SQLite for testing
- Proper DB can be connected once its properly set up