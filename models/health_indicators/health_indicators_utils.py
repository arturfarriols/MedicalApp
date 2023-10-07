import math

# Symbols for calculateHealthIndicators functions #
PERCENTAGE = "%" 
MILLIGRAMS = "mg"
MICROLITER = "μL"
MICROLITERPERMINUTE = "μL/min"

# Minimum indicators to have a unhealthy heart
MINIMUM_INDICATORS_UNHEALTHY_HEART = 3

# Intervals for compareHealthIndicators #

# BW Intervals
BW_POSITIVEINTERVAL = 25.7+3.6
BW_NEGATIVEINTERVAL = 25.7-3.6

# HR Intervals
HR_POSITIVEINTERVAL = 535+75
HR_NEGATIVEINTERVAL = 535-75

# LV mass Intervals
LVMASS_POSITIVEINTERVAL = 96+18
LVMASS_NEGATIVEINTERVAL = 96-18

# LVPWd mass Intervals
LVPWD_POSITIVEINTERVAL = 0.79+0.22
LVPWD_NEGATIVEINTERVAL = 0.79-0.22

# LVPWs mass Intervals
LVPWS_POSITIVEINTERVAL = 1.12+0.33
LVPWS_NEGATIVEINTERVAL = 1.12-0.33

# LVIDs Intervals
LVIDS_POSITIVEINTERVAL = 2.20+0.50
LVIDS_NEGATIVEINTERVAL = 2.20-0.50

# LVIDd Intervals
LVIDD_POSITIVEINTERVAL = 3.69+0.41
LVIDD_NEGATIVEINTERVAL = 3.69-0.41

# IVSd Intervals
IVSD_POSITIVEINTERVAL = 0.71+0.15
IVSD_NEGATIVEINTERVAL = 0.71-0.15

# IVSs Intervals
IVSS_POSITIVEINTERVAL = 0.97+0.19
IVSS_NEGATIVEINTERVAL = 0.97-0.19

# LVESV Intervals
LVESV_POSITIVEINTERVAL = 19.35+11.30
LVESV_NEGATIVEINTERVAL = 19.35-11.30

# LVEDV Intervals
LVEDV_POSITIVEINTERVAL = 57.7+16.5
LVEDV_NEGATIVEINTERVAL = 57.7-16.5

#EF Intervals
EF_POSITIVEINTERVAL = 71+11
EF_NEGATIVEINTERVAL = 71-11

#FS Intervals
FS_POSITIVEINTERVAL = 43+9
FS_NEGATIVEINTERVAL = 43-9

#SV Intervals
SV_POSITIVEINTERVAL = 35.1+8.5
SV_NEGATIVEINTERVAL = 35.1-8.5

#CO Intervals
CO_POSITIVEINTERVAL = 17.7+3.8
CO_NEGATIVEINTERVAL = 17.7-3.8


# PRINT UTILS
NORMAL_TEXT = "\033[0m"
BOLD_TEXT = "\033[1m"
RED_TEXT = "\x1b[1;31m"
GREEN_TEXT = "\x1b[1;32m"

#Health indicators names
ID = "ID"
BW_NAME = "BW"
HR_NAME = "HR"
LVMASS_NAME = "LV_mass"
LVPWD_NAME = "LVPWd"
LVPWS_NAME = "LVPWs"
LVIDS_NAME = "LVIDs"
LVIDD_NAME = "LVIDd"
IVSD_NAME = "IVSd"
IVSS_NAME = "IVSs"
LVESV_NAME = "LVESV"
LVEDV_NAME = "LVEDV"
EF_NAME = "EF"
FS_NAME = "FS"
SV_NAME = "SV"
CO_NAME = "CO"
HR_NAME = "HR"
UNHEALTHY_INDICATORS = "Unhealthy indicators counter"
HEALTHY_INDICATORS = "Healhy indicators counter"

    
PIXEL_TO_METRICS = {"upper_min_differences": IVSD_NAME,
                            "upper_max_differences": IVSS_NAME,
                            "min_central_differences": LVIDS_NAME,
                            "max_central_differences": LVIDD_NAME,
                            "lower_min_differences": LVPWD_NAME,
                            "lower_max_differences": LVPWS_NAME,
                            }

BASE_METRICS_DEFAULT_DICTIONARY = {IVSS_NAME: -1,
                            IVSD_NAME: -1,
                            LVIDS_NAME: -1,
                            LVIDD_NAME: -1,
                            LVPWS_NAME: -1,
                            LVPWD_NAME: -1,
                            HR_NAME: -1,
                            }

HEART_RATE_FORMULA = lambda x: -205.58321340 / (1 + -1.1300887 * math.exp(0.0083321 * x))

#Check the interval to know if is healthy or unhealthy and prints it
def checkInterval(negativeInterval, positiveInterval, value, name, print_it = False):
    negativeInterval = round(negativeInterval, 2)
    positiveInterval = round(positiveInterval, 2)
    healthy = True
    pr = BOLD_TEXT + str(name) + NORMAL_TEXT + " value and interval : "

    if value < negativeInterval:
        pr = pr+RED_TEXT+str(value)+NORMAL_TEXT
        healthy = False

    pr = pr + " " + str(negativeInterval)
    
    if value >= negativeInterval and value <= positiveInterval:
        pr = pr + " "+ (GREEN_TEXT+str(value)+NORMAL_TEXT)

    pr = pr + " " + str(positiveInterval)

    if value > positiveInterval:
        pr = pr + " "+ (RED_TEXT+str(value)+NORMAL_TEXT)
        healthy = False
    
    if(print_it):
        print(pr)

        if(healthy): print("VALUE IS" + GREEN_TEXT+ " HEALTHY!"+NORMAL_TEXT+"\n") 
        else: print("VALUE IS" + RED_TEXT+ " UNHEALTHY!"+NORMAL_TEXT+"\n") 
    

    return healthy

#Print de total of healthy and unhealthy indicators and if the patient has a healthy or unhealthy heart
def printRecountIndicators(healthyCont, unhealthyCont,):
    print("TOTAL HEALTHY INDICATORS: "+ str(healthyCont))
    print("TOTAL UNHEALTHY INDICATORS: "+ str(unhealthyCont))

    if(unhealthyCont >= MINIMUM_INDICATORS_UNHEALTHY_HEART):
        print("PATIENT HAS A"+RED_TEXT+" UNHEALTHY"+NORMAL_TEXT+" HEART" )
    else: print("PATIENT HAS A"+GREEN_TEXT+" HEALTHY"+NORMAL_TEXT+" HEART" )