
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
cd .\SimplyScan\
python -m venv myenv
cd ..
```
#### Activate the Virtual Environment
- .\SimplyScan\myenv\Scripts\activate

## Install Dependencies
```sh
.\myenv\Scripts\activate
pip install -r requirements.txt
```


## To run individual services or API Gateway
### Activate virtual environment
- .\SimplyScan\myenv\Scripts\activate

### Run the codes in 4 separate powershells all in virtual environment
- Run as a module from package 
- python -m SimplyScan.backend.accountContainer.accountSub.accountService.main
- python -m SimplyScan.backend.transactionContainer.transactionSub.transactionService.main
- python -m SimplyScan.backend.tripContainer.tripSub.tripService.main
- python -m SimplyScan.backend.visionContainer.visionSub.visionService.main

### Run API Gateway in a separate powershell in virtual environment
- uvicorn SimplyScan.backend.apiContainer.apiSub.apiGateway.main:app --host 0.0.0.0 --port 80

#### To kill a port in cmd
- netstat -ano | findstr :<port number>
- taskkill /PID <pid> /F
- Hope we never have to use this

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
- Make sure to change _pb2_grpc.py files to "from . import account_pb2 as account__pb2" to fix not found error (remove this? I don't even see this)

## To Dockerize
- For frontend, navigate to frontend directory
    - Run 'docker build -t frontend_service .'
    - Run 'docker run --privileged -p 80:80 frontend_service'

- For API Gateway, navigate to apiContainer directory
    - Run 'docker build -t api_gateway .'
    - Run 'docker run -p 8080:8080 api_gateway'

- For each microservice, navigate to their respective Container folder and perform the following steps. Let's use accounts for example.
- Go to accountContainer 
    - Run 'docker-compose up --build
    - Run 'docker-compose down' to stop the container if needed


## To Deploy
- Make sure to have k3d and Kubectl installed
- Run your Docker Desktop 
- Open up command prompt and create a Kubernetes cluster
    - k3d cluster create simplycluster --agents 2 --port "6443:6443@loadbalancer"
    - Once created try running kubectl cluster-info to try connecting to Kubernetes
        - If issue occurs, go inside your config file and change the server "host.docker.internal"
        - Change it to "http://localhost:6443"
    - You should be connected to Kubernetes now
- Start your Kubernetes cluster (if not started)
    - k3d cluster start simplycluster
- Create Kubernetes Secrets
    - For access to account database:
        - Run 'kubectl create secret generic account-db-secret --from-literal=DATABASE_URL=postgres://avnadmin:AVNS_rOO_xCE2pecb4TH8FOY@cloudmrt-cloudmrt.j.aivencloud.com:19275/accountDB?sslmode=require'
    - For access to transaction database:
        - Run 'kubectl create secret generic transaction-db-secret --from-literal=DATABASE_URL=postgres://avnadmin:AVNS_rOO_xCE2pecb4TH8FOY@cloudmrt-cloudmrt.j.aivencloud.com:19275/transactionDB?sslmode=require'
    - For access to trip database:
        - Run 'kubectl create secret generic trip-db-secret --from-literal=DATABASE_URL=postgres://avnadmin:AVNS_rOO_xCE2pecb4TH8FOY@cloudmrt-cloudmrt.j.aivencloud.com:19275/tripDB?sslmode=require'
    - For access to vision database:
        - Run 'kubectl create secret generic vision-db-secret --from-literal=DATABASE_URL=postgres://avnadmin:AVNS_rOO_xCE2pecb4TH8FOY@cloudmrt-cloudmrt.j.aivencloud.com:19275/visionDB?sslmode=require'
- Navigate to the Kubernetes directory
    - To apply the YAML files which includes both deployment and service:
        - Ensure that the image inside are linked to the Docker images that are pushed in Docker Hub
        - For Account: Run 'kubectl apply -f account_deployment.yaml'
        - For Frontend: Run 'kubectl apply -f frontend_deployment.yaml'
        - For API Gateway: Run 'kubectl apply -f gateway_deployment.yaml'
        - For Transaction: Run 'kubectl apply -f transaction_deployment.yaml'
        - For Trip: Run 'kubectl apply -f trip_deployment.yaml'
        - For Vision: Run 'kubectl apply -f vision_deployment.yaml'
- Inside your terminal run the following commands to check if the deployments are running
    - kubectl get deployments
    - kubectl get pods
    - kubectl get services
- Check on the status of the pods if all are running well
    - If error persists, check on the YAML file configurations or database connections
    - Use 'kubectl logs <pod-name>' to check the error message of the pod
- Portforward frontend and gateway
    - Run 'kubectl port-forward svc/frontend-service 3000:80'
        - Enter localhost:3000 in your browser and you will see the page loaded
    - Run 'kubectl port-forward svc/api-gateway-service 8080:80'
        - Enter localhost:8080/docs to see the documentation page for testing of the API gateway


