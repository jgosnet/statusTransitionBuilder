"""
Author: Julien Gosnet
Last modified: Mon, 13-Mar-2023 04:07:54, US Mountain Standard Time
"""
import dataclasses
import logging
from uuid import uuid4
from timecode import Timecode
import jmespath
from rally import asset
from rally.exceptions import NotFound
import __pl_logging
from __pl_files import RallyFiles
from __pl_technical import TechnicalReport



@dataclasses.dataclass
class AssetData:
    key: str
    asset_name: str
    label: str
    proxy_mapping: str
    tc_in: str = None
    tc_out: str = None
    duration_frames: int = 0
    include_video: bool = True
    include_audio: bool = True

    @classmethod
    def from_dict(cls, asset_data_dict):
        if asset_data_dict.get("source_alias"):
            key = asset_data_dict.get("source_alias")
        else:
            key = f'{str(uuid4())[:4]}_{asset_data_dict.get("label")}'
        return cls(asset_name=asset_data_dict.get("asset_name"),
                   key=key,
                   label=asset_data_dict.get("label"),
                   proxy_mapping=asset_data_dict.get("proxy_mapping"),
                   include_video=asset_data_dict.get("include_video", True),
                   include_audio=asset_data_dict.get("include_audio", True))

    def to_options(self):
        return {
            "include_video": self.include_video,
            "include_audio": self.include_audio,
        }

