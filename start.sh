#!/usr/bin/env bash
export PORT=$PORT
gunicorn app:app
