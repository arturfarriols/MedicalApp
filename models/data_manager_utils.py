# import pandas as pd
# import uuid
# from . import health_indicators_utils as HIUtils
# import time
# import os

# def healthInformationToExcel(BW, HR, LVPWd, LVPWs, LVIDs, LVIDd, IVSd, IVSs, LVESV, LVEDV, EF, FS, SV, CO, healthyCounter, unhealthyCounter):
    
#     isExist = os.path.exists('excels')
#     if not isExist:
#         # Create a new directory because it does not exist
#         os.makedirs('excels')

#     timestr = time.strftime("%Y_%m_%d-%H_%M_%S")
#     path = f'excels/result-{timestr}.xlsx'
    
#     healthDataFrame = pd.DataFrame(columns=[HIUtils.ID,
#                                             HIUtils.BW_NAME, 
#                                             HIUtils.HR_NAME, 
#                                             HIUtils.LVMASS_NAME, 
#                                             HIUtils.LVPWD_NAME, 
#                                             HIUtils.LVPWS_NAME, 
#                                             HIUtils.LVIDS_NAME, 
#                                             HIUtils.LVIDD_NAME,
#                                             HIUtils.IVSD_NAME,
#                                             HIUtils.IVSS_NAME,
#                                             HIUtils.LVESV_NAME,
#                                             HIUtils.LVEDV_NAME,
#                                             HIUtils.EF_NAME,
#                                             HIUtils.FS_NAME,
#                                             HIUtils.SV_NAME,
#                                             HIUtils.CO_NAME,
#                                             HIUtils.HEALTHY_INDICATORS,
#                                             HIUtils.UNHEALTHY_INDICATORS])
#     id = uuid.uuid4()
#     newRow = pd.DataFrame({ HIUtils.ID: [str(id)],
#                             HIUtils.BW_NAME: [BW], 
#                             HIUtils.HR_NAME: [HR], 
#                             # HIUtils.LVMASS_NAME: [LV_mass], 
#                             HIUtils.LVPWD_NAME: [LVPWd], 
#                             HIUtils.LVPWS_NAME: [LVPWs], 
#                             HIUtils.LVIDS_NAME: [LVIDs], 
#                             HIUtils.LVIDD_NAME: [LVIDd],
#                             HIUtils.IVSD_NAME: [IVSd],
#                             HIUtils.IVSS_NAME: [IVSs],
#                             HIUtils.LVESV_NAME: [LVESV],
#                             HIUtils.LVEDV_NAME: [LVEDV],
#                             HIUtils.EF_NAME: [EF],
#                             HIUtils.FS_NAME: [FS],
#                             HIUtils.SV_NAME: [SV],
#                             HIUtils.CO_NAME: [CO],
#                             HIUtils.HEALTHY_INDICATORS: [healthyCounter],
#                             HIUtils.UNHEALTHY_INDICATORS: [unhealthyCounter]})   

#     healthDataFrame = pd.concat([healthDataFrame, newRow])
#     print(healthDataFrame)

#     healthDataFrame.to_excel(path, sheet_name="Indicators")
    