#!/bin/bash
set -e

uvicorn main:app --reload --port 8081 --host 0.0.0.0 &
streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0