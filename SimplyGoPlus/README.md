
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

## To run the API Gateway Service
- uvicorn SimplyGoPlus.apiGateway.main:app --host 0.0.0.0 --port 80

## To compile protobuf
- python -m grpc_tools.protoc -I. --python_out=. --pyi_out=. --grpc_python_out=. account.proto
- Make sure to change _pb2_grpc.py files to "from . import account_pb2 as account__pb2" to fix not found error

## To run individual services or API Gateway
- Run as a module from package
- python -m SimplyGoPlus.accountService
- uvicorn SimplyGoPlus.apiGateway.main:app --host 0.0.0.0 --port 80

## Database
- Initial use of SQLite for testing
- Proper DB can be connected once its properly set up