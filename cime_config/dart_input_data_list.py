import os, sys, shutil

_CIMEROOT = os.getenv("CIMEROOT")
sys.path.append(os.path.join(_CIMEROOT, "scripts", "Tools"))

from CIME.ParamGen.paramgen_nml import ParamGen

class DART_input_data_list(ParamGen):
    '''Stage DART input_data_list file'''

    def write(self, output_path, case):

        self.reduce(lambda varname: case.get_value(varname))

        with open(os.path.join(output_path), 'w') as f:
            for file_category, file_paths in self.data['dart.input_data_list'].items():
                if file_paths is not None:
                    if not isinstance(file_paths, list):
                         file_paths = [file_paths]
                    for i,file_path in enumerate(file_paths):
                        file_path = file_path.replace('"','').replace("'","")
                        if os.path.isabs(file_path):
                            f.write(f"{file_category.strip()}({str(i)}) = {file_path}\n")
                else:
                    pass # skip if custom INPUTDIR is used.



                
