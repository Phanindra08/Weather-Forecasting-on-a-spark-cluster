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

from pyspark.sql import SparkSession
from statsmodels.tsa.arima_model import ARIMA
import time

def predict(_):
	result=[]
	model=ARIMA(data_hum,order=(5,1,1))
	model_fit=model.fit(disp=0)
	output=model_fit.forecast()[0]
	data_hum.append(output)
	result.append(output)
	print("Predicted Value: "+str(output))
	model=ARIMA(data_temp,order=(5,1,1))
	model_fit=model.fit(disp=0)
	output=model_fit.forecast()[0]
	data_temp.append(output)
	print("Predicted Value: "+str(output))
	result.append(output)
	model=ARIMA(data_dew,order=(5,1,1))
	model_fit=model.fit(disp=0)
	output=model_fit.forecast()[0]
	data_dew.append(output)
	print("Predicted Value: "+str(output))
	result.append(output)
	return result

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: ARIMA <file>", file=sys.stderr)
        exit(-1)

    print("WARN: This is a naive implementation of ARIMA Weather Forecast and is given as an example!\n",
          file=sys.stderr)

    # Initialize the spark context.
    spark = SparkSession\
        .builder\
        .appName("ARIMAWeatherForcast")\
        .getOrCreate()

    data_hum=[]
    data_temp=[]
    data_dew=[]
    data = spark.read.text(sys.argv[1]).rdd.map(lambda r: r[0]).collect()
    number=int(sys.argv[2])
    data=data[1:]
    for row in data:
        splitdata=row.split(',')
        data_hum.append(float(splitdata[1]))
    	data_temp.append(float(splitdata[2]))
    	data_dew.append(float(splitdata[3]))
    #predictions=[]
    #size = int(len(data_hum)*0.999)
    #train,test=data_hum[0:size],data_hum[size:]    
    result = spark.sparkContext.parallelize(range(number),2).map(predict).collect()
    #print(result)
	
	
    spark.stop()
