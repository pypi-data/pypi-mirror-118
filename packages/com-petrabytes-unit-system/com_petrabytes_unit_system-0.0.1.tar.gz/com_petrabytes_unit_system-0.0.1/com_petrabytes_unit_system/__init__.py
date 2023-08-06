import numpy as np
import pint
ureg = pint.UnitRegistry()


def unit_convert(data_array, from_unit, to_unit, isInverse):
    if isInverse:
        from_unit = from_unit.split("/")
        to_unit = to_unit.split("/")
        a = data_array * (ureg[from_unit[0]] / ureg[from_unit[1]])
        result = 1 / (a.to(ureg[to_unit[1]] / ureg[to_unit[0]]))
    else:
        a = data_array * (ureg[from_unit])
        result = a.to(ureg[to_unit])

    return result.magnitude

#Convert EMW to abspressure:
def convertEMWtoAbsPressPascal(tvd_df, data_df, from_unit):
  data_df_kg_m3 = unit_convert(data_df, from_unit, "kilogram/meter**3", False)
  data_df_pascal = 9.80665 * tvd_df * data_df_kg_m3
  return data_df_pascal

#Convert abspressure to EMW:
def convertAbsPressuretoEMW_kg_m3(tvd_df, data_df, from_unit):
  data_df_pascal = unit_convert(data_df, from_unit, "pascal", False)
  data_df_kg_m3 = data_df_pascal/(9.80665 * tvd_df)
  return data_df_kg_m3