class RallySource:
    rally_files = RallyFiles()
    tech_report = TechnicalReport()
    logger = logging.getLogger(__qualname__)

    def __init__(self,
                 key,
                 label,
                 asset_name=None,
                 primary=False,
                 proxy_mapping=None,
                 name=None):
        self.source_type = "generic"
        self.key = key
        self.label = label
        self.asset_name = asset_name
        self.proxy_mapping = proxy_mapping
        self.primary = primary
        self.name = name or label

        self.mediainfo_report = RallySource.tech_report.get_report(self.label, self.asset_name)
        self.framerate = "29.97"

        self.errors = []
        self.is_valid = self._validate_source()

    def __str__(self):
        return f"{self.asset_name}:{self.label} ({self.source_type})"

    def to_json(self, use_proxy_mapping=False):
        res = {
            "label": self.label,
            "primary": self.primary
        }
        print(f"res: {res} --> use proxy: {use_proxy_mapping}")
        if use_proxy_mapping:
            res["label"] = self.proxy_mapping or self.label
        if self.asset_name:
            res["asset"] = self.asset_name
        # check the file type (extension + mediainfo)
        # if audio: check the audio layout
        return res

    def to_access3_media(self, bin_folder="./media", use_proxy_mapping=False):
        return {
            "token": self.key,
            "name": self.name,
            "bin": bin_folder
        }

    @staticmethod
    def create_rally_source(key,
                            label,
                            asset_name=None,
                            primary=False,
                            proxy_mapping=None,
                            default_framerate="29.97"):
        source_map = {
            "video": RallySourceVideo,
            "audio": RallySourceAudio,
            "text": RallySourceCaption
        }

        mediainfo_report = RallySource.tech_report.get_report(label, asset_name)
        for kind, source_class in source_map.items():
            try:
                RallySource.logger.info(f"{asset_name}:{label} (primary: {primary}) == {kind} file")
                return source_class(key=key,
                                    label=label,
                                    asset_name=asset_name,
                                    primary=primary,
                                    proxy_mapping=proxy_mapping,
                                    default_framerate=default_framerate)
            except Exception as err:
                RallySource.logger.info(f"function map does not exist for this type {kind}: {err}")
                continue
        RallySource.logger.info("Type not found")
        return None

    @classmethod
    def from_edl_source(cls, source_key, source_value):
        return cls(key=source_key,
                   label=source_value.get("label"),
                   asset_name=source_value.get("asset_name"))


    def retrieve_tc_in_out_frames(self,
                                  edit_rate,
                                  tc_in,
                                  tc_out=None,
                                  duration_frames=None):
        """
        Checks that the provided tcin and out are within bounds of the file
        :param edit_rate: provided by the edl
        :param tc_in: timecode
        :param tc_out: timecode
        :param duration_frames: int
        :return: Boolean: true if it is good, false if out of bounds.
        """
        res = {
            "tc_in": 0,
            "tc_out": self.duration_tc.frames
        }
        if tc_in:
            start_tc = Timecode(edit_rate, tc_in)
            if start_tc.frames - 1 > self.duration_frames:
                raise Exception(f"tc_in: {tc_in} is out of bounds. (duration of file: {self.duration_tc})")
            res["tc_in"] = start_tc.frames
        if duration_frames:
            end_tc = Timecode(edit_rate, frames=duration_frames)
            if (end_tc.frames - 1) > self.duration_frames:
                raise Exception(f"duration_frames provided: {end_tc} is out of bounds. (duration of file: {self.duration_tc})")
            res["tc_out"] = end_tc.frames + start_tc.frames
        elif tc_out:
            end_tc = Timecode(edit_rate, tc_out)
            print(f"{self.duration_frames} --> {end_tc.frames}")
            if (end_tc.frames - 1) > self.duration_frames:
                raise Exception(
                    f"duration_frames provided: {tc_out} is out of bounds. (duration of file: {self.duration_tc})")
            res["tc_out"] = end_tc.frames - 1
        return res


    def build_tracks_from_source(self,
                                 tracks=None,
                                 source_timing=None,
                                 options=None):
        tracks = []
        RallySource.logger.info(f"generic Tracks not included")
        return tracks


    def build_video_tracks_from_source(self, tracks=None, source_timing=None):
        tracks = []
        tc_in_frames = source_timing.get("tc_in", 0)
        tc_out_frames = source_timing.get("tc_out", 1)
        for index, video_track in enumerate(self.mediainfo_report.get("video") or []):
            track = self._build_video_track(index + 1,
                                            [self._build_element(self.key,
                                                                 index + 1,
                                                                 tc_in_frames,
                                                                 self.duration_tc.frames - 1)])
            tracks.append(track)
        return tracks

    def _build_video_track(self, track_num, elements):
        return {
            'trackName': f'Video-{track_num}',
            'track': track_num,
            'type': 'video',
            'elements': elements
        }

    def _build_audio_track(self, track_num, format, num_channels, elements):
        return {
            'trackName': f'Audio-{track_num}',
            'track': track_num,
            'type': 'audio',
            'format': format,
            'channels': num_channels,
            'elements': elements
        }

    def _build_element(self, key, track, element_in, element_duration):
        return {
            'elementName': key,
            'elementTrack': track,
            'elementIn': element_in,
            'elementDuration': element_duration,
        }

    def build_audio_tracks_from_source(self, tracks=None, source_timing=None):
        new_tracks = []
        track_num = len([x for x in jmespath.search("[?type == 'audio']", tracks)]) + 1
        framerate = float(self.framerate)

        for index, audio_track in enumerate(self.mediainfo_report.get("audio") or []):
            duration_seconds = float(jmespath.search("duration", audio_track)) / 1000
            print(f"duration seconds: {duration_seconds}")
            track_duration = Timecode(framerate, start_seconds=duration_seconds).frames
            num_channels = int(audio_track["channels"])
            if num_channels == 2:
                track = self._build_audio_track(track_num,
                                                "stereo",
                                                num_channels,
                                                [self._build_element(self.key, 1, 0, track_duration)])

                new_tracks.append(track)
                track_num += 1
            else:
                for channel_index in range(num_channels):
                    track = self._build_audio_track(track_num,
                                                    "mono",
                                                    num_channels,
                                                    [self._build_element(self.key, channel_index + 1, 0, track_duration)])
                    new_tracks.append(track)

                    track_num += 1
        return new_tracks

    def _build_caption_track(self, index, track_num, caption_format, elements):
        return {
            'trackName': f'Captions-{index}',
            'type': 'data',
            'track': track_num,
            "metadata": {
                "captionFormat": caption_format,
            },
            'elements': elements
        }

    def build_caption_tracks_from_source(self, tracks=None, source_timing=None):
        tracks = []
        track_num = len([x for x in jmespath.search("[?type == 'audio']", tracks)]) + 1
        tc_in_frames = source_timing.get("tc_in", 0)
        tc_out_frames = source_timing.get("tc_out", 1)
        for index, video_track in enumerate(self.mediainfo_report.get("video") or []):
            track = self._build_caption_track(index,
                                              track_num + index + 1,
                                              self.caption_format,
                                              [{
                                                  'elementName': self.key,
                                                  'elementDuration': self.duration_tc.frames - 1
                                              }])
            tracks.append(track)
        return tracks

    ###########################
    ##### internal functions
    def _validate_source(self):
        # check if the label exists
        if not self.label:
            self.errors.append("Source does not have a label")
            return False
            # raise Exception("Source does not have a label")
        if asset:
            try:
                asset.get_asset(self.asset_name)
            except NotFound as err:
                self.errors.append(f"asset: {self.asset_name} does not exist")
                return False
                # raise Exception(f"asset: {self.asset_name} does not exist")

        # Check if the file exists and is online
        if not RallySource.rally_files.is_label_available(self.label):
            self.errors.append(f"label: {self.label} is not available")
            return False
            # raise Exception(f"label: {self.label} is not available")

        # check if audio for the channels type
        # FIXME


