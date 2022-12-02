
from client import RestClient
import requests
from config_reader import ConfigReader
import time
import requests
import json
from collections import defaultdict
from serpapi import GoogleSearch

config_reader = ConfigReader()
configuration = config_reader.read_config()

def DataForSeo(keyword,region):
    

    
    
    # You can download this file from here https://cdn.dataforseo.com/v3/examples/python/python_Client.zip
    client = RestClient( configuration['DATA_FOR_SEO_USERNAME'], configuration['DATA_FOR_SEO_API'])


    post_data = dict()
    # simple way to set a task
    post_data[len(post_data)] = dict(
        location_name=region,
        keywords=[keyword],
        
        language_name="English"


    )
    # POST /v3/keywords_data/google_ads/search_volume/live
    # the full list of possible parameters is available in documentation
    response = client.post("/v3/keywords_data/google_ads/search_volume/live", post_data)
    # you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors
    if response["status_code"] == 20000:
        #print(response)
        dataforseo_result=response
        return dataforseo_result['tasks'][0]['result'][0]
        # do something with result
    else:
        #print("error. Code: %d Message: %s" % (response["status_code"], response["status_message"]))
        return ("error. Code: %d Message: %s" % (response["status_code"], response["status_message"]))

def serpapi(keyword,region,gl):
    
    
#     gl={'united states':"us",'india':"in",'united kingdom':"uk"}
    
    params = {
      "device": "desktop",
      "engine": "google",
      "google_domain": "google.com",
      "q": keyword,
      "gl":gl,
      "hl": "en",
      "location": region,
      "api_key":  configuration['SERP_API']
            }
#     print(params)
    search = GoogleSearch(params)
    results = search.get_dict()
#     print(results)
    ads_results = results.get('ads')
    shopping_results = results.get('shopping_results')
    
    if shopping_results and ads_results:

        
        return_dict= {'ads_results': ads_results, 'shopping_results': shopping_results}
        # return_dict['statistic_information']: None

    elif ads_results and not shopping_results:
        
        return_dict= {'ads_results': ads_results,
                                          'shopping_results': "No Shopping Results for this keyword in this particular location."}
        # return_dict['statistic_information'] = None

    elif shopping_results and not ads_results:
        
        return_dict = {'ads_results': 'No Ads for this keyword in this particular location!',
                                          'shopping_results': shopping_results}
        # return_dict['statistic_information'] = None
    else:
               
        
        return_dict = {'ads_results': 'No Ads for this keyword in this particular location!',
                                          'shopping_results':  'No shopping results for this keyword in this particular location!'}
        # return_dict['statistic_information'] = None
        
    

    return return_dict

def main_output(keyword,country,gl):
    
    
    try:
        

        
                     
        dataforseo_result=DataForSeo(keyword,country)
        #dataforseo_result=dataforseo_result['tasks'][0]['result'][0]
#         print(dataforseo_result)
        serpapi_results=serpapi(keyword,country,gl)
#         print(serpapi_results)
        
        output_dict={'keyword':keyword,'scraping_result':serpapi_results,'statistic_information':dataforseo_result}
#         print(output_dict)
        
    
       
                      

        return output_dict

     
    except Exception as e:

        error={'error':e}
        return error


# print(main_output('shoes','united states'))
