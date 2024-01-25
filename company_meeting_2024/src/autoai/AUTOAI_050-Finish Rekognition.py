from rally import asset
from __pl_asset_status import RallyAssetStatus

def eval_main(context):

    status_helper = RallyAssetStatus()

    status_helper.remove_status_containing_text("Rekog", "AI Module")

    status_helper.add_status_if_unique("Rekog Celebrity: Complete", "AI Module", "fas fa-robot", "green")
    status_helper.add_status_if_unique("Rekog Moderation: Complete", "AI Module", "fas fa-robot", "green")
    status_helper.add_status_if_unique("Rekog Transcribe: Complete", "AI Module", "fas fa-robot", "green")

