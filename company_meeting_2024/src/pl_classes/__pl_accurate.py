""" This module contains the basic version of an accurate WO
    2 additional classes are derived from this basic version
"""
import dataclasses
import logging
import jmespath
import uuid
from __pl_files import RallyFiles
from __pl_technical import TechnicalReport as TechReport
from rally import asset

rallyfiles = RallyFiles()
tech_report = TechReport()


@dataclasses.dataclass
class Metadata:
    jpath: str
    key: str

    def get_config(self, user_md):
        """
        Get metadata value from SDVI usermetatada dict
        :param user_md:
        :return:
        """
        if not self.jpath or not self.key:
            return None
        return {
            "key": self.key,
            "value": jmespath.search(self.jpath, user_md)
        }


class FileItem:
    """ Class that represents a file in File Inventory"""

    def __init__(self, label, asset_name=None, required=False):
        self.label = label
        self.asset_name = asset_name
        self.required = required

    def __str__(self):
        return f"{self.label}:{self.asset_name}"

    def __eq__(self, other):
        return self.label == other.label and self.asset_name == other.asset_name

    @classmethod
    def from_dict(cls, details_dict):
        """
        Generate file item from dict
        :param details_dict:
        e.g. structure
            {
            "label": "",
            "asset_name": ""
            }
        :return:
        """
        if not details_dict:
            return None
        label = details_dict.get("label")
        asset_name = details_dict.get("asset_name")
        return cls(label, asset_name)

    def is_available(self):
        """
        Checks if file is available in file inventory.
        :return:
        """
        return rallyfiles.is_label_available(self.label, self.asset_name)

    def is_required(self):
        return self.required


class VideoItem(FileItem):
    def __init__(self, label, asset_name=None, required=True):
        super().__init__(label, asset_name, required)
        self.duration_tc = tech_report.get_duration_timecode(self.label, self.asset_name)
        self.framerate = tech_report.get_framerate_float(self.label, self.asset_name)


class AudioItem(FileItem):
    def __init__(self, name, label, asset_name=None, required=False, language=None, enabled=False):
        super().__init__(label, asset_name, required)
        self.name = name
        self.language = language
        self.enabled = enabled

    @classmethod
    def from_dict(cls, name, details_dict):
        """
        Generate file item from dict
        :param name: str
        :param details_dict: dict
        e.g. structure
            {
            "label": "",
            "asset_name": "",
            "language" : "",
            "enabled": ""
            }
        :return:
        """
        label = details_dict.get("label")
        asset_name = details_dict.get("asset_name")
        language = details_dict.get("language")
        enabled = details_dict.get("enabled", False)
        required = details_dict.get("required", False)
        return cls(name, label, asset_name, required, language, enabled)

    def get_config(self, index, source_manager):
        """
        Get basic Audio configuration for Accurate.
        :param index: int
        :param source_manager: sources
        :return: AccurateWO config
        """
        audio_uuid = source_manager.find_source_item(self).uuid
        config = {
            "src": f"<{audio_uuid}>",
            "channelCount": tech_report.get_audio_total_channel_count(self.label, self.asset_name),
            "enabled": self.enabled
        }
        if self.language:
            config["language"] = self.language
        if index:
            config["id"] = f"{index}".zfill(2)
        return config

    def get_validate_config(self, index, source_manager, video_framerate):
        """
        Get Audio configuration for validate. Validate has extra configuration items than basic.
        :param index:
        :param source_manager:
        :param video_framerate:
        :return: AccurateWO config
        """
        config = self.get_config(index, source_manager)
        audio_duration = tech_report.get_audio_track_audio_duration(self.label, self.asset_name)
        config.update({
            "codec": tech_report.get_audio_track_codec(self.label, self.asset_name) or "",
            "bitRate": tech_report.get_audio_track_bit_rate(self.label, self.asset_name) or 0,
            "sampleRate": tech_report.get_audio_track_sample_rate(self.label, self.asset_name) or 0,
            "duration": tech_report.convert_tc_to_frames(audio_duration, video_framerate),
        })
        if self.language:
            config["fileMetadata"] = [
                {
                    "key": "language",
                    "value": self.language
                }
            ]
        return config


