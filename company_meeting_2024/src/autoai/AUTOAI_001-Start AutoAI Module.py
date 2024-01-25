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

    # Get the provider that was selected in the Metadata Edit widget
    provider = data.get("provider", "").lower()
    logger.info(f"Provider selected: {provider}")

    provider_mapping = {
        "aws rekognition": "aws_rekog",
        "google video intelligence": "google_vi",
        "azure video indexer": "azure_vi"
    }
    if provider not in provider_mapping:
        logger.error(f"unsupported provider: {provider}")
        status_helper.execute_transition(f"on_unsupported_provider", parameters_dict=data)
        data.update({
            "status": "fail",
            "module": "ai"
        })
        return supplyChain.SupplyChainStep("statemanager", dynamic_preset_data=data)

    status_helper.execute_transition(f"on_start", parameters_dict=data)
    return supplyChain.SupplyChainStep(name=provider_mapping.get(provider),
                                       dynamic_preset_data=data)
















