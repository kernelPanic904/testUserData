#!/bin/zsh

alembic upgrade head
python3 start_app.py
