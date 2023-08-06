
import requests
import shapely
import numpy as np
import json
import plotly.express as px
import plotly.figure_factory as ff
import pandas as pd
import plotly.graph_objects as go
class heliRouteService:
    def route(apikey,lst,transport_mode):
		    payload = {'list':'{}'.format(lst),'apikey':'{}'.format(apikey),'transport-mode':'{}'.format(transport_mode)}
		    r = requests.post("https://nav.heliware.co.in/api/route/",data=payload)
		    return  r.json()
    def isochrone(apikey,lat,lon,transport_mode):
        payload = {'lat': lat, 'long':lon,'apikey':'{}'.format(apikey),'transport-mode':'{}'.format(transport_mode)}
        r = requests.get("https://nav.heliware.co.in/api/isochorome/",params=payload)
        return  r.json()

class heliGeoprocessingService:
    
    def Union(apikey,newdata):
        # nd = "{}".format(newdata)
        # data = [{"type": "FeatureCollection", "features": [{"type": "Feature", "properties": {"name": "I1", "styleUrl": "#msn_ylw-pushpin"}, "geometry": {"type": "Polygon", "coordinates": [[[77.4029103817493, 28.36918941103731, 0.0], [77.40184896262588, 28.3722403721131, 0.0], [77.39922678901301, 28.37081966588294, 0.0], [77.40030856003351, 28.36816909494472, 0.0], [77.4029103817493, 28.36918941103731, 0.0]]]}}], "name": "I1"},{"type": "FeatureCollection", "features": [{"type": "Feature", "properties": {"name": "i2", "styleUrl": "#msn_ylw-pushpin"}, "geometry": {"type": "Polygon", "coordinates": [[[77.40486731638147, 28.36831967535351, 0.0], [77.40416140548453, 28.37080235923333, 0.0], [77.40218550684746, 28.3699755298779, 0.0], [77.40187364471585, 28.36769815943599, 0.0], [77.40486731638147, 28.36831967535351, 0.0]]]}}], "name": "i2"}]
        payload = {"apikey":apikey,"data":"{}".format(newdata)}
        r = requests.post("https://ai.heliware.co.in/api/geoprocessing/union/",data=payload)
        return  r.json()
    def Intersection(apikey,newdata):
        # nd = "{}".format(newdata)
        # data = [{"type": "FeatureCollection", "features": [{"type": "Feature", "properties": {"name": "I1", "styleUrl": "#msn_ylw-pushpin"}, "geometry": {"type": "Polygon", "coordinates": [[[77.4029103817493, 28.36918941103731, 0.0], [77.40184896262588, 28.3722403721131, 0.0], [77.39922678901301, 28.37081966588294, 0.0], [77.40030856003351, 28.36816909494472, 0.0], [77.4029103817493, 28.36918941103731, 0.0]]]}}], "name": "I1"},{"type": "FeatureCollection", "features": [{"type": "Feature", "properties": {"name": "i2", "styleUrl": "#msn_ylw-pushpin"}, "geometry": {"type": "Polygon", "coordinates": [[[77.40486731638147, 28.36831967535351, 0.0], [77.40416140548453, 28.37080235923333, 0.0], [77.40218550684746, 28.3699755298779, 0.0], [77.40187364471585, 28.36769815943599, 0.0], [77.40486731638147, 28.36831967535351, 0.0]]]}}], "name": "i2"}]
        payload = {"apikey":apikey,"data":"{}".format(newdata)}
        r = requests.post("https://ai.heliware.co.in/api/geoprocessing/intersection/",data=payload)
        return  r.json()
    def PointBuffer(apikey,lst,area):
        payload = {"apikey":apikey,"area":area,"latlonglist":"{}".format(lst)}
        r = requests.post("https://ai.heliware.co.in/api/geoprocessing/bufferpolygon/",data=payload)
        return  r.json()

    def LineBuffer(apikey,lst,area):
        payload = {"apikey":apikey,"area":area,"latlonglist":"{}".format(lst)}
        r = requests.post("https://ai.heliware.co.in/api/geoprocessing/bufferline/",data=payload)
        return  r.json()
    def PointWithinPoly(apikey,pointdata,polydata):
        payload = {"apikey":apikey,"pointdata":"{}".format(pointdata),"polygondata":"{}".format(polydata)}
        r = requests.post("https://ai.heliware.co.in/api/geoprocessing/pointcheck/",data=payload)
        return r.json()
    def AliasLinestring(apikey,lsd,gap,quantity):
        payload = {"apikey":apikey,"lsd":"{}".format(lsd),"gap":"{}".format(gap),"quantity":"{}".format(quantity)}
        r = requests.post("https://ai.heliware.co.in/api/dls/",data=payload)
        return r.json()
    def CropGeo(apikey,bbdata,geodata):        
        payload = {"apikey":"{}".format(apikey),"bb":"{}".format(bbdata),"gd":"{}".format(geodata)}
        r = requests.post("https://ai.heliware.co.in/api/cg/",data=payload)
        return r.json()
    def PolyGrid(apikey,polygondata,gridsize):
        payload = {"apikey":"{}".format(apikey),"pd":"{}".format(polygondata),"gridsize":"{}".format(gridsize)}
        r = requests.post("https://ai.heliware.co.in/api/pg/",data=payload)
        return r.json()
    def PolyCenter(apikey,polygondata):
        payload = {"apikey":"{}".format(apikey),"pd":"{}".format(polygondata)}
        r = requests.post("https://ai.heliware.co.in/api/fpc/",data=payload)
        return r.json()



