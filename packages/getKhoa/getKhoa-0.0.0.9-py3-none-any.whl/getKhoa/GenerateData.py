"""Khoa data download using api"""
# Author: Chang Je Cho
# License: GNU General Public License v3 (GPLv3)

import requests
import pandas as pd
import numpy as np
import re
       
st_time=pd.DataFrame({'obs_post_name':['가덕도','강화대교','거문도','거제도','경인항',
                               '고흥발포','광양','군산','대산','덕적도',
                               '동해항','마산','모슬포','목포','묵호',
                               '보령','부산','부산항신항','삼천포','서귀포',
                               '서천마량','성산포','속초','순천만','안산',
                               '안흥','어청도','여수','영광','영종대교',
                               '영흥도','완도','울릉도','울산','위도',
                               '인천','인천송도','장항','제주','진도',
                               '추자도','태안','통영','평택','포항',
                               '향화도','후포','흑산도','교본초','복사초',
                               '왕돌초','이어도','옹진소청초','신안가거초','경포대해수욕장',
                               '한수원_온양','한수원_덕천','한수원_나곡','상왕등도','우이도',
                               '생일도','태안항','여수항','통영항','임랑해수욕장',
                               '부산항','완도항','송정해수욕장','광양항','한수원_기장',
                               '한수원_고리','한수원_진하','해운대해수욕장','대천해수욕장','평택당진항',
                               '군산항','경인항','중문해수욕장','인천항','감천항',
                               '마산항','낙산해수욕장','부산항신항','군산항','망상해수욕장',
                               '속초해수욕장','제주남부','대한해협','남해동부','제주해협',
                               '울릉도북동','울릉도북서'],
              'start_time':['2019-11-04','2006-12-01','1982-01-01','2006-01-01','2012-11-01',
                            '2004-12-01','2010-10-01','1980-02-01','2003-01-01','2020-09-28',
                            '2011-12-01','2002-12-01','2003-11-01','1956-01-01','1965-02-01',
                            '1985-09-01','1956-01-01','2011-12-01','2013-12-30','1985-01-01',
                            '2010-10-01','2003-11-01','1973-12-01','2010-01-01','2002-01-01',
                            '2020-09-13','2007-12-01','1965-02-01','2001-11-01','2009-12-01',
                            '2009-08-01','1983-01-01','1965-09-01','1962-09-01','2020-11-12',
                            '1959-05-01','2010-09-01','2003-12-01','1964-01-01','2006-01-01',
                            '1983-10-01','2010-10-01','1976-02-01','1992-06-01','2018-09-13',
                            '2020-09-25','2002-10-01','1965-08-01','2009-08-01','2009-08-01',
                            '2008-12-01','2003-06-01','2016-01-06','2016-01-06','2016-06-21',
                            np.nan,np.nan,np.nan,'2015-07-20','2015-07-19',
                            '2015-07-19','2015-07-28','2015-07-31','2015-09-06','2019-05-10',
                            '2015-10-08','2014-12-15','2017-05-30','2014-11-20',np.nan,
                            np.nan,np.nan,'2010-10-11','2013-07-07','2013-11-02',
                            '2012-06-13','2014-11-27','2014-11-20','2014-11-30','2015-10-30',
                            '2015-08-29','2018-06-30','2015-09-04','2012-06-13',np.nan,
                            '2020-05-20','2010-11-30','2012-09-06','2012-09-06','2012-09-08',
                            '2012-11-22','2012-11-02'
                            ]})

class GetData:
    def __init__(self,key,station_type_list):
        self.key=key#khoa user key
        self.station_type=station_type_list#download station type
        stations,status=self.getData('ObsServiceObj')#station info        
        self.stations=pd.merge(stations,st_time,how='outer')
        
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
            start_time=pd.to_datetime(self.stations.loc[station==self.stations.obs_post_id,'start_time'])
            date_list=[i.strftime('%Y%m%d') for i in time_range if (start_time<=i).values]
            #date_list=[i.strftime('%Y%m%d') for i in time_range]
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

