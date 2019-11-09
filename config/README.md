# Project Configurations
This directory includes various settings for projects, mainly k8s.

## Kubernetes
This project uses blue/green deployment pattern, and followings are important metadatas:

* Namespace: takealook
* Naming convetion: { resource-type }-{ resource-name }-{ suffix }
* Apps: main, db
* Labels: env, app

### Microsoft Azure
At az directory, there's macro shell script for cluster setup/teardown.

* <b>setup.bash</b>: create related resource groups step by step.
* <b>teardown.bash</b>: terminate all resource groups so that additional charges not be made.

Secrets will not be included in code repository, or will be included with password encrypted zip file.

### Google Cloud Platform
RESERVED