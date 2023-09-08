from CIME.XML.standard_module_setup import *
from CIME.SystemTests.system_tests_common import SystemTestsCommon
from CIME.SystemTests.system_tests_common import SystemTestsCommon
from CIME.case.case_run import _do_data_assimilation
import glob

logger = logging.getLogger(__name__)


class DAG(SystemTestsCommon):
    """
    Implementation of DART-OCN data assimilation test.
    """

    def __init__(self, case, **kwargs):
        """
        initialize an object interface to the DAT system test
        """
        SystemTestsCommon.__init__(self, case, **kwargs)

    def _dat_first_phase(self):
        stop_n = self._case.get_value("STOP_N")
        stop_option = self._case.get_value("STOP_OPTION")
        expect(stop_n > 0, "Bad STOP_N: {:d}".format(stop_n))

        self._case.set_value("REST_OPTION", stop_option)
        self._case.set_value("REST_N", stop_n)

        logger.info(
            "doing an initial run with no data assimilation"
        )
        self.run_indv()

    def _dat_second_phase(self):

        logger.info(
            "doing a continued run with data assimilation enabled"
        )
        self._case.set_value("STOP_N", 1)
        self._case.set_value("STOP_OPTION", "ndays")
        self._case.set_value("CONTINUE_RUN", True)
        self._case.set_value("DATA_ASSIMILATION_OCN", True)
        self._case.set_value("DATA_ASSIMILATION_CYCLES", 1)
        self._case.flush()
        self._case.create_namelists() 
        self.build_indv()
        self._skip_pnl = False
        ###self.run_indv(suffix="rest")
        self.run_indv()

        # Compare restart file
        ###self._component_compare_test("base", "rest")

    def run_phase(self):
        self._dat_first_phase()
        self._dat_second_phase()
