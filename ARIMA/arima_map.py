
from __future__ import print_function

import re
import sys
from operator import add

from pyspark.sql import SparkSession
from statsmodels.tsa.arima_model import ARIMA
import time

def predict(x):
	if x[0]=="hum":
		#hum
		p=1
		q=2
	elif x[0]=="tempm":
		#temp
		p=2
		q=2
	elif x[0]=="dewptm":
		#dew
		p=3
		q=2
	d=1
	model=ARIMA(x[1:],order=(p,d,q))
	model_fit=model.fit(disp=0)
	output=model_fit.forecast()[0][0]
	#print("Predicted Value of ",x[0],": ",output)
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
    
    #Prediction process begins
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
