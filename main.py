#Author:Jack Birch
#This my Api. In order to run the api, ensure you are in the directory containing main.py and test.py 
#running "python main.py" starts the server. Then running "python test.py" will send a request to the server with a get 
#request and the name of json file.   

from flask import Flask
from flask_restful import Api, Resource
import json 
import pandas as pd
import requests 

app = Flask(__name__)
api = Api(app)

#Import the region data into a data frame to be manipulated
df_region_1 = pd.read_excel("ONSByRegion2019.xlsx", index_col = 1)
df_region_2 = pd.read_excel("ONSByRegion2019.xlsx", index_col = 2)

#Takes the input caseid and extracts the postcodes into a list
def retrieve_postcode(caseid):
    postcode_list = []

    client_data = json.load(open(caseid + ".json"))
    for element in client_data['clients']:
        postcode_list.append(element['details']['address']['postcode'])

    return postcode_list

#Goes to postcodes.io and retreives json containing the region
def lookup_postcode(postcode_list):
    region = []

    for element in postcode_list:
        url = "http://api.postcodes.io/postcodes/{}"
        url = url.format(element)
        response = requests.get(url)
        region.append(response.json()["result"]["region"])
    
    return region

#Converts the format of the region "East of Englad" to "East" as that is what is used in the excel spreadsheet for easy lookups 
def change_region_format(region_list):
    for element in region_list:
        if element == "East of England":
            region_list[element.index("East of England")] = "East"

    return region_list 

#Finds the required outgoings and stores them in a dictionary for each client
def find_required_fields(region_list):
    outgoings_for_clients = []
    for element in region_list:
        dict_outgoings = {}

        #For the clients lookup there different qualities 
        dict_outgoings["outgoings_communications:"] = str(df_region_1.loc["Communication", element])
        dict_outgoings["outgoings_food:"] = str(df_region_1.loc["Food", element])
        dict_outgoings["outgoings_mortgage_rent:"] = str(df_region_1.loc["Actual rentals for housing", element])
        dict_outgoings["outgoings_mortgage_insurance:"] = str(df_region_1.loc["Insurance", element])
        dict_outgoings["outgoings_mortgage_investments:"] = str(df_region_1.loc["Savings and investments", element])
        dict_outgoings["outgoings_council_tax:"] = str(df_region_1.loc["council tax etc.", element])      #As row index "Housing: mortgage interest payments council tax etc." went over two lines only accepted second line as row index
        dict_outgoings["outgoings_clothing:"] = str(df_region_1.loc["Clothing", element])
        dict_outgoings["outgoings_water:"] = str(df_region_1.loc["relating to the dwelling", element])
        dict_outgoings["outgoings__other_living_costs:"] = str(df_region_1.loc["Electricity, gas and other fuels", element])
        dict_outgoings["outgoings_entertainment:"] = str(df_region_1.loc["processing equipment", element])
        dict_outgoings["outgoings_holidays:"] = str(df_region_1.loc["Package holidays", element])
        dict_outgoings["outgoings_pension"] = str(df_region_1.loc["Life assurance, contributions to pension funds", element])
        dict_outgoings["outgoings_car_costs"] = str(df_region_1.loc["Purchase of vehicles", element])
        dict_outgoings["outgoings_other_transport_costs"] = str(df_region_1.loc["Transport services", element])
        dict_outgoings["outgoings_car_costs"] = str(df_region_1.loc["Purchase of vehicles", element])
        
        dict_outgoings["outgoings_sports:"] = str(df_region_2.loc["and equipment hire", element])
        dict_outgoings["outgoings_child_care"] = str(df_region_2.loc["hire/repair of furniture/furnishings", element])
        dict_outgoings["outgoings_fuel"] = str(df_region_2.loc["Petrol, diesel and other motor oils", element])
        dict_outgoings["outgoings_ground_rent_service_charge_chared_equity_rent"] = str(df_region_2.loc["Second dwelling rent", element])
        #dict_outgoings["outgoings_television_license"] = str(df_region_2.loc["and TV licences", element]) #This lookup didn't work
        dict_outgoings["outgoings_household_repairs"] = str(df_region_2.loc["hire/repair of furniture/furnishings", element])
        
        outgoings_for_clients.append(dict_outgoings)
    
    return outgoings_for_clients

#This will return a dictionary in a similar format to the input including the case ID and client ID for both clients
def format_output(outgoings_for_clients, caseid):
    output = {}
    client_list = []
    
    client_data = json.load(open(caseid + ".json"))
    output["case_id"] = client_data["case_id"]

    index = 0
    for element in client_data['clients']:
        client_dic = {}

        client_dic["client_id"] = element["client_id"]
        client_dic["first_name"] = element["details"]["first_name"]
        client_dic["last_name"] = element["details"]["last_name"]
        client_dic["outgoings"] = outgoings_for_clients[index]
        
        client_list.append(client_dic)
        index += 1

    output["clients"] = client_list
    return output

class data(Resource):
    def get(self, caseid):
        postcode_list = retrieve_postcode(caseid)
        region_list = lookup_postcode(postcode_list)
        region_list = change_region_format(region_list)
        outgoings_for_clients = find_required_fields(region_list)
        return format_output(outgoings_for_clients, caseid)
        
api.add_resource(data, "/data/<string:caseid>")

if __name__ == "__main__":
    app.run(debug = True)