class CaptionItem(FileItem):
    def __init__(self, name, label, asset_name=None, required=False, file_format=None, enabled=False, start_time=None):
        super().__init__(label, asset_name, required)
        self.name = name
        self.enabled = enabled
        self.format = file_format
        self.start_time = start_time

    @classmethod
    def from_dict(cls, name, details_dict):
        """
        Extract relevant keys from the dpd config.
        :param name: str
        :param details_dict: dict
        e.g. structure
        {
            "label": "",
            "asset_name": "",
            "format" : "",
            "start_time": "",
            "enabled": ""
        }
        :return:
        """
        label = details_dict.get("label")
        asset_name = details_dict.get("asset_name")
        file_format = details_dict.get("format")
        start_time = details_dict.get("start_time")
        enabled = details_dict.get("enabled")
        required = details_dict.get("required", False)
        return cls(name, label, asset_name, required, file_format, enabled, start_time)

    def get_config(self, index, source_manager, video_framerate):
        """
        Get Accurate configuration for captions
        :param index: int
        :param source_manager: sources
        :param video_framerate: str
        :return: AccurateWO config
        """
        subtitle_extension_dict = {
            "ttml": "ttml",
            "vtt": "webvtt",
            "webvtt": "webvtt",
            "xml": "ttml"
        }

        caption_uuid = source_manager.find_source_item(self).uuid
        config = {
            "src": f"<{caption_uuid}>",
            "enabled": self.enabled,
            "format": self.format or "vtt"
        }
        # Automatically find the file extension of the provided caption label
        file_extension = rallyfiles.get_file_extension(self.label, self.asset_name).lower()
        try:
            config["format"] = subtitle_extension_dict[file_extension]
        except KeyError as err:
            extensions = list(subtitle_extension_dict.keys())
            exception_msg = f"""Extension '{file_extension}'
                            detected for subtitle '{self.label}:{self.asset_name}' is unsupported.
                            File extension must match {extensions}"""
            raise Exception(exception_msg) from err
        # Check if a start TC was provided for the caption
        caption_start_time = self.start_time or 0
        if caption_start_time:
            config["startTime"] = {
                "frame": TechReport.convert_tc_to_frames(caption_start_time,
                                                         video_framerate),
                "denominator": 1,
                "numerator": float(video_framerate)
            }

        if index:
            config["id"] = f"{index}".zfill(2)
        return config


class TbmdItem(FileItem):
    def __init__(self, name, label, asset_name=None, required=False):
        super().__init__(label, asset_name, required)
        self.name = name

    @classmethod
    def from_dict(cls, name, details_dict):
        """
        Extract relevant keys from the dpd config.
        :param name: str
        :param details_dict: dict
        :return: AccurateWO config
        """
        label = details_dict.get("label")
        asset_name = details_dict.get("asset_name")
        required = details_dict.get("required", False)
        return cls(name, label, asset_name, required)

    def get_config(self, source_manager):
        """
        Get Accurate configuration for TBMD
        :param source_manager: sources
        :return: AccurateWO config
        """
        _uuid = source_manager.find_source_item(self).uuid
        return {
            self.name: f"<{_uuid}>"
        }


class SpritemapItem(FileItem):
    def __init__(self, name, label, asset_name=None, required=False):
        super().__init__(label, asset_name, required)
        self.name = name

    @classmethod
    def from_dict(cls, name, details_dict):
        """
        Extract relevant keys from the dpd config.
        :param name: str
        :param details_dict: dict
        :return: AccurateWO config
        """
        label = details_dict.get("label")
        asset_name = details_dict.get("asset_name")
        required = details_dict.get("required", False)
        return cls(name, label, asset_name, required)


class SpritemapManifestItem(SpritemapItem):
    def __init__(self, name, label, asset_name=None, required=False):
        super().__init__(name, label, asset_name, required)

    def get_config(self, source_manager):
        """
        Get Accurate configuration for Spritemap Manifest
        :param source_manager: sources
        :return: AccurateWO config
        """
        _uuid = source_manager.find_source_item(self).uuid
        return {
            "manifestSrc": f"<{_uuid}>"
        }


class SpritemapImageItem(SpritemapItem):
    def __init__(self, name, label, asset_name=None, required=False):
        super().__init__(name, label, asset_name, required)

    def get_config(self, source_manager):
        """
        Get Accurate configuration for Spritemap Image
        :param source_manager: sources
        :return: AccurateWO config
        """
        _uuid = source_manager.find_source_item(self).uuid
        return {
            "imageSrc": f"<{_uuid}>"
        }


@dataclasses.dataclass
class AccurateSource:
    """ Class responsible for the relationship between labels, asset name, and uuid.
    Used for refrencing files in the AccurateWO """
    label: str
    asset_name: str
    uuid: str

    def to_inputspec(self):
        """
        Convert to MIO input spec
        :return:
        """
        res = {
            self.uuid: {
                "label": self.label
            }
        }
        if self.asset_name:
            res[self.uuid]["asset"] = self.asset_name
        return res


@dataclasses.dataclass
class AccurateSourceManager:
    sources: list

    def find_source_item(self, item: FileItem):
        """
        Return the source item
        :param item:
        :return: source
        """
        for source in self.sources:
            if source.label == item.label and source.asset_name == item.asset_name:
                return source
        return

    def add_source_item(self, item: FileItem):
        """
        Add source item and generate uuid to prevent overriding similar named souces.
        :param item:
        :return: source
        """
        existing_source = self.find_source_item(item)
        if existing_source:
            return existing_source
        uuid_num = f"{uuid.uuid4()}"[:4]
        new_uuid = f"{uuid_num}[{item.label}]"
        new_source = AccurateSource(label=item.label,
                                    asset_name=item.asset_name,
                                    uuid=new_uuid)
        self.sources.append(new_source)
        return new_source


class AccurateLauncherException(Exception):
    """
    Exception used to capture generic Accurate exception
    while generating the necessary data
    """