class heliVisualizationService:
    def hex_map_from_geojson(ak='',file_path='',hover_properties='',basemap_style='light',hexagon_quantity=10,zoom_level=10):
        if len(ak) > 1:
            res = requests.get("https://ai.heliware.co.in/api/get-api-key/")
            if res.json()['api-key'] == ak:
                px.set_mapbox_access_token(ak)
                if len(file_path) > 1:
                    nd,files = {'new_hp':hover_properties},{'file': open(file_path, 'rb')}
                    response = requests.post('https://ai.heliware.co.in/api/glfg/',data=nd,files=files)
                    if "message" in response.json():
                        raise Exception("Key error hover properties not exist in data")
                    elif "lats" in response.json() and len(response.json()['lats'])>1:
                        df1,df2,df3 = pd.DataFrame(response.json()['lats']),pd.DataFrame(response.json()['lons']),pd.DataFrame(response.json()['name'])
                        df = pd.concat([df1,df2,df3],axis=1)
                        df.columns = ['lat','long',hover_properties]
                        fig = ff.create_hexbin_mapbox(data_frame=df, lat="lat", lon="long",nx_hexagon=hexagon_quantity, opacity=1,labels={"color":hover_properties},color=hover_properties,zoom=zoom_level)
                        fig.update_layout(mapbox_style=basemap_style,margin=dict(b=0, t=0, l=0, r=0))
                        return fig
                else:
                    raise Exception("please provide a valid file path")
            else:
                raise Exception("Api key is not valid!!!")
        else:
            raise Exception("Please provide a valid api key!!!!")
        
       
    def hex_map_from_csv(ak='',file_path='',lat_col_name='',long_col_name='',hover_properties='',basemap_style='light',hexagon_quantity=10,zoom_level=10):
        if len(ak) > 1:
            res = requests.get("https://ai.heliware.co.in/api/get-api-key/")
            if res.json()['api-key'] == ak:
                px.set_mapbox_access_token(ak)
                if len(file_path) > 1:
                    nd,files = {'new_hp':hover_properties,'lcn':lat_col_name,'longcn':long_col_name},{'file': open(file_path, 'rb')}
                    response = requests.post('https://ai.heliware.co.in/api/glfg/',data=nd,files=files)
                    if "message" in response.json():
                        raise Exception("KeyError!!")
                    elif "lats" in response.json() and len(response.json()['lats'])>0:
                        df1,df2,df3 = pd.DataFrame(response.json()['lats']),pd.DataFrame(response.json()['lons']),pd.DataFrame(response.json()['name'])
                        df = pd.concat([df1,df2,df3],axis=1)
                        df.columns = ['lat','long',hover_properties]
                        fig = ff.create_hexbin_mapbox(data_frame=df, lat="lat", lon="long",nx_hexagon=hexagon_quantity, opacity=1,labels={"color":hover_properties},color=hover_properties,zoom=zoom_level)
                        # fig.update_layout(mapbox_style=basemap_style,margin=dict(b=0, t=0, l=0, r=0))
                        # fig.show()
                        return fig 

                else:
                    raise Exception("please provide a valid file path")
            else:
                raise Exception("Api key is not valid!!!")
        else:
            raise Exception("Please provide a valid api key!!!!")
          
    def scatter_map_from_geojson(ak='',file_path='',hover_properties='',basemap_style='light',zoom_level=10):
        if len(ak) > 1:
            res = requests.get("https://ai.heliware.co.in/api/get-api-key/")
            if res.json()['api-key'] == ak:
                px.set_mapbox_access_token(ak)
                if len(file_path) > 1:
                    nd,files = {'new_hp':hover_properties},{'file': open(file_path, 'rb')}
                    response = requests.post('https://ai.heliware.co.in/api/glfg/',data=nd,files=files)
                    if "message" in response.json():
                        raise Exception("Key error hover properties not exist in data")
                    elif "lats" in response.json() and len(response.json()['lats'])>0:
                        df1,df2,df3 = pd.DataFrame(response.json()['lats']),pd.DataFrame(response.json()['lons']),pd.DataFrame(response.json()['name'])
                        # df1,df2,df3 = pd.DataFrame(lats),pd.DataFrame(lons),pd.DataFrame(name)
                        df = pd.concat([df1,df2,df3],axis=1)
                        df.columns = ['lat','long',hover_properties]
                        fig = px.scatter_mapbox(df, lat="lat", lon="long",labels={"color":hover_properties},color=hover_properties,zoom=zoom_level)
                        fig.update_layout(mapbox_style=basemap_style)
                        fig.update_layout(mapbox_style=basemap_style,margin=dict(b=0, t=0, l=0, r=0))
                        return fig
                else:
                    raise Exception("please provide a valid file path")
            else:
                raise Exception("Api key is not valid!!!")
        else:
            raise Exception("Please provide a valid api key!!!!")

    def scatter_map_from_csv(ak='',file_path='',lat_col_name='',long_col_name='',hover_properties='',basemap_style='light',zoom_level=10):
        if len(ak) > 1:
            res = requests.get("https://ai.heliware.co.in/api/get-api-key/")
            if res.json()['api-key'] == ak:
                px.set_mapbox_access_token(ak)
                if len(file_path) > 1:
                    nd,files = {'new_hp':hover_properties,'lcn':lat_col_name,'longcn':long_col_name},{'file': open(file_path, 'rb')}
                    response = requests.post('https://ai.heliware.co.in/api/glfg/',data=nd,files=files)
                    if "message" in response.json():
                        raise Exception("KeyError!!")
                    elif "lats" in response.json() and len(response.json()['lats'])>0:
                        df1,df2,df3 = pd.DataFrame(response.json()['lats']),pd.DataFrame(response.json()['lons']),pd.DataFrame(response.json()['name'])
                        df = pd.concat([df1,df2,df3],axis=1)
                        df.columns = ['lat','long',hover_properties]
                        fig = px.scatter_mapbox(df, lat="lat", lon="long",labels={"color":hover_properties},color=hover_properties,zoom=zoom_level)
                        fig.update_layout(mapbox_style=basemap_style)
                        # fig.update_layout(mapbox_style=basemap_style,margin=dict(b=0, t=0, l=0, r=0))
                        return fig

                else:
                    raise Exception("please provide a valid file path")
            else:
                raise Exception("Api key is not valid!!!")
        else:
            raise Exception("Please provide a valid api key!!!!")
          
    def line_map_from_geojson(ak='',file_path='',hover_properties='',basemap_style='light',zoom_level=10):
        if len(ak) > 1:
            res = requests.get("https://ai.heliware.co.in/api/get-api-key/")
            if res.json()['api-key'] == ak:
                px.set_mapbox_access_token(ak)
                if len(file_path) > 1:
                    nd,files = {'new_hp':hover_properties},{'file': open(file_path, 'rb')}
                    response = requests.post('https://ai.heliware.co.in/api/glfg2/',data=nd,files=files)
                    if "message" in response.json():
                        raise Exception("Key error hover properties not exist in data")
                    elif "lats" in response.json() and len(response.json()['lats'])>0:
                        df1,df2,df3 = pd.DataFrame(response.json()['lats']),pd.DataFrame(response.json()['lons']),pd.DataFrame(response.json()['name'])
                        df = pd.concat([df1,df2,df3],axis=1)
                        df.columns = ['lat','long',hover_properties]
                        fig = px.line_mapbox(df, lat="lat", lon="long",labels={"color":hover_properties},color=hover_properties,zoom=zoom_level)
                        fig.update_layout(mapbox_style=basemap_style)
                        return fig
                else:
                    raise Exception("please provide a valid file path")
            else:
                raise Exception("Api key is not valid!!!")
        else:
            raise Exception("Please provide a valid api key!!!!")
            


    def fill_geo_map_from_geojson(ak='',file_path='',color='red',basemap_style='carto-positron',legend=False,zoom_level=5):
        if len(ak) > 1:
            res = requests.get("https://ai.heliware.co.in/api/get-api-key/")
            if res.json()['api-key'] == ak:
                px.set_mapbox_access_token(ak)
                if len(file_path) > 1:
                    files ={'file': open(file_path, 'rb')}
                    response = requests.post('https://ai.heliware.co.in/api/glfg3/',files=files)
                    if "message" in response.json():
                        raise Exception("Key error hover properties not exist in data")
                    elif "lats" in response.json() and len(response.json()['lats'])>0:
                        lats,lons= response.json()['lats'],response.json()['lons']
                        fig = go.Figure(go.Scattermapbox(
                        fill = "toself",
                        lon = lons, lat = lats,
                        marker = { 'size': 10, 'color': color }))

                        fig.update_layout(
                            mapbox = {
                                'style': basemap_style,
                                'zoom': zoom_level},
                            showlegend =legend)
                        return fig
                else:
                    raise Exception("please provide a valid file path")
            else:
                raise Exception("Api key is not valid!!!")
        else:
            raise Exception("Please provide a valid api key!!!!")
            

    def density_map_from_geojson(ak='',file_path='',hover_properties='',basemap_style='light',zoom_level=10):
        if len(ak) > 1:
            res = requests.get("https://ai.heliware.co.in/api/get-api-key/")
            if res.json()['api-key'] == ak:
                px.set_mapbox_access_token(ak)
                if len(file_path) > 1:
                    nd,files = {'new_hp':hover_properties},{'file': open(file_path, 'rb')}
                    response = requests.post('https://ai.heliware.co.in/api/glfg/',data=nd,files=files)
                    if "message" in response.json():
                        raise Exception("Key error hover properties not exist in data")
                    elif "lats" in response.json() and len(response.json()['lats'])>0:
                        df1,df2,df3 = pd.DataFrame(response.json()['lats']),pd.DataFrame(response.json()['lons']),pd.DataFrame(response.json()['name'])
                        df = pd.concat([df1,df2,df3],axis=1)
                        df.columns = ['lat','long',hover_properties]
                        fig = px.density_mapbox(df, lat='lat', lon='long', z=hover_properties, radius=20,zoom=zoom_level,mapbox_style=basemap_style)
                        return fig
                else:
                    raise Exception("please provide a valid file path")
            else:
                raise Exception("Api key is not valid!!!")
        else:
            raise Exception("Please provide a valid api key!!!!")
            
           

    def density_map_from_csv(ak='',file_path='',lat_col_name='',long_col_name='',hover_properties='',basemap_style='light',zoom_level=16):
        if len(ak) > 1:
            res = requests.get("https://ai.heliware.co.in/api/get-api-key/")
            if res.json()['api-key'] == ak:
                px.set_mapbox_access_token(ak)
                if len(file_path) > 1:
                    nd,files = {'new_hp':hover_properties,'lcn':lat_col_name,'longcn':long_col_name},{'file': open(file_path, 'rb')}
                    response = requests.post('https://ai.heliware.co.in/api/glfg/',data=nd,files=files)
                    if "message" in response.json():
                        raise Exception("KeyError!!")
                    elif "lats" in response.json() and len(response.json()['lats'])>0:
                        df1,df2,df3 = pd.DataFrame(response.json()['lats']),pd.DataFrame(response.json()['lons']),pd.DataFrame(response.json()['name'])
                        df = pd.concat([df1,df2,df3],axis=1)
                        df.columns = ['lat','long',hover_properties]
                        fig = px.density_mapbox(df, lat='lat', lon='long', z=hover_properties, radius=10,zoom=0,mapbox_style=basemap_style)
                        return fig

                else:
                    raise Exception("please provide a valid file path")
            else:
                raise Exception("Api key is not valid!!!")
        else:
            raise Exception("Please provide a valid api key!!!!")
        