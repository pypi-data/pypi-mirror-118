#ts2.py

# Author: Riccardo Remo Appino
# Created on: 07/01/2021

# note:

# import external modules ---------------------------------------------------------------------------------------------------------------------------------------------

import pandas as pd 
import json as json
from datetime import datetime as dt

# classes --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class Inconsistent_Input(Exception):
    pass

# metadata standard ------------------------------------------------------------------------------------------------------------------------------------------------------------

metadata_series = {
   'quantity': '',
   'spec': '',
   'area': '', 
   'sample1': '',
   'sample2': '',
   'type': '', 
   'comment': '',
   'normalized': ''
   } 

metadata_json = {
   'ts_start': '',
   'ts_end': '', 
   'ts_freq': '', 
   'study':'',
   'scenario':'',
   'sensitivity': '',
   'source': '',
   'author': '',
   'creation': ''
   } 

standardMetadata = {
   'type': ['historical','elaborated',''], 
}

# check functions --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def check_metadata_series(metadata_ToCheck):# check that metadata_ToCheck is compliant with the standard, to be used for series metadata ----------------------------------------------------------------------------------------------------------------------------

    # input: ...
    # output: ...
    # description: ...
        
    for key in metadata_series:
        if not key in metadata_ToCheck:
            metadata_ToCheck[key] = ''
            print('Missing {}.'.format(key))
        else:
            if key in standardMetadata:
                if not metadata_ToCheck[key] in standardMetadata[key]:
                    print('Value {} not valid for {}; value erased.'.format(metadata_ToCheck[key],key))
                    metadata_ToCheck[key] = ''

    return metadata_ToCheck

def check_metadata_json(metadata_ToCheck): # check that metadata_ToCheck is compliant with the standard, to be used for json metadata ----------------------------------------------------------------------------------------------------------------------------------------

    # input: ...
    # output: ...
    # description: ...
    
    for key in metadata_json:
        if not key in metadata_ToCheck:
            metadata_ToCheck[key] = ''
            print('Missing {}.'.format(key))

    return metadata_ToCheck

def check_add_input(data_json,data,ts_json): # ... ------------------------------------------------------------------------------------------------------------------------------------------------------------

    # check and correct missing and/or not valid values for series metadata

    try: 
        data_json = check_metadata_json(data_json)
    except:
        print ('JSON metadata must be a dictionary.')
        raise Inconsistent_Input('JSON metadata must be a dictionary.')

    # check if data_json is consistent with metadata in ts_json and retrive ID

    try: 
        check_corresponding_metadata(data_json,ts_json) 
    except Inconsistent_Input:
        raise Inconsistent_Input('JSON metadata error.')

    # check and correct missing and/or not valid values for series metadata

    try: 
        data = check_metadata_series(data) 
    except:
        print('Series metadata must be a dictionary.')
        raise Inconsistent_Input('Series metadata must be a dictionary.')

def check_corresponding_metadata(ts_json,metadata_json): # ... ------------------------------------------------------------------------------------------------------------------------------------------------------------

    # input: ...
    # output: ...
    # description: ...

    if not list(ts_json.keys()):
        print('Trying to add a time series to an empty JSON. Initialize JSON before adding time series.')
        raise Inconsistent_Input('Trying to add a time series to an empty JSON. Initialize JSON before adding time series.')
    elif not (ts_json['ts_start'] == metadata_json['ts_start'] and ts_json['ts_end'] == metadata_json['ts_end'] and ts_json['ts_freq'] == metadata_json['ts_freq']):
        print('JSON metadata does not correspond to metadata in selected JSON.')
        raise Inconsistent_Input('JSON metadata does not correspond to metadata in selected JSON.')
    
    return

# main functions --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def save(ts_json,filename): # save ts_json as JSON file with filename -----------------------------------------------------------------------------------------------------------------------------------------

    # input: ...
    # output: ...
    # description: ...
    
    with open(filename, 'w') as outfile:
        json.dump(ts_json, outfile)
    print('JSON file salvato.')