class AccurateWorkOrder:
    """
    Basic Accurate workorder representation, allowing to turn a simplified input
    pointing at labels and extract necessary attributes to build a working
    "accurate" representation of a WO
    """
    logger = logging.getLogger(__qualname__)
    rallyfiles = RallyFiles()
    tech_report = TechReport()

    def __init__(self, payload, ignore_missing_files=False):
        """
        Initialize
        :param payload: Payload is the dynamic preset data
        :param ignore_missing_files: set to True to ignore missing files
        """
        self.source_manager = AccurateSourceManager([])
        self.video_item = self._extract_video_item(payload)
        self.audio_items = self._extract_audio_items(payload)
        self.caption_items = self._extract_caption_items(payload)
        self.start_tc = self._extract_start_tc(payload)
        self.ignore_missing_files = ignore_missing_files
        self.missing_file_items = []

    def _extract_video_item(self, payload):
        """ Add video file to sources """
        video_item = VideoItem.from_dict(payload.get("video_details", {}))
        self.source_manager.add_source_item(video_item)
        return video_item

    def _extract_audio_items(self, payload):
        """ Add video file to sources """
        audio_items = []
        for audio_name, audio_dict in payload.get("audio_details").items():
            audio_item = AudioItem.from_dict(audio_name, audio_dict)
            audio_items.append(audio_item)
            self.source_manager.add_source_item(audio_item)
        return audio_items

    def _extract_caption_items(self, payload):
        """ Add video file to sources """
        caption_items = []
        for caption_name, caption_dict in payload.get("caption_details").items():
            caption_item = CaptionItem.from_dict(caption_name, caption_dict)
            caption_items.append(caption_item)
            self.source_manager.add_source_item(caption_item)
        return caption_items

    def get_video_framerate(self):
        """ Returns the video framerate as a float """
        return self.video_item.framerate

    def _extract_start_tc(self, payload):
        """
        Get the Timecode from the string provided in the payload
        :param payload:
        :return:
        """
        return TechReport.convert_to_timecode(payload.get("start_tc") or "00:00:00:00",
                                              self.get_video_framerate())

    def get_input_specs(self, component_items):
        """ Return generated input Specs """
        res = {}
        for component in component_items:
            if isinstance(component, VideoItem):
                component = [component]
            for item in component:
                if item in self.missing_file_items:
                    continue
                res.update(self.source_manager.find_source_item(item).to_inputspec())
        return res

    def _get_missing_file_items(self, component_items):
        """
        Checks if file items are missing.
        :param component_items:
        :return:
        """
        missing_file_items = []
        missing_required_file_items = []
        for component in component_items:
            if isinstance(component, VideoItem):
                # Raise exception if a video item is missing. This is the only file that MUST be available.
                if not component.is_available():
                    raise AccurateLauncherException(f"Video item is not available: {component}")
                component = [component]
            for item in component:
                FileItem: item
                if not item.is_available():
                    if item.is_required():
                        missing_required_file_items.append(item)
                    missing_file_items.append(item)
        if not self.ignore_missing_files:
            message = ""
            if missing_required_file_items:
                str_missing_required_file_items = [str(i) for i in missing_required_file_items]
                message = f"Some files, marked as required, are missing: {str_missing_required_file_items}\n"
                raise AccurateLauncherException(message)
        return missing_file_items

    def _remove_optional_file_items(self, component_items):
        """
        Remove file items which are optional and missing.
        :param component_items:
        :return:
        """
        for j, item_list in enumerate(component_items):
            item_list_copy = item_list.copy()
            for n, item in enumerate(item_list_copy):
                if not item.is_required() and not item.is_available():
                    len_diff = len(item_list_copy)-len(component_items[j])
                    component_items[j].pop(n-len_diff)

    def _get_audio_tracks(self):
        """ Parses the info of each audio track provided
        and generates an accurate representation """
        res = {}
        index = 1
        for audio_item in self.audio_items:
            if audio_item in self.missing_file_items:
                continue
            res[audio_item.name] = audio_item.get_config(index, self.source_manager)
            index += 1
        return res

    def _get_subtitle_tracks(self):
        """
            Parses the info of each subtitle track provided
            and generates an accurate representation
        """
        res = {}
        index = 1
        for caption_item in self.caption_items:
            if caption_item in self.missing_file_items:
                continue
            res[caption_item.name] = caption_item.get_config(index, self.source_manager,
                                                             self.get_video_framerate())
            index += 1
        return res

    def get_video_data(self):
        """ Returns resolved data for accurate WO based on provided labels/asset_names """
        video_token = self.source_manager.find_source_item(self.video_item).uuid
        return {
            "audioTracks": self._get_audio_tracks(),
            "subtitles": self._get_subtitle_tracks(),
            "frameOffset": self.start_tc.frames - 1,
            "dropFrame": tech_report.is_dropframe(f"{self.video_item.duration_tc}",
                                                  self.get_video_framerate()),
            "frameRate": {
                "numerator": tech_report.framerate_numerator_int(self.video_item.label,
                                                                 self.video_item.asset_name),
                "denominator": 1000
            },
            "src": f"<{video_token}>",
            "advanced": False,
            "tbmd": {},
            "channelCount": tech_report.get_audio_total_channel_count(self.video_item.label,
                                                                      self.video_item.asset_name)
        }

    @staticmethod
    def check_components(errors, infos, payload, name):
        """ check the minimum attributes for audio/subtitle components have been provided """
        component_list = payload.get(name, {})
        if component_list:
            if not isinstance(component_list, dict):
                errors.append({
                    "key": f"{name}",
                    "description": "details not available or in the wrong format."
                })
            else:
                for item_key, item_data in component_list.items():
                    if isinstance(item_data, dict):
                        if "label" not in item_data.keys():
                            errors.append({
                                "key": f"{name}",
                                "description": f"label key not available for {item_key}"
                            })
                    else:
                        errors.append({
                            "key": f"{name}",
                            "description": "wrong format"
                        })
        else:
            infos.append({
                "key": f"{name}",
                "description": f"No `{name}` data provided. "
            })

    @staticmethod
    def check_dpd_keys(errors, infos, payload, required_keys, optional_keys):
        """
        Generate a list of info or errors based on available keys for a dynamic preset data
        :param errors: list
        :param infos: list
        :param payload: dynamic preset data (dict)
        :param required_keys: string
        :param optional_keys:
        :return:
        """
        for required_key in required_keys:
            if required_key not in payload.keys():
                errors.append({
                    "key": required_key,
                    "description": f"{required_key} not available"
                })

        for optional_key in optional_keys:
            if optional_key not in payload.keys():
                infos.append({
                    "key": optional_key,
                    "description": f"{optional_key} not available"
                })

    @staticmethod
    def check_dpd_format(payload):
        """
        This function validates the provided dpd is sufficient
        to convert into an accurate representation
        :param payload: dynamic preset data (dict)
        :return:
        """
        if not isinstance(payload, dict):
            return {
                "infos": [],
                "errors": [
                    {
                        "key": "dynamic_preset_data",
                        "description": "The dpd input is not in the right format."
                    }
                ]
            }
        infos = []
        errors = []

        required_keys = ["video_details"]
        optional_keys = ["audio_details", "caption_details", "ignore_missing_labels", "start_tc"]
        AccurateWorkOrder.check_dpd_keys(errors, infos, payload, required_keys, optional_keys)

        if errors:
            return {
                "infos": infos,
                "errors": errors
            }

        # check video label:
        if not payload.get("video_details") or not isinstance(payload.get("video_details"), dict):
            errors.append({
                "key": "video_details",
                "description": "Video details not available or in the wrong format."
            })

        # check audio and caption details:
        for _details in ["audio_details", "caption_details"]:
            AccurateWorkOrder.check_components(errors,
                                               infos,
                                               payload,
                                               _details)

        if not payload.get("start_tc"):
            infos.append({
                "key": "start_tc",
                "description": "No start_tc info provided"
            })
        if not payload.get("ignore_missing_labels"):
            infos.append({
                "key": "ignore_missing_labels",
                "description": """Option not specified / left to False
                -> will stop if anything is missing."""
            })

        return {
            "infos": infos,
            "errors": errors
        }


