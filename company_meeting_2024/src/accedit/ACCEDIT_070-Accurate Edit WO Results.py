from rally import supplyChain
from __pl_files import RallyFiles
from __pl_asset_status import RallyAssetStatus
import jmespath
import json
import logging
import __pl_logging
from __pl_status_transitions import StatusHelper
from ACCEDIT_status_transitions import STATUS_TRANSITIONS
from ACCEDIT_utils import FileItem
from __state_manager import AccurateEditModule

STEP_NAME = "accurate_edit"
logger = logging.getLogger(STEP_NAME)
status_helper = StatusHelper(STATUS_TRANSITIONS, STEP_NAME)
rf = RallyFiles()

class MissingEDLException(Exception):
    """ """

def eval_main(context):
    data = context.get("dynamicPresetData") or {}
    logger.info(f"dynamicPresetData: {data}\n----\n")

    status_helper.execute_transition("on_complete_wo",
                                     parameters_dict=data)

    accurate_edl_label = 'accurate_edl'
    if not rf.is_label_available(label=accurate_edl_label):
        status_helper.execute_transition("on_edl_not_found", parameters_dict={})
        return supplyChain.SupplyChainStep('statemanager',
                                           dynamic_preset_data={
                                               "status": "fail",
                                               "module": AccurateEditModule.NAME
                                           })

    input_specs = jmespath.search('accurateEditWorkOrderData.input_specs', data) or {}
    input_specs['edl'] = {
        'label': accurate_edl_label
    }
    # Todo: Logic to switch input spec labels to High Res
    logger.info(f'-----AME Input Spec-----')
    logger.info(f'{json.dumps(input_specs, indent=4)}')

    data['ameData'] = {
        'input_specs': input_specs
    }

    # Todo: Logic to decide AME profile
    status_helper.execute_transition("on_render_start", parameters_dict={})
    # utils_asset_status.add_status_if_unique(message='Accurate Edit: AME Render Started',
    #                                         group='Edit Module',
    #                                         icon='fas fa-spinner',
    #                                         color='blue',
    #                                         curate_message=True,
    #                                         curate_group=True)

    sequence = supplyChain.SupplyChainSequence()
    sequence.add_step(supplyChain.SupplyChainStep(name='resume', dynamic_preset_data=data))
    sequence.add_step(supplyChain.SupplyChainStep(name='resume', dynamic_preset_data=data))

    return sequence

