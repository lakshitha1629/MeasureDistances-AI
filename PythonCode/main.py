#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pyodbc
import gmplot
import json
import pandasql as ps
import pandas as pd
from datetime import datetime, timezone, timedelta
import dateparser
import numpy as np
import pytz
import json
from urllib import request
from urllib.parse import urlencode
from azure.servicebus import ServiceBusClient, ServiceBusMessage
import vrp
import ast
from multiprocessing import Process
from threading import *


# In[2]:


def checkOrderStoreRejected(ORDERDATAFRAME):
    PROG_START = datetime.utcnow()
    try:
        store_rejected_status = order['OrderStatus']
        store_rejected_OrderId = order['OrderId']
        if(store_rejected_status=='Store-Rejected'):
            print('Order Store-Rejected')
            print('ORDERDATAFRAME',ORDERDATAFRAME)
            ORDERDATAFRAME = ORDERDATAFRAME[ORDERDATAFRAME.Order_ID != store_rejected_OrderId]
            print('ORDERDATAFRAME drop',ORDERDATAFRAME)
            return True
        PROG_END = datetime.utcnow()
        print('Execution Time: check Order Store Rejected {}'.format(PROG_END-PROG_START))   
        return False
    except KeyError:
        PROG_END = datetime.utcnow()
        print('Execution Time: check Order Store Rejected --> KeyError {}'.format(PROG_END-PROG_START))  


# In[3]:


def checkOrderValidity():
    PROG_START = datetime.utcnow()
    try:
        order_time = dateparser.parse(order['ExpectedDeliveryDateTime'])
        treshold = pytz.UTC.localize(datetime.now() - timedelta(hours=1))
        if(order_time > treshold):
            print('Order rejected')
            return False
        PROG_END = datetime.utcnow()
        print('Execution Time: check Order Validity {}'.format(PROG_END-PROG_START))   
        return True
    except KeyError:
        PROG_END = datetime.utcnow()
        print('Execution Time: check Order Validity --> KeyError {}'.format(PROG_END-PROG_START))  
# checkOrderValidity()


# ## Stores Data

# In[4]:


def getOrderItems():
    PROG_START = datetime.utcnow()
    try:
        ordered_items = {}
        items_ordered = {}

        ordered_items[order['OrderId']] = []
        for j in order['OrderItems']:
            items_ordered[j['ItemId']] = {'quantity': 0, 'order_id': []}

        for j in order['OrderItems']:
            ordered_items[order['OrderId']].append(j['ItemId'])
            items_ordered[j['ItemId']]['quantity'] = items_ordered[j['ItemId']]['quantity'] + j['Quantity']
            items_ordered[j['ItemId']]['order_id'].append(order['OrderId'])
        PROG_END = datetime.utcnow()
        print('Execution Time: get Order Items {}'.format(PROG_END-PROG_START))   
        return ordered_items, items_ordered
    except KeyError:
        PROG_END = datetime.utcnow()
        print('Execution Time: get Order Items --> KeyError {}'.format(PROG_END-PROG_START))   
# print(items_ordered)


# In[5]:


def getValidStores(items_ordered):
    PROG_START = datetime.utcnow()
    try:
        stores = pd.DataFrame()
        for i in items_ordered:
            sql_str = "SELECT Inventory.StoreId, Inventory.ArticleId, Article.Weight                         FROM Inventory, Article WHERE Inventory.ArticleId = Article.ArticleId                         AND Inventory.Volume>Inventory.Threshold AND Inventory.ArticleId = {}                         AND Inventory.Volume > {} ".format(str(i), str(items_ordered[i]['quantity']))
            if(stores.empty):
                stores = ps.sqldf(sql_str)
            else:
                stores = stores.append(ps.sqldf(sql_str))
        stores = stores.drop_duplicates()
        order_weight = sum([stores.iloc[i]['Weight'] for i in range(len(stores.index))])
        PROG_END = datetime.utcnow()
        print('Execution Time: get Valid Stores {}'.format(PROG_END-PROG_START))   
        return tuple(list(set([str(stores.iloc[i]['StoreId']) for i in range(len(stores.index))]))), order_weight
    except KeyError:
        PROG_END = datetime.utcnow()
        print('Execution Time: get Valid Stores --> KeyError {}'.format(PROG_END-PROG_START))  
