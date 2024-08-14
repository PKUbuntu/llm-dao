#!/bin/bash

. .venv/bin/activate 

export  PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python

streamlit run homepage.py