class RallyEdl:
    """
    EDL helper class
    """
    logger = logging.getLogger(__qualname__)
    tech_report = TechnicalReport()

    def __init__(self, edit_rate="29.97", start_tc="00:00:00;00", segments=None, sources=None):
        self.errors = []
        self.edit_rate = edit_rate
        self.start_tc = start_tc
        self.segments = segments or []
        self.sources = sources or []

    ###########################
    ##### Constructors
    @classmethod
    def from_primary_label(cls, label, asset_name=None):
        framerate = RallyEdl.tech_report.get_framerate_str(label, asset_name)
        start_tc = RallyEdl.tech_report.get_start_timecode(label, asset_name, default="00:00:00;00")
        return cls(framerate, start_tc)


    ###########################
    ##### Interfaces
    def add_segment_by_source(self,
                              video_assets,
                              audio_assets=None,
                              caption_assets=None,
                              marker_in=None):
        # Create and add segment from that source
        segment = self._create_segment(video_assets,
                                       audio_assets=audio_assets,
                                       caption_assets=caption_assets,
                                       marker_in=marker_in)

        # Insert at the end unless a marker_in has been provided.
        RallyEdl.logger.info(f"marker_in: {marker_in}")
        self._insert_segment_at_tc(segment, marker_in)

    def get_input_spec(self, use_proxy=False):
        input_spec = {}
        if not self.sources:
            return {}
        first_iteration = 0
        for source in self.sources:
            input_spec[source.key] = source.to_json(use_proxy)

            # Associate primary randomly if none is specified.
            if first_iteration == 0 and not jmespath.search("*|[?primary]", self.sources):
                input_spec[source.key]["primary"] = True
            first_iteration += 1
        return input_spec

    def get_access3_media_list(self, use_proxy=True):
        media_list = []
        for source in self.sources:
            media_list.append(source.to_access3_media("./media", use_proxy_mapping=use_proxy))
        return media_list

    def to_premiere_edl(self):
        sequence_duration = self._get_sequence_duration_frames()
        local_sources = self._prepare_sources_output()

        res = {
            "sources": local_sources,
            "edl": {
                "editRate": float(self.edit_rate),
                "startTc": f"{self.start_tc}",
                "duration": sequence_duration,
                "segments": self.segments
            }
        }
        return res


    def find_segment_by_tc(self, marker_in_tc):
        current_tc = Timecode(self.edit_rate, "00:00:00;00")
        RallyEdl.logger.info(f"segments ==> {self.segments}")
        for segment in self.segments:
            video_tracks = jmespath.search("tracks[?type=='video']", segment) or []
            longest_track_frames = 0
            for video_track in video_tracks:
                current_video_track_frames = 0
                for element in video_track.get("elements", []):
                    current_video_track_frames += element.get("elementDuration", 0)
                longest_track_frames = max(current_video_track_frames, longest_track_frames)
            end_of_segment = Timecode(self.edit_rate, frames=longest_track_frames)
            RallyEdl.logger.info(f"The Timecode {marker_in_tc} may be under: {end_of_segment}")
            # check if current_tc within the bounds:
            if marker_in_tc.frames < end_of_segment.frames + current_tc.frames - 1:
                RallyEdl.logger.info(f"The Timecode {marker_in_tc} is in the segment: {segment.get('segmentName')}")
                return segment, current_tc
            current_tc = Timecode(self.edit_rate, frames=end_of_segment.frames + current_tc.frames)
        return None

    def get_sequence_duration_tc(self):
        total_segments_duration = Timecode(self.edit_rate, frames=1)
        # Get the duration of each segment
        for segment in self.segments:
            total_segments_duration += self._get_segment_duration(segment)
            # find the different tracks (only audio/video)
            RallyEdl.logger.info(self.segments)
        try:
            total_segments_duration = total_segments_duration - Timecode(self.edit_rate, frames=1)
            RallyEdl.logger.info(f"total duration is: {total_segments_duration} ({total_segments_duration.frames})")
            return total_segments_duration
        except Exception as err:
            return None

    ###########################
    ##### internal functions
    def _create_segment(self,
                        video_assets=None,
                        audio_assets=None,
                        caption_assets=None,
                        marker_in=None):
        tracks = []
        asset_data_types = (("video", video_assets),
                            ("audio", audio_assets),
                            ("captions", caption_assets))
        for (name, asset_list) in asset_data_types:
            for asset_data in asset_list or []:
                RallyEdl.logger.info(f"parsing asset data: {asset_data}")
                tracks += self._build_tracks_from_asset_data(asset_data, tracks=tracks)
                RallyEdl.logger.info(f"{name} being added to segment: {asset_data}")

        return {
            "segmentName": f"Segment-{len(self.segments) + 1}",
            "tracks": tracks
        }

    def _build_tracks_from_asset_data(self, asset_data_dict, tracks=None):
        asset_data = AssetData.from_dict(asset_data_dict)
        RallyEdl.logger.info(f"assetdata: {asset_data.__dict__}")
        # Add source
        added_source = self._add_source(key=asset_data.key,
                                        label=asset_data.label,
                                        asset_name=asset_data.asset_name,
                                        proxy_mapping=asset_data.proxy_mapping)

        # Check that the tc is correct [returns exception if an input is out of bounds]
        source_timing = added_source.retrieve_tc_in_out_frames(self.edit_rate,
                                                               tc_in=asset_data.tc_in,
                                                               tc_out=asset_data.tc_out,
                                                               duration_frames=asset_data.duration_frames)
        options = asset_data.to_options()
        RallyEdl.logger.info(f"options: {options}")
        tracks = added_source.build_tracks_from_source(tracks=tracks,
                                                       source_timing=source_timing,
                                                       options=options)
        return tracks

    def _insert_segment_at_tc(self, segment, marker_in):
        # Add to tail
        if not marker_in:
            self.segments.append(segment)
            return

        marker_in_tc = Timecode(self.edit_rate, marker_in)
        RallyEdl.logger.info("entering insert segment at")
        segment_to_update, segment_start_tc = self.find_segment_by_tc(marker_in_tc)
        if not segment_to_update:
            RallyEdl.logger.info(f"Inserting at tail ")
            self.segments.append(segment)
            return
        # Else segment was returned: split the current segment.
        # split_segments = self._split_segment(segment, marker_in_tc, segment_to_update, segment_start_tc)

    def _add_source(self, key, label, asset_name, proxy_mapping=None):
        # make sure there is no duplicates
        existing_source = self._find_rally_source(label, asset_name)
        if existing_source:
            return existing_source
        RallyEdl.logger.info(f"testing: {label}, {asset_name}")
        is_primary = False
        # Checks if there are already sources marked as primary
        if not [x for x in self.sources if x.primary]:
            is_primary = True
        source = RallySource.create_rally_source(key,
                                                 label,
                                                 asset_name,
                                                 primary=is_primary,
                                                 proxy_mapping=proxy_mapping,
                                                 default_framerate=self.edit_rate)
        RallyEdl.logger.info(f"--> added source: {source}")
        self.sources.append(source)
        return source

    def _find_rally_source(self, label, asset_name=None) -> RallySource:
        RallyEdl.logger.info(f"looking for: {label} - {asset_name}")
        for source in self.sources or []:
            RallyEdl.logger.info(f"\t comparing to: {source.label} - {source.asset_name}")
            if source.label == label and source.asset_name == asset_name:
                return source
        return None

    def _prepare_sources_output(self):
        sources = {}
        for source in self.sources:
            sources[source.key] = source.to_json(use_proxy_mapping=False)
        return sources

    def _get_sequence_duration_frames(self):
        total_segment_duration_frames = self.get_sequence_duration_tc()
        if not total_segment_duration_frames:
            return 0
        return total_segment_duration_frames.frames

    def _get_segment_duration(self, segment):
        max_duration = Timecode(self.edit_rate, frames=1)
        for track in segment.get("tracks", []):
            track_duration = self._get_track_duration(track.get("elements", []), track.get("trackName", "n/a"))
            if track_duration > max_duration:
                max_duration = track_duration
        return max_duration

    def _get_track_duration(self, elements, name):
        duration = 0
        for element in elements:
            duration += int(element.get("elementDuration", 0))
        # RallyEdl.logger.info(f": duration {duration}")
        if not duration:
            return None
        tc = Timecode(self.edit_rate, frames=duration)
        RallyEdl.logger.info(f"{name} in TC: {tc} - {tc.frames}")
        return tc