# getValidStores()


# In[6]:


def getValidStoresDetails(STOREDATAFRAME,stores_tuple):
    PROG_START = datetime.utcnow()
    try:
        sql_store_string = "SELECT DISTINCT StoreVehicle.StoreId AS Store_ID, Address, Latitude, Longitude FROM Store INNER JOIN StoreVehicle ON Store.StoreId = StoreVehicle.StoreId WHERE StoreVehicle.StoreId IN {};".format(stores_tuple)
        #print(sql_store_string)
        stores_details = ps.sqldf(sql_store_string)
        stores_details = stores_details.drop_duplicates()
        # store_df.to_csv('Store_data.csv',index=False)
        STOREDATAFRAME = STOREDATAFRAME.append(stores_details)
        STOREDATAFRAME = STOREDATAFRAME.drop_duplicates()
        PROG_END = datetime.utcnow()
        print('Execution Time: get Valid Stores Details {}'.format(PROG_END-PROG_START))   
        return STOREDATAFRAME, stores_details
    except KeyError:
        PROG_END = datetime.utcnow()
        print('Execution Time: get Valid Stores Details --> KeyError {}'.format(PROG_END-PROG_START))   


# In[7]:


def dbToDf(table_name):
    PROG_START = datetime.utcnow()
    try:
        sql_str = "select * from {}".format(table_name)
        df = pd.read_sql(sql_str,conn)
        PROG_END = datetime.utcnow()
        print('Execution Time: database to dataframe {}'.format(PROG_END-PROG_START))   
        return df
    except KeyError:
        PROG_END = datetime.utcnow()
        print('Execution Time: database to dataframe --> KeyError {}'.format(PROG_END-PROG_START))


# ## Order Data

# In[8]:


def getOrderDetails(ORDERDATAFRAME,order_weight):
    PROG_START = datetime.utcnow()
    try:
        order_data = []
        address = order['Address']['Address1']+", "+order['Address']['City']
        location = gmplot.GoogleMapPlotter.geocode(address, apikey=APIKEY)
        order_data.append({'Order_ID': order['OrderId'], 'Address': address, 'Latitude':location[0], 'Longitude': location[1], 'Weight': order_weight, 'ExpectedDeliveryDateTime': order['ExpectedDeliveryDateTime']})
        order_df = pd.DataFrame(order_data)
        #order_df.to_csv('Order_data.csv',index=False)
        #print(ORDERDATAFRAME)
        ORDERDATAFRAME = ORDERDATAFRAME.append(order_df)
        PROG_END = datetime.utcnow()
        print('Execution Time: get Order Details {}'.format(PROG_END-PROG_START))   
        return ORDERDATAFRAME, order_df
    except KeyError:
        PROG_END = datetime.utcnow()
        print('Execution Time: get Order Details --> KeyError {}'.format(PROG_END-PROG_START))


# ## Vehicle Data

# In[9]:


def getVehicleDetails(VEHICLEDATAFRAME, TOTALWEIGHT, ORDERCOMPLETE, order_weight, stores_tuple):
    PROG_START = datetime.utcnow()
    try:
        sql_vehicle_string = "SELECT StoreVehicle.StoreId AS Store_ID,VehicleMaster.VehicleId AS Vehicle_ID,        VehicleMaster.VehicleType AS Vehicle_Type,        VehicleMaster.CapacityLitre AS Capacity,        VehicleMaster.CreatedDate AS 'Availability Start',        VehicleMaster.UpdatedDate AS 'Availability End'        FROM VehicleMaster        INNER JOIN StoreVehicle ON StoreVehicle.VehicleId = VehicleMaster.VehicleId        AND StoreVehicle.StoreId IN {};".format(stores_tuple)
        #print(sql_vehicle_string)
        vehicle_df = ps.sqldf(sql_vehicle_string)
        vehicle_df = vehicle_df.dropna()
        order_time = dateparser.parse(order['ExpectedDeliveryDateTime'])
