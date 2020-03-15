import os, sys, glob
import datetime
import pandas as pd
import numpy as np
print("current datet time is ", datetime.datetime.now())

pd.DataFrame({"col1":[1,2,3]}).to_csv("test.csv")
