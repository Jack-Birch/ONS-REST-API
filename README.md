# ONS-REST-API
This an Office for National Statistics (ONS) Application Programming Interface that I created.
I used flask, flask_restful, and pandas to create the API. The API accesses client information 
(which it should recieve in JSON file format) and identifies the postcode of the client. The Region
of the client is looked up via postcodes.io. Once the region has been identified, the excel 
file is accessed and the average outgoings (for various costs) for the given region are stored in a dictionary. This dictionary
is then formated in a similar style to the input and is returned in a JSON format. 