#         for i in range(len(vehicle_df.index)):
#             start_time = pytz.UTC.localize(dateparser.parse(vehicle_df.iloc[i]['Availability Start']))
#             end_time = pytz.UTC.localize(dateparser.parse(vehicle_df.iloc[i]['Availability End']))
#             if(not(start_time < order_time and end_time> order_time)):
#                 vehicle_df.drop(i)
        vehicle_df = vehicle_df.drop_duplicates(['Vehicle_ID'])
        total_vehicle_capacities = vehicle_df['Capacity'].sum()
        if(total_vehicle_capacities < TOTALWEIGHT and total_vehicle_capacities < TOTALWEIGHT + order_weight):
            PROG_END = datetime.utcnow()
            print('Execution Time: get Vehicle Details --> if(total_vehicle_capacities < TOTALWEIGHT and total_vehicle_capacities < TOTALWEIGHT + order_weight) {}'.format(PROG_END-PROG_START))  
            return VEHICLEDATAFRAME, True, vehicle_df
        else:
            TOTALWEIGHT += order_weight
            VEHICLEDATAFRAME = VEHICLEDATAFRAME.append(vehicle_df)
            VEHICLEDATAFRAME = VEHICLEDATAFRAME.drop_duplicates()
            PROG_END = datetime.utcnow()
            print('Execution Time: get Vehicle Details --> Not if(total_vehicle_capacities < TOTALWEIGHT and total_vehicle_capacities < TOTALWEIGHT + order_weight) {}'.format(PROG_END-PROG_START))  
            return VEHICLEDATAFRAME, False, vehicle_df
    except KeyError:
        PROG_END = datetime.utcnow()
        print('Execution Time: get Vehicle Details --> KeyError {}'.format(PROG_END-PROG_START))  
        return VEHICLEDATAFRAME, False, vehicle_df


# In[10]:


def rejectedOrderJson():
    PROG_START = datetime.utcnow()
    try:
        rejected_order = CUR_ORDER_DF.iloc[-1]
        send_data = {}
        send_data_orders = {}
        send_data_orders['OrderId'] = rejected_order['Order_ID']
        send_data_orders['DeliveryAddress'] = {}
        send_data_orders['OrderStatus'] = 'Rejected'
        send_data_orders['NextSequenceId'] = 0
        send_data_orders['DeliveryAddress']['Latitude'] = rejected_order['Latitude']
        send_data_orders['DeliveryAddress']['Longitude'] = rejected_order['Longitude']
        send_data_orders['ScheduledDeliveryDateTimeStart'] = ''
        send_data_orders['ScheduledDeliveryDateTimeEnd'] = ''
        send_data['Orders'] = []
        send_data['Orders'].append(send_data_orders)
        send_data['Path'] = {}
        send_data['Path']['ScheduledPathId'] = 0
        send_data['Path']['ScheduledStoreId'] = 0
        send_data['Path']['PathDeliveryDateTimeStart'] = ''
        send_data['Path']['ScheduledVehicleId'] = 0
        send_data['Path']['ScheduledDriverId'] = 0
        send_data['Path']['DeliveryType'] = ''
        send_data['Path']['PathStatus'] = ''
        PROG_END = datetime.utcnow()
        print('Execution Time: rejected Order Json {}'.format(PROG_END-PROG_START))   
        return send_data
    except KeyError:
        PROG_END = datetime.utcnow()
        print('Execution Time: rejected Order Json --> KeyError {}'.format(PROG_END-PROG_START))   
        
# rejectedOrderJson()


# In[11]:


'''
    Initializing keys, databases and service bus configuration
'''
#Google API key
APIKEY = 'AIzaSyC2GDcJ58aAx5wnVJpBet5mKbVEmAVW--0'
    
#Azure sql server
SERVER = 'smtdelsqlsereaus01.database.windows.net'
DATABASE = 'smtdelsqldb02'
UID = 'smtdeldev'
PWD = 'SmtDel@2020'   
DRIVER = '{ODBC Driver 17 for SQL Server}'
conn_string = 'DRIVER='+DRIVER+';SERVER='+SERVER+';PORT=1433;DATABASE='+DATABASE+';UID='+UID+";PWD="+PWD
conn = pyodbc.connect(conn_string)
cursor = conn.cursor()
    
    
#Azure service bus
ENDPOINT = "Endpoint=sb://smrdelserbusnamespace.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=1cspxNWpYJlsbMCZaY2tFYu2v+OIc42J1c5klSXIq+I="
LISTENQUEUE = 'smt-del-engine-msg'
SENDQUEUE  = 'smt-del-engine-res-msg'
servicebus_client = ServiceBusClient.from_connection_string(conn_str=ENDPOINT, logging_enable=True)