def read(filename): # open JSON file saved as filename as a ts_json dictionary -----------------------------------------------------------------------------------------------------------------------------------------

    with open(filename) as json_file:
        ts_json = json.load(json_file)
    
    return ts_json

def get_metadata_json(ts_json): # get metadata given a JSON file -----------------------------------------------------------------------------------------------------------------------------------------

    # input: ...
    # output: ...
    # description:

    # note: ...

    data_json = metadata_json.copy()

    for key in data_json:
        data_json[key] = ts_json[key]

    return data_json

def get_ID(ts_json): # return the first series ID that can be used to add data to the json ------------------------------------------------------------------------------------------------------------------------------------------------------------

    if not ts_json['series'].keys():
        return 0 #initiate ID to 0 because ts_json is empty
    else:
        return int(list(ts_json['series'].keys())[-1])+1  #initiate ID to last ID in ts_json

def delete_ts(ts_json,filter): # removes from ts_json the seires with the metadata as in filter ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    # list the ID of the series to be removed

    key_toDelete = []

    for key in ts_json['series']:
        deleteTS = True
        for category,list_category in filter.items():
            categoryChecked = False
            for x in list_category:
                categoryChecked = categoryChecked or ts_json['series'][key][category] == x
            deleteTS = deleteTS and categoryChecked
        if deleteTS:
            key_toDelete.append(key)

    # remove the series in the ID list

    for key in key_toDelete:
        ts_json['series'].pop(key)

    return ts_json

def add_fromDF(ts_json, DF, dataToAdd = {}, checkTimeIndex = False): # add series to ts_json retriving the series metadata from the header of the DF -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    data = metadata_series.copy()

    # get ID from ts_json
    tsID = get_ID(ts_json)

    # check consistency of time indexes
    if checkTimeIndex:
        if not (pd.Timestamp(ts_json['ts_start'], freq = ts_json['ts_freq']) == DF.index[0] and pd.Timestamp(ts_json['ts_end'], freq = ts_json['ts_freq']) == DF.index[-1]):
            print('Dataframe index does not match the json metadata. No series added')
            return ts_json

    # clear index 
    DF.reset_index(drop = True, inplace = True)

    # iterate over DF columns
    for (columnName, columnData) in DF.iteritems():
        
        # get metadata from header
        for attribute in DF.columns.names:
            data[attribute] = DF.columns.get_level_values(level = attribute)[DF.columns.get_loc(columnName)]

        #custom data overwrites other data
        for key, value in dataToAdd.items():
            data[key] = value

        # check consistency of data
        data = check_metadata_series(data)

        # add series to ts_json
        data['ts'] = dict(zip(DF[columnName].index.format(), DF[columnName]))
        ts_json['series'][str(tsID)] = data.copy()

        # increase ID
        tsID += 1        

    return ts_json

def toDF(ts_json,metadata,filter,metadata_json = []): # go from JSON to DF with selected metadata -----------------------------------------------------------------------------------------------------------------------------------------

    # input: none
    # output: empty df with ...
    # description:

    if (len(metadata) + len(metadata_json)) > 1:
        my_header = pd.MultiIndex.from_product([[] for x in metadata]+[[] for x in metadata_json],names=metadata)
    else:
        my_header = pd.Index([],name=metadata[0])
    time_index = pd.date_range(start=ts_json['ts_start'], end=ts_json['ts_end'], freq=ts_json['ts_freq'])
    tsdf = pd.DataFrame(index = time_index, columns = my_header)

    for key in ts_json['series']:
        addTs = True
        for category,list_category in filter.items():
            categoryChecked = False
            for x in list_category:
                categoryChecked = categoryChecked or ts_json['series'][key][category] == x
            addTs = addTs and categoryChecked
        if addTs:
            if (len(metadata) + len(metadata_json)) > 1:
                my_header = pd.MultiIndex.from_product([[ts_json['series'][key][category]] for category in metadata]+[[ts_json[category_json]] for category_json in metadata_json],names=metadata)
            else:
                my_header = pd.Index([ts_json['series'][key][metadata[0]]],name=metadata[0])
            tsdf_temp = pd.DataFrame([x for x in ts_json['series'][key]['ts'].values()], index = time_index, columns = my_header)
            tsdf = tsdf.join(tsdf_temp, how = 'left')

    return tsdf

