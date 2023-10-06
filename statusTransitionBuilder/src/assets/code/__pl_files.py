""" This module provides helpers to access file attributes within rally."""
import logging
import json
import requests
import xmltodict
from rally import files, supplyChain, exceptions
from rally_token_auth import RallyTokenAuth


class MissingLabelException(Exception):
    """ Custom exceptions from RallyFiles module """

class RallyFiles:
    """
    This class provides helper functions to find if files are available,
    get file extension based on label, etc. and cache it so if it gets
    requested multiple times within a preset, it won't perform another API call
    """
    logger = logging.getLogger(__qualname__)

    def __init__(self):
        self.cache = {}

    def cache_inventory(self, asset_name_list):
        """ Cache the whole inventory ahead of time to avoid multiple get_inventory calls """
        for asset_name in asset_name_list:
            self.logger.info(f"Caching: {asset_name}")
            if asset_name not in self.cache:
                self.cache[asset_name] = {}
            for rallyfile in files.get_inventory(assetName=asset_name):
                label = rallyfile.label
                if label not in self.cache[asset_name]:
                    self.cache[asset_name][label] = [rallyfile]


    def is_label_available(self, label, asset_name=None):
        """ checks if a label is available
            returns the first rally_file found
        """
        cached_rally_files = self._from_cache(label, asset_name)
        if not cached_rally_files:
            self.logger.debug(f"Label does not exist: {label}")
            return None

        for rally_file in cached_rally_files:
            if self._is_rally_file_available(rally_file):
                return rally_file
        self.logger.debug("no available files found")
        return None

    def get_md5(self, label, asset_name=None):
        """ Returns the md5 value of a label
        (requires a hasher to have run on that job or the returned value will be null).
        """
        file_found = self.is_label_available(label, asset_name=asset_name)
        if not file_found:
            self.logger.debug(f"Label does not exist: {label}")
            return None
        return file_found.hashes.get("md5")

    def get_filesize(self, label, asset_name=None):
        """ Returns the size in bytes of a file."""
        file_found = self.is_label_available(label, asset_name=asset_name)
        if not file_found:
            self.logger.debug(f"Label does not exist: {label}")
            return None
        return file_found.locations[0].get("size", 0)

    def get_filename(self, label, asset_name=None, rsl=None):
        """ Returns the s3 uri for the first found rsl (using provided rsl if available) """
        file_found = self.is_label_available(label, asset_name=asset_name)
        if not file_found:
            self.logger.debug(f"Label does not exist: {label}")
            return None
        for location in file_found.locations:
            if not rsl or rsl in f"rsl://{location.get('rsl')}/":
                filename = location.get("name", "")
                self.logger.debug(f"filename: {filename}")
                return filename
        self.logger.debug(f"no files found for the requested rsl: {rsl}")
        return None

    def get_source_file_uri(self, label, asset_name=None, rsl=None):
        """ Returns the s3 uri for the first found rsl (using provided rsl if available) """
        file_found = self.is_label_available(label, asset_name=asset_name)
        if not file_found:
            self.logger.debug(f"Label does not exist: {label}")
            return None
        for location in file_found.locations:
            if not rsl or rsl in f"rsl://{location.get('rsl')}/":
                raw_url = location.get("url", "")
                self.logger.debug(f"raw url: {raw_url}")
                return raw_url
        self.logger.debug(f"no files found for the requested rsl: {rsl}")
        return None


    def update_file_tags(self, label, asset_name=None, add_tags=None, delete_tags=None):
        """ add and remove tags from a rallyFile and refresh the current cache """
        if not label:
            raise MissingLabelException(f"missing label: {label}")
        if not add_tags:
            add_tags = []
        if not delete_tags:
            delete_tags = []
        rally_file = self._from_cache(label, asset_name)
        if not rally_file:
            raise MissingLabelException(f"label does not exist: {label}:{asset_name}")

        rally_file[0].add_tags(add_tags)
        rally_file[0].remove_tags(delete_tags)

    def get_file_extension(self, label, asset_name=None):
        """ get extension of a label based on first file found
        """
        rfs = self._from_cache(label, asset_name)
        if not rfs:
            print(f"no label found for: {label}")
            return None
        if rfs[0].locations[0]:
            return rfs[0].locations[0].get("name").split(".")[-1]
        return ""

    def get_content_as_bytes(self, label, asset_name=None):
        """ returns the content as bytes """
        rally_file = self.is_label_available(label, asset_name)
        if not rally_file:
            return None
        raw_content = rally_file.content()
        return raw_content

    def get_content(self, label, encoding="utf-8", asset_name=None):
        """ returns the content of a label (needs to be under 50MB)"""
        rally_file = self.is_label_available(label, asset_name)
        if not rally_file:
            return None
        raw_content = rally_file.content()

        return raw_content.decode(encoding)

    def get_xml_content_as_dict(self, label, encoding="utf-8", asset_name=None):
        """ returns the content of a label as dict (needs to be under 50MB)"""
        content = self.get_content(label, encoding, asset_name)
        try:
            json_content = xmltodict.parse(content)
        except exceptions.RallyApiError as err:
            supplyChain.create_supply_chain_marker('There was an error reading the xml',
                                                   'fas fa-bug',
                                                   color='red')
            raise Exception(f'Error Parsing the XML: {err}') from err

        return json_content

    def get_content_as_dict(self, label, encoding="utf-8", asset_name=None):
        """
        returns the content of a label as dict (needs to be under 50MB)
        :param label:
        :param encoding:
        :return:
        """
        content = self.get_content(label, encoding, asset_name)

        try:
            json_content = json.loads(content)
        except exceptions.RallyApiError as err:
            supplyChain.create_supply_chain_marker('There was an error reading the content',
                                                   'fas fa-bug',
                                                   color='red')
            raise Exception(f'Error with the content - not JSON formatted. \n{err}') from err

        return json_content

    def _from_cache(self, label, asset_name=None):
        """ Return the file from the cache, pull via api if not available in cache yet """
        if asset_name not in self.cache:
            self.cache[asset_name] = {}
        self.logger.info(f"caching: {label}:{asset_name}")
        if label not in self.cache[asset_name]:
            self.cache[asset_name][label] = list(files.get_inventory(label=label, assetName=asset_name))
        return self.cache[asset_name][label]

    def _is_rally_file_available(self, rally_file):
        """ Return the RallyFile object if a file is available, None otherwise"""
        for location in rally_file.locations:
            if location.get('status') in ["available", "archive"]:
                return True
        return False

    @staticmethod
    def extract_json_from_fileuri(file_uri):
        """
        Static method reading a file uri and returning the content as json
        :param file_uri: (s3 or rsl path)
        :return: dict
        """
        if not file_uri:
            raise Exception("No `fileUri` found.")
        try:
            content = json.loads(files.read_file(file_uri))
            return content
        except exceptions.RallyApiError as err:
            raise Exception(f"failed to read: {file_uri}\nError: {err}") from err

    @staticmethod
    def extract_xml_from_fileuri(file_uri):
        """
        Static method reading a file uri and returning the content as json
        :param file_uri: (s3 or rsl path)
        :return: dict
        """
        if not file_uri:
            raise Exception("No `fileUri` found.")
        try:
            content = xmltodict.parse(files.read_file(file_uri))
            return content
        except exceptions.RallyApiError as err:
            raise Exception(f"failed to read xML file: {file_uri}\nError: {err}") from err

    @staticmethod
    def delete_labels_starting_with(partial_labels, tag=None):
        """ Delete all labels of current asset based on partial label matches """
        RallyFiles.logger.debug(f"Deleting partially matching reports with tag: {tag}: {partial_labels}")
        for rally_file in files.get_inventory(tag=tag):
            try:
                for prefix in partial_labels:
                    if rally_file.label.startswith(prefix):
                        files.remove_inventory(rallyfile=rally_file,
                                               mode="shared_delete")
            except exceptions.RallyApiError as err:
                RallyFiles.logger.error(f"Error: {err}")

    @staticmethod
    def delete_labels_by_exact_match(labels, tag=None):
        """ Delete all labels of current asset based on exact label matches """
        RallyFiles.logger.debug(f"Deleting reports with tag: {tag}: {labels}")
        for rally_file in files.get_inventory(tag=tag):
            try:
                for label in labels:
                    if rally_file.label == label:
                        files.remove_inventory(rallyfile=rally_file,
                                               mode="shared_delete")
            except exceptions.RallyApiError as err:
                RallyFiles.logger.error(f"Error: {err}")


    @staticmethod
    def _prepare_file_registration_body(file_uri, target_label, tag_list, asset_name):
        """ Prepares body for Rally api request """
        tags = {}
        for tag in tag_list:
            tags[tag] = True
        return {
            "data": {
                "type": "files",
                "attributes": {
                    "label": target_label,
                    "tagList": tags,
                    "tags": tags,
                    "available": True,
                    "instances": {
                        "1": {
                            "uri": file_uri,
                            "status": "available"
                        }
                    }
                },
                "relationships": {
                    "asset": {
                        "data": {
                            "attributes": {"name": asset_name},
                            "type": "assets"
                        }
                    }
                }
            }
        }


    @staticmethod
    def register_file_to_remote_asset(context, file_uri, label, tags, asset_name):
        """ Register a file against a remote asset (Caution when using this function, it can cause
        some race condition issues with ongoing supply chains)"""
        file_url = f"{context.get('rallyUrl')}/v2/files"
        body = RallyFiles._prepare_file_registration_body(file_uri, label, tags, asset_name)
        RallyFiles.logger.info(f"{json.dumps(body, indent=4)}")
        response = requests.post(file_url,
                                 json=body,
                                 auth=RallyTokenAuth(),
                                 timeout=60)
        print(response)
        if not response.ok:
            RallyFiles.logger.info(f"Problem registering the file: {response.json()}")
            raise Exception(response.json())
        return True
