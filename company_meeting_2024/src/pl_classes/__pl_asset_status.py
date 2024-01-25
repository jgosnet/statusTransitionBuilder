"""
Author: Julien Gosnet
Last modified: Mon, 13-Mar-2023 04:07:54, US Mountain Standard Time
"""
""" This module contains functions to facilitate the manipulation of asset status within rally """
import logging
from rally import asset

class RallyAssetStatus:
    """ Helper class to deal with more complex operations on Asset Status such as:
        - avoiding duplicates,
        - deleting partial matches,
        - etc.
    """
    logger = logging.getLogger(__qualname__)

    @staticmethod
    def get_matching_status(message, group=None):
        """ Return a list of status matching a message (Any group if Group=None) """
        matching_statuses = []
        for status_indicator in asset.get_asset_status_indicators(group=group):
            if status_indicator.get("message") == message and not status_indicator.get("cleared"):
                matching_statuses.append(status_indicator)
        return matching_statuses

    @staticmethod
    def get_partial_status(message, group=None):
        """ Return a list of status partial message patches (Any group if Group=None) """
        partial_statuses = []
        for status_indicator in asset.get_asset_status_indicators(group=group):
            if message in status_indicator.get("message", "") and not status_indicator.get("cleared"):
                partial_statuses.append(status_indicator)
        return partial_statuses

    @staticmethod
    def add_status_if_unique(message, group, icon, color, curate_message=False,  curate_group=False):
        """ Checks if asset_status already exists before adding a new one """
        matching_status_list = RallyAssetStatus.get_matching_status(message, group)
        # only add if not already in the group
        if not matching_status_list:
            RallyAssetStatus.logger.debug(f"status does not already exist. Adding: {group}-{message}")
            asset.add_asset_status_indicator(message,
                                             group,
                                             icon,
                                             color,
                                             curate_message=curate_message,
                                             curate_group=curate_group)
        else:
            RallyAssetStatus.logger.debug(f"status already exist. {group}-{message}")

    @staticmethod
    def remove_status(message, group=None):
        """ Delete status based on message (Any group if Group=None) """
        matching_status_list = RallyAssetStatus.get_matching_status(message, group)
        for matching_status in matching_status_list:
            RallyAssetStatus.logger.debug(f"deleting asset status indicator: {matching_status.get('id')}")
            asset.clear_asset_status_indicator(indicator_id=matching_status.get('id'))

    @staticmethod
    def remove_status_containing_text(contained_string, group=None):
        """ Delete status based on partial message matches (Any group if Group=None) """
        containing_statuses = RallyAssetStatus.get_partial_status(contained_string, group)
        for matching_status in containing_statuses:
            RallyAssetStatus.logger.debug(f"deleting asset status indicator: {matching_status.get('id')}")
            asset.clear_asset_status_indicator(indicator_id=matching_status.get('id'))
