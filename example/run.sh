#!/usr/bin/env bash
gunicorn -b :9000 -k flask_sockets.worker flask_ws:app --debug  --log-level info