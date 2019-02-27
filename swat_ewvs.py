import os
import zipfile, io
import pandas, numpy, itertools


rch_zf = zipfile.ZipFile('./Data/output_rch.zip', 'r')
sub_zf = zipfile.ZipFile('./Data/output_sub.zip', 'r')

rch_data = io.StringIO(rch_zf.read('output.rch').decode('utf_8'))
sub_data = io.StringIO(sub_zf.read('output.sub').decode('utf_8'))

rch_ds = pandas.read_fwf(rch_data, widths = [5, 5, 9, 6, 12, 12, 12, 12, 12], skiprows = 8, parse_dates = False)
sub_ds = pandas.read_fwf(sub_data, widths = [6, 4, 9, 5, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10], skiprows = 8, parse_dates = False)

subs = sub_ds.SUB.unique()
yrs = list(itertools.chain.from_iterable(itertools.repeat(x, len(subs) * 12) for x in range(1985, 2007)))

rch_z = rch_ds[rch_ds['MON'] <= 12]
sub_z = sub_ds[sub_ds['MON'] <= 12]

rch_z['YEAR'] = yrs
sub_z['YEAR'] = yrs

rch_zz = rch_z.groupby(['YEAR', 'MON']).mean()
sub_zz = sub_z.groupby(['YEAR', 'MON']).mean()

ewvs = {'EWV_PRECIPITATION'       : sub_zz['PRECIPmm'],
        'EWV_ET'                  : sub_zz['ETmm'],
        'EWV_PET'                 : sub_zz['PETmm'],
        'EWV_SNOW_MELT'           : sub_zz['SNOMELTmm'],
        'EWV_SOIL_MOISTURE'       : sub_zz['SWmm'],
        'EWV_GW_Q'                : sub_zz['GW_Qmm'],
        'EWV_AQU_RECHARGE'        : sub_zz['PERCmm'],
        'EWV_RUNOFF'              : sub_zz['SURQmm'],
        'EWV_WATER_YIELD'         : sub_zz['WYLDmm'],
        'EWV_N_RUNOFF'            : sub_zz['NSURQkg/ha'],
        'EWV_RIVER_FLOWcms'       : rch_zz['FLOW_OUTcms'],
        'EWV_NO3_OUTkg'               : rch_zz['NO3_OUTkg']
        }

ewvs_df = pandas.DataFrame(data = ewvs)

ewvs_df = ewvs_df.drop(ewvs_df.columns[[2, 3, 4]], axis=1)

print(ewvs_df)
