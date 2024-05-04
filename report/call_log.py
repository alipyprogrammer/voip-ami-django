from django.shortcuts import render
from queuelog.models import *
import pandas as pd



def Call_log_report(Start, End, Type, Agent:list, Queuename:list,company):

    ###############
    #FILTER_QUERY
    if company=='hamkadeh':
        if Agent !=[]:
            Agent=[int(i) for i in Agent]
            Queue_log=QueueLoghamkadeh.objects.using("hamkadeh").filter(time__gte=Start, time__lte=End, agent__in=Agent )

        else:
            Queue_log=QueueLoghamkadeh.objects.using("hamkadeh").filter(time__gte=Start, time__lte=End)


        if Queuename !=[]:
            Queuename=[int(i) for i in Queuename]
            Queue_log=Queue_log.filter(time__gte=Start, time__lte=End, Queuename__in=Agent )
        else:
            Queue_log=Queue_log.filter(time__gte=Start, time__lte=End)


    elif company=="5040":
        if Agent !=[]:
            Agent=[int(i) for i in Agent]
            Queue_log=QueueLog.objects.using("5040").filter(time__gte=Start, time__lte=End, agent__in=Agent )
        else:
            Queue_log=QueueLog.objects.using("5040").filter(time__gte=Start, time__lte=End)


        if Queuename !=[]:
            Queuename=[int(i) for i in Queuename]            
            Queue_log=Queue_log.filter(time__gte=Start, time__lte=End, queuename__in=Queuename )
        else:

            Queue_log=Queue_log.filter(time__gte=Start, time__lte=End) 

    ###############

    ##############
    #create_df
    queue = Queue_log.values("event", "callid", "agent", "queuename", "data1", "data2", "data3", "data4", "data5","time")  

    list_Queue=list(queue)
    Queue_DF = pd.DataFrame.from_records(list_Queue)
    Queue_DF=pd.DataFrame(list_Queue)
        
    ##############

    #############
    #get_phone



    try:
        Queue_DF['time']=Queue_DF['time'].apply(lambda x:x.hour)

        
        get_phone_df=Queue_DF[Queue_DF['event']=='ENTERQUEUE']
        
        Queue_DF_connect_to_agent_COMPLETECALLER=Queue_DF[Queue_DF['event']=='COMPLETECALLER']
        Queue_DF_connect_to_agent_COMPLETEAGENT=Queue_DF[(Queue_DF['event']=='COMPLETEAGENT')]
        Queue_DF_connect_to_agent_RINGNOANSWER=Queue_DF[(Queue_DF['event']=='RINGNOANSWER')]   


        Queue_DF_connect_to_agent_RINGNOANSWER=Queue_DF_connect_to_agent_RINGNOANSWER[Queue_DF_connect_to_agent_RINGNOANSWER['data1']!='0']
        Queue_DF_connect_to_agent_RINGNOANSWER=Queue_DF_connect_to_agent_RINGNOANSWER[Queue_DF_connect_to_agent_RINGNOANSWER['data1']!='1000']
  


        
        
        
        if Type=='call':
            Queue_DF_connect_to_agent_COMPLETECALLER["data1"]=Queue_DF_connect_to_agent_COMPLETECALLER["data1"].apply(lambda x:int(x))
            Queue_DF_connect_to_agent_RINGNOANSWER["data1"]=Queue_DF_connect_to_agent_RINGNOANSWER["data1"].apply(lambda x:int(x))
            Queue_DF_connect_to_agent_COMPLETEAGENT["data1"]=Queue_DF_connect_to_agent_COMPLETEAGENT["data1"].apply(lambda x:int(x))
            
            
      
            
            
            voip_report=get_phone_df.loc[:, ['callid', 'data2']]    
            voip_report=voip_report.rename(columns={"data2":"mobile"})             
            Queue_DF_NOT_connect_to_agent=Queue_DF[(Queue_DF['event']=='ABANDON')]
            Queue_DF_NOT_connect_to_agent_hold_sum=Queue_DF_NOT_connect_to_agent.groupby(["callid"])["data3"].sum()
            Queue_DF_NOT_connect_to_agent_hold_sum = Queue_DF_NOT_connect_to_agent_hold_sum.to_frame().reset_index()  
            Queue_DF_NOT_connect_to_agent_hold_sum=Queue_DF_NOT_connect_to_agent_hold_sum.rename(columns={"data3":"ABANDON"})
            voip_report=voip_report.merge(Queue_DF_NOT_connect_to_agent_hold_sum,on="callid",how="outer").fillna(0)



            Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum=Queue_DF_connect_to_agent_COMPLETECALLER.groupby(["callid"])["data1"].sum()
            Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum = Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum.to_frame().reset_index() 
            Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum=Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum.rename(columns={"data1":"COMPLETECALLER"})
            voip_report=voip_report.merge(Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum,on="callid",how="outer").fillna(0)

            
            
            

            Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum=Queue_DF_connect_to_agent_COMPLETEAGENT.groupby(["callid"])["data1"].sum()
            Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum = Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum.to_frame().reset_index()            
            Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum=Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum.rename(columns={"data1":"COMPLETEAGENT"})
            voip_report=voip_report.merge(Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum,on="callid",how="outer").fillna(0)
            
            
           
            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum=(Queue_DF_connect_to_agent_RINGNOANSWER.groupby(["callid"])["data2"].sum())/1000
            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum = Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum.to_frame().reset_index() 
            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum=Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum.rename(columns={"data1":"MISS_DURATION"})
            voip_report=voip_report.merge(Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum,on="callid",how="outer").fillna(0)




            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum=Queue_DF_connect_to_agent_RINGNOANSWER.groupby(["callid"])["data1"].count()
            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum = Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum.to_frame().reset_index() 
            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum=Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum.rename(columns={"data1":"TRY"})
            voip_report=voip_report.merge(Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum,on="callid",how="outer").fillna(0)

            
            voip_report["COMPLETECALLER"]=voip_report["COMPLETECALLER"].apply(lambda x:int(x))
            voip_report["MISS_DURATION"]=voip_report["MISS_DURATION"].apply(lambda x:int(x))
            voip_report["COMPLETEAGENT"]=voip_report["COMPLETEAGENT"].apply(lambda x:int(x))
            voip_report["ABANDON"]=voip_report["ABANDON"].apply(lambda x:int(x))


            # print(type(voip_report['MISS_DURATION'][0]))
            # print(type(voip_report["COMPLETEAGENT"][0]))
            # print(type(voip_report["COMPLETECALLER"][0]))
            # print(type(voip_report["ABANDON"][0]))          


            voip_report['SUM'] = voip_report["MISS_DURATION"] + voip_report["COMPLETECALLER"] + voip_report["COMPLETEAGENT"] + voip_report["ABANDON"]
            voip_report['SUM'] = voip_report['SUM'].where(voip_report['TRY'] == 0, voip_report["COMPLETEAGENT"] + voip_report["COMPLETECALLER"] + voip_report["ABANDON"])


  

        
        elif Type=='agent':

                     
            Queue_DF_connect_to_agent_COMPLETECALLER["data1"]=Queue_DF_connect_to_agent_COMPLETECALLER["data1"].apply(lambda x:int(x))
            Queue_DF_connect_to_agent_RINGNOANSWER["data1"]=Queue_DF_connect_to_agent_RINGNOANSWER["data1"].apply(lambda x:int(x))
            Queue_DF_connect_to_agent_COMPLETEAGENT["data1"]=Queue_DF_connect_to_agent_COMPLETEAGENT["data1"].apply(lambda x:int(x))
            

            Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum=Queue_DF_connect_to_agent_COMPLETECALLER.groupby(["agent"])["data2"].sum()
            Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum = Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum.to_frame().reset_index() 
            Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum=Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum.rename(columns={"data1":"COMPLETECALLER"})


            
            
            

            Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum=Queue_DF_connect_to_agent_COMPLETEAGENT.groupby(["agent"])["data2"].sum()
            Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum = Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum.to_frame().reset_index()            
            Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum=Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum.rename(columns={"data1":"COMPLETEAGENT"})
            voip_report=Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum.merge(Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum,on="agent",how="outer").fillna(0)
            
            
           
            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum=(Queue_DF_connect_to_agent_RINGNOANSWER.groupby(["agent"])["data1"].sum())/1000
            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum = Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum.to_frame().reset_index() 
            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum=Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum.rename(columns={"data1":"MISS_DURATION"})
            voip_report=voip_report.merge(Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum,on="agent",how="outer").fillna(0)




            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum=Queue_DF_connect_to_agent_RINGNOANSWER.groupby(["agent"])["data1"].count()
            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum = Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum.to_frame().reset_index() 
            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum=Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum.rename(columns={"data1":"NUMBER_MISS"})
            voip_report=voip_report.merge(Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum,on="agent",how="outer").fillna(0)


            voip_report["COMPLETECALLER"]=voip_report["COMPLETECALLER"].apply(lambda x:int(x))
            voip_report["MISS_DURATION"]=voip_report["MISS_DURATION"].apply(lambda x:int(x))
            voip_report["COMPLETEAGENT"]=voip_report["COMPLETEAGENT"].apply(lambda x:int(x))

       
            voip_report['call_duration'] = voip_report["COMPLETEAGENT"] + voip_report["COMPLETECALLER"] 


            voip_report=voip_report.rename(columns={"agent":"agent"})        
        
        elif Type=='hourcall':
            
            
            
            
            Queue_DF_connect_to_agent_COMPLETECALLER["data1"]=Queue_DF_connect_to_agent_COMPLETECALLER["data1"].apply(lambda x:int(x))
            Queue_DF_connect_to_agent_RINGNOANSWER["data1"]=Queue_DF_connect_to_agent_RINGNOANSWER["data1"].apply(lambda x:int(x))
            Queue_DF_connect_to_agent_COMPLETEAGENT["data1"]=Queue_DF_connect_to_agent_COMPLETEAGENT["data1"].apply(lambda x:int(x))
            
            
      
            
            
            voip_report=get_phone_df.loc[:, ['callid', 'data2']]    
            voip_report=voip_report.rename(columns={"data2":"mobile"})             
            Queue_DF_NOT_connect_to_agent=Queue_DF[(Queue_DF['event']=='ABANDON')]
            Queue_DF_NOT_connect_to_agent_hold_sum=Queue_DF_NOT_connect_to_agent.groupby(["time"])["data3"].sum()
            Queue_DF_NOT_connect_to_agent_hold_sum = Queue_DF_NOT_connect_to_agent_hold_sum.to_frame().reset_index()  
            Queue_DF_NOT_connect_to_agent_hold_sum=Queue_DF_NOT_connect_to_agent_hold_sum.rename(columns={"data3":"ABANDON"})
            voip_report=voip_report.merge(Queue_DF_NOT_connect_to_agent_hold_sum,on="callid",how="outer").fillna(0)



            Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum=Queue_DF_connect_to_agent_COMPLETECALLER.groupby(["time"])["data1"].sum()
            Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum = Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum.to_frame().reset_index() 
            Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum=Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum.rename(columns={"data1":"COMPLETECALLER"})
            voip_report=voip_report.merge(Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum,on="callid",how="outer").fillna(0)

            
            
            

            Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum=Queue_DF_connect_to_agent_COMPLETEAGENT.groupby(["time"])["data1"].sum()
            Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum = Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum.to_frame().reset_index()            
            Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum=Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum.rename(columns={"data1":"COMPLETEAGENT"})
            voip_report=voip_report.merge(Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum,on="callid",how="outer").fillna(0)
            
            
           
            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum=(Queue_DF_connect_to_agent_RINGNOANSWER.groupby(["time"])["data2"].sum())/1000
            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum = Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum.to_frame().reset_index() 
            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum=Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum.rename(columns={"data1":"MISS_DURATION"})
            voip_report=voip_report.merge(Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum,on="callid",how="outer").fillna(0)




            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum=Queue_DF_connect_to_agent_RINGNOANSWER.groupby(["time"])["data1"].count()
            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum = Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum.to_frame().reset_index() 
            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum=Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum.rename(columns={"data1":"TRY"})
            voip_report=voip_report.merge(Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum,on="callid",how="outer").fillna(0)

            
            voip_report["COMPLETECALLER"]=voip_report["COMPLETECALLER"].apply(lambda x:int(x))
            voip_report["MISS_DURATION"]=voip_report["MISS_DURATION"].apply(lambda x:int(x))
            voip_report["COMPLETEAGENT"]=voip_report["COMPLETEAGENT"].apply(lambda x:int(x))
            voip_report["ABANDON"]=voip_report["ABANDON"].apply(lambda x:int(x))


            # print(type(voip_report['MISS_DURATION'][0]))
            # print(type(voip_report["COMPLETEAGENT"][0]))
            # print(type(voip_report["COMPLETECALLER"][0]))
            # print(type(voip_report["ABANDON"][0]))          


            voip_report['SUM'] = voip_report["MISS_DURATION"] + voip_report["COMPLETECALLER"] + voip_report["COMPLETEAGENT"] + voip_report["ABANDON"]
            voip_report['SUM'] = voip_report['SUM'].where(voip_report['TRY'] == 0, voip_report["COMPLETEAGENT"] + voip_report["COMPLETECALLER"] + voip_report["ABANDON"])

        
        elif Type=='houragent':

                     
            Queue_DF_connect_to_agent_COMPLETECALLER["data1"]=Queue_DF_connect_to_agent_COMPLETECALLER["data1"].apply(lambda x:int(x))
            Queue_DF_connect_to_agent_RINGNOANSWER["data1"]=Queue_DF_connect_to_agent_RINGNOANSWER["data1"].apply(lambda x:int(x))
            Queue_DF_connect_to_agent_COMPLETEAGENT["data1"]=Queue_DF_connect_to_agent_COMPLETEAGENT["data1"].apply(lambda x:int(x))
            

            Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum=Queue_DF_connect_to_agent_COMPLETECALLER.groupby(["agent","time"])["data2"].sum()
            Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum = Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum.to_frame().reset_index() 
            Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum=Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum.rename(columns={"data1":"COMPLETECALLER"})


            
            
            

            Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum=Queue_DF_connect_to_agent_COMPLETEAGENT.groupby(["agent","time"])["data2"].sum()
            Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum = Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum.to_frame().reset_index()            
            Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum=Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum.rename(columns={"data1":"COMPLETEAGENT"})
            voip_report=Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum.merge(Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum,on="agent",how="outer").fillna(0)
            
            
           
            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum=(Queue_DF_connect_to_agent_RINGNOANSWER.groupby(["agent","time"])["data1"].sum())/1000
            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum = Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum.to_frame().reset_index() 
            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum=Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum.rename(columns={"data1":"MISS_DURATION"})
            voip_report=voip_report.merge(Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum,on="agent",how="outer").fillna(0)




            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum=Queue_DF_connect_to_agent_RINGNOANSWER.groupby(["agent","time"])["data1"].count()
            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum = Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum.to_frame().reset_index() 
            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum=Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum.rename(columns={"data1":"NUMBER_MISS"})
            voip_report=voip_report.merge(Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum,on="agent",how="outer").fillna(0)


            voip_report["COMPLETECALLER"]=voip_report["COMPLETECALLER"].apply(lambda x:int(x))
            voip_report["MISS_DURATION"]=voip_report["MISS_DURATION"].apply(lambda x:int(x))
            voip_report["COMPLETEAGENT"]=voip_report["COMPLETEAGENT"].apply(lambda x:int(x))

       
            voip_report['call_duration'] = voip_report["COMPLETEAGENT"] + voip_report["COMPLETECALLER"] 


            voip_report=voip_report.rename(columns={"agent":"agent"})                   
        
        
        
        
        
        
        
        
        
        
        
        
        
        else:
            raise Exception('type invalid')






    except KeyError as error:
        voip_report="NO Report"
        print("Error:", error)

    
    return(voip_report)








