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
from pyramid.arima import auto_arima
import time

def predict(x):
	model = auto_arima(x, start_p=1, start_q=1,
                           max_p=10, max_q=2, m=12,
                           start_P=0, seasonal=True,
                           d=1, D=1, trace=True,
                           error_action='ignore',  
                           suppress_warnings=True, 
                           stepwise=True)
	model_fit=model.fit(disp=0)
	output=model_fit.forecast()[0][0]
	print("Predicted Value of ",x[0],": ",output)
	return (x[0],output)

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
    splitdata=data[0].split(',')
    data_hum.append(splitdata[1])
    data_temp.append(splitdata[2])
    data_dew.append(splitdata[3])
    for row in data[1:]:
        splitdata=row.split(',')
        data_hum.append(float(splitdata[1]))
    	data_temp.append(float(splitdata[2]))
    	data_dew.append(float(splitdata[3]))
    
    #Prediction process begins!!!!!
    data_div=[data_hum,data_temp,data_dew]
    results=[]
    for i in range(number):
    	result = spark.sparkContext.parallelize(data_div,3).map(lambda x: predict(x)).collect()
    	
    	for pred in result:
    		if pred[0]=="hum":
    			#hum
    			data_hum.append(pred[1])
    		elif pred[0]=="tempm":
    			#temp
    			data_temp.append(pred[1])
    		elif pred[0]=="dewptm":
    			#dew
    			data_dew.append(pred[1])
    		
    	results.append(result)
    #print("Results: ",results)
    for i in range(number):
    	print("\nIteration: ",i+1,"\n")
    	for pred in results[i]:
    		print("Predicted Value of ",pred[0],": ",pred[1])
    	print("\n")
	
	
    spark.stop()
