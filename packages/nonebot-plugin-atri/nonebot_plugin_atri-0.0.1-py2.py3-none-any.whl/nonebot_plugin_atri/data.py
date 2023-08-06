#!/usr/bin/python3
# coding: utf-8
import json
from pathlib import Path

V_PATH = str(Path("resources/voice").absolute()) + "/"
T_PATH = str(Path("resources/text").absolute()) + "/"

with open(f"{T_PATH}atri.json", "r", encoding="utf-8") as file:
    atri_text = json.load(file)
