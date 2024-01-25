from rally import supplyChain
from __pl_files import RallyFiles
from __pl_asset_status import RallyAssetStatus
import logging
import __pl_logging
from __pl_status_transitions import StatusHelper
from ACCEDIT_status_transitions import STATUS_TRANSITIONS
from ACCEDIT_utils import FileItem

STEP_NAME = "accurate_edit" 
logger = logging.getLogger(STEP_NAME)
status_helper = StatusHelper(STATUS_TRANSITIONS, STEP_NAME)
rf = RallyFiles()

class TooManyPrimaryAssetsException(Exception):
    """ """

class MissingFileException(Exception):
    """ """


def eval_main(context):
    data = context.get("dynamicPresetData") or {}
    logger.info(f"dynamicPresetData: {data}\n----\n")

    status_helper.execute_transition("on_init", parameters_dict={})
    # utils_asset_status = RallyAssetStatus()
    # utils_asset_status.remove_status_containing_text(contained_string='Accurate Edit', group='Edit Module')

    # Check if there are multiple Primary Assets Found and raise exception if so
    primary_assets = data.get('primary_asset', [])
    if len(primary_assets) > 1:
        status_helper.execute_transition("on_too_many_primary", parameters_dict={})
        raise TooManyPrimaryAssetsException(f'Multiple Primary Assets Found In Collection Bin. Assets Found are {primary_assets}. Stopping Supply Chain')

    # Check that Secondary Files Exist and Raise Exception if they do not
    for secondary_file in data.get('secondary_files', []):
        file_item = FileItem.from_file_collection(secondary_file)
        if not rf.is_label_available(file_item.label, file_item.asset_name):
            status_helper.execute_transition("on_missing_file", parameters_dict={})
            raise MissingFileException(f'Secondary file {file_item} not Found. Stopping Supply Chain')

    # utils_asset_status.add_status_if_unique(message='Accurate Edit: Module Started',
    #                                         group='Edit Module',
    #                                         icon='fas fa-play',
    #                                         color='blue',
    #                                         curate_message=True,
    #                                         curate_group=True)
    status_helper.execute_transition("on_start", parameters_dict={})

    # Check if Primary Asset proxy exists to determine next steps
    primary_edit_proxy_label = 'SdviProxy'
    if not rf.is_label_available(label=primary_edit_proxy_label):
        status_helper.execute_transition("on_proxy_needed", parameters_dict={})
        return supplyChain.SupplyChainStep('proxy', dynamic_preset_data=data)

    return supplyChain.SupplyChainStep('resume', dynamic_preset_data=data)

