import pymupdf
import pandas as pd
from datetime import datetime
import os
import sys
import json
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import jsonschema
import copy

from common_functions import readExcel

configuration = {"test text": "test",
                 "test num": 2,
                 "test array": [1,2,3]
                 }



with open('config1.json', 'w') as json_file:
    json.dump(configuration, json_file, indent=4)