class AccurateBasicWO(AccurateWorkOrder):
    """ Basic Accurate workorder class """
    logger = logging.getLogger(__qualname__)

    def __init__(self, payload, ignore_missing_files=False):
        super().__init__(payload, ignore_missing_files)
        self.missing_file_items = self._get_missing_file_items([self.video_item,
                                                                self.audio_items,
                                                                self.caption_items])
        self._remove_optional_file_items([self.audio_items, self.caption_items])

    def get_input_specs(self):
        """
        Prepare the input specs for a specific accurate work order
        :return: resulting Work Order Dict
        """
        res = super().get_input_specs([self.video_item,
                                       self.audio_items,
                                       self.caption_items])
        return res


class AccurateValidateWO(AccurateWorkOrder):
    """ "Validate" variation of a "basic" Accurate workorder """
    logger = logging.getLogger(__qualname__)

    def __init__(self, payload, ignore_missing_files=False):
        super().__init__(payload, ignore_missing_files)
        self.tbmd_items = self._extract_tbmd_items(payload)
        self.sprite_items = self._extract_sprite_items(payload)
        self.metadata_list = self._extract_metadata_list(payload)
        self.missing_file_items = self._get_missing_file_items([self.video_item,
                                                                self.tbmd_items,
                                                                self.audio_items,
                                                                self.sprite_items,
                                                                self.caption_items])
        self._remove_optional_file_items([self.tbmd_items,
                                          self.audio_items,
                                          self.sprite_items,
                                          self.caption_items])

    def _extract_tbmd_items(self, payload):
        """
        Get tbmd items from dynamic preset data
        :param payload: dict
        :return: list of tbmd items
        """
        tbmd_files = []
        for tbmd_name, tbmd_file in (payload.get("tbmd_details") or {}).items():
            tbmd_file = TbmdItem.from_dict(tbmd_name, tbmd_file)
            self.source_manager.add_source_item(tbmd_file)
            tbmd_files.append(tbmd_file)
            self.logger.info(f"Adding tbmd: {tbmd_file}")
        return tbmd_files

    def _extract_sprite_items(self, payload):
        """
        Get sprite items from dynamic preset data
        :param payload: dict
        :return: list of spritemap items
        """
        spritemap_files = []
        spritemap_details = payload.get("spritemap_details", {})
        spritemap_image = SpritemapImageItem.from_dict('image',
                                                       spritemap_details.get("spritemap_image", {}))
        spritemap_manifest = SpritemapManifestItem.from_dict('manifest',
                                                             spritemap_details.get("spritemap_manifest", {}))
        if not spritemap_details:
            return spritemap_files
        for item in [spritemap_image, spritemap_manifest]:
            self.source_manager.add_source_item(item)
            spritemap_files.append(item)
            self.logger.info(f"Adding spritemap {item.name}: {item.label}")
        return spritemap_files

    @staticmethod
    def _extract_metadata_list(payload):
        """
        Retrieve from all metadata key/value pairs found in payload.
        :param payload: dict
        :return: list of metadata items
        """
        md_list = []
        for item in payload.get("metadata", []):
            md_list.append(Metadata(jpath=item.get("jmespath"),
                                    key=item.get("key")))

        return md_list

    def _get_audio_tracks(self):
        """
        Bypass the function to use validate config instead
        :return: resulting Work Order Dict
        """
        res = {}
        index = 1
        for audio_item in self.audio_items:
            res[audio_item.name] = audio_item.get_validate_config(index,
                                                                  self.source_manager,
                                                                  self.get_video_framerate())
            index += 1
        return res

    @staticmethod
    def check_dpd_format(payload):
        """
        Function to validate the edit part of a WO.
        :param payload: dynamic preset data
        :return: dict (containing only infos/errors)
        """
        res = AccurateBasicWO.check_dpd_format(payload)
        infos, errors = res.get("infos"), res.get("errors")
        optional_keys = ["spritemap_details", "tbmd_details"]
        AccurateValidateWO.check_dpd_keys(errors,
                                          infos,
                                          payload,
                                          [],
                                          optional_keys)
        if errors:
            return {
                "infos": infos,
                "errors": errors
            }

        # check tbmd files
        AccurateBasicWO.check_components(errors,
                                         infos,
                                         payload.get("tbmd_details"),
                                         "tbmd_details")
        # check sprite details
        if not isinstance(payload.get("spritemap_details"), dict):
            infos.append({
                "key": "sprite_details",
                "description": "no sprite_details information provided"
            })
        else:
            required_keys = ["spritemap_image", "spritemap_manifest"]
            for required_key in required_keys:
                if required_key not in payload.get("spritemap_details").keys():
                    errors.append({
                        "key": "spritemap_details",
                        "description": f"{required_key} key not available"
                    })
                else:
                    required_key_config = jmespath.search(f"spritemap_details.{required_key}", payload)
                    if "label" not in required_key_config.keys():
                        errors.append({
                            "key": "spritemap_details",
                            "description": f"label key not available for {required_key}"
                        })
        return {
            "infos": infos,
            "errors": errors
        }

    def get_input_specs(self):
        """
        Prepare the input specs for a specific accurate work order
        :return: resulting Work Order Dict
        """
        res = super().get_input_specs([self.video_item,
                                       self.tbmd_items,
                                       self.sprite_items,
                                       self.audio_items,
                                       self.caption_items])
        return res

    def _add_spritemap_if_available(self, res):
        """
        If Spritemaps are found, add it to the Accurate WO
        :param res: resulting Work Order Dict
        :return:
        """
        spritemap_dict = {}
        for spritemap_item in self.sprite_items:
            self.logger.info(f"spritemap -> {spritemap_item.name} - {spritemap_item.label}:{spritemap_item.asset_name}")
            spritemap_dict.update(spritemap_item.get_config(self.source_manager))
        if spritemap_dict and len(spritemap_dict) < 2:
            self.logger.info("Spritemap skipped due to either missing Image or Manifest file")
            return
        res["spritemap"] = spritemap_dict

    def _add_tbmd_if_available(self, res):
        """
        If TBMD is found, add it to the Accurate WO
        :param res: resulting Work Order Dict
        :return:
        """
        tbmd_dict = {}
        for tbmd_item in self.tbmd_items:
            self.logger.info(f"tbmd -> {tbmd_item.name} - {tbmd_item.label}:{tbmd_item.asset_name}")
            tbmd_dict.update(tbmd_item.get_config(self.source_manager))
        res["tbmd"] = tbmd_dict

    def _get_metadata_values(self):
        """ Temporary retrieve the asset metadata """
        user_md = asset.get_user_metadata() or {}
        metadata_output = []
        for metadata_item in self.metadata_list:
            md_config = metadata_item.get_config(user_md)
            if not md_config:
                continue
            metadata_output.append(md_config)

        return metadata_output

    def get_video_data(self):
        """ Return resolved data for accurate WO based on provided labels/asset_names """
        res = super().get_video_data()
        res.update({
            "startTimeFrame": self.start_tc.frames - 1,
            "duration": f"{tech_report.get_duration_timecode(self.video_item.label, self.video_item.asset_name)}",
            "advanced": True,
            "app": "validate",
            "resolution": tech_report.get_resolution(self.video_item.label, self.video_item.asset_name),
            "aspectRatio": tech_report.get_aspect_ratio(self.video_item.label, self.video_item.asset_name),
            "bitRate": tech_report.get_video_general_overall_bitrate(self.video_item.label,
                                                                     self.video_item.asset_name) or 0,
            "codec": tech_report.get_video_general_codec(self.video_item.label, self.video_item.asset_name) or "",
            "metadata": self._get_metadata_values()
        })

        # Deal with spritemap and tbmd
        self._add_spritemap_if_available(res)
        self._add_tbmd_if_available(res)

        print(f"finished preparing the video data: {res}")
        return res