# In[12]:


def Orders():
    PROG_START = datetime.utcnow()
    try:
        order = []
#         with open('./data_received.json') as f: # Comment this when in deployment
#             order_pre1 = json.load(f)
#         order = order_pre1[0]
        with servicebus_client:
            receiver = servicebus_client.get_queue_receiver(queue_name=LISTENQUEUE, max_wait_time=5)
            with receiver:
                for msg in receiver:
                    print("-----------------------")
                    print("Received Message:" + str(msg))
                    print("-----------------------")
                    message = str(msg)
                    receiver.complete_message(msg)
                    order.append(json.loads(message))
        PROG_END = datetime.utcnow()
        print('Execution Time: Receive Orders {}'.format(PROG_END-PROG_START))          
        return order,True
    except KeyError:
        PROG_END = datetime.utcnow()
        print('Execution Time: Receive Orders --> KeyError {}'.format(PROG_END-PROG_START))  
        return order,False


# In[13]:


def orderProcess(STOREDATAFRAME,ORDERDATAFRAME,VEHICLEDATAFRAME,CUR_ORDER_DF,DRIVER_SHIFT_DF):
    PROG_START = datetime.utcnow()
    print("<------- SUB THREAD -------->")
    try:
        REJECT = False
        store_ids, stores_points, addresses, store_demands = vrp.get_store_location_data(STOREDATAFRAME)
        vehicle_types, capacities, availablity, starts, vehicle_store_ids = vrp.get_store_vehicle_data(VEHICLEDATAFRAME,
                                                                                                       store_ids)
        distance_matrix, nodes = vrp.initialize(stores_points)
        order_ids, demands, drop_points, addresses = vrp.get_order_data(ORDERDATAFRAME)
        distance_matrix, nodes = vrp.generate_distance_matrix(distance_matrix, nodes, drop_points)
        data = vrp.create_data_model(distance_matrix, starts, starts, len(starts), store_demands + demands, capacities)
        solution, manager, routing = vrp.vrp(data)

        routes = vrp.get_routes(data, manager, routing, solution, stores_points + drop_points, vehicle_store_ids, store_ids,
                                order_ids, vehicle_types)
        routes = vrp.get_directions(routes)

        ROUTES_DF_TEMP = pd.DataFrame.from_dict(routes, orient="index")
#         print('ROUTES_DF',ROUTES_DF_TEMP)
        ROUTES_DF = vrp.route_df_explode(ROUTES_DF_TEMP, ['route','durations','durations'], fill_value='')
#         print('ROUTES_DF_VRP',ROUTES_DF)
#         print('CUR_ORDER_DF',CUR_ORDER_DF)

        if (len(stores_tuple) < 1 or not checkOrderValidity() or CUR_STORE_DF.empty or CUR_ORDER_DF.empty or
                CUR_VEHICLE_DF.empty or VEHICLEDATAFRAME.empty or ORDERDATAFRAME.empty or STOREDATAFRAME.empty):
            REJECT = True

        if (MAX_ORDER_COUNT == len(ORDERDATAFRAME)):  # or VEHICLE_FILLED
            #  If order complete apply vehicle routing
            vrp.draw_map(routes, APIKEY)
            fullMessageList = vrp.convertRoutesToJson(routes,DRIVER_SHIFT_DF)

            for send_data_json in fullMessageList:
                print("Sent Full Message:" + str(send_data_json))

                def send_message(sender):
                    message = ServiceBusMessage(str(send_data_json))
                    sender.send_messages(message)

        elif (REJECT):
            send_rejected_data_json = rejectedOrderJson()
            print("Sent Rejected Message:" + str(send_rejected_data_json))

            def send_message(sender):
                message = ServiceBusMessage(str(send_rejected_data_json))
                sender.send_messages(message)

        else:
            send_open_data_json = vrp.openOrderJson(ROUTES_DF,CUR_ORDER_DF)
            print("Sent Open Message:" + str(send_open_data_json))

            def send_message(sender):
                message = ServiceBusMessage(str(send_open_data_json))
                sender.send_messages(message)

        with servicebus_client:
            sender = servicebus_client.get_queue_sender(queue_name=SENDQUEUE)
            with sender:
                send_message(sender)
        print("-----------------------")
        print("Done sending messages")
        print("-----------------------")

        PROG_END = datetime.utcnow()
        print('Execution Time: {}'.format(PROG_END - PROG_START))
    except Exception as exp:
        print("Process Order"+exp)


