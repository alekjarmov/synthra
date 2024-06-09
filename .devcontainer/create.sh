#!/bin/bash

sudo mkdir /assets && sudo chown vscode /assets

cd /synthra/backend && poetry install --no-root
cd /synthra/backend && poetry run pre-commit install

cd /synthra/frontend && npm i
