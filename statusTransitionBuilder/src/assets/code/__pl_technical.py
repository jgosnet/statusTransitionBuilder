""" This module helps with retrieving media info properties from a specific label/asset_name """
import logging
import re
import json
import jmespath
from timecode import Timecode
from rally import jobs, exceptions

class TechnicalReport:
    """ This class provides helper function to retrieve different media properties,
    And cache the reports already pulled based on label/asset_name
    """
    logger = logging.getLogger(__qualname__)

    def __init__(self):
        self.rally_reports = {}

    def get_report(self, label, asset_name=None):
        """ Retrieve report from cache """
        return self._from_cache(label, asset_name)

    def get_framerate_str(self, label, asset_name=None):
        """ Returns the framerate as a string """
        framerate = jmespath.search('movie.frameRate', self.get_report(label, asset_name))
        return framerate

    def get_framerate_float(self, label, asset_name=None):
        """ Returns the framerate as a float """
        framerate = jmespath.search('movie.frameRate', self.get_report(label, asset_name))
        return float(framerate)

    def get_duration_timecode(self, label, asset_name=None):
        """ Returns the duration as a timecode object """
        duration_str = jmespath.search('movie.duration', self.get_report(label, asset_name))
        return Timecode(self.get_framerate_float(label, asset_name), duration_str)

    def framerate_numerator_int(self, label, asset_name=None):
        """ Returns the framerate numerator as an int """
        return int(self.get_framerate_float(label, asset_name) * 1000)

    @staticmethod
    def convert_to_timecode(timecode_str, framerate):
        """ Convert a string to a timecode based on provided framerate """
        if re.search("^[0-9]+$", f"{timecode_str}"):
            return Timecode(framerate, frames=int(timecode_str))
        if re.search("^(([0-9]){2}[:;]){3}([0-9]){2}$", f"{timecode_str}"):
            return Timecode(framerate, start_timecode=timecode_str)
        return Timecode(framerate, timecode_str)

    @staticmethod
    def convert_tc_to_frames(timecode_str, framerate):
        """ Convert a string to a frame count as int based on provided framerate """
        if re.search("^[0-9]+$", f"{timecode_str}"):
            tc = Timecode(framerate, frames=int(timecode_str))
        elif re.search("^(([0-9]){2}[:;]){3}([0-9]){2}$", f"{timecode_str}"):
            tc = Timecode(framerate, start_timecode=timecode_str)
        else:
            tc = Timecode(framerate, timecode_str)
            print(f"Unrecognized timecode format: {timecode_str} - {tc} - {tc.frames}")
        print(f"timecode found for: {timecode_str} - {tc} - {tc.frames}")
        return tc.frames

    @staticmethod
    def is_dropframe(duration: str, framerate: str):
        """
        Returns if the media file is dropframe or not
        :param duration: The during of the media file (e.g. '00:12:13:10' )
        :param framerate: The framerate of the media file (e.g. '23.976')
        :return: bool
        """
        ndf_framerates = ["24.000", "25.0", "25.000", "30.000", "50.000", "60.000"]

        if len(duration) > 8:
            return duration[8] == ';'
        return not framerate in ndf_framerates

    @staticmethod
    def framerate_denominator_int():
        """ Return the framerate denominator = hardcoded to 1000"""
        return 1000

    def get_start_timecode(self, label, asset_name=None, default=None):
        """ Find the start timecode based on mediainfo analysis"""
        default = default or "00:00:00;00"
        return jmespath.search('movie.startTc', self.get_report(label, asset_name)) or default

    def get_start_timecode_frames(self, label, asset_name=None, default=None):
        """ Find the start timecode based on mediainfo analysis. Return as a timecode object"""
        default = default or "00:00:00;00"
        timecode_str = self.get_start_timecode(label, asset_name, default=default)
        return Timecode(self.get_framerate_float(label, asset_name), timecode_str).frames - 1

    def get_aspect_ratio(self, label, asset_name=None, default_ratio=None):
        """ return the aspect ratio as a tuple"""
        default_ratio = default_ratio or "16:9"
        aspect_ratio = jmespath.search('video[0].aspectRatio',
                                       self.get_report(label, asset_name)) or default_ratio
        return {
            "width": int(aspect_ratio.split(':')[0]),
            "height": int(aspect_ratio.split(':')[-1])
        }

    def get_resolution(self, label, asset_name=None, default_width=None, default_height=None):
        """ return the width and height as a tuple"""
        default_width = default_width or "1920"
        default_height = default_height or "1080"
        width = jmespath.search('video[0].width',
                                self.get_report(label, asset_name)) or default_width
        height = jmespath.search('video[0].height',
                                 self.get_report(label, asset_name)) or default_height
        return {
            "width": int(width),
            "height": int(height)
        }

    def get_audio_total_channel_count(self, label, asset_name=None):
        """
        Get the number of channels in an audio track
        :param label: track label
        :param asset_name: name of the asset (None if current asset)
        :return:
        """
        print(f'checking audio channel count for: {label} | {asset_name}\n')
        report = self.get_report(label, asset_name)
        audio_tracks = len(jmespath.search("audio", report) or [])
        audio_channels = int(jmespath.search("audio[0].channels", report) or 0)
        return int(audio_channels * audio_tracks)

    def get_audio_layout(self, label, asset_name=None):
        """ Get the audio layout, dictionary containing audio track x channels  """
        print(f'checking audio layout for: {label} | {asset_name}\n')
        report = self.get_report(label, asset_name)
        audio_layout = {}
        for track in jmespath.search("audio", report) or []:
            channels = jmespath.search(f"channels", track) or 0
            trackNum = jmespath.search(f"trackNum", track) or 0
            audio_layout[int(trackNum)] = int(channels)
        return dict(sorted(audio_layout.items()))

    def get_audio_track_codec(self, label, asset_name=None):
        """ Return the audio track codec """
        return jmespath.search('audio[0].codec',
                               self.get_report(label, asset_name))

    def get_audio_track_bit_rate(self, label, asset_name=None):
        """ Return the audio track bitrate """
        res = jmespath.search('audio[0].bitRate', self.get_report(label, asset_name))
        if res:
            return int(res)
        return None

    def get_audio_track_sample_rate(self, label, asset_name=None):
        """ Return the audio track sampleRate """
        res = jmespath.search('audio[0].sampleRate', self.get_report(label, asset_name))
        if res:
            return int(res)
        return None

    def get_audio_track_audio_duration(self, label, asset_name=None):
        """ Return the audio tracks duration """
        res = jmespath.search('audio[0].duration', self.get_report(label, asset_name))

        return res

    def get_video_general_overall_bitrate(self, label, asset_name=None):
        """ Return the general bitrate """
        return int(jmespath.search('MediaInfo.General."OverallBitRate"',
                                   self.get_report(label, asset_name)))

    def get_video_general_codec(self, label, asset_name=None):
        """ Return the video codec """
        return jmespath.search('MediaInfo.General.Video_Format_List',
                               self.get_report(label, asset_name))

    def _from_cache(self, label, asset_name=None):
        """ Returns cached report if already pulled, otherwise updates the report cache. """
        if asset_name not in self.rally_reports:
            self.rally_reports[asset_name] = {}
        if label not in self.rally_reports[asset_name]:
            self.logger.info(f"analyze: {label}")
            try:
                raw_report = jobs.get_job_report('SdviAnalyze', label, 'summary', asset_name=asset_name)
            except exceptions.RallyApiError as err:
                self.logger.critical(f"Report missing for: {label}:{asset_name}")
                raise exceptions.RallyApiError(f"Report missing for: {label}:{asset_name} ({err})")
            report = json.loads(raw_report)
            self.rally_reports[asset_name][label] = report
            self.logger.info(f"""cached asset_names: {self.rally_reports.keys()}\n
            cached label: {label}: {self.rally_reports[asset_name].get(label)}""")
        return self.rally_reports[asset_name][label]