def toDF_singleColumns(ts_json,metadata,filter,metadata_json = []): # go from JSON to DF with selected metadata -----------------------------------------------------------------------------------------------------------------------------------------

    # input: none
    # output: empty df with ...
    # description:

    if (len(metadata) + len(metadata_json)) > 1:
        my_header = pd.MultiIndex.from_product([[] for x in metadata]+[[] for x in metadata_json],names=metadata)
    else:
        my_header = pd.Index([],name=metadata[0])
    time_index = pd.date_range(start=ts_json['ts_start'], end=ts_json['ts_end'], freq=ts_json['ts_freq'])
    tsdf = pd.DataFrame(index = time_index, columns = my_header)

    for key in ts_json['series']:
        addTs = True
        for category,list_category in filter.items():
            categoryChecked = False
            for x in list_category:
                categoryChecked = categoryChecked or ts_json['series'][key][category] == x
            addTs = addTs and categoryChecked
        if addTs:
            if (len(metadata) + len(metadata_json)) > 1:
                my_header = pd.MultiIndex.from_product([[ts_json['series'][key][category]] for category in metadata]+[[ts_json[category_json]] for category_json in metadata_json],names=metadata)
            else:
                my_header = pd.Index([ts_json['series'][key][metadata[0]]],name=metadata[0])
            tsdf_temp = pd.DataFrame([x for x in ts_json['series'][key]['ts'].values()], index = time_index, columns = my_header)
            tsdf = tsdf.join(tsdf_temp, how = 'left')

        # the following code returns one column per metadata

        tsdf = tsdf.stack(level=list(range(0,len(metadata))))
        tsdf = tsdf.to_frame()
        tsdf.reset_index(inplace = True)
        tsdf.rename(columns={0:"value","level_0":"dateTime"},inplace = True)

    return tsdf

def saveExcel(ts_json,fileName,metadata,filter,metadata_json = []): # go from JSON to DF with selected metadata -----------------------------------------------------------------------------------------------------------------------------------------

    # input: none
    # output: empty df with ...
    # description:

    if (len(metadata) + len(metadata_json)) > 1:
        my_header = pd.MultiIndex.from_product([[] for x in metadata]+[[] for x in metadata_json],names=metadata)
    else:
        my_header = pd.Index([],name=metadata[0])
    time_index = pd.date_range(start=ts_json['ts_start'], end=ts_json['ts_end'], freq=ts_json['ts_freq'])
    tsdf = pd.DataFrame(index = time_index, columns = my_header)

    for key in ts_json['series']:
        addTs = True
        for category,list_category in filter.items():
            categoryChecked = False
            for x in list_category:
                categoryChecked = categoryChecked or ts_json['series'][key][category] == x
            addTs = addTs and categoryChecked
        if addTs:
            if (len(metadata) + len(metadata_json)) > 1:
                my_header = pd.MultiIndex.from_product([[ts_json['series'][key][category]] for category in metadata]+[[ts_json[category_json]] for category_json in metadata_json],names=metadata)
            else:
                my_header = pd.Index([ts_json['series'][key][metadata[0]]],name=metadata[0])
            tsdf_temp = pd.DataFrame([x for x in ts_json['series'][key]['ts'].values()], index = time_index, columns = my_header)
            tsdf = tsdf.join(tsdf_temp, how = 'left')

    # get one column per metadata

    tsdf = tsdf.stack(level=list(range(0,len(metadata))))
    tsdf = tsdf.to_frame()
    tsdf.reset_index(inplace = True)
    tsdf.rename(columns={0:"value","level_0":"dateTime"},inplace = True)

    tsdf.to_excel(fileName)  
    print('File excel salvato.')

    return

# Debug section ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":

    pass

    

