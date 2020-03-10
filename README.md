Hawaii Vacation Analysis

 A basic climate analysis and data exploration using data from a sqlite database. The analysis was completed using SQLAlchemy ORM queries, Pandas, and Matplotlib.  The initial analysis was of twelve months of preciptation and graphed using Matplotlib (see Output/precipatation.png files for pictures of the graph).  

Queries were used to learn the total number of stations and the most active stations.  The data was then sorted in a pandas dataframe in descending order to discover which station had the highest number of observations.

Lastly, after retrieving 12cmonths of tempature observations, the data was ploted by tempature and frequency. (see Output/climate_analysis.png files for pictures of the graph).  

The code was then used to create a python / Flask API app to create a webpage of the data.
