# from . import health_indicators_utils as HIUtils
# from . import data_manager_utils as DMUtils

# ####### COMPARATORS: 3 OR MORE = UNHEALTHY HEART ####### 

# # BW (g) 25.7+-3.6
# def compareBW(BW, print_it = False):
#     """
#     Compare if BW (g) 25.7+-3.6

#     TRUE = Healthy (between the intervals) \n
#     FALSE = Unhealthy (not between the invervals)
#     """
#     return HIUtils.checkInterval(HIUtils.BW_NEGATIVEINTERVAL, HIUtils.BW_POSITIVEINTERVAL, BW, "BW",print_it)


# # HR(b.p.m) 535+-75
# def compareHR(HR, print_it = False):
#     """
#     Compare if HR(b.p.m) 535+-75

#     TRUE = Healthy (between the intervals) \n
#     FALSE = Unhealthy (not between the invervals)
#     """
#     return HIUtils.checkInterval(HIUtils.HR_NEGATIVEINTERVAL, HIUtils.HR_POSITIVEINTERVAL, HR, "HR", print_it)


# # LV mass (mg) 96+-18
# def compareLV_mass(LV_mass, print_it = False):
#     """
#     Compare if LV mass (mg) 96+-18

#     TRUE = Healthy (between the intervals) \n
#     FALSE = Unhealthy (not between the invervals)
#     """
#     return HIUtils.checkInterval(HIUtils.LVMASS_NEGATIVEINTERVAL, HIUtils.LVMASS_POSITIVEINTERVAL, LV_mass, "LV_mass", print_it)

# #LVPWd (mm) 0.79+-0.22
# def compareLVPWd(LVPWd, print_it = False):
#     """
#     Compare if LVPWd (mm) 0.79+-0.22

#     TRUE = Healthy (between the intervals) \n
#     FALSE = Unhealthy (not between the invervals)
#     """
#     return HIUtils.checkInterval(HIUtils.LVPWD_NEGATIVEINTERVAL, HIUtils.LVPWD_POSITIVEINTERVAL, LVPWd, "LVPWd", print_it)

# #LVPWs (mm) 1.12+-0.33
# def compareLVPWs(LVPWs, print_it = False):
#     """
#     Compare if LVPWs (mm) 1.12+-0.33

#     TRUE = Healthy (between the intervals) \n
#     FALSE = Unhealthy (not between the invervals)
#     """
#     return HIUtils.checkInterval(HIUtils.LVPWS_NEGATIVEINTERVAL, HIUtils.LVPWS_POSITIVEINTERVAL, LVPWs, "LVPWs", print_it)


# #LVIDs (mm) 2.20+-0.50
# def compareLVIDs(LVIDs, print_it = False):
#     """
#     Compare if LVIDs (mm) 2.20+-0.50

#     TRUE = Healthy (between the intervals) \n
#     FALSE = Unhealthy (not between the invervals)
#     """
#     return HIUtils.checkInterval(HIUtils.LVIDS_NEGATIVEINTERVAL, HIUtils.LVIDS_POSITIVEINTERVAL, LVIDs, "LVIDs", print_it)


# #LVIDd (mm) 3.69+-0.41
# def compareLVIDd(LVIDd, print_it = False):
#     """
#     Compare if LVIDd (mm) 3.69+-0.41

#     TRUE = Healthy (between the intervals) \n
#     FALSE = Unhealthy (not between the invervals)
#     """
#     return HIUtils.checkInterval(HIUtils.LVIDD_NEGATIVEINTERVAL, HIUtils.LVIDD_POSITIVEINTERVAL, LVIDd, "LVIDd", print_it)


# #IVSd (mm) 0.71+-0.15
# def compareIVSd(IVSd, print_it = False):
#     """
#     Compare if IVSd (mm) 0.71+-0.15

#     TRUE = Healthy (between the intervals) \n
#     FALSE = Unhealthy (not between the invervals)
#     """
#     return HIUtils.checkInterval(HIUtils.IVSD_NEGATIVEINTERVAL, HIUtils.IVSD_POSITIVEINTERVAL, IVSd, "IVSd", print_it)


# #IVSs (mm) 0.97+-0.19
# def compareIVSs(IVSs, print_it = False):
#     """
#     Compare if IVSs (mm) 0.97+-0.19

#     TRUE = Healthy (between the intervals) \n
#     FALSE = Unhealthy (not between the invervals)
#     """
#     return HIUtils.checkInterval(HIUtils.IVSS_NEGATIVEINTERVAL, HIUtils.IVSS_POSITIVEINTERVAL, IVSs, "IVSs", print_it)


# #LVESV (μL) 19.35+-11.30
# def compareLVESV(LVESV, print_it = False):
#     """
#     Compare if LVESV (μL) 19.35+-11.30

#     TRUE = Healthy (between the intervals) \n
#     FALSE = Unhealthy (not between the invervals)
#     """
#     return HIUtils.checkInterval(HIUtils.LVESV_NEGATIVEINTERVAL, HIUtils.LVESV_POSITIVEINTERVAL, LVESV, "LVESV", print_it)


# #LVEDV (μL) 57.7+-16.5
# def compareLVEDV(LVEDV, print_it = False):
#     """
#     Compare if LVEDV (μL) 57.7+-16.5