def Call_log_report_excell(Start, End, Type, Agent:list, Queuename:list,company):

   

    ###############
    #FILTER_QUERY
    if company=='hamkadeh':
        if Agent !=[]:
            Agent=[int(i) for i in Agent]
            Queue_log=QueueLoghamkadeh.objects.using("hamkadeh").filter(time__gte=Start, time__lte=End, agent__in=Agent )

        else:
            Queue_log=QueueLoghamkadeh.objects.using("hamkadeh").filter(time__gte=Start, time__lte=End)


        if Queuename !=[]:
            Queuename=[int(i) for i in Queuename]
            Queue_log=Queue_log.filter(time__gte=Start, time__lte=End, Queuename__in=Agent )
        else:
            Queue_log=Queue_log.filter(time__gte=Start, time__lte=End)


    elif company=="5040":
        if Agent !=[]:
            Agent=[int(i) for i in Agent]
            Queue_log=QueueLog.objects.using("5040").filter(time__gte=Start, time__lte=End, agent__in=Agent )
        else:
            Queue_log=QueueLog.objects.using("5040").filter(time__gte=Start, time__lte=End)


        if Queuename !=[]:
            Queuename=[int(i) for i in Queuename]            
            Queue_log=Queue_log.filter(time__gte=Start, time__lte=End, queuename__in=Queuename )
        else:

            Queue_log=Queue_log.filter(time__gte=Start, time__lte=End) 

    ##############
    #create_df
    queue = Queue_log.values("event", "callid", "agent", "queuename", "data1", "data2", "data3", "data4", "data5",)  

    list_Queue=list(queue)
    Queue_DF = pd.DataFrame.from_records(list_Queue)
    Queue_DF=pd.DataFrame(list_Queue)
        
    ##############

    #############
    #get_phone



    try:
       
        get_phone_df=Queue_DF[Queue_DF['event']=='ENTERQUEUE']
        
        Queue_DF_connect_to_agent_COMPLETECALLER=Queue_DF[Queue_DF['event']=='COMPLETECALLER']
        Queue_DF_connect_to_agent_COMPLETEAGENT=Queue_DF[(Queue_DF['event']=='COMPLETEAGENT')]
        Queue_DF_connect_to_agent_RINGNOANSWER=Queue_DF[(Queue_DF['event']=='RINGNOANSWER')]   


        Queue_DF_connect_to_agent_RINGNOANSWER=Queue_DF_connect_to_agent_RINGNOANSWER[Queue_DF_connect_to_agent_RINGNOANSWER['data1']!='0']
        Queue_DF_connect_to_agent_RINGNOANSWER=Queue_DF_connect_to_agent_RINGNOANSWER[Queue_DF_connect_to_agent_RINGNOANSWER['data1']!='1000']
  


        
        
        
        if Type=='call':
            Queue_DF_connect_to_agent_COMPLETECALLER["data1"]=Queue_DF_connect_to_agent_COMPLETECALLER["data1"].apply(lambda x:int(x))
            Queue_DF_connect_to_agent_RINGNOANSWER["data1"]=Queue_DF_connect_to_agent_RINGNOANSWER["data1"].apply(lambda x:int(x))
            Queue_DF_connect_to_agent_COMPLETEAGENT["data1"]=Queue_DF_connect_to_agent_COMPLETEAGENT["data1"].apply(lambda x:int(x))
            
            
      
            
            
            voip_report=get_phone_df.loc[:, ['callid', 'data2']]    
            voip_report=voip_report.rename(columns={"data2":"موبایل"})             
            Queue_DF_NOT_connect_to_agent=Queue_DF[(Queue_DF['event']=='ABANDON')]
            Queue_DF_NOT_connect_to_agent_hold_sum=Queue_DF_NOT_connect_to_agent.groupby(["callid"])["data3"].sum()
            Queue_DF_NOT_connect_to_agent_hold_sum = Queue_DF_NOT_connect_to_agent_hold_sum.to_frame().reset_index()  
            Queue_DF_NOT_connect_to_agent_hold_sum=Queue_DF_NOT_connect_to_agent_hold_sum.rename(columns={"data3":"از صف خارج شده"})
            voip_report=voip_report.merge(Queue_DF_NOT_connect_to_agent_hold_sum,on="callid",how="outer").fillna(0)



            Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum=Queue_DF_connect_to_agent_COMPLETECALLER.groupby(["callid"])["data1"].sum()
            Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum = Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum.to_frame().reset_index() 
            Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum=Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum.rename(columns={"data1":"قطع شده توسط مراجع"})
            voip_report=voip_report.merge(Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum,on="callid",how="outer").fillna(0)

            
            
            

            Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum=Queue_DF_connect_to_agent_COMPLETEAGENT.groupby(["callid"])["data1"].sum()
            Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum = Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum.to_frame().reset_index()            
            Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum=Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum.rename(columns={"data1":"قطع شده توسط کاربر"})
            voip_report=voip_report.merge(Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum,on="callid",how="outer").fillna(0)
            
            
           
            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum=(Queue_DF_connect_to_agent_RINGNOANSWER.groupby(["callid"])["data1"].sum())/1000
            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum = Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum.to_frame().reset_index() 
            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum=Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum.rename(columns={"data1":"مدت میسکال"})
            voip_report=voip_report.merge(Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum,on="callid",how="outer").fillna(0)




            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum=Queue_DF_connect_to_agent_RINGNOANSWER.groupby(["callid"])["data1"].count()
            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum = Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum.to_frame().reset_index() 
            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum=Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum.rename(columns={"data1":"تلاش"})
            voip_report=voip_report.merge(Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum,on="callid",how="outer").fillna(0)

            
            voip_report["قطع شده توسط کاربر"]=voip_report["قطع شده توسط کاربر"].apply(lambda x:int(x))
            voip_report["مدت میسکال"]=voip_report["مدت میسکال"].apply(lambda x:int(x))
            voip_report["قطع شده توسط مراجع"]=voip_report["قطع شده توسط مراجع"].apply(lambda x:int(x))
            voip_report["از صف خارج شده"]=voip_report["از صف خارج شده"].apply(lambda x:int(x))


            # print(type(voip_report['MISS_DURATION'][0]))
            # print(type(voip_report["COMPLETEAGENT"][0]))
            # print(type(voip_report["COMPLETECALLER"][0]))
            # print(type(voip_report["ABANDON"][0]))          


            voip_report['مجموع'] = voip_report["مدت میسکال"] + voip_report['قطع شده توسط مراجع'] + voip_report["قطع شده توسط کاربر"] + voip_report["از صف خارج شده"]
            voip_report['مجموع'] = voip_report['مجموع'].where(voip_report['تلاش'] == 0, voip_report["قطع شده توسط کاربر"] + voip_report["قطع شده توسط مراجع"] + voip_report["از صف خارج شده"])


  

        
        elif Type=='agent':

                     
            Queue_DF_connect_to_agent_COMPLETECALLER["data1"]=Queue_DF_connect_to_agent_COMPLETECALLER["data1"].apply(lambda x:int(x))
            Queue_DF_connect_to_agent_RINGNOANSWER["data1"]=Queue_DF_connect_to_agent_RINGNOANSWER["data1"].apply(lambda x:int(x))
            Queue_DF_connect_to_agent_COMPLETEAGENT["data1"]=Queue_DF_connect_to_agent_COMPLETEAGENT["data1"].apply(lambda x:int(x))
            

            Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum=Queue_DF_connect_to_agent_COMPLETECALLER.groupby(["agent"])["data1"].sum()
            Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum = Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum.to_frame().reset_index() 
            Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum=Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum.rename(columns={"data1":"قطع شده توسط مراجع"})


            
            
            

            Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum=Queue_DF_connect_to_agent_COMPLETEAGENT.groupby(["agent"])["data2"].sum()
            Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum = Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum.to_frame().reset_index()            
            Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum=Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum.rename(columns={"data1":"قطع شده توسط کاربر"})
            voip_report=Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum.merge(Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum,on="agent",how="outer").fillna(0)
            
            
           
            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum=(Queue_DF_connect_to_agent_RINGNOANSWER.groupby(["agent"])["data2"].sum())/1000
            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum = Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum.to_frame().reset_index() 
            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum=Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum.rename(columns={"data1":"مدت میسکال"})
            voip_report=voip_report.merge(Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum,on="agent",how="outer").fillna(0)




            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum=Queue_DF_connect_to_agent_RINGNOANSWER.groupby(["agent"])["data1"].count()
            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum = Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum.to_frame().reset_index() 
            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum=Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum.rename(columns={"data1":"تعداد میسکال"})
            voip_report=voip_report.merge(Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum,on="agent",how="outer").fillna(0)


            voip_report["قطع شده توسط کاربر"]=voip_report["قطع شده توسط کاربر"].apply(lambda x:int(x))
            voip_report["مدت میسکال"]=voip_report["مدت میسکال"].apply(lambda x:int(x))
            voip_report["قطع شده توسط مراجع"]=voip_report["قطع شده توسط مراجع"].apply(lambda x:int(x))


       
            voip_report['مدت مکالمه'] =  voip_report["قطع شده توسط کاربر"] + voip_report["قطع شده توسط مراجع"] 
            

            voip_report=voip_report.rename(columns={"agent":"داخلی"})        
        



        elif Type=='hourcall':
            Queue_DF_connect_to_agent_COMPLETECALLER["data1"]=Queue_DF_connect_to_agent_COMPLETECALLER["data1"].apply(lambda x:int(x))
            Queue_DF_connect_to_agent_RINGNOANSWER["data1"]=Queue_DF_connect_to_agent_RINGNOANSWER["data1"].apply(lambda x:int(x))
            Queue_DF_connect_to_agent_COMPLETEAGENT["data1"]=Queue_DF_connect_to_agent_COMPLETEAGENT["data1"].apply(lambda x:int(x))
            
            
      
            
            
            voip_report=get_phone_df.loc[:, ['callid', 'data2']]    
            voip_report=voip_report.rename(columns={"data2":"موبایل"})             
            Queue_DF_NOT_connect_to_agent=Queue_DF[(Queue_DF['event']=='ABANDON')]
            Queue_DF_NOT_connect_to_agent_hold_sum=Queue_DF_NOT_connect_to_agent.groupby(["time"])["data3"].sum()
            Queue_DF_NOT_connect_to_agent_hold_sum = Queue_DF_NOT_connect_to_agent_hold_sum.to_frame().reset_index()  
            Queue_DF_NOT_connect_to_agent_hold_sum=Queue_DF_NOT_connect_to_agent_hold_sum.rename(columns={"data3":"از صف خارج شده"})
            voip_report=voip_report.merge(Queue_DF_NOT_connect_to_agent_hold_sum,on="callid",how="outer").fillna(0)



            Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum=Queue_DF_connect_to_agent_COMPLETECALLER.groupby(["time"])["data1"].sum()
            Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum = Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum.to_frame().reset_index() 
            Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum=Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum.rename(columns={"data1":"قطع شده توسط مراجع"})
            voip_report=voip_report.merge(Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum,on="callid",how="outer").fillna(0)

            
            
            

            Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum=Queue_DF_connect_to_agent_COMPLETEAGENT.groupby(["time"])["data1"].sum()
            Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum = Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum.to_frame().reset_index()            
            Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum=Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum.rename(columns={"data1":"قطع شده توسط کاربر"})
            voip_report=voip_report.merge(Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum,on="callid",how="outer").fillna(0)
            
            
           
            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum=(Queue_DF_connect_to_agent_RINGNOANSWER.groupby(["time"])["data1"].sum())/1000
            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum = Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum.to_frame().reset_index() 
            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum=Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum.rename(columns={"data1":"مدت میسکال"})
            voip_report=voip_report.merge(Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum,on="callid",how="outer").fillna(0)




            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum=Queue_DF_connect_to_agent_RINGNOANSWER.groupby(["callid"])["data1"].count()
            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum = Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum.to_frame().reset_index() 
            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum=Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum.rename(columns={"data1":"تلاش"})
            voip_report=voip_report.merge(Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum,on="callid",how="outer").fillna(0)

            
            voip_report["قطع شده توسط کاربر"]=voip_report["قطع شده توسط کاربر"].apply(lambda x:int(x))
            voip_report["مدت میسکال"]=voip_report["مدت میسکال"].apply(lambda x:int(x))
            voip_report["قطع شده توسط مراجع"]=voip_report["قطع شده توسط مراجع"].apply(lambda x:int(x))
            voip_report["از صف خارج شده"]=voip_report["از صف خارج شده"].apply(lambda x:int(x))


            # print(type(voip_report['MISS_DURATION'][0]))
            # print(type(voip_report["COMPLETEAGENT"][0]))
            # print(type(voip_report["COMPLETECALLER"][0]))
            # print(type(voip_report["ABANDON"][0]))          


            voip_report['مجموع'] = voip_report["مدت میسکال"] + voip_report['قطع شده توسط مراجع'] + voip_report["قطع شده توسط کاربر"] + voip_report["از صف خارج شده"]
            voip_report['مجموع'] = voip_report['مجموع'].where(voip_report['تلاش'] == 0, voip_report["قطع شده توسط کاربر"] + voip_report["قطع شده توسط مراجع"] + voip_report["از صف خارج شده"])


  

        
        elif Type=='houragent':

                     
            Queue_DF_connect_to_agent_COMPLETECALLER["data1"]=Queue_DF_connect_to_agent_COMPLETECALLER["data1"].apply(lambda x:int(x))
            Queue_DF_connect_to_agent_RINGNOANSWER["data1"]=Queue_DF_connect_to_agent_RINGNOANSWER["data1"].apply(lambda x:int(x))
            Queue_DF_connect_to_agent_COMPLETEAGENT["data1"]=Queue_DF_connect_to_agent_COMPLETEAGENT["data1"].apply(lambda x:int(x))
            

            Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum=Queue_DF_connect_to_agent_COMPLETECALLER.groupby(["agent","time"])["data1"].sum()
            Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum = Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum.to_frame().reset_index() 
            Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum=Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum.rename(columns={"data1":"قطع شده توسط مراجع"})


            
            
            

            Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum=Queue_DF_connect_to_agent_COMPLETEAGENT.groupby(["agent","time"])["data2"].sum()
            Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum = Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum.to_frame().reset_index()            
            Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum=Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum.rename(columns={"data1":"قطع شده توسط کاربر"})
            voip_report=Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum.merge(Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum,on="agent",how="outer").fillna(0)
            
            
           
            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum=(Queue_DF_connect_to_agent_RINGNOANSWER.groupby(["agent","time"])["data2"].sum())/1000
            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum = Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum.to_frame().reset_index() 
            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum=Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum.rename(columns={"data1":"مدت میسکال"})
            voip_report=voip_report.merge(Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum,on="agent",how="outer").fillna(0)




            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum=Queue_DF_connect_to_agent_RINGNOANSWER.groupby(["agent","time"])["data1"].count()
            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum = Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum.to_frame().reset_index() 
            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum=Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum.rename(columns={"data1":"تعداد میسکال"})
            voip_report=voip_report.merge(Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum,on="agent",how="outer").fillna(0)


            voip_report["قطع شده توسط کاربر"]=voip_report["قطع شده توسط کاربر"].apply(lambda x:int(x))
            voip_report["مدت میسکال"]=voip_report["مدت میسکال"].apply(lambda x:int(x))
            voip_report["قطع شده توسط مراجع"]=voip_report["قطع شده توسط مراجع"].apply(lambda x:int(x))


       
            voip_report['مدت مکالمه'] =  voip_report["قطع شده توسط کاربر"] + voip_report["قطع شده توسط مراجع"] 
            

            voip_report=voip_report.rename(columns={"agent":"داخلی"})        
        
        else:
            raise Exception('type invalid')




    except KeyError as error:
        voip_report="NO Report"
        print("Error:", error)

    
    return(voip_report)











