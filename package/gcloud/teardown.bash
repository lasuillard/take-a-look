[ -z "$GCP_PROJECT_ID" ] && GCP_PROJECT_ID=take-a-look-257807
[ -z "$GKE_CLUSTER_NAME" ] && GKE_CLUSTER_NAME=gke-cluster
[ -z "$GCP_FILESTORE_INSTANCE_NAME" ] && GCP_FILESTORE_INSTANCE_NAME=nfs-server

echo "Tearing high-cost services down"
echo "- Delete GKE Cluster"
gcloud container clusters delete $GKE_CLUSTER_NAME \
    --project $GCP_PROJECT_ID \
    --async

echo
echo "- Delete Cloud Filestore instance"
gcloud filestore instances delete $GCP_FILESTORE_INSTANCE_NAME \
    --project $GCP_PROJECT_ID \
    --zone "asia-northeast1-a" \
    --async
