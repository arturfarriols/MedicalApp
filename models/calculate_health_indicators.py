from . import health_indicators_utils as HIUtils
from . import compare_health_indicators as compareHI
import json

class HealthIndicatorsCalculator:
    @staticmethod
    def calculateLVESV(LVIDs):
        """
        CALCULATE LVESV = [7/(2.4+LVIDs)]*(LVIDs^3)

        Returns LVESV value and its symbol (μL)
        """
        LVESVCalculation = (7 / (2.4 + LVIDs)) * (LVIDs ** 3)
        return LVESVCalculation

    @staticmethod
    def calculateLVEDV(LVIDd):
        """
        CALCULATE LVEDV = [7/(2.4+LVIDd)]*(LVIDd^3)

        Returns LVEDV value and its symbol (μL)
        """
        LVEDVCalculation = (7 / (2.4 + LVIDd)) * (LVIDd ** 3)
        return LVEDVCalculation

    @staticmethod
    def calculateFS(LVIDd, LVIDs):
        """
        CALCULATE FS(%) = (LVIDd-LVIDs)/LVIDd*100

        Returns FS value and its symbol (%)
        """
        FSCalculation = ((LVIDd - LVIDs) / LVIDd) * 100
        return FSCalculation

    @staticmethod
    def calculateEF(LVEDV, LVESV):
        """
        CALCULATE EF(%) = (LVEDV-LVESV)/LVEDV*100

        Returns EF value and its symbol (%)
        """
        EFCalculation = ((LVEDV - LVESV) / LVEDV) * 100
        return EFCalculation

    @staticmethod
    def calculateLV_mass(LVIDd, LVAWd, LVPWd):
        """
        CALCULATE LV mass (mg) = 1.04[(LVIDd+LVAWd+LVPWd)^3-(LVIDd^3)]*0.8+0.6

        Returns LV mass value and its symbol (mg)
        """
        LV_massCalculation = 1.04 * ((((LVIDd + LVAWd + LVPWd) ** 3) - (LVIDd ** 3)) * 0.8) + 0.6
        return LV_massCalculation

    @staticmethod
    def calculateStroke_volume(LVEDV, LVESV):
        """
        CALCULATE Stroke volume: SV (μL) = (LVEDV-LVESV)

        Returns Stroke volume value and its symbol (μL)
        """
        SVCalculation = (LVEDV - LVESV)
        return SVCalculation

    @staticmethod
    def calculateCardiac_output(SV, HR):
        """
        CALCULATE Cardiac output: CO (μL/min) = SV * HR

        Returns Cardiac output and its symbol (mL/min)
        """
        COCalculation = SV * HR / 1000
        return COCalculation

    @staticmethod
    def calculateRelative_wall_thickness(LVPWd, LVIVSd, LVIDd):
        """
        Relative wall thickness: RWT = (LVPWd + LVIVSd) / LVIDd

        Returns Relative wall thickness value
        """
        RWTCalculation = (LVPWd + LVIVSd) / LVIDd
        return RWTCalculation

    @staticmethod
    def calculate_basic_metrics(pixel_metrics, milimeter_to_pixels):
        mean_horizontal_distance = 0
        metrics = {}

        for key, value in pixel_metrics.items():
            if key not in ["upper_mean_distances", "lower_mean_distances"]:
                metrics[HIUtils.PIXEL_TO_METRICS[key]] = value / milimeter_to_pixels
            else:
                mean_horizontal_distance += value

        mean_horizontal_distance /= 2
        print(mean_horizontal_distance)
        metrics['HR'] = HIUtils.HEART_RATE_FORMULA(mean_horizontal_distance)

        return metrics

    @staticmethod
    def calculateAll(metrics, print_it=True):
        # MISSING VALUES

        LVESV_value = HealthIndicatorsCalculator.calculateLVESV(metrics[HIUtils.LVIDS_NAME])  # LVIDs
        LVEDV_value = HealthIndicatorsCalculator.calculateLVEDV(metrics[HIUtils.LVIDD_NAME])  # LVIDd
        FS_value = HealthIndicatorsCalculator.calculateFS(metrics[HIUtils.LVIDD_NAME], metrics[HIUtils.LVIDS_NAME])  # LVIDd, LVIDs
        EF_value = HealthIndicatorsCalculator.calculateEF(LVEDV_value, LVESV_value)
        SV_value = HealthIndicatorsCalculator.calculateStroke_volume(LVEDV_value, LVESV_value)
        CO_value = HealthIndicatorsCalculator.calculateCardiac_output(SV_value, metrics[HIUtils.HR_NAME])  # HR
        RWT_value = HealthIndicatorsCalculator.calculateRelative_wall_thickness(metrics[HIUtils.LVPWD_NAME], metrics[HIUtils.IVSD_NAME], metrics[HIUtils.LVIDD_NAME])  # LVPWd, IVSd, LVIDd

        json_response = {'LVESV': LVESV_value,
                         'LVEDV': LVEDV_value,
                         'FS': FS_value,
                         'EF': EF_value,
                         #    'LV_MASS': LV_mass_value,
                         'SV': SV_value,
                         'CO': CO_value,
                         'RWT': RWT_value}

        json_response.update(metrics)

        # result = compareHI.compareAll(25, HR, LVPWd, LVPWs, LVIDs, LVIDd, IVSd, IVSs, LVESV_value, LVEDV_value, EF_value, FS_value, SV_value, CO_value, print_it)
        # json_response['healthy_num'] = result[0]
        # json_response['unhealthy_num'] = result[1]

        if (print_it):
            print(json.dumps(json_response))

        return json_response