#     TRUE = Healthy (between the intervals) \n
#     FALSE = Unhealthy (not between the invervals)
#     """
#     return HIUtils.checkInterval(HIUtils.LVEDV_NEGATIVEINTERVAL, HIUtils.LVEDV_POSITIVEINTERVAL, LVEDV, "LVEDV", print_it)


# #EF(%) 71+-11
# def compareEF(EF, print_it = False):
#     """
#     Compare if EF(%) 71+-11

#     TRUE = Healthy (between the intervals) \n
#     FALSE = Unhealthy (not between the invervals)
#     """
#     return HIUtils.checkInterval(HIUtils.EF_NEGATIVEINTERVAL, HIUtils.EF_POSITIVEINTERVAL, EF, "EF", print_it)


# #FS(%) 43+-9
# def compareFS(FS, print_it = False):
#     """
#     Compare if FS(%) 43+-9

#     TRUE = Healthy (between the intervals) \n
#     FALSE = Unhealthy (not between the invervals)
#     """
#     return HIUtils.checkInterval(HIUtils.FS_NEGATIVEINTERVAL, HIUtils.FS_POSITIVEINTERVAL, FS, "FS", print_it)


# #SV(μL) 35.1+-8.5
# def compareSV(SV, print_it = False):
#     """
#     Compare if SV(μL) 35.1+-8.5

#     TRUE = Healthy (between the intervals) \n
#     FALSE = Unhealthy (not between the invervals)
#     """
#     return HIUtils.checkInterval(HIUtils.SV_NEGATIVEINTERVAL, HIUtils.SV_POSITIVEINTERVAL, SV, "SV", print_it)


# #CO(mL/min) 17.7+-3.8
# def compareCO(CO, print_it = False):
#     """
#     Compare if CO(mL/min) 17.7+-3.8

#     TRUE = Healthy (between the intervals) \n
#     FALSE = Unhealthy (not between the invervals)
#     """
#     return HIUtils.checkInterval(HIUtils.CO_NEGATIVEINTERVAL, HIUtils.CO_POSITIVEINTERVAL, CO, "CO", print_it)

# def compareAll(BW, HR, LVPWd, LVPWs, LVIDs, LVIDd, IVSd, IVSs, LVESV, LVEDV, EF, FS, SV, CO, print_it = False):
#     """
#     Compare all the health indicators, if number of unhealthy indicators are 3 or more the heart is unhealthy.

#     Return: \n
#     TRUE = Healthy heart // FALSE = Unhealthy heart \n
#     A list with all the comparations done and if the intervals are healthy or unhealthy
#     """
#     unhealthyCont = 0
#     healthyCont = 0 

#     if(compareBW(BW)): healthyCont = healthyCont + 1
#     else: unhealthyCont = unhealthyCont +1

#     if compareHR(HR): healthyCont = healthyCont + 1
#     else: unhealthyCont = unhealthyCont +1
    
#     # if compareLV_mass(LV_mass): healthyCont = healthyCont + 1
#     # else: unhealthyCont = unhealthyCont +1

#     if compareLVPWd(LVPWd): healthyCont = healthyCont + 1
#     else: unhealthyCont = unhealthyCont +1

#     if compareLVPWs(LVPWs): healthyCont = healthyCont + 1
#     else: unhealthyCont = unhealthyCont +1

#     if compareLVIDs(LVIDs): healthyCont = healthyCont + 1
#     else: unhealthyCont = unhealthyCont +1

#     if compareLVIDd(LVIDd): healthyCont = healthyCont + 1
#     else: unhealthyCont = unhealthyCont +1

#     if compareIVSd(IVSd): healthyCont = healthyCont + 1
#     else: unhealthyCont = unhealthyCont +1

#     if compareIVSs(IVSs): healthyCont = healthyCont + 1
#     else: unhealthyCont = unhealthyCont +1

#     if compareLVESV(LVESV): healthyCont = healthyCont + 1
#     else: unhealthyCont = unhealthyCont +1

#     if compareLVEDV(LVEDV): healthyCont = healthyCont + 1
#     else: unhealthyCont = unhealthyCont +1

#     if compareEF(EF): healthyCont = healthyCont + 1
#     else: unhealthyCont = unhealthyCont +1

#     if compareFS(FS): healthyCont = healthyCont + 1
#     else: unhealthyCont = unhealthyCont +1

#     if compareSV(SV): healthyCont = healthyCont + 1
#     else: unhealthyCont = unhealthyCont +1

#     if compareCO(CO): healthyCont = healthyCont + 1
#     else: unhealthyCont = unhealthyCont +1
    
#     if(print_it):
#         HIUtils.printRecountIndicators(healthyCont, unhealthyCont)
#         DMUtils.healthInformationToExcel(BW, HR, LVPWd, LVPWs, LVIDs, LVIDd, IVSd, IVSs, LVESV, LVEDV, EF, FS, SV, CO, healthyCont, unhealthyCont)
    
#     return [healthyCont, unhealthyCont]





# #compareAll(1,500,1,1,1,1.8,3.5,0.7,1,12,50,61,35,30,15)
