## Microservice for German Sentiment Classifier with Bert

This microservice encapsulates an off-the-shelf sentiment classifier for sentiment analysis tasks (https://huggingface.co/oliverguhr/german-sentiment-bert) with docker.

### Creating the image
To create a docker image named german.sentiment.classifier:latest execute the following command:
`sh build.sh`

### Using the endpoint
To run the image, execute the following command:
`sh run.sh`
This will start a container named classifier in detach mode. The microservice can be accessed on localhost:8000.

To use the endpoint, send a POST request to http://localhost:8000/api/v1/classify. 
The body of the request should be a dictionary containing a key named *texts* and a value containing a list of the sentences to be classified.

Example POST request:

`curl -d '{"texts": ["Mit keinem guten Ergebniss", "Das ist gar nicht mal so gut", "Total awesome!", "nicht so schlecht wie erwartet", "Der Test verlief positiv.", "Sie fährt ein grünes Auto."]}' -H "Content-Type: application/json" -X POST http://localhost:8000/api/v1/classify`

### Deployment in AWS
With Amazon ECS, we can define our cluster with load balancers and configure the scaling based on certain predefined metrics.
If the deployment structure requires the Kubernetes engine, we can even go with Amazon EKS. But for now Amazon ECS is
a good option for us.

The steps required to deploy the service on ECS will include:
* We will have one Amazon ECR repository for each microservice.
* Specify the task definitions for the service, which typically includes specifying the service name, the docker image to be used, port mappings and resource management configurations.
* Configure the application load balancer. Whenever the client application makes a request, the load balancer inspects the request, then based on the routing rules, it directs the request to an instance and port from the target group that matches the rule.
* In case of multiple services, listener rules can be configured.
* Once everything is setup and the microservice is running, we can simply make REST calls to the endpoints hosted on our domain.

### Deployment in Azure Container Services
These will be the required steps:
* Create an Azure Resource Group.
* Create Azure Container Register (ACR) to push and share local docker image.
* Add Azure Service Principal to use ACR with Azure Kubernetes Service (AKS).
* Configure AKS cluster managed by kubectl.
* Create deployment definition file.
* Deploy the service.
* Make REST calls to IP provided.