#!/bin/bash

SQLALCHEMY_DATABASE_URI="postgresql://aam_aadmi_aspataal:aam_aadmi_aspataal@db:5432/aam_aadmi_aspataal"

if [[ ! -d "docker" ]]; then
    echo "This script must be run from the top level directory of the aam_aadmi_aspataal source."
    exit -1
fi

function invoke_docker_compose {
    docker-compose -f docker/docker-compose.yml \
                -p aam_aadmi_aspataal \
                "$@"
}

function invoke_manage {
    invoke_docker_compose run --rm api_server \
            python3 manage.py \
            "$@"
}

function open_psql_shell {
    invoke_docker_compose run --rm api_server psql \
        $SQLALCHEMY_DATABASE_URI
}

if [ "$1" == "manage" ]; then shift
    echo "Invoking manage.py..."
    invoke_manage "$@"
    exit

elif [ "$1" == "psql" ]; then
    echo "Entering into PSQL shell to query DB..."
    open_psql_shell
    exit

else
    echo "Running docker-compose with the given command..."
    invoke_docker_compose "$@"
fi
