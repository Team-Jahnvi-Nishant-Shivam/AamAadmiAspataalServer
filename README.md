# Aam Aadmi Aspataal

Aam Aadmi Aspataal is an online hospital (Android app) to consult doctors and schedule 30 minute appointments for people feeling unsafe to visit hospitals due to COVID pandemic. It includes features like automated appointment scheduling, one-to-one video calling, real-time chat and prescriptions uploading. Also includes applying medical image processing filters on uploaded reports in a single click.

# Set up

This guide helps you set up a development environment
and run the project locally on your workstation. By the end of this guide, you
will have…

* Installed system dependencies
* Initialized development databases
* Running Aam Aadmi Aspataal Server

## Clone Aam Aadmi Aspataal

Aam Aadmi Aspataal is hosted on GitHub at https://github.com/Team-Jahnvi-Nishant-Shivam/AamAadmiAspataalServer.
You can use ``git`` to clone it to your computer

    git clone https://github.com/Team-Jahnvi-Nishant-Shivam/AamAadmiAspataalServer

Install docker
--------------

Aam Aadmi Aspataal server uses Docker for development. This helps you to easily create your development
environment. Therefore, to work on the project, you first need to install Docker.
If you haven't already, follow the [docker installation instructions for your platform](https://docs.docker.com/get-docker/).


## Initialize containers

Next, run

    ./develop.sh build

in the root of the repository. Using ``docker-compose``, this will build multiple
Docker images for the different services that make up the server.

The first time you run this script it might take some time while it downloads all of the
required dependencies and builds the services.

## Initialize databases

Your development environment needs some specific databases to work. Before
proceeding, run these commands to initialize the databases.

    ./develop.sh manage init_db --create-db

Your development environment is now ready. Now, let's actually see Aam Aadmi Aspataal load locally!

## Run the magic script

Now that the databases are initialized, you can start your development
environment by running ``develop.sh up``.

    ./develop.sh up

You will see the output of ``docker-compose``. You can shut down Aam Aadmi Aspataal server by pressing CTRL^C. Once everything is running, visit your new site in a browser!

    http://localhost

Now, you are all set to begin making changes and seeing them in real-time inside
of your local environment. If you make changes to python code, the server will be
automatically restarted. If you make changes to javascript code it will be
automatically compiled.