class RallySourceVideo(RallySource):
    def __init__(self,
                 key,
                 label,
                 asset_name=None,
                 primary=False,
                 proxy_mapping=None,
                 default_framerate="29.97"):
        super().__init__(key, label, asset_name, primary, proxy_mapping)

        self.source_type = "video"
        # Additional attributes
        RallySource.logger.info(f"{self.asset_name}:{self.label}")
        self.framerate = jmespath.search("MediaInfo.General.FrameRate", self.mediainfo_report) or default_framerate
        duration_tc_str = jmespath.search('MediaInfo.General."Duration/String4"', self.mediainfo_report)
        self.duration_tc = Timecode(self.framerate, duration_tc_str)


    def build_tracks_from_source(self,
                                 tracks=None,
                                 source_timing=None,
                                 options=None):
        options = options or {}
        new_tracks = []
        # prepare video tracks
        RallySource.logger.info(f"options: {options}")
        if options.get("include_video"):
            new_tracks += self.build_video_tracks_from_source(tracks, source_timing)

        # prepare audio tracks
        if options.get("include_audio"):
            new_tracks += self.build_audio_tracks_from_source(tracks, source_timing)
        # # prepare caption tracks
        # tracks += self.build_timedtext_tracks_from_source(source_timing)
        return new_tracks

