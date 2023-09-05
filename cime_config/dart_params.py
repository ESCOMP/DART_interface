import os, sys, shutil

_CIMEROOT = os.getenv("CIMEROOT")
sys.path.append(os.path.join(_CIMEROOT, "scripts", "Tools"))

from CIME.ParamGen.paramgen_nml import ParamGen

class DART_params(ParamGen):
    '''A minimalistic DART_params.csh file intended to be sourced by assimilate.csh script only.'''
    def write(self, output_path, case):
        self.reduce(lambda varname: case.get_value(varname))
        with open(os.path.join(output_path), 'w') as f:
          f.write(
              '#!/bin/csh\n'
              '#\n'
              '# A minimalistic DART_params.csh file intended to be sourced by assimilate.csh script only.\n'
              '#\n\n'
          )
          for var, val in self.data.items():
              if val is not None:
                  f.write(f'set {var} = {val}\n')
                
