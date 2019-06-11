#!/bin/bash
source venv/bin/activate || . venv/Scripts/activate

export FLASK_APP=hippo_server
export FLASK_ENV=development

echo $FLASK_APP
echo $FLASK_ENV

echo "Done loading venv."