class AccurateEditWO(AccurateValidateWO):
    """ Edit variation of a "validate" Accurate workorder class """
    logger = logging.getLogger(__qualname__)

    def get_video_data(self):
        """ Prepare the same payload as a "validate" WO,
        and changes the app/sourcename"""
        res = super().get_video_data()
        res["app"] = "edit"
        res["sourceName"] = self.source_manager.find_source_item(self.video_item).uuid
        return res

    @staticmethod
    def check_dpd_format(payload):
        """ Function to validate the edit part of a WO """
        res = AccurateValidateWO.check_dpd_format(payload)
        infos = res.get("infos")
        errors = res.get("errors")
        return {
            "infos": infos,
            "errors": errors
        }


class AccurateConfiguration():
    def __init__(self):
        self.input_specs = {}
        self.video_data = {}

    def add_input_specs_dict(self, spec_dict):
        self.input_specs.update(spec_dict)

    def add_video_specs_dict(self, name, spec_dict):
        self.video_data.update({name: spec_dict})

    def get_specs(self):
        return self.__dict__


class Spritemap:
    """ Class used to facilitate the generation of a spritemap """

    logger = logging.getLogger(__qualname__)

    def __init__(self, label, column_len=10):
        tech_report = TechReport()
        self.row_len = 0  # Number of images from top to bottom
        self.column_len = column_len  # Number of images from left to right
        self.snapshots_sec_list = []
        self.framerate = round(tech_report.get_framerate_float(label))
        self.duration_timecode = tech_report.get_duration_timecode(label)

    def get_ffmpeg_commands(self, frequency=3):
        """
        Generate ffmpeg commands. Specify frequency to create more/less images per minute interval of video.
        :param frequency: Number of images generated per minute. Default 3 image per minute.
                frequency = 3, 3 images per minute of video
                frequency = 60, 60 images per minute of video or 1 image per second
        :return:
        """
        img_interval = int(60 / frequency) or 1
        duration_secs = round(self.duration_timecode.frames / self.framerate)  # frames: 17602
        positions = range(0, duration_secs, img_interval)
        number_of_images = len(positions)
        commands_dict = {
            "spritemap_ffmpeg_images": {
                "seconds": [],
                "outputs": []
            },
            "spritemap_ffmpeg_output": {
                "input": "",
                "filter-complex": ""
            }
        }
        for x, i in enumerate(positions):
            commands_dict["spritemap_ffmpeg_images"]["seconds"].append(str(i))
            commands_dict["spritemap_ffmpeg_images"]["outputs"].append("output_%s.jpg" % x)
        command_input = ["-i output_%s.jpg" % i for i in range(number_of_images)]
        chunked_list = [command_input[i:i + self.column_len] for i in range(0, len(command_input), self.column_len)]
        hstrips = []
        commands_dict["spritemap_ffmpeg_htform"] = {"input": "", "filter_complex": ""}
        commands_dict["spritemap_ffmpeg_vtform"] = {"inputs": [], "outputs": [], "filter_complex": ""}
        for x, image_arr in enumerate(chunked_list):
            if len(image_arr) % self.column_len:
                diff = self.column_len - len(image_arr)
                # Pad the rest of the images with the last image found, this assures complete coverage of image canvas
                for i in range(diff):
                    image_arr.append(image_arr[-1])
            filter_complex = f"hstack=inputs={self.column_len}"
            ffmpeg_input = " ".join(image_arr)
            output_name = f"hstrip_{x}.jpg"
            commands_dict["spritemap_ffmpeg_vtform"]["inputs"].append(ffmpeg_input)
            commands_dict["spritemap_ffmpeg_vtform"]["outputs"].append(output_name)
            commands_dict["spritemap_ffmpeg_vtform"]["filter_complex"] = filter_complex
            hstrips.append(output_name)
        commands_dict["spritemap_ffmpeg_htform"]["input"] = " ".join([f"-i {i}" for i in hstrips])
        commands_dict["spritemap_ffmpeg_htform"]["filter_complex"] = f"vstack=inputs={len(hstrips)}"
        self.row_len = len(hstrips)
        self.snapshots_sec_list = commands_dict["spritemap_ffmpeg_images"]["seconds"]
        return commands_dict

    def get_manifest_dict(self):
        """
        Creates a spritemap image mapping dict from spritemap image specs
        :return: dict
        """
        spr_width, spr_height = 240, 135

        def generate_new_sprite_coords(_x, _y, _t):
            _dict = {
                "x": _x,
                "y": _y,
                "t": _t
            }
            return _dict

        video_timecode_duration_secs = self.duration_timecode.frames / float(self.duration_timecode.framerate)
        self.logger.info("Duration", video_timecode_duration_secs)
        canvas_width, canvas_height = self.column_len * spr_width, spr_height * self.row_len

        canvas = {
            "x": canvas_width,
            "y": canvas_height
        }

        sprite_map_dict = {
            "width": spr_width,
            "height": spr_height,
            "sprites": []
        }

        x_coords = [i for i in range(0, canvas['x'], spr_width)]
        y_coords = [i for i in range(0, canvas['y'], spr_height)]

        flick = 705600000  # Each flick is ~1 second
        # We use the duration of the video to calculate evenly the number of spritemap images shown in
        # the accurate timeline
        interval = int(video_timecode_duration_secs / ((canvas_width / spr_width) * (canvas_height / spr_height)))
        image_count = 0
        for y in y_coords:
            for x in x_coords:
                if image_count < len(self.snapshots_sec_list):
                    t_time = flick * int(self.snapshots_sec_list[image_count])
                    sprite_dict = generate_new_sprite_coords(x, y, t_time)
                    sprite_map_dict["sprites"].append(sprite_dict)
                    image_count += 1
        return sprite_map_dict
