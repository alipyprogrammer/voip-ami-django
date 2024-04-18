from django.shortcuts import render
from queuelog.models import *
import pandas as pd



def Call_log_report(Start, End, Type, Agent:list, Queuename:list):
   
    ###############
    #FILTER_QUERY
    if Agent !=[]:
        Queue_log=QueueLog.objects.using('hamkadeh').filter(time__gte=Start, time__lte=End, agent__in=Agent )
    else:
        Queue_log=QueueLog.objects.using('hamkadeh').filter(time__gte=Start, time__lte=End)
    

    if Queuename !=[]:
        Queue_log=QueueLog.objects.using('hamkadeh').filter(time__gte=Start, time__lte=End, queuename__in=Queuename )
    else:
        Queue_log=QueueLog.objects.using('hamkadeh').filter(time__gte=Start, time__lte=End)    
    ###############

    ##############
    #create_df
    queue = Queue_log.values("event", "callid", "agent", "queuename", "data1", "data2", "data3", "data4", "data5",)  
    list_Queue=list(queue)
    Queue_DF = pd.DataFrame.from_records(list_Queue)
    Queue_DF=pd.DataFrame(list_Queue)
    ##############
    
    #############
    #get_phone
    get_phone_df=Queue_DF[Queue_DF['event']=='ENTERQUEUE']
    voip_report=get_phone_df.loc[:, ['callid', 'data2']]    
    voip_report=voip_report.rename(columns={"data2":"موبایل"})



    try:
        
        Queue_DF_connect_to_agent_COMPLETECALLER=Queue_DF[Queue_DF['event']=='COMPLETECALLER']
        Queue_DF_connect_to_agent_COMPLETEAGENT=Queue_DF[(Queue_DF['event']=='COMPLETEAGENT')]
        Queue_DF_connect_to_agent_RINGNOANSWER=Queue_DF[(Queue_DF['event']=='RINGNOANSWER')]        
        
        if Type=='call':
            Queue_DF_NOT_connect_to_agent=Queue_DF[(Queue_DF['event']=='ABANDON')]
            Queue_DF_NOT_connect_to_agent_hold_sum=Queue_DF_NOT_connect_to_agent.groupby(["callid"])["data3"].sum()
            Queue_DF_NOT_connect_to_agent_hold_sum = Queue_DF_NOT_connect_to_agent_hold_sum.to_frame().reset_index()  
            Queue_DF_NOT_connect_to_agent_hold_sum=Queue_DF_NOT_connect_to_agent_hold_sum.rename(columns={"data3":"ترک شده"})
            voip_report=voip_report.merge(Queue_DF_NOT_connect_to_agent_hold_sum,on="callid",how="outer").fillna(0)



            Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum=Queue_DF_connect_to_agent_COMPLETECALLER.groupby(["callid"])["data1"].sum()
            Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum = Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum.to_frame().reset_index() 
            Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum=Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum.rename(columns={"data1":"تکمیل شده توسط مراحع"})
            voip_report=voip_report.merge(Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum,on="callid",how="outer").fillna(0)

            
            
            

            Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum=Queue_DF_connect_to_agent_COMPLETEAGENT.groupby(["callid"])["data1"].sum()
            Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum = Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum.to_frame().reset_index()            
            Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum=Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum.rename(columns={"data1":"تکمیل شده توسط کاربر"})
            voip_report=voip_report.merge(Queue_DF_connect_to_agent_COMPLETEAGENT_hold_sum,on="callid",how="outer").fillna(0)
            
            
           
            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum=Queue_DF_connect_to_agent_RINGNOANSWER.groupby(["callid"])["data1"].sum()
            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum = Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum.to_frame().reset_index() 
            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum=Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum.rename(columns={"data1":"میسکال"})
            voip_report=voip_report.merge(Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum,on="callid",how="outer").fillna(0)




            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum=Queue_DF_connect_to_agent_RINGNOANSWER.groupby(["callid"])["data1"].count()
            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum = Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum.to_frame().reset_index() 
            Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum=Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum.rename(columns={"data1":"تلاش"})
            voip_report=voip_report.merge(Queue_DF_connect_to_agent_RINGNOANSWER_hold_sum,on="callid",how="outer").fillna(0)




        else:
            pass
            
            # Queue_DF_connect_to_agent_COMPLETECALLER_hold_sum=Queue_DF_connect_to_agent_COMPLETECALLER.groupby(["agent"])["sale_entry_id"].count()
            # number_cartable_registered_factor_df = number_cartable_registered_factor_df.to_frame().reset_index()                 
























    except KeyError as error:
        Queue_DF="NO Report"
        print(error)

    
    return(Queue_DF)















