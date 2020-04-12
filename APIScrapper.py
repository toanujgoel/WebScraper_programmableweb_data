from bs4 import BeautifulSoup
import requests 
import pandas as pd


url = "https://www.programmableweb.com/category/all/apis"

while True:

    data_list = {'api': [],
                 'desc': [],
                 'cat': [],
                 'version': []}
    response = requests.get(url)
    data = response.text
    soup = BeautifulSoup(data,'html.parser')
    api_names = soup.find_all('td',{'class':'views-field views-field-pw-version-title'})
    desc_set = soup.find_all('td',{'class':'views-field views-field-search-api-excerpt views-field-field-api-description hidden-xs visible-md visible-sm col-md-8'})
    cat_set = soup.find_all('td',{'class':'views-field views-field-field-article-primary-category'})
    version_set = soup.find_all('td',{'class':'views-field views-field-pw-version-title'})
    
    for api in api_names:
        
        name = api.find('a').text
        data_list['api'].append(name.encode('utf-8'))
    
    for desc in desc_set:
        desc = desc.text
        data_list['desc'].append(desc.encode('utf-8'))
    
    for cat in cat_set:
        cat_name = cat.find('a')
        cat_name = cat_name.text if cat_name else "N/A"
        data_list['cat'].append(cat_name.encode('utf-8'))
    
    for version in version_set:
        version_name = version.find('a').text
        data_list['version'].append(version_name.encode('utf-8'))
#     
#     print(data_list['api'])

#     for i in range (0,len(data_list['api'])):
#         print("\nAPI NAME : "+data_list['api'][i]+"\nDesc : "+data_list['desc'][i]+"\nCAT : "+data_list['cat'][i]+"\nVersion : "+data_list['version'][i])

    url_tag = soup.find('a',{'title':'Go to next page'})
    if url_tag.get('href'):
        url= 'https://www.programmableweb.com/' + url_tag.get('href')
        print("\nThis page url: "+url)
    else:
        break


api_data_frame = pd.DataFrame.from_dict(data_list)
 
api_data_frame.head(n=15)

api_data_frame.to_csv('API_DATA.csv')


