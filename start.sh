#!/bin/bash

source calendar_micro/bin/activate
calendar_micro/bin/gunicorn --bind 0.0.0.0:5000 app:app --timeout 0 --reload
