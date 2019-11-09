[ -z "$ACR_RES_GROUP" ] && ACR_RES_GROUP=takealook-acr
[ -z "$AKS_RES_GROUP" ] && AKS_RES_GROUP=takealook-aks
[ -z "$SP_NAME" ] && SP_NAME=takealook-sp

echo "Delete ACR resource group"
az group delete --resource-group $ACR_RES_GROUP --yes
echo "Delete AKS resource group"
az group delete --resource-group $AKS_RES_GROUP --yes
echo "Delete SP"
az ad sp delete --id $(az ad sp show --id http://$SP_NAME --query appId --output tsv)
