from rally import supplyChain
import logging
import __pl_logging
from __pl_status_transitions import StatusHelper
from AUTOAI_transitions import STATUS_TRANSITIONS

STEP_NAME = "ai"
logger = logging.getLogger(STEP_NAME)
status_helper = StatusHelper(STATUS_TRANSITIONS, STEP_NAME)

def eval_main(context):
    data = context.get('dynamicPresetData') or {}
    logger.info(f"dynamic_preset_Data: {data}\n----\n")

    ai_provider = data.get("ai_provider")

    status_helper.execute_transition(f"on_complete",
                                     parameters_dict=data)

    return supplyChain.SupplyChainStep("statemanager",
                                       dynamic_preset_data={
                                           "status": "complete",
                                           "module": "ai",
                                           "provider": ai_provider
                                       })