class RallySourceAudio(RallySource):
    def __init__(self,
                 key,
                 label,
                 asset_name=None,
                 primary=False,
                 proxy_mapping=None,
                 default_framerate="29.97"):
        super().__init__(key, label, asset_name, primary, proxy_mapping)

        self.source_type = "audio"
        # Additional attributes
        self.framerate = jmespath.search("MediaInfo.General.FrameRate", self.mediainfo_report) or default_framerate
        duration_tc_str = jmespath.search('MediaInfo.General."Duration/String3"', self.mediainfo_report)
        RallySource.logger.info(f"audio duration: {duration_tc_str}")
        self.duration_tc = Timecode(self.framerate, duration_tc_str)
        RallySource.logger.info(f"audio duration: {self.duration_tc}")

    def build_tracks_from_source(self,
                                 tracks=None,
                                 source_timing=None,
                                 options=None):
        new_tracks = []
        # prepare audio tracks
        new_tracks += self.build_audio_tracks_from_source(tracks, source_timing)
        return new_tracks



class RallySourceCaption(RallySource):
    def __init__(self,
                 key,
                 label,
                 asset_name=None,
                 primary=False,
                 proxy_mapping=None,
                 default_framerate="29.97"):
        super().__init__(key, label, asset_name, primary, proxy_mapping)

        self.source_type = "timed_text"
        # Additional attributes
        self.framerate = jmespath.search("MediaInfo.General.FrameRate", self.mediainfo_report) or default_framerate
        duration_tc_str = jmespath.search('MediaInfo.General."Duration/String4"', self.mediainfo_report)
        self.duration_tc = Timecode(self.framerate, duration_tc_str)

    def build_tracks_from_source(self,
                                 tracks=None,
                                 source_timing=None,
                                 options=None):
        new_tracks = []
        # prepare caption tracks
        new_tracks += self.build_audio_tracks_from_source(tracks, source_timing)
        return new_tracks