export GCP_PROJECT_ID=take-a-look-257807
export GKE_CLUSTER_NAME=gke-cluster
export GCP_FILESTORE_INSTANCE_NAME=nfs-server

# prerequisites
read -p "GCR and GCB should be created manually on Google Cloud Console. continue(y/n)? " answer
case $answer in
    y|Y) echo ;;
    *) exit 1 ;;
esac

# create gke cluster
echo
echo "Setting up GKE; Google Kubernetes Engine"
echo "- Create cluster"
gcloud container clusters create $GKE_CLUSTER_NAME \
    --project $GCP_PROJECT_ID \
    --zone "asia-northeast1-a" \
    --cluster-version "1.13.11-gke.14" \
    --machine-type "n1-standard-1" \
    --num-nodes "5"

echo
echo "- Fetching k8s credentials"
gcloud container clusters get-credentials $GKE_CLUSTER_NAME

# setup cloud filestore instance
echo
echo "Create Filestore Instance for NFS"
gcloud filestore instances create $GCP_FILESTORE_INSTANCE_NAME \
    --project $GCP_PROJECT_ID \
    --zone "asia-northeast1-a" \
    --tier=STANDARD \
    --file-share name="data",capacity="1TB" \
    --network name="default"
