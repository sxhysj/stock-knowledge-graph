#!/bin/bash

rm data/import/cayley.nq
python build_csv.py
cayley load -c data/cayley.yml -i data/import/cayley.nq
cayley http -i data/import/cayley.nq --host="192.168.3.13:64210"
