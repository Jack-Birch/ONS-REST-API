# ONS-REST-API
This an Office for National Statistics (ONS) Application Programming Interface that I created.
I used flask, flask_restful, and pandas to create the API. The API accesses client information 
(which it should recieve in JSON file format) and identifies the postcode of the client. The Region
of the client is looked up via postcodes.io. Once the region has been identified, the excel 
file is accessed and the average outgoings (for various costs) for the given region are stored in a dictionary. This dictionary
is then formated in a similar style to the input and is returned in a JSON format. 

In this repository there is the client information which is stored in case.json. There is the main.py 
file which contains the code for the API. The test.py when run sends a get request to the server. The
requirements.txt file contains the dependables of my program and the ONSByRegion2019.xlsx contains 
typical expenditure (by region) from the Office for National Statistics. 

To run the program make sure you are in the directory contianing main.py and test.py. Then run 
"python main.py" to start the server. Then by running "python test.py" a get request will be 
sent to the server, with the name of the JSON file.
