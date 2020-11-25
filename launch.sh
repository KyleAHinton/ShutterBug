#!/bin/bash
trap "exit" INT TERM ERR

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

cd $DIR
django_cmd="pipenv run python backend/manage.py runserver"
vue_cmd="npm run serve"

$django_cmd &
djangoPID=$!
trap "kill $djangoPID" EXIT
cd shutterbug
$vue_cmd &
vuePID=$!
trap "kill $vuePID" EXIT
wait