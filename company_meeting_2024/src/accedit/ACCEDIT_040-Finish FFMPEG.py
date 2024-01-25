from rally import supplyChain
from __pl_files import RallyFiles
import logging
import __pl_logging
from __pl_status_transitions import StatusHelper
from ACCEDIT_status_transitions import STATUS_TRANSITIONS
from __state_manager import AccurateEditModule

STEP_NAME = "accurate_edit"
logger = logging.getLogger(STEP_NAME)
status_helper = StatusHelper(STATUS_TRANSITIONS, STEP_NAME)
rf = RallyFiles()

def eval_main(context):
    data = context.get("dynamicPresetData") or {}
    logger.info(f"dynamicPresetData: {data}\n----\n")

    status_helper.execute_transition("on_proxy_complete", parameters_dict=data)

    proxy_label = 'SdviProxy'
    if not rf.is_label_available(label=proxy_label):
        status_helper.execute_transition("on_proxy_missing", parameters_dict=data)
        return supplyChain.SupplyChainStep('statemanager',
                                           dynamic_preset_data={
                                               "status": "fail",
                                               "module": AccurateEditModule.NAME
                                           })

        # raise Exception(f'Unable to find proxy file: {proxy_label}')

    return supplyChain.SupplyChainStep('resume', dynamic_preset_data=data)

