from . import health_indicators_utils as HIUtils
from . import compare_health_indicators as compareHI
import json
####### CALCULATIONS TO KNOW THE HEALTH INDICATORS #######

# LVESV = [7/(2.4+LVIDs)]*(LVIDs^3)
def calculateLVESV(LVIDs):
    """
    CALCULATE LVESV = [7/(2.4+LVIDs)]*(LVIDs^3)

    Returns LVESV value and it symbol (μL)
    """
    LVESVCalculation = (7/(2.4+LVIDs))*(LVIDs**3)

    return LVESVCalculation#, HIUtils.MICROLITER)

# LVEDV = [7/(2.4+LVIDd)]*(LVIDd^3)
def calculateLVEDV(LVIDd):
    """
    CALCULATE LVEDV = [7/(2.4+LVIDd)]*(LVIDd^3)

    Returns LVEDV value and it symbol (μL)
    """
    LVEDVCalculation = (7/(2.4+LVIDd))*(LVIDd**3)
    return LVEDVCalculation#, HIUtils.MICROLITER)

# FS(%) = (LVIDd-LVIDs)/LVIDd*100
def calculateFS(LVIDd, LVIDs):
    """
    CALCULATE FS(%) = (LVIDd-LVIDs)/LVIDd*100

    Returns FS value and it symbol (%)
    """
    FSCalculation = ((LVIDd-LVIDs)/LVIDd)*100
    return FSCalculation#, HIUtils.PERCENTAGE)

# EF(%) = (LVEDV-LVESV)/LVEDV*100
def calculateEF(LVEDV, LVESV):
    """
    CALCULATE EF(%) = (LVEDV-LVESV)/LVEDV*100

    Returns EF value and it symbol (%)
    """
    EFCalculation = ((LVEDV-LVESV)/LVEDV)*100
    return EFCalculation#, HIUtils.PERCENTAGE(

# LV mass (mg) = 1.04[(LVIDd+LVAWd+LVPWd)^3-(LVIDd^3)]*0.8+0.6
def calculateLV_mass(LVIDd, LVAWd, LVPWd):
    """
    # CALCULATE LV mass (mg) = 1.04[(LVIDd+LVAWd+LVPWd)^3-(LVIDd^3)]*0.8+0.6

    Returns LV mass value and it symbol (mg)

    """
    LV_massCalculation = 1.04*((((LVIDd+LVAWd+LVPWd)**3)-(LVIDd**3))*0.8)+0.6
    return LV_massCalculation#, HIUtils.MILLIGRAMS}

# Stroke volume, SV (μL) = (LVEDV-LVESV)
def calculateStroke_volume(LVEDV, LVESV):
    """
    CALCULATE Stroke volume: SV (μL) = (LVEDV-LVESV)

    Returns Stroke volume value and it symbol (μL)

    """
    SVCalculation = (LVEDV-LVESV)
    return SVCalculation#, HIUtils.MICROLITER}

# Cardiac output : CO(μL/min) = SV*HR
def calculateCardiac_output(SV, HR):
    """
    CALCULATE Cardiac output : CO(μL/min) = SV*HR
    
    Returns Cardiac output and it symbol (mL/min)

    """
    COCalculation = SV*HR/1000
    return COCalculation#, HIUtils.MICROLITERPERMINUTE}

# Relative wall thickness: RWT = (LVPWd+LVIVSd)/(LVIDd)
def calculateRelative_wall_thickness(LVPWd, LVIVSd, LVIDd):
    """
    Relative wall thickness: RWT = (LVPWd+LVIVSd)/(LVIDd)
    
    Returns Relative wall thickness value

    """
    RWTCalculation = (LVPWd+LVIVSd)/(LVIDd)
    return RWTCalculation

def calculateAll(IVSd, IVSs, LVIDd, LVIDs, LVPWd, LVPWs, HR, print_it = False):
    # MISSING VALUES

    LVESV_value = calculateLVESV(LVIDs)
    LVEDV_value = calculateLVEDV(LVIDd)
    FS_value = calculateFS(LVIDd, LVIDs)
    EF_value = calculateEF(LVEDV_value,LVESV_value)
    # LV_mass_value = calculateLV_mass(LVIDd, LVAWd, LVPWd)
    SV_value = calculateStroke_volume(LVEDV_value, LVESV_value)
    CO_value = calculateCardiac_output(SV_value, HR)
    RWT_value = calculateRelative_wall_thickness(LVPWd,IVSd,LVIDd)
    
    json_response = {'LVESV': LVESV_value, 
                       'LVEDV': LVEDV_value,
                       'FS': FS_value,
                       'EF': EF_value,
                    #    'LV_MASS': LV_mass_value,
                       'SV': SV_value,
                       'CO': CO_value,
                       'RWT': RWT_value}

    

    result = compareHI.compareAll(25, HR, LVPWd, LVPWs, LVIDs, LVIDd, IVSd, IVSs, LVESV_value, LVEDV_value, EF_value, FS_value, SV_value, CO_value, print_it)
    json_response['healthy_num'] = result[0]
    json_response['unhealthy_num'] = result[1]

    if(not print_it):
        print(json.dumps(json_response))

    return result




