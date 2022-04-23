#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

echo -e "isort :\n"
isort .
echo -e "black :\n"
black app
echo -e "flake8 :\n"
flake8 app
