
# twitter insight k8s service 📝  
bla bla

## Get Started 🚀  
we are using minikube to  run the k8s cluster

### Install minikube
`pip install minikube/brew install minikube`
`minikube start`
`minikube addons enable ingress`


## Build the images 🔥  
Build all the images

```sh
make
```

Or build specific images

```sh
make frontend
```

### Create namespace

Create namespace for the k8s resources

```sh
kubectl create namespace twitty
```

### Create deployments

Create deployments and volumes

```sh
kubectl apply -f ./k8s -n twitty
```

## Access the frontend

Enable port forwarding

you can track the deployment with the minikube dashboard (`minikube dashboard`) or via kubectl.
to access the service go port forwarding...or go ingress, in which case:
- go `minikube tunnel` to allow ingress calls into minikube to happen on yr 127.0.0.1.
- edit yr hosts file (`/etc/hosts` on unixlikes) and add `127.0.0.1 twitty.com`

the UI should be available via `http://twitty.com` in yr browser.


## Cleanup

<!-- Delete all resources

```sh
kubectl delete -f ./k8s -n twitty
``` -->

Delete the namespace

```sh
kubectl delete namespace twitty
```
