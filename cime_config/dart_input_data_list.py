import os, sys, shutil

_CIMEROOT = os.getenv("CIMEROOT")
sys.path.append(os.path.join(_CIMEROOT, "scripts", "Tools"))

from CIME.ParamGen.paramgen_nml import ParamGen

class DART_input_data_list(ParamGen):
    '''Stage DART input_data_list file'''

    def write(self, output_path, case):

        self.reduce(lambda varname: case.get_value(varname))

        run_startdate = case.get_value("RUN_STARTDATE")
        run_startyear = int(run_startdate[:4])

        # run duration in seconds (upper limit)
        stop_option = case.get_value("STOP_OPTION").strip()
        stop_n = int(case.get_value("STOP_N"))
        upper_run_duration_sec = 0.0 + \
            ( \
                (stop_option == "nseconds") * 1 + \
                (stop_option == "nminutes") * 60 + \
                (stop_option == "nhours") * 3600 + \
                (stop_option == "ndays") * 86400 + \
                (stop_option == "nmonths") * 86400 * 31 + \
                (stop_option == "nyears") * 86400 * 366 \
            ) * stop_n
        
        assert upper_run_duration_sec>0, \
            "DART namelist generator couldn't determine the run duration. This is likely "+\
            "Due to an unsupported STOP_OPTION selection."

        #calculate an upper limit on run end year
        run_endyear = int(run_startyear + upper_run_duration_sec / (86400 * 360))

        data_assimilation = {
            cc: case.get_value(f"DATA_ASSIMILATION_{cc.upper()}")
            for cc in ["atm", "cpl", "ocn", "wav", "glc", "ice", "rof", "lnd"]
        }
        n_da_comp = sum(data_assimilation.values())

        # todo: to remove the below assertion, generalize the way file_year is deducted below
        assert n_da_comp==0 or (n_da_comp==1 and data_assimilation["ocn"] is True), \
            "While attempting to write dart.input_data_list, an unsupported combination of "+\
            "DATA_ASSIMILATION flag was encountered."

        with open(os.path.join(output_path), 'w') as f:
            for file_category, file_paths in self.data['dart.input_data_list'].items():
                if file_paths is not None:
                    if not isinstance(file_paths, list):
                         file_paths = [file_paths]
                    for i,file_path in enumerate(file_paths):
                        file_path = file_path.replace('"','').replace("'","")
                        file_year = int(file_path.split('.')[-1][:4]) #todo: generalize the way file_year is deducted.
                        if not (run_startyear <= file_year <= run_endyear):
                            continue
                        if os.path.isabs(file_path):
                            f.write(f"{file_category.strip()}({str(i)}) = {file_path}\n")
                else:
                    pass # skip if custom INPUTDIR is used.



                