# In[ ]:


if __name__ == '__main__':
    #Save db to dataframe
    Inventory = dbToDf('[dwh].[Inventory]')
    Article = dbToDf('[dwh].[Article]')
    Store = dbToDf('[dwh].[Store]')
    StoreVehicle = dbToDf('[dwh].[StoreVehicle]')
    VehicleMaster = dbToDf('[dwh].[VehicleMaster]')
    DriverShift = dbToDf('[dwh].[DriverShift]')

    TOTALWEIGHT = 0
    MAX_ORDER_COUNT = 3
    ORDERCOMPLETE = False
    DROPOFF = 900

    ORDERDATAFRAME = pd.DataFrame(columns=['Order_ID', 'Address','Latitude', 'Longitude', 'Weight'])
    STOREDATAFRAME = pd.DataFrame(columns=['Store_ID', 'Address','Latitude', 'Longitude'])
    VEHICLEDATAFRAME = pd.DataFrame(columns=['Store_ID', 'Vehicle_ID','Vehicle_Type', 'Capacity'])

    orders=[]
    while(True):
        try:
            order,order_status = Orders()
            print("<-------MAIN THREAD-------->")

            if order_status:
                orders=orders+order;

            if(len(orders)>0):
                order=orders.pop(0);
                
                if(checkOrderStoreRejected(ORDERDATAFRAME)):
                    print('Store-Rejected')

                else:
                    ordered_items, items_ordered = getOrderItems()
                    stores_tuple, order_weight = getValidStores(items_ordered)

                    # stores_tuple_pre=('C_012',) # remove this in production
                    # stores_tuple = (stores_tuple_pre[0],) + ("None",)

                    STOREDATAFRAME, CUR_STORE_DF = getValidStoresDetails(STOREDATAFRAME, stores_tuple)
#                     print("STOREDATAFRAME", STOREDATAFRAME)
                    ORDERDATAFRAME, CUR_ORDER_DF = getOrderDetails(ORDERDATAFRAME, order_weight)
#                     print("ORDERDATAFRAME", ORDERDATAFRAME)
                    print(order_weight)
                    VEHICLEDATAFRAME, VEHICLE_FILLED, CUR_VEHICLE_DF = getVehicleDetails(VEHICLEDATAFRAME, TOTALWEIGHT,
                                                                                         ORDERCOMPLETE,
                                                                                         order_weight, stores_tuple)
#                     print("VEHICLEDATAFRAME", VEHICLEDATAFRAME)
                    tempThread = Thread(target=orderProcess(STOREDATAFRAME, ORDERDATAFRAME, VEHICLEDATAFRAME,CUR_ORDER_DF,DriverShift))
                    tempThread.start()

                    if (MAX_ORDER_COUNT == len(ORDERDATAFRAME)):
                        Inventory = dbToDf('[dwh].[Inventory]')
                        Article = dbToDf('[dwh].[Article]')
                        Store = dbToDf('[dwh].[Store]')
                        StoreVehicle = dbToDf('[dwh].[StoreVehicle]')
                        VehicleMaster = dbToDf('[dwh].[VehicleMaster]')
                        DriverShift = dbToDf('[dwh].[DriverShift]')

                        # Re init other dataframes
                        ORDERDATAFRAME = pd.DataFrame(columns=['Order_ID', 'Address', 'Latitude', 'Longitude', 'Weight'])
                        STOREDATAFRAME = pd.DataFrame(columns=['Store_ID', 'Address', 'Latitude', 'Longitude'])
                        VEHICLEDATAFRAME = pd.DataFrame(columns=['Store_ID', 'Vehicle_ID', 'Vehicle_Type', 'Capacity'])


            else:
                print("An exception occurred")
                
                
        except:
              print("<-------LISTENQUEUE-------->")

