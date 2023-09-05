import os, sys, shutil

_CIMEROOT = os.getenv("CIMEROOT")
sys.path.append(os.path.join(_CIMEROOT, "scripts", "Tools"))

from CIME.ParamGen.paramgen_nml import ParamGen_NML

class DART_input_nml(ParamGen_NML):
    def write(self, output_path, case):
        self.reduce(lambda varname: case.get_value(varname))
        self.write_nml(output_path)
