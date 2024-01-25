from rally import supplyChain
import logging
import __pl_logging
from __pl_status_transitions import StatusHelper
from AUTOAI_transitions import STATUS_TRANSITIONS
from AUTOAI_rekognition_config import MODULE_NAME
from __pl_files import RallyFiles

STEP_NAME = "ai"
logger = logging.getLogger(STEP_NAME)
status_helper = StatusHelper(STATUS_TRANSITIONS, STEP_NAME)
rf = RallyFiles()

def eval_main(context):
    data = context.get('dynamicPresetData') or {}
    logger.info(f"dynamic_preset_Data: {data}\n----\n")
    data["module_name"] = MODULE_NAME

    status_helper.execute_transition(f"on_aws_rekog", parameters_dict=data)

    data["ai_provider"] = "rekog"

    proxy_label = "SdviProxy"
    if rf.is_label_available(proxy_label):
        status_helper.execute_transition("on_ai_start", parameters_dict=data)

        split = supplyChain.SupplyChainSplit(supplyChain.SupplyChainStep("join", dynamic_preset_data=data))
        split.add_split("celeb")
        split.add_split("moderation")
        split.add_split("transcribe")

        return split

    logger.info("Proxy creation required")
    status_helper.execute_transition("on_proxy_needed", parameters_dict=data)

    return supplyChain.SupplyChainStep("prepare_ffmpeg", dynamic_preset_data=data)
