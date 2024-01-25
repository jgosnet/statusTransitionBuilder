from __pl_files import RallyFiles
from __pl_asset_status import RallyAssetStatus
import logging
import __pl_logging
from __pl_status_transitions import StatusHelper
from ACCEDIT_status_transitions import STATUS_TRANSITIONS
from ACCEDIT_utils import FileItem
from rally import supplyChain
from __state_manager import AccurateEditModule

STEP_NAME = "accurate_edit"
logger = logging.getLogger(STEP_NAME)
status_helper = StatusHelper(STATUS_TRANSITIONS, STEP_NAME)
rf = RallyFiles()

def eval_main(context):
    data = context.get("dynamicPresetData") or {}
    logger.info(f"dynamicPresetData: {data}\n----\n")

    status_helper.execute_transition("on_render_complete", parameters_dict={})


    accurate_ame_render_label = 'ACC_Edit_Render'
    if not rf.is_label_available(label=accurate_ame_render_label):
        status_helper.execute_transition("on_missing_render", parameters_dict={})
        return supplyChain.SupplyChainStep("statemanager", dynamic_preset_data={
            "module": AccurateEditModule.NAME,
            "status": "fail"
        })

    status_helper.execute_transition("on_complete", parameters_dict={})

    # Todo: Change to resume for state manager and add an additional necessary information
    return supplyChain.SupplyChainStep("statemanager", dynamic_preset_data={
        "module": AccurateEditModule.NAME,
        "status": "complete"
    })

