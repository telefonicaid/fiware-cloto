
# How to use fiware-cloto with Docker

There are several options to use fiware-cloto very easily using docker. These are (in order of complexity):

- _"Have everything automatically done for me"_. See Section **1. The Fastest Way** (recommended).
- _"Check the unit tests associated to the component"_. See Section **2. Run Unit Test of fiware-cloto**.
- _"Check the acceptance tests are running properly"_ or _"I want to check that my fiware-cloto instance run properly"_ . See Section **3. Run Acceptance tests**.

You do not need to do all of them, just use the first one if you want to have a fully operational fiware-cloto instance and maybe third one to check if your fiware-cloto instance run properly.

You do need to have docker in your machine. See the [documentation](https://docs.docker.com/installation/) on how to do this. Additionally, you can use the proper FIWARE Lab docker functionality to deploy dockers image there. See the [documentation](https://docs.docker.com/installation/)

----
## 1. The Fastest Way

Docker allows you to deploy an fiware-cloto container in a few minutes. This method requires that you have installed docker or can deploy container into the FIWARE Lab (see previous details about it).

Consider this method if you want to try fiware-cloto and do not want to bother about losing data.

Follow these steps:

- Download [fiware-cloto' source code](https://github.com/telefonicaid/fiware-cloto) from GitHub (`git clone https://github.com/telefonicaid/fiware-cloto.git`)
- `cd fiware-cloto/docker`
- Using the command-line and within the directory you created type: `docker build -t fiware-cloto -f Dockerfile .`.

After a few seconds you should have your fiware-cloto image created. Just run the command `docker images` and you see the following response:

    REPOSITORY          TAG                 IMAGE ID            CREATED              SIZE
    fiware-cloto       latest              bd78d006c2ea        About a minute ago   480.8 MB
    ...

fiware-cloto image needs somce dockers mysql and rabbit alredy deployed. Thus, to deploy the container we need to execute the command `docker run -p 8000:8000 -e PASSWORD=$PASSWORD -l rabbit -l mysql fiware-cloto`.
It will launch the fiware-cloto service listening on port 8000, which is linked to mysql and rabbit dockers.

To check that the service is running correcly, just do

	curl <IP address of a machine>:8000

You can obtain the IP address of the machine just executing `docker-machine ip`. What you have done with this method is the creation of the [fiware-cloto](https://hub.docker.com/r/fiware/bosun-cloto/)
image from the public repository of images called [Docker Hub](https://hub.docker.com/).

If you want to stop the scenario you have to execute `docker ps` and you see something like this:

    CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                    NAMES
    b8e1de41deb5        fiware-cloto       "/bin/sh -c ./start.s"   6 minutes ago       Up 6 minutes        0.0.0.0:8000->8000/tcp   fervent_davinci
    ...

Take the Container ID and execute `docker stop b8e1de41deb5` or `docker kill b8e1de41deb5`. Note that you will lose any data that was being used in fiware-cloto using this method.

However, there is a simpler way to deploy the container. That is docker-compose and it avoids to deploy containers previously and specifies the port for fiware-cloto.
It involves just executing docker-compose up -d to launch the architecture, after exporting a set of environment variables.

    export KEYSTONE_IP=<IP of the keystone instance>
    export ADM_TENANT_ID=<admin tenant id in the OpenStack environment>
    export ADM_TENANT_NAME=<admin tenant name>
    export ADM_USERNAME=<admin username>
    export ADM_PASSWORD=<admin password>
    export OS_USER_DOMAIN_NAME=<OpenStack user domain name>
    export OS_PROJECT_DOMAIN_NAME=<OpenStack project domain name>

If you want to check the containers just execute docker-compose ps.

           Name                      Command               State                                                Ports
    ----------------------------------------------------------------------------------------------------------------------------------------------------------------
    docker_fiwarecloto_1   /bin/sh -c ./start.sh            Up      0.0.0.0:8000->8000/tcp
    mysql                  docker-entrypoint.sh mysqld      Up      0.0.0.0:3306->3306/tcp
    rabbit                 /docker-entrypoint.sh rabb ...   Up      0.0.0.0:25672->25672/tcp, 0.0.0.0:4369->4369/tcp, 0.0.0.0:5671->5671/tcp, 0.0.0.0:5672->5672/tc

You can take a look to the log generated executing docker-compose logs.


----
## 2. Run Unit Test of fiware-cloto

Taking into account that you download the repository from GitHub (See Section **1. The Fastest Way**), this method will launch a container running fiware-cloto, and execute the unit tests associated to the component. You should move to the UnitTests folder `./UnitTests`. Just create a new docker image executind `docker build -t fiware-cloto-unittests -f Dockerfile .`. Please keep in mind that if you do not change the name of the image it will automatically create a new one for unit tests and change the previous one to tag none.

To see that the image is created run `docker images` and you see something like this:

    REPOSITORY                TAG                 IMAGE ID            CREATED             SIZE
    fiware-cloto-unittests    latest              103464a8ede0        30 seconds ago      551.3 MB
    ...

To execute the unit tests of this component, just execute `docker run --name fiware-cloto-unittests fiware-cloto-unittests`. Finally you can extract the information of the executed tests
just executing `docker cp fiware-cloto-unittests:/opt/fiware-cloto/report .`


> TIP: If you are trying these methods or run them more than once and come across an error saying that the container already exists you can delete it with `docker rm fiware-cloto-unittests`.
If you have to stop it first do `docker stop fiware-cloto-unittests`.

Keep in mind that if you use these commands you get access to the tags and specific versions of fiware-cloto. If you do not specify a version you are pulling from `latest` by default.


----
## 3. Run Acceptance tests

Taking into account that you download the repository from GitHub (See Section **1. The Fastest Way**). This method will launch a container to run the E2E tests of the fiware-cloto component, previously you should launch or configure a FIWARE Lab access. You have to define the following environment variables:

    export KEYSTONE_IP=<IP of the keystone instance>
    export ADM_TENANT_ID=<admin tenant id in the OpenStack environment>
    export ADM_TENANT_NAME=<admin tenant name>
    export ADM_USERNAME=<admin username>
    export ADM_PASSWORD=<admin password>
    export OS_USER_DOMAIN_NAME=<OpenStack user domain name>
    export OS_PROJECT_DOMAIN_NAME=<OpenStack project domain name>

Take it, You should move to the AcceptanceTests folder `./AcceptanceTests`. Just create a new docker image executing `docker build -t fiware-cloto-acceptance .`. To see that the image is created run `docker images` and you see something like this:

    REPOSITORY                 TAG                 IMAGE ID            CREATED             SIZE
    fiware-cloto-acceptance   latest              eadbe0b2e186        About an hour ago   579.3 MB
    fiware-cloto              latest              a46ffad45e60        4 hours ago         480.8 MB
    ...

Now is time to execute the container. This time, we take advantage of the docker compose. Just execute `docker-compose up` to launch the architecture. You can take a look to the log generated executing `docker-compose logs`. If you want to get the result of the acceptance tests, just execute `docker cp docker_fiware-cloto-acceptance_1:/opt/fiware-aiakos/test/acceptance/testreport .`

Please keep in mind that if you do not change the name of the image it will automatically create a new one for unit tests and change the previous one to tag none.

> TIP: you can launch a FIWARE Lab testbed container to execute the fiware-cloto E2E test. Just follow the indications in [FIWARE Testbed Deploy](https://hub.docker.com/r/fiware/testbed-deploy/). It will launch a virtual machine in which a reproduction of the FIWARE Lab is installed. Keep in mind that in that case Region1 have to be configured with the value qaregion.

----
## 4. Other info

Things to keep in mind while working with docker containers and fiware-cloto.

### 4.1 Data persistence
Everything you do with fiware-cloto when dockerized is non-persistent. *You will lose all your data* if you turn off the fiware-cloto container. This will happen with either method presented in this README.

### 4.2 Using `sudo`

If you do not want to have to use `sudo` follow [these instructions](http://askubuntu.com/questions/477551/how-can-i-use-docker-without-sudo).
  
# How to use fiware-cloto with Docker

There are several options to use fiware-cloto very easily using docker. These are (in order of complexity):

- _"Have everything automatically done for me"_. See Section **1. The Fastest Way** (recommended).
- _"Check the unit tests associated to the component"_. See Section **2. Run Unit Test of fiware-cloto**.
- _"Check the acceptance tests are running properly"_ or _"I want to check that my fiware-cloto instance run properly"_ . See Section **3. Run Acceptance tests**.

You do not need to do all of them, just use the first one if you want to have a fully operational fiware-cloto instance and maybe third one to check if your fiware-cloto instance run properly.

You do need to have docker in your machine. See the [documentation](https://docs.docker.com/installation/) on how to do this. Additionally, you can use the proper FIWARE Lab docker functionality to deploy dockers image there. See the [documentation](https://docs.docker.com/installation/)
