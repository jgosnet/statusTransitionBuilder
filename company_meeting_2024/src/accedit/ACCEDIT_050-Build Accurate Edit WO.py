from __pl_accurate import AccurateEditWO
from __pl_accurate import AccurateConfiguration
from __pl_files import RallyFiles
from __pl_asset_status import RallyAssetStatus
from rally import asset, supplyChain
import json
import logging
import __pl_logging
from __pl_status_transitions import StatusHelper
from ACCEDIT_status_transitions import STATUS_TRANSITIONS
from ACCEDIT_utils import FileItem

STEP_NAME = "accurate_edit"
logger = logging.getLogger(STEP_NAME)
status_helper = StatusHelper(STATUS_TRANSITIONS, STEP_NAME)
rf = RallyFiles()


def get_sample_secondary_files():
    return [
        {
            "assetName":"SDVI VOD Opens",
            "label":"SDVI_Stinger_10sec_Proxy"
        },
        {
            "assetName":"SDVI VOD Opens",
            "label":"SDVI_Stinger_5sec_Proxy"
        }
    ]


def get_accurate_dpd_format(label, asset_name):

    return {
        "ignore_missing_labels": False,
        "start_tc": "00:00:00;00",
        "video_details": {
            "label": label,
            "asset_name": asset_name
        },
        "audio_details": {
        },
        "caption_details": {
        },
        "tbmd_details": {
        },
        "spritemap_details": {
        },
        "metadata": [
        ]
    }


def eval_main(context):
    data = context.get("dynamicPresetData") or {}
    logger.info(f"dynamicPresetData: {data}\n----\n")

    status_helper.execute_transition("on_edl_prep",
                                     parameters_dict=data)


    primary_asset_name = asset.get_asset()["name"]
    primary_proxy_label = "SdviProxy"
    secondary_files = data.get("secondary_files", [])

    # Uncomment below if you want canned secondary files
    #secondary_files = get_sample_secondary_files()

    primary_work_order = AccurateEditWO(get_accurate_dpd_format(label=primary_proxy_label,
                                                                asset_name=primary_asset_name),
                                        ignore_missing_files=False)
    secondary_work_orders = []

    # Workaround to get multiple files added to an accurate session
    if secondary_files:
        for file_data in secondary_files:
            file_item = FileItem.from_file_collection(file_data)
            secondary_work_order_data = AccurateEditWO(get_accurate_dpd_format(file_item.label,
                                                                               file_item.asset_name),
                                                       ignore_missing_files=True)
            secondary_work_orders.append(secondary_work_order_data)

    accurate_configuration = AccurateConfiguration()
    accurate_configuration.add_input_specs_dict(primary_work_order.get_input_specs())
    accurate_configuration.add_video_specs_dict('video', primary_work_order.get_video_data())

    if secondary_work_orders:
        for index, work_order in enumerate(secondary_work_orders):
            accurate_configuration.add_input_specs_dict(work_order.get_input_specs())
            accurate_configuration.add_video_specs_dict(f'secondary_{index + 1}', work_order.get_video_data())


    logger.info(f'-----Accurate Edit Work Order Data-----')
    logger.info(f'{json.dumps(accurate_configuration.get_specs(), indent=4)}')

    data['accurateEditWorkOrderData'] = accurate_configuration.get_specs()

    # utils_asset_status.add_status_if_unique(message='Accurate Edit: Work Order Open',
    #                                         group='Edit Module',
    #                                         icon='fas fa-clipboard-list',
    #                                         color='blue',
    #                                         curate_message=True,
    #                                         curate_group=True)

    status_helper.execute_transition("on_active_wo",
                                     parameters_dict=data)

    sequence = supplyChain.SupplyChainSequence()
    sequence.add_step(supplyChain.SupplyChainStep(name='resume', dynamic_preset_data=data))
    sequence.add_step(supplyChain.SupplyChainStep(name='resume', dynamic_preset_data=data))

    return sequence

