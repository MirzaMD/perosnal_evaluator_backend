#!/usr/bin/env bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker src.app.main:app
