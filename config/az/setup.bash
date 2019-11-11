export ACR_RES_GROUP=takealook-acr
export ACR_REPOSITORY_NAME=takealook
export SP_NAME=takealook-sp
export AKS_RES_GROUP=takealook-aks
export AKS_CLUSTER_NAME=takealook-aks-cluster

# setup acr
echo "Setting up ACR; Azure Container Registry"
echo "- Create resource group:$ACR_RES_GROUP"
az group create --resource-group $ACR_RES_GROUP --location koreacentral
echo "- Create container registry: $ACR_REPOSITORY_NAME"
az acr create --resource-group $ACR_RES_GROUP --name $ACR_REPOSITORY_NAME --sku Standard --location koreacentral

# connect
echo "Setting up SP; Service Principal"
export ACR_ID=$(az acr show --name $ACR_REPOSITORY_NAME --query id --output tsv)
export SP_PASSWD=$(az ad sp create-for-rbac --name $SP_NAME --role Reader --scopes $ACR_ID --query password --output tsv)
export APP_ID=$(az ad sp show --id http://$SP_NAME --query appId --output tsv)

# setup aks
echo "Setting up AKS; Azure Kubernetes Service"
echo "Create resource group: $AKS_RES_GROUP"
az group create --resource-group $AKS_RES_GROUP --location koreacentral
echo "Create kubernetes cluster: $AKS_CLUSTER_NAME"
az aks create \
	--name $AKS_CLUSTER_NAME \
	--resource-group $AKS_RES_GROUP \
	--node-count 3 \
	--kubernetes-version 1.14.8 \
	--node-vm-size Standard_DS1_v2 \
	--generate-ssh-keys \
	--service-principal $APP_ID \
	--client-secret $SP_PASSWD
echo "Fetch k8s credentials (~/.kube)"
az aks get-credentials --admin --resource-group $AKS_RES_GROUP --name $AKS_CLUSTER_NAME
