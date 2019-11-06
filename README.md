# Take a Look

## Introduction
This is a term project of 2019-fall SNUST Web Server Programming.

Main feature is classifying given picture whether it is dog or cat, by trained model with Kaggle dataset: [Dogs vs Cats (2013)](https://www.kaggle.com/c/dogs-vs-cats).

### Teams
- 14109359 Yuchan Lee (dldbcks95@gmail.com)

### Environment
#### Local (docker-compose)
- Database: PostgreSQL
- Resource API Server: Django (http://localhost:8000)
    - Primary URLs: /admin, /api
- Rendering Server: Tomcat (http://localhost:8080)
    - Primary URLs: /
- Web Server: Nginx (http://localhost:80)
    - Primary URLs: /static, /media
    - URLs above will also be handled here with proxy

#### Staging & Production (k8s)
- RESERVED


## Installation

### Requirements: 
- Docker version with supporting docker-compose version 3.4 or later.

### How To
1. Install Docker
2. Clone this project with git command or by downloading it as archive
3. Unzip if is compressed and move to project root directory
4. If you have no secret.json then you should get it from project developer
5. Open command prompt and run following command

```
path/to/project/root> docker-compose up -d --build
```
6. Wait until build processes are done
7. When done, go to the browser and access http://localhost:80 and browse.
