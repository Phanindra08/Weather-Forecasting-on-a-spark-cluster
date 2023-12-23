#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from __future__ import print_function

import re
import sys
from operator import add
import pyspark
from pyspark.sql import SparkSession
from pyspark.mllib.common import _py2java, _java2py
from pyspark.mllib.linalg import Vectors

from sparkts.models import ARIMA
from sparkts.models.ARIMA import ARIMAModel, fit_model
		
if __name__ == "__main__":
	if len(sys.argv) != 2:
		print("Usage: ARIMA <file>", file=sys.stderr)
		exit(-1)
	print("WARN: This is a naive implementation of ARIMA Weather Forecast and is given as an example!\n",
          file=sys.stderr)

    # Initialize the spark context.
	spark = SparkSession\
        .builder\
        .appName("ARIMAWeatherForcast")\
        .getOrCreate()

    
	data = spark.read.text(sys.argv[1]).rdd.map(lambda r: r[0]).collect()
    
	data_hum=[]
	data_temp=[]
	data_dew=[]
    #data_temp=data[:,2]
    #data_dew=data[:,3]
	row=data[1].split(',')
	for i in range(len(data)):
		row=data[i].split(',')
		data_temp.append(row[2])
		data_hum.append(row[1])
		data_dew.append(row[3])
	size = int(len(data) * 0.999)
	train, test = data[0:size], data[size:len(data)]
	pred=[]
	model=ARIMAModel(5,1,1,test)
	

	spark.stop()
