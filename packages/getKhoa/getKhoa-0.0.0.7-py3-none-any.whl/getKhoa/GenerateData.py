"""Khoa data download using api"""
# Author: Chang Je Cho
# License: GNU General Public License v3 (GPLv3)

import requests
import pandas as pd
import numpy as np
import re
       
class GetData:
    def __init__(self,key,station_type_list):
        self.key=key#khoa user key
        self.station_type=station_type_list#download station type
        stations,status=self.getData('ObsServiceObj')#station info
        self.stations=stations
        
    def getData(self,data_type,add_query='',timeout=10):
        base=f'http://www.khoa.go.kr/oceangrid/grid/api/{data_type}/search.do?ServiceKey={self.key}&ResultType=json'
        query=f'{base}{add_query}'
        res=requests.get(query, timeout=timeout)
        if res.status_code==200:
            _res=res.json()['result']
            if 'meta' in _res.keys():
                print(f"remaining query : {_res['meta']['obs_last_req_cnt']}")
            if not 'error' in _res.keys():
                return pd.DataFrame.from_dict(_res['data']),res.status_code
            else:
                return pd.DataFrame([]),res.status_code
        else:
            return pd.DataFrame([]),res.status_code

    def getMetaData(self,data_type,add_query='',timeout=10):
        base=f'http://www.khoa.go.kr/oceangrid/grid/api/{data_type}/search.do?ServiceKey={self.key}&ResultType=json'
        query=f'{base}{add_query}'
        res=requests.get(query, timeout=timeout)
        if res.status_code==200:
            _res=res.json()['result']['meta']
            print(f"remaining query : {_res['meta']['obs_last_req_cnt']}")
            return _res,res.status_code

    def getSeafogData(self,data_type,add_query='',timeout=10):
            base=f'http://www.khoa.go.kr/oceangrid/grid/api/{data_type}/search.do?ServiceKey={self.key}&ResultType=json'
            query=f'{base}{add_query}'
            res=requests.get(query, timeout=timeout)
            if res.status_code==200:
                _res=res.json()['result']
                if 'meta' in _res.keys():
                    print(int(_res['meta']['obs_last_req_cnt'].split('/')[0]))
                print(not 'error' in _res.keys())
                if not 'error' in _res.keys():
                    out=pd.DataFrame.from_dict(_res['data']).stack(
                        dropna=False).reset_index().set_index('level_1') .drop('level_0',axis=1).T
                    out.columns=['pre_time_3h','under_vis_1000_prob_3h','prob_3h','under_vis_500_prob_3h',
                                 'pre_time_6h','under_vis_1000_prob_6h','prob_6h','under_vis_500_prob_6h',
                                 'pre_time_9h','under_vis_1000_prob_9h','prob_9h','under_vis_500_prob_9h']
                    return out,res.status_code
                
    def downloadApi(self,start_date,end_date,
                    add_query='',time_type='H',station_list=[],
                    data_type_list=['tideObs','tideObsTemp','tideObsSalt','tideObsAirTemp','tideObsAirPres','tideObsWind']):
        #station infomation 
        ls=list()
        for station_type in self.station_type:
            print(station_type)
            ls.append(self.stations[self.stations['data_type'].str.findall(station_type).str[0].notna()])
        station_df=pd.concat(ls)
        
        #station list
        if len(station_list)==0:
            station_list=station_df.obs_post_id.values
        err_station=list();err_date=list();err_data_type=list()
        out_dfs=list()
        time_range=pd.date_range(
                    pd.to_datetime(start_date), pd.to_datetime(end_date), freq='1D')
        for station in station_list:
            date_list=[i.strftime('%Y%m%d') for i in time_range]
            data_list=list()
            _col=set()#자료가 없는경우 애러에 대한 예외처리
            for data_type in data_type_list:
                dfs=list()
                for date in date_list:
                    time_list=pd.date_range(pd.to_datetime(date), pd.to_datetime(date)+pd.to_timedelta(1,unit='d'), freq=time_type)
                    if not self.stations.loc[self.stations['obs_post_id']==station,'data_type'].values in ['조위관측소','해양관측소']:#(해양관측소 조위관측소) 
                        data_type=data_type.replace('tideObs','tidalBu')
                    temp_df,status=self.getData(data_type,add_query=f'&ObsCode={station}&Date={date}')
                    if status!=200:
                        err_station.append(station)
                        err_date.append(date)
                        err_data_type.append(data_type)
                        
                    if temp_df.shape[0]!=0:
                        #날짜 결측 제거
                        time_name=[i for i in temp_df.columns if re.compile('time').findall(i)][0]
                        temp_df[time_name]=pd.to_datetime(temp_df[time_name])
                        temp_df=temp_df.set_index(time_name)
                        if time_type=='H':
                            temp_df=temp_df[temp_df.index.minute==0]
                        temp_df=temp_df.reset_index()
                        na_date=set(time_list)-set(temp_df[time_name])
                        if len(na_date)!=0:
                            temp_df=pd.concat([temp_df,pd.Series(list(na_date)).to_frame(name=time_name)],axis=0)
                            temp_df=temp_df.sort_values(time_name)
                        temp_df=temp_df.reset_index().drop('index',axis=1)
                        temp_df=temp_df.set_index(time_name)
                        temp_df=temp_df.loc[pd.to_datetime(date).strftime('%Y-%m-%d')]
                        temp_df=temp_df.reset_index()
                        dfs.append(temp_df)
                        print(station,data_type ,date ,temp_df.shape)
                    else:
                        print(date,'data empty')
                if len(dfs)!=0:
                    data_list.append(pd.concat(dfs))
            try:
                df=pd.concat(data_list,axis=1)
                df['obs_post_id']=station
                if sum(df.columns==time_name)>1:
                    record_time=df[time_name].iloc[:,0].values
                    df=df.drop(time_name,axis=1)
                    df[time_name]=record_time
                df=df.drop_duplicates()
                out_dfs.append(df)
                out_type=0
                _col.update(df.columns)
            except:
                out_type=1
        if out_type==0:            
            for i in range(len(out_dfs)):
                diff_columns=list(_col-set(out_dfs[i].columns))
                print(list(diff_columns))
                if len(diff_columns)!=0:
                    for gen_col in diff_columns:
                        out_dfs[i][gen_col]=np.NaN
                out_dfs[i]=out_dfs[i][list(_col)]
            return pd.concat(out_dfs),pd.DataFrame({'station':err_station,'date':err_date,'data_type':err_data_type})
        else:
            return data_list,pd.DataFrame({'station':err_station,'date':err_date,'data_type':err_data_type})

