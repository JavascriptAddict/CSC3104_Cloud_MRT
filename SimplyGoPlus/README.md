
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
- Note: Run this command in the root folder
- .\SimplyGoPlus\myenv\Scripts\activate

## Install Dependencies
### Activate Virtual Environment if needed
- .\SimplyGoPlus\myenv\Scripts\activate
- pip install -r requirements.txt

## To run individual services or API Gateway
### Activate virtual environment if needed
- Note: Run this command in the root folder
- .\SimplyGoPlus\myenv\Scripts\activate

### Run the codes in 4 separate powershells all in virtual environment
- Run as a module from package 
- Note: Run these commands in the root folder
- python -m SimplyGoPlus.accountService.main
- python -m SimplyGoPlus.transactionService.main
- python -m SimplyGoPlus.tripService.main
- python -m SimplyGoPlus.visionService.main

### Run API Gateway in a separate powershell in virtual environment
- Note: Run this command in the root folder
- uvicorn SimplyGoPlus.apiGateway.main:app --host 0.0.0.0 --port 80

## Database
- PostgreSQL online aiven database is used
- credentials in .env file in root folder

## To compile protobuf
- Script automation work in progress
- Will have to shift the files manually into generated folder for now
#### Codes for generating pb2 files
From inside the SimplyGoPlus folder, invoke this code and change trip to whatever you're generating
```sh
python -m grpc_tools.protoc -I protos --python_out=./generated --pyi_out=./generated --grpc_python_out=./generated protos/trip.proto
```
