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
    
    Queue_DF=Queue_DF[Queue_DF['data2']!='from-trunk']
    Queue_DF.fillna(0, inplace=True)
    
    Queue_DF['data3']=Queue_DF['data3'].apply(lambda x:0 if x=="" else x)
    Queue_DF['data3']=Queue_DF['data3'].apply(lambda x:float(x))        
    



    ##############

    #############
    #get_phone



    try:
        Queue_DF['time']=Queue_DF['time'].apply(lambda x:int(x.hour))

        
        get_phone_df=Queue_DF[Queue_DF['event']=='ENTERQUEUE']
        # get_agent_df=Queue_DF.loc[0:,['agent','callid']]
        


        Queue_DF_connect_to_agent_COMPLETECALLER=Queue_DF[Queue_DF['event']=='COMPLETECALLER']
        Queue_DF_connect_to_agent_COMPLETEAGENT=Queue_DF[(Queue_DF['event']=='COMPLETEAGENT')]
        Queue_DF_connect_to_agent_RINGNOANSWER=Queue_DF[(Queue_DF['event']=='RINGNOANSWER')]   

        

        Queue_DF_connect_to_agent=Queue_DF[(Queue_DF['event']=='COMPLETEAGENT' )|(Queue_DF['event']=='COMPLETEAGENT')]
        Queue_DF_connect_to_agent=Queue_DF_connect_to_agent.loc[0:,['callid','agent']]


        Queue_DF_connect_to_agent_RINGNOANSWER=Queue_DF_connect_to_agent_RINGNOANSWER[Queue_DF_connect_to_agent_RINGNOANSWER['data1']!='0']
        Queue_DF_connect_to_agent_RINGNOANSWER=Queue_DF_connect_to_agent_RINGNOANSWER[Queue_DF_connect_to_agent_RINGNOANSWER['data1']!='1000']
  
        Queue_DF_connect_to_agent_COMPLETEAGENT['data2']=Queue_DF_connect_to_agent_COMPLETEAGENT['data2'].apply(lambda x:0 if x=="" else x)
        Queue_DF_connect_to_agent_COMPLETEAGENT['data2']=Queue_DF_connect_to_agent_COMPLETEAGENT['data2'].apply(lambda x:float(x))


        Queue_DF_connect_to_agent_COMPLETECALLER['data2']=Queue_DF_connect_to_agent_COMPLETECALLER['data2'].apply(lambda x:0 if x=="" else x)
        Queue_DF_connect_to_agent_COMPLETECALLER['data2']=Queue_DF_connect_to_agent_COMPLETECALLER['data2'].apply(lambda x:float(x))

        Queue_DF_connect_to_agent_RINGNOANSWER['data2']=Queue_DF_connect_to_agent_RINGNOANSWER['data2'].apply(lambda x:0 if x=="" else x)
        Queue_DF_connect_to_agent_RINGNOANSWER['data2']=Queue_DF_connect_to_agent_RINGNOANSWER['data2'].apply(lambda x:float(x))



        
        
        if Type=='call':
            Queue_DF_connect_to_agent_COMPLETECALLER["data1"]=Queue_DF_connect_to_agent_COMPLETECALLER["data1"].apply(lambda x:int(x))
            Queue_DF_connect_to_agent_RINGNOANSWER["data1"]=Queue_DF_connect_to_agent_RINGNOANSWER["data1"].apply(lambda x:int(x))
            Queue_DF_connect_to_agent_COMPLETEAGENT["data1"]=Queue_DF_connect_to_agent_COMPLETEAGENT["data1"].apply(lambda x:int(x))
            
            

            
            
            get_phone_df=get_phone_df.loc[:, ['callid', 'data2']] 
            # voip_report=voip_report.merge(Queue_DF_connect_to_agent,on="callid",how="outer").fillna(0)   
            get_phone_df=get_phone_df.rename(columns={"data2":"mobile"})             
            Queue_DF_NOT_connect_to_agent=Queue_DF[(Queue_DF['event']=='ABANDON')]
            Queue_DF_NOT_connect_to_agent_hold_sum=Queue_DF_NOT_connect_to_agent.groupby(["callid"])["data3"].sum()
            Queue_DF_NOT_connect_to_agent_hold_sum = Queue_DF_NOT_connect_to_agent_hold_sum.to_frame().reset_index()  
            voip_report=Queue_DF_NOT_connect_to_agent_hold_sum.rename(columns={"data3":"ABANDON"})
            voip_report=voip_report.merge(get_phone_df,on="callid",how="left").fillna(0)



            Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum=Queue_DF_connect_to_agent_COMPLETECALLER.groupby(["callid"])["data2"].sum()
            Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum = Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum.to_frame().reset_index() 
            Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum=Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum.rename(columns={"data2":"COMPLETECALLER"})
            voip_report=voip_report.merge(Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum,on="callid",how="outer").fillna(0)

            
            
            

            Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum=Queue_DF_connect_to_agent_COMPLETEAGENT.groupby(["callid"])["data2"].sum()
            Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum = Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum.to_frame().reset_index()            
            Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum=Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum.rename(columns={"data2":"COMPLETEAGENT"})
            voip_report=voip_report.merge(Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum,on="callid",how="outer").fillna(0)
            voip_report=voip_report.merge(Queue_DF_connect_to_agent,on="callid",how="outer").fillna(0)
            
            
            Queue_DF_connect_to_agent_COMPLETECALLER_number=Queue_DF_connect_to_agent_COMPLETECALLER.groupby(["callid"])["data2"].count()
            Queue_DF_connect_to_agent_COMPLETECALLER_number = Queue_DF_connect_to_agent_COMPLETECALLER_number.to_frame().reset_index() 
            Queue_DF_connect_to_agent_COMPLETECALLER_number=Queue_DF_connect_to_agent_COMPLETECALLER_number.rename(columns={"data2":"number_COMPLETECALLER"})
            voip_report=voip_report.merge(Queue_DF_connect_to_agent_COMPLETECALLER_number,on="callid",how="outer").fillna(0)

            

            

            Queue_DF_connect_to_agent_COMPLETEAGENT_number=Queue_DF_connect_to_agent_COMPLETEAGENT.groupby(["callid"])["data2"].count()
            Queue_DF_connect_to_agent_COMPLETEAGENT_number = Queue_DF_connect_to_agent_COMPLETEAGENT_number.to_frame().reset_index()            
            Queue_DF_connect_to_agent_COMPLETEAGENT_number=Queue_DF_connect_to_agent_COMPLETEAGENT_number.rename(columns={"data2":"number_COMPLETEAGENT"})
            voip_report=voip_report.merge(Queue_DF_connect_to_agent_COMPLETEAGENT_number,on="callid",how="outer").fillna(0)

            voip_report['number_answered']=voip_report['number_COMPLETECALLER']+voip_report['number_COMPLETEAGENT']







           
            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum=(Queue_DF_connect_to_agent_RINGNOANSWER.groupby(["callid"])["data2"].sum())/1000
            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum = Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum.to_frame().reset_index() 
            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum=Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum.rename(columns={"data2":"MISS_DURATION"})
            voip_report=voip_report.merge(Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum,on="callid",how="outer").fillna(0)




            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum=Queue_DF_connect_to_agent_RINGNOANSWER.groupby(["callid"])["data1"].count()
            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum = Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum.to_frame().reset_index() 
            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum=Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum.rename(columns={"data1":"TRY"})
            voip_report=voip_report.merge(Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum,on="callid",how="outer").fillna(0)

            
            voip_report["COMPLETECALLER"]=voip_report["COMPLETECALLER"].apply(lambda x:int(x))
            voip_report["MISS_DURATION"]=voip_report["MISS_DURATION"].apply(lambda x:int(x))
            voip_report["COMPLETEAGENT"]=voip_report["COMPLETEAGENT"].apply(lambda x:int(x))
            voip_report["ABANDON"]=voip_report["ABANDON"].apply(lambda x:int(x))



            voip_report['SUM'] = voip_report["MISS_DURATION"] + voip_report["COMPLETECALLER"] + voip_report["COMPLETEAGENT"] + voip_report["ABANDON"]
            voip_report['SUM'] = voip_report['SUM'].where(voip_report['TRY'] == 0, voip_report["COMPLETEAGENT"] + voip_report["COMPLETECALLER"] + voip_report["ABANDON"])




        
        elif Type=='agent':

                     
            Queue_DF_connect_to_agent_COMPLETECALLER["data1"]=Queue_DF_connect_to_agent_COMPLETECALLER["data1"].apply(lambda x:int(x))
            Queue_DF_connect_to_agent_RINGNOANSWER["data1"]=Queue_DF_connect_to_agent_RINGNOANSWER["data1"].apply(lambda x:int(x))
            Queue_DF_connect_to_agent_COMPLETEAGENT["data1"]=Queue_DF_connect_to_agent_COMPLETEAGENT["data1"].apply(lambda x:int(x))
            

            Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum =Queue_DF_connect_to_agent_COMPLETECALLER.groupby(["agent"])["data2"].sum()
            Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum = Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum.to_frame().reset_index() 
            voip_report =Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum.rename(columns={"data2":"COMPLETECALLER"})




            Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum =Queue_DF_connect_to_agent_COMPLETEAGENT.groupby(["agent"])["data2"].sum()
            Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum = Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum.to_frame().reset_index()            
            Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum =Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum.rename(columns={"data2":"COMPLETEAGENT"})
            voip_report =voip_report.merge(Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum,on="agent",how="outer").fillna(0)
            


            Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum_number=Queue_DF_connect_to_agent_COMPLETECALLER.groupby(["agent"])["data2"].count()
            Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum_number = Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum_number.to_frame().reset_index() 
            Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum_number=Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum_number.rename(columns={"data2":"number_COMPLETECALLER"})
            voip_report =voip_report.merge(Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum_number,on="agent",how="outer").fillna(0)


            Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum_number =Queue_DF_connect_to_agent_COMPLETEAGENT.groupby(["agent"])["data2"].count()
            Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum_number = Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum_number.to_frame().reset_index()            
            Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum_number =Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum_number.rename(columns={"data2":"number_COMPLETEAGENT"})
            voip_report =voip_report.merge(Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum_number,on="agent",how="outer").fillna(0)

            voip_report['number_answered']=voip_report['number_COMPLETECALLER']+voip_report['number_COMPLETEAGENT']
           
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
            

      
            

     
            Queue_DF_NOT_connect_to_agent=Queue_DF[(Queue_DF['event']=='ABANDON')]
            Queue_DF_NOT_connect_to_agent_hold_sum=Queue_DF_NOT_connect_to_agent.groupby(["time"])["data3"].sum()
            Queue_DF_NOT_connect_to_agent_hold_sum = Queue_DF_NOT_connect_to_agent_hold_sum.to_frame().reset_index()  
            voip_report=Queue_DF_NOT_connect_to_agent_hold_sum.rename(columns={"data3":"ABANDON"})

           
           


            Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum=Queue_DF_connect_to_agent_COMPLETECALLER.groupby(["time"])["data2"].sum()
            Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum = Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum.to_frame().reset_index() 
            Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum=Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum.rename(columns={"data2":"COMPLETECALLER"})
            voip_report=voip_report.merge(Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum,on="time",how="outer").fillna(0)

            
            
            

            Queue_DF_connect_to_agent_COMPLETEAGENT_number=Queue_DF_connect_to_agent_COMPLETEAGENT.groupby(["time"])["data2"].count()
            Queue_DF_connect_to_agent_COMPLETEAGENT_number = Queue_DF_connect_to_agent_COMPLETEAGENT_number.to_frame().reset_index()            
            Queue_DF_connect_to_agent_COMPLETEAGENT_number=Queue_DF_connect_to_agent_COMPLETEAGENT_number.rename(columns={"data2":"number_COMPLETEAGENT"})
            voip_report=voip_report.merge(Queue_DF_connect_to_agent_COMPLETEAGENT_number,on="time",how="outer").fillna(0)
            

            Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum=Queue_DF_connect_to_agent_COMPLETECALLER.groupby(["time"])["data2"].count()
            Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum = Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum.to_frame().reset_index() 
            Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum=Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum.rename(columns={"data2":"number_COMPLETECALLER"})
            voip_report=voip_report.merge(Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum,on="time",how="outer").fillna(0)

            
            
            

            Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum=Queue_DF_connect_to_agent_COMPLETEAGENT.groupby(["time"])["data2"].sum()
            Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum = Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum.to_frame().reset_index()            
            Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum=Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum.rename(columns={"data2":"COMPLETEAGENT"})
            voip_report=voip_report.merge(Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum,on="time",how="outer").fillna(0)
            





            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum=(Queue_DF_connect_to_agent_RINGNOANSWER.groupby(["time"])["data1"].sum())/1000
            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum = Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum.to_frame().reset_index() 
            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum=Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum.rename(columns={"data1":"MISS_DURATION"})
            voip_report=voip_report.merge(Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum,on="time",how="outer").fillna(0)




            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum=Queue_DF_connect_to_agent_RINGNOANSWER.groupby(["time"])["data1"].count()
            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum = Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum.to_frame().reset_index() 
            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum=Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum.rename(columns={"data1":"number_miss"})
            voip_report=voip_report.merge(Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum,on="time",how="outer").fillna(0)

            
            voip_report["COMPLETECALLER"]=voip_report["COMPLETECALLER"].apply(lambda x:int(x))
            voip_report["MISS_DURATION"]=voip_report["MISS_DURATION"].apply(lambda x:int(x))
            voip_report["COMPLETEAGENT"]=voip_report["COMPLETEAGENT"].apply(lambda x:int(x))
            voip_report["ABANDON"]=voip_report["ABANDON"].apply(lambda x:int(x))



            voip_report['call_duration'] = voip_report["MISS_DURATION"] + voip_report["COMPLETECALLER"] + voip_report["COMPLETEAGENT"] + voip_report["ABANDON"]
            voip_report['call_duration'] = voip_report['call_duration'].where(voip_report['number_miss'] == 0, voip_report["COMPLETEAGENT"] + voip_report["COMPLETECALLER"] + voip_report["ABANDON"])

        
            voip_report.sort_values(by=['time'], inplace=True)





        elif Type=='houragent':
           
            
            
            Queue_DF_connect_to_agent_COMPLETECALLER["data1"]=Queue_DF_connect_to_agent_COMPLETECALLER["data1"].apply(lambda x:int(x))
            Queue_DF_connect_to_agent_RINGNOANSWER["data1"]=Queue_DF_connect_to_agent_RINGNOANSWER["data1"].apply(lambda x:int(x))
            Queue_DF_connect_to_agent_COMPLETEAGENT["data1"]=Queue_DF_connect_to_agent_COMPLETEAGENT["data1"].apply(lambda x:int(x))
            




            Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum=Queue_DF_connect_to_agent_COMPLETECALLER.groupby(["time","agent"])["data2"].sum()
            Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum = Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum.to_frame().reset_index() 
            voip_report=Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum.rename(columns={"data2":"COMPLETECALLER"})


            
            
            

            Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum=Queue_DF_connect_to_agent_COMPLETEAGENT.groupby(["time","agent"])["data2"].sum()
            Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum = Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum.to_frame().reset_index()            
            Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum=Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum.rename(columns={"data2":"COMPLETEAGENT"})
            voip_report=voip_report.merge(Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum,on=["time","agent"],how="outer").fillna(0)
            

            Queue_DF_connect_to_agent_COMPLETECALLER_number=Queue_DF_connect_to_agent_COMPLETECALLER.groupby(["time","agent"])["data2"].count()
            Queue_DF_connect_to_agent_COMPLETECALLER_number = Queue_DF_connect_to_agent_COMPLETECALLER_number.to_frame().reset_index() 
            Queue_DF_connect_to_agent_COMPLETECALLER_number=Queue_DF_connect_to_agent_COMPLETECALLER_number.rename(columns={"data2":"number_COMPLETECALLER"})
            voip_report=voip_report.merge(Queue_DF_connect_to_agent_COMPLETECALLER_number,on=["time","agent"],how="outer").fillna(0)

            
            
            

            Queue_DF_connect_to_agent_COMPLETEAGENT_number=Queue_DF_connect_to_agent_COMPLETEAGENT.groupby(["time","agent"])["data2"].count()
            Queue_DF_connect_to_agent_COMPLETEAGENT_number = Queue_DF_connect_to_agent_COMPLETEAGENT_number.to_frame().reset_index()            
            Queue_DF_connect_to_agent_COMPLETEAGENT_number=Queue_DF_connect_to_agent_COMPLETEAGENT_number.rename(columns={"data2":"number_COMPLETEAGENT"})
            voip_report=voip_report.merge(Queue_DF_connect_to_agent_COMPLETEAGENT_number,on=["time","agent"],how="outer").fillna(0)






            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum=(Queue_DF_connect_to_agent_RINGNOANSWER.groupby(["time","agent"])["data1"].sum())/1000
            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum = Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum.to_frame().reset_index() 
            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum=Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum.rename(columns={"data1":"MISS_DURATION"})
            voip_report=voip_report.merge(Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum,on=["time","agent"],how="outer").fillna(0)




            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum=Queue_DF_connect_to_agent_RINGNOANSWER.groupby(["time","agent"])["data1"].count()
            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum = Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum.to_frame().reset_index() 
            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum=Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum.rename(columns={"data1":"number_miss"})
            voip_report=voip_report.merge(Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum,on=["time","agent"],how="outer").fillna(0)

            
            voip_report["COMPLETECALLER"]=voip_report["COMPLETECALLER"].apply(lambda x:int(x))
            voip_report["MISS_DURATION"]=voip_report["MISS_DURATION"].apply(lambda x:int(x))
            voip_report["COMPLETEAGENT"]=voip_report["COMPLETEAGENT"].apply(lambda x:int(x))

      


            voip_report['call_duration'] = voip_report["MISS_DURATION"] + voip_report["COMPLETECALLER"] + voip_report["COMPLETEAGENT"] 
            voip_report['call_duration'] = voip_report['call_duration'].where(voip_report['number_miss'] == 0, voip_report["COMPLETEAGENT"] + voip_report["COMPLETECALLER"])

        
            voip_report.sort_values(by=['time'], inplace=True)


        

        
        
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

    ###############

    ##############
    #create_df
    queue = Queue_log.values("event", "callid", "agent", "queuename", "data1", "data2", "data3", "data4", "data5","time")  

    list_Queue=list(queue)
    Queue_DF = pd.DataFrame.from_records(list_Queue)
    Queue_DF=pd.DataFrame(list_Queue)   
    
    Queue_DF=Queue_DF[Queue_DF['data2']!='from-trunk']
    Queue_DF.fillna(0, inplace=True)
    
    Queue_DF['data3']=Queue_DF['data3'].apply(lambda x:0 if x=="" else x)
    Queue_DF['data3']=Queue_DF['data3'].apply(lambda x:float(x))        
    



    


    ##############

    #############
    #get_phone



    try:
        Queue_DF['time']=Queue_DF['time'].apply(lambda x:int(x.hour))

        
        get_phone_df=Queue_DF[Queue_DF['event']=='ENTERQUEUE']
        
        Queue_DF_connect_to_agent_COMPLETECALLER=Queue_DF[Queue_DF['event']=='COMPLETECALLER']
        Queue_DF_connect_to_agent_COMPLETEAGENT=Queue_DF[(Queue_DF['event']=='COMPLETEAGENT')]
        Queue_DF_connect_to_agent=Queue_DF[(Queue_DF['event']=='COMPLETEAGENT' )|(Queue_DF['event']=='COMPLETEAGENT')]
        Queue_DF_connect_to_agent=Queue_DF_connect_to_agent.loc[0:,['callid','agent']]
        Queue_DF_connect_to_agent_RINGNOANSWER=Queue_DF[(Queue_DF['event']=='RINGNOANSWER')]   


        Queue_DF_connect_to_agent_RINGNOANSWER=Queue_DF_connect_to_agent_RINGNOANSWER[Queue_DF_connect_to_agent_RINGNOANSWER['data1']!='0']
        Queue_DF_connect_to_agent_RINGNOANSWER=Queue_DF_connect_to_agent_RINGNOANSWER[Queue_DF_connect_to_agent_RINGNOANSWER['data1']!='1000']
  
        Queue_DF_connect_to_agent_COMPLETEAGENT['data2']=Queue_DF_connect_to_agent_COMPLETEAGENT['data2'].apply(lambda x:0 if x=="" else x)
        Queue_DF_connect_to_agent_COMPLETEAGENT['data2']=Queue_DF_connect_to_agent_COMPLETEAGENT['data2'].apply(lambda x:float(x))


        Queue_DF_connect_to_agent_COMPLETECALLER['data2']=Queue_DF_connect_to_agent_COMPLETECALLER['data2'].apply(lambda x:0 if x=="" else x)
        Queue_DF_connect_to_agent_COMPLETECALLER['data2']=Queue_DF_connect_to_agent_COMPLETECALLER['data2'].apply(lambda x:float(x))

        Queue_DF_connect_to_agent_RINGNOANSWER['data2']=Queue_DF_connect_to_agent_RINGNOANSWER['data2'].apply(lambda x:0 if x=="" else x)
        Queue_DF_connect_to_agent_RINGNOANSWER['data2']=Queue_DF_connect_to_agent_RINGNOANSWER['data2'].apply(lambda x:float(x))


        
        
        if Type=='call':
            Queue_DF_connect_to_agent_COMPLETECALLER["data1"]=Queue_DF_connect_to_agent_COMPLETECALLER["data1"].apply(lambda x:int(x))
            Queue_DF_connect_to_agent_RINGNOANSWER["data1"]=Queue_DF_connect_to_agent_RINGNOANSWER["data1"].apply(lambda x:int(x))
            Queue_DF_connect_to_agent_COMPLETEAGENT["data1"]=Queue_DF_connect_to_agent_COMPLETEAGENT["data1"].apply(lambda x:int(x))
            
            
      
            
            
            voip_report=get_phone_df.loc[:, ['callid', 'data2']]    
            voip_report=voip_report.rename(columns={"data2":"mobile"})             
            Queue_DF_NOT_connect_to_agent=Queue_DF[(Queue_DF['event']=='ABANDON')]
            Queue_DF_NOT_connect_to_agent_hold_sum=Queue_DF_NOT_connect_to_agent.groupby(["callid"])["data3"].sum()
            Queue_DF_NOT_connect_to_agent_hold_sum = Queue_DF_NOT_connect_to_agent_hold_sum.to_frame().reset_index()  
            Queue_DF_NOT_connect_to_agent_hold_sum=Queue_DF_NOT_connect_to_agent_hold_sum.rename(columns={"data3":"از صف خارج شده"})
            voip_report=voip_report.merge(Queue_DF_NOT_connect_to_agent_hold_sum,on="callid",how="outer").fillna(0)



            Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum=Queue_DF_connect_to_agent_COMPLETECALLER.groupby(["callid"])["data2"].sum()
            Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum = Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum.to_frame().reset_index() 
            Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum=Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum.rename(columns={"data2":"قطع شده توسط مراجع"})
            voip_report=voip_report.merge(Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum,on="callid",how="outer").fillna(0)

            
            
            

            Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum=Queue_DF_connect_to_agent_COMPLETEAGENT.groupby(["callid"])["data2"].sum()
            Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum = Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum.to_frame().reset_index()            
            Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum=Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum.rename(columns={"data2":"قطع شده توسط کاربر"})
            voip_report=voip_report.merge(Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum,on="callid",how="outer").fillna(0)
            
            
            Queue_DF_connect_to_agent_COMPLETECALLER_number=Queue_DF_connect_to_agent_COMPLETECALLER.groupby(["callid"])["data2"].count()
            Queue_DF_connect_to_agent_COMPLETECALLER_number = Queue_DF_connect_to_agent_COMPLETECALLER_number.to_frame().reset_index() 
            Queue_DF_connect_to_agent_COMPLETECALLER_number=Queue_DF_connect_to_agent_COMPLETECALLER_number.rename(columns={"data2":"تعداد تماس قطع شده توسط کاربر"})
            voip_report=voip_report.merge(Queue_DF_connect_to_agent_COMPLETECALLER_number,on="callid",how="outer").fillna(0)

            
            
            

            Queue_DF_connect_to_agent_COMPLETEAGENT_number=Queue_DF_connect_to_agent_COMPLETEAGENT.groupby(["callid"])["data2"].count()
            Queue_DF_connect_to_agent_COMPLETEAGENT_number = Queue_DF_connect_to_agent_COMPLETEAGENT_number.to_frame().reset_index()            
            Queue_DF_connect_to_agent_COMPLETEAGENT_number=Queue_DF_connect_to_agent_COMPLETEAGENT_number.rename(columns={"data2":"تعداد تماس قطع شده توسط مراجع"})
            voip_report=voip_report.merge(Queue_DF_connect_to_agent_COMPLETEAGENT_number,on="callid",how="outer").fillna(0)




            voip_report['تعداد پاسخداد']=voip_report["تعداد تماس قطع شده توسط مراجع"]+voip_report["تعداد تماس قطع شده توسط کاربر"]



           
            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum=(Queue_DF_connect_to_agent_RINGNOANSWER.groupby(["callid"])["data2"].sum())/1000
            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum = Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum.to_frame().reset_index() 
            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum=Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum.rename(columns={"data2":"مدت میسکال"})
            voip_report=voip_report.merge(Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum,on="callid",how="outer").fillna(0)




            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum=Queue_DF_connect_to_agent_RINGNOANSWER.groupby(["callid"])["data1"].count()
            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum = Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum.to_frame().reset_index() 
            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum=Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum.rename(columns={"data1":"تعداد میسکال"})
            voip_report=voip_report.merge(Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum,on="callid",how="outer").fillna(0)

            
            voip_report["قطع شده توسط مراجع"]=voip_report["قطع شده توسط مراجع"].apply(lambda x:int(x))
            voip_report["مدت میسکال"]=voip_report["مدت میسکال"].apply(lambda x:int(x))
            voip_report["قطع شده توسط کاربر"]=voip_report["قطع شده توسط کاربر"].apply(lambda x:int(x))
            voip_report["از صف خارج شده"]=voip_report["از صف خارج شده"].apply(lambda x:int(x))



            voip_report["مدت مکالمه"] = voip_report["مدت میسکال"] + voip_report["قطع شده توسط مراجع"] + voip_report["قطع شده توسط کاربر"] + voip_report["از صف خارج شده"]
            voip_report["مدت مکالمه"] = voip_report["مدت مکالمه"].where(voip_report["تعداد میسکال"] == 0, voip_report["قطع شده توسط کاربر"] + voip_report["قطع شده توسط مراجع"] + voip_report["از صف خارج شده"])


  

        
        elif Type=='agent':

                     
            Queue_DF_connect_to_agent_COMPLETECALLER["data1"]=Queue_DF_connect_to_agent_COMPLETECALLER["data1"].apply(lambda x:int(x))
            Queue_DF_connect_to_agent_RINGNOANSWER["data1"]=Queue_DF_connect_to_agent_RINGNOANSWER["data1"].apply(lambda x:int(x))
            Queue_DF_connect_to_agent_COMPLETEAGENT["data1"]=Queue_DF_connect_to_agent_COMPLETEAGENT["data1"].apply(lambda x:int(x))
            

            Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum=Queue_DF_connect_to_agent_COMPLETECALLER.groupby(["agent"])["data2"].sum()
            Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum = Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum.to_frame().reset_index() 
            voip_report=Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum.rename(columns={"data2":"قطع شده توسط مراجع"})


            
            
            

            Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum =Queue_DF_connect_to_agent_COMPLETEAGENT.groupby(["agent"])["data2"].sum()
            Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum = Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum.to_frame().reset_index()            
            Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum =Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum.rename(columns={"data2":"قطع شده توسط کاربر"})
            voip_report =voip_report.merge(Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum,on="agent",how="outer").fillna(0)
            


        
            
            
           

            Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum_number=Queue_DF_connect_to_agent_COMPLETECALLER.groupby(["agent"])["data2"].count()
            Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum_number = Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum_number.to_frame().reset_index() 
            Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum_number=Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum_number.rename(columns={"data2":"تعداد تماس قطع شده توسط کاربر"})
            voip_report =voip_report.merge(Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum_number,on="agent",how="outer").fillna(0)


            Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum_number =Queue_DF_connect_to_agent_COMPLETEAGENT.groupby(["agent"])["data2"].count()
            Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum_number = Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum_number.to_frame().reset_index()            
            Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum_number =Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum_number.rename(columns={"data2":"تعداد تماس قطع شده توسط مراجع"})
            voip_report =voip_report.merge(Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum_number,on="agent",how="outer").fillna(0)

            voip_report['تعداد پاسخداد']=voip_report["تعداد تماس قطع شده توسط مراجع"]+voip_report["تعداد تماس قطع شده توسط کاربر"]

           
            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum=(Queue_DF_connect_to_agent_RINGNOANSWER.groupby(["agent"])["data1"].sum())/1000
            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum = Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum.to_frame().reset_index() 
            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum=Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum.rename(columns={"data1":"مدت میسکال"})
            voip_report=voip_report.merge(Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum,on="agent",how="outer").fillna(0)




            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum=Queue_DF_connect_to_agent_RINGNOANSWER.groupby(["agent"])["data1"].count()
            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum = Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum.to_frame().reset_index() 
            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum=Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum.rename(columns={"data1":"تعداد میسکال"})
            voip_report=voip_report.merge(Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum,on="agent",how="outer").fillna(0)


            voip_report["قطع شده توسط مراجع"]=voip_report["قطع شده توسط مراجع"].apply(lambda x:int(x))
            voip_report["مدت میسکال"]=voip_report["مدت میسکال"].apply(lambda x:int(x))
            voip_report["قطع شده توسط کاربر"]=voip_report["قطع شده توسط کاربر"].apply(lambda x:int(x))

       
            voip_report["مدت مکالمه "] = voip_report["قطع شده توسط کاربر"] + voip_report["قطع شده توسط مراجع"] 


            voip_report=voip_report.rename(columns={"agent":"agent"})        
        






        elif Type=='hourcall':
            
            
            
            
            Queue_DF_connect_to_agent_COMPLETECALLER["data1"]=Queue_DF_connect_to_agent_COMPLETECALLER["data1"].apply(lambda x:int(x))
            Queue_DF_connect_to_agent_RINGNOANSWER["data1"]=Queue_DF_connect_to_agent_RINGNOANSWER["data1"].apply(lambda x:int(x))
            Queue_DF_connect_to_agent_COMPLETEAGENT["data1"]=Queue_DF_connect_to_agent_COMPLETEAGENT["data1"].apply(lambda x:int(x))
            

      
            

     
            Queue_DF_NOT_connect_to_agent=Queue_DF[(Queue_DF['event']=='ABANDON')]
            Queue_DF_NOT_connect_to_agent_hold_sum=Queue_DF_NOT_connect_to_agent.groupby(["time"])["data3"].sum()
            Queue_DF_NOT_connect_to_agent_hold_sum = Queue_DF_NOT_connect_to_agent_hold_sum.to_frame().reset_index()  
            voip_report=Queue_DF_NOT_connect_to_agent_hold_sum.rename(columns={"data3":"از صف خارج شده"})

           
           


            Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum=Queue_DF_connect_to_agent_COMPLETECALLER.groupby(["time"])["data2"].sum()
            Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum = Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum.to_frame().reset_index() 
            Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum=Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum.rename(columns={"data2":"قطع شده توسط مراجع"})
            voip_report=voip_report.merge(Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum,on="time",how="outer").fillna(0)

            
            
            

            Queue_DF_connect_to_agent_COMPLETEAGENT_number=Queue_DF_connect_to_agent_COMPLETEAGENT.groupby(["time"])["data2"].count()
            Queue_DF_connect_to_agent_COMPLETEAGENT_number = Queue_DF_connect_to_agent_COMPLETEAGENT_number.to_frame().reset_index()            
            Queue_DF_connect_to_agent_COMPLETEAGENT_number=Queue_DF_connect_to_agent_COMPLETEAGENT_number.rename(columns={"data2":"تعداد تماس قطع شده توسط مراجع"})
            voip_report=voip_report.merge(Queue_DF_connect_to_agent_COMPLETEAGENT_number,on="time",how="outer").fillna(0)
            

            Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum=Queue_DF_connect_to_agent_COMPLETECALLER.groupby(["time"])["data2"].count()
            Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum = Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum.to_frame().reset_index() 
            Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum=Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum.rename(columns={"data2":"تعداد تماس قطع شده توسط کاربر"})
            voip_report=voip_report.merge(Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum,on="time",how="outer").fillna(0)

            
            
            

            Queue_DF_connect_to_agent_COMPLETEAGENT_number=Queue_DF_connect_to_agent_COMPLETEAGENT.groupby(["time"])["data2"].sum()
            Queue_DF_connect_to_agent_COMPLETEAGENT_number = Queue_DF_connect_to_agent_COMPLETEAGENT_number.to_frame().reset_index()            
            Queue_DF_connect_to_agent_COMPLETEAGENT_number=Queue_DF_connect_to_agent_COMPLETEAGENT_number.rename(columns={"data2":"قطع شده توسط کاربر"})
            voip_report=voip_report.merge(Queue_DF_connect_to_agent_COMPLETEAGENT_number,on="time",how="outer").fillna(0)
            





            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum=(Queue_DF_connect_to_agent_RINGNOANSWER.groupby(["time"])["data1"].sum())/1000
            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum = Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum.to_frame().reset_index() 
            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum=Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum.rename(columns={"data1":"مدت میسکال"})
            voip_report=voip_report.merge(Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum,on="time",how="outer").fillna(0)




            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum=Queue_DF_connect_to_agent_RINGNOANSWER.groupby(["time"])["data1"].count()
            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum = Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum.to_frame().reset_index() 
            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum=Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum.rename(columns={"data1":"تعداد میسکال"})
            voip_report=voip_report.merge(Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum,on="time",how="outer").fillna(0)

            
            voip_report["قطع شده توسط مراجع"]=voip_report["قطع شده توسط مراجع"].apply(lambda x:int(x))
            voip_report["مدت میسکال"]=voip_report["مدت میسکال"].apply(lambda x:int(x))
            voip_report["قطع شده توسط کاربر"]=voip_report["قطع شده توسط کاربر"].apply(lambda x:int(x))
            voip_report["از صف خارج شده"]=voip_report["از صف خارج شده"].apply(lambda x:int(x))


            # print(type(voip_report['MISS_DURATION'][0]))
            # print(type(voip_report["قطع شده توسط کاربر"][0]))
            # print(type(voip_report["قطع شده توسط مراجع"][0]))
            # print(type(voip_report["از صف خارج شده"][0]))          


            voip_report["مدت مکالمه"] = voip_report["مدت میسکال"] + voip_report["قطع شده توسط مراجع"] + voip_report["قطع شده توسط کاربر"] + voip_report["از صف خارج شده"]
            voip_report["مدت مکالمه"] = voip_report["مدت مکالمه"].where(voip_report["تعداد میسکال"] == 0, voip_report["قطع شده توسط کاربر"] + voip_report["قطع شده توسط مراجع"] + voip_report["از صف خارج شده"])

        
            voip_report.sort_values(by=['time'], inplace=True)



        
        elif Type=='houragent':
           
            
            
            Queue_DF_connect_to_agent_COMPLETECALLER["data1"]=Queue_DF_connect_to_agent_COMPLETECALLER["data1"].apply(lambda x:int(x))
            Queue_DF_connect_to_agent_RINGNOANSWER["data1"]=Queue_DF_connect_to_agent_RINGNOANSWER["data1"].apply(lambda x:int(x))
            Queue_DF_connect_to_agent_COMPLETEAGENT["data1"]=Queue_DF_connect_to_agent_COMPLETEAGENT["data1"].apply(lambda x:int(x))
            




            Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum=Queue_DF_connect_to_agent_COMPLETECALLER.groupby(["time","agent"])["data2"].sum()
            Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum = Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum.to_frame().reset_index() 
            voip_report=Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum.rename(columns={"data2":"قطع شده توسط مراجع"})


            
            
            

            Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum=Queue_DF_connect_to_agent_COMPLETEAGENT.groupby(["time","agent"])["data2"].sum()
            Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum = Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum.to_frame().reset_index()            
            Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum=Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum.rename(columns={"data2":"قطع شده توسط کاربر"})
            voip_report=voip_report.merge(Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum,on=["time","agent"],how="outer").fillna(0)
            

            Queue_DF_connect_to_agent_COMPLETECALLER_number=Queue_DF_connect_to_agent_COMPLETECALLER.groupby(["time","agent"])["data2"].count()
            Queue_DF_connect_to_agent_COMPLETECALLER_number = Queue_DF_connect_to_agent_COMPLETECALLER_number.to_frame().reset_index() 
            Queue_DF_connect_to_agent_COMPLETECALLER_number=Queue_DF_connect_to_agent_COMPLETECALLER_number.rename(columns={"data2":"تعداد تماس قطع شده توسط مراجع"})
            voip_report=voip_report.merge(Queue_DF_connect_to_agent_COMPLETECALLER_number,on=["time","agent"],how="outer").fillna(0)

            
            
            

            Queue_DF_connect_to_agent_COMPLETEAGENT_number=Queue_DF_connect_to_agent_COMPLETEAGENT.groupby(["time","agent"])["data2"].count()
            Queue_DF_connect_to_agent_COMPLETEAGENT_number = Queue_DF_connect_to_agent_COMPLETEAGENT_number.to_frame().reset_index()            
            Queue_DF_connect_to_agent_COMPLETEAGENT_number=Queue_DF_connect_to_agent_COMPLETEAGENT_number.rename(columns={"data2":"تعداد تماس قطع شده توسط کاربر"})
            voip_report=voip_report.merge(Queue_DF_connect_to_agent_COMPLETEAGENT_number,on=["time","agent"],how="outer").fillna(0)









            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum=(Queue_DF_connect_to_agent_RINGNOANSWER.groupby(["time","agent"])["data1"].sum())/1000
            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum = Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum.to_frame().reset_index() 
            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum=Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum.rename(columns={"data1":"مدت میسکال"})
            voip_report=voip_report.merge(Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum,on=["time","agent"],how="outer").fillna(0)




            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum=Queue_DF_connect_to_agent_RINGNOANSWER.groupby(["time","agent"])["data1"].count()
            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum = Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum.to_frame().reset_index() 
            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum=Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum.rename(columns={"data1":"تعداد میسکال"})
            voip_report=voip_report.merge(Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum,on=["time","agent"],how="outer").fillna(0)

            
            voip_report["قطع شده توسط مراجع"]=voip_report["قطع شده توسط مراجع"].apply(lambda x:int(x))
            voip_report["مدت میسکال"]=voip_report["مدت میسکال"].apply(lambda x:int(x))
            voip_report["قطع شده توسط کاربر"]=voip_report["قطع شده توسط کاربر"].apply(lambda x:int(x))

      


            voip_report["مدت مکالمه "] = voip_report["مدت میسکال"] + voip_report["قطع شده توسط مراجع"] + voip_report["قطع شده توسط کاربر"] 
            voip_report["مدت مکالمه "] = voip_report["مدت مکالمه "].where(voip_report['تعداد میسکال'] == 0, voip_report["قطع شده توسط کاربر"] + voip_report["قطع شده توسط مراجع"])

        
            voip_report.sort_values(by=['time'], inplace=True)


        

        
        
        else:
            raise Exception('type invalid')






    except KeyError as error:
        voip_report="NO Report"
        print("Error:", error)

    
    return(voip_report)


