from __pl_files import RallyFiles
from __pl_technical import TechnicalReport
import __pl_logging
import logging
import json
import jmespath
from dataclasses import dataclass, field

logger = logging.getLogger('AmeRallyConfig')

rally_files = RallyFiles()
tech_report = TechnicalReport()


class AmeRallyConfig:
    """
    Class to assist with building the Rally Config of an AME preset by adding AmeOutput objects.

    The Rally Config for AME consists of the normal MIO inputSpec and outputSpec, and also an outputs list
    which defines the files AME will produce. This can be built in a variety of ways, and values in this list
    are referenced in the inputSpec and outputSpec, which this class automatically ties together.
    For more information on the AME Rally Config, please reference the Rally Preset Docs...
        https://<MySilo>.sdvi.com/docs/preset/mediaEncoder.html#rally-preset-configuration-panel-version-0-76

    AmeOutput objects can be added using the add_ame_output function. Once all outputs have been added, the inputSpec,
    outputSpec, and outputs can be generated using the get_input_spec, get_output_spec, and get_outputs functions.

    :param file_mapping: (optional) json that maps proxies to the high resolution version used in the Input Spec.
    This Must follow the following formation:
    [
        {
            'proxy_label': 'AccessProxy',
            'highres_label': 'Movie',
            'asset_name': None
        }
    ]
    """

    def __init__(self, file_mapping=None):
        self.file_mapping = file_mapping or []
        self.ame_outputs = []

    def add_ame_output(self, ame_output):
        """
        Adds an instance of the AmeOutput object to the ame_outputs class attribute
        :param ame_output: Instance of the AmeOutput object
        """

        # The add_ame_output function relies on class attributes from the AmeOutput class
        # Check if the output data is actually an instance of the AmeOutput object
        if not isinstance(ame_output, AmeOutput):
            logger.info(f'Current Output Type: {type(ame_output)}')
            raise Exception(f'Output not an instance of the AmeOutput class')

        logger.debug(f'Adding AME Output: {ame_output}')
        self.ame_outputs.append(ame_output)

    def get_input_spec(self):
        """
        Creates Input Spec from all AmeOutput Objects.
        Raises an exception for the following:
        - If a duplicate token is found with a different label
        - Any label is not available in inventory
        :return: Dict containing properly formatted Input Spec value that can be Jinja substituted into a Rally Config
        """

        input_spec = {}
        input_spec_errors = []
        for output in self.ame_outputs:
            sources = self._process_file_mapping(output, self.file_mapping)
            for key, value in sources.items():
                if key not in input_spec.keys():
                    input_spec[key] = value
                    logger.debug(f'Adding to Input Spec. Key: {key}, Value: {value}')
                    continue
                # Key already exists so lets make sure the labels match. Log an error if not.
                # NOTE: manifest/edl source tokens can contain dots (for prefixes) which break jmespath expressions.
                label = value.get('label')
                existing_label = input_spec.get(key).get('label')
                logger.debug(f'Checking Label: {label} against Existing Label: {existing_label}')
                if label != existing_label:
                    error = f'Output Token: {key}, Label: {label} already exists in Rally Config Input Spec with a different label {input_spec}'
                    logger.info(error)
                    input_spec_errors.append(error)

        # Check all used labels and verify they are actually available in inventory
        for value in input_spec.values():
            label = value.get('label')
            asset_name = value.get('asset')
            if not rally_files.is_label_available(label, asset_name):
                error = f'Input Spec Label: {label} not available in inventory'
                logger.info(error)
                input_spec_errors.append(error)

        if input_spec_errors:
            raise Exception(f'Input Spec Errors: {json.dumps(input_spec_errors, indent=4)}')
        return input_spec

    def get_output_spec(self):
        """
        Creates Output Spec from all AmeOutput Objects.
        Raises an exception for the following:
        - If a duplicate output is found in the Output Spec
        :return: Dict containing properly formatted Output Spec value that can be Jinja substituted into a Rally Config
        """

        output_spec = {}
        output_spec_errors = []
        for output in self.ame_outputs:
            # Check if the output already exists in the output spec
            has_error = False
            for file in output_spec.keys():
                if output.filename in file:
                    has_error = True
                    error = f'Current Output: {output.filename} already exists in Rally Config Output Spec: {output_spec}'
                    logger.info(error)
                    output_spec_errors.append(error)

            # Validation has passed so let's add the Output Spec Data
            if not has_error:
                key = f'{output.filename}.*'
                value = {
                    'label': output.label,
                    'name': f'{output.output_spec_prefix}{output.filename}',
                    'location': output.rsl,
                    'tags': output.tags
                }
                output_spec[key] = value
                logger.debug(f'Adding to Output Spec: Key: {key} Value: {value} ')

        if output_spec_errors:
            raise Exception(f'Output Spec Errors: {json.dumps(output_spec_errors, indent=4)}')
        return output_spec

    def get_outputs(self):
        """
        Creates Outputs List from all AmeOutput Objects.
        Raises an exception for the following:
        - If a duplicate output is found in the Outputs List
        :return: List containing properly formatted Ame Outputs value that can be Jinja substituted into a Rally Config
        """

        outputs_data = []
        outputs_data_errors = []
        for output in self.ame_outputs:
            # Check if new output data already exists
            has_error = False
            for output_data in outputs_data:
                if output_data.get('name') == output.filename:
                    has_error = True
                    error = f'Current Output Name: {output.filename} already in Rally Config Outputs: {outputs_data}'
                    logger.info(error)
                    outputs_data_errors.append(error)

            # Validation has passed so let's add the Output Data
            if not has_error:
                new_output_data = {
                    f'{output.token_type}Token': output.token_type,
                    'name': output.filename,
                }
                if output.cuts:
                    new_output_data['cuts'] = output.cuts

                if output.token_type == 'project':
                    if output.sequence_token:
                        new_output_data['sequenceToken'] = output.sequence_token
                    if output.sequence_name:
                        new_output_data['sequenceName'] = output.sequence_name

                outputs_data.append(new_output_data)
                logger.debug(f'Adding to AME Outputs: {new_output_data}')

        if outputs_data_errors:
            raise Exception(f'AME Output Errors: {json.dumps(outputs_data_errors, indent=4)}')
        return outputs_data

    def _process_file_mapping(self, ame_output, file_mapping):

        """
        Internal function called by 'get_input_spec' to process the file mapping
        :return: New dict of sources tokens/labels
        """

        logger.info(f'Checking {ame_output.filename} sources against file mapping')
        logger.debug(f'{ame_output.filename} Sources: {ame_output.sources}')
        logger.debug(f'File Mapping Data: {file_mapping}')

        sources = ame_output.sources
        new_sources = {}
        # Loop through sources and try to find a match in the file mapping
        for key, value in sources.items():
            label = value.get('label')
            match_found = False
            for file_info in file_mapping:
                # If a match is found, then lets replace the source with the High Res Label
                if label == file_info.get('proxy_label') and file_info.get('highres_label'):
                    logger.info(f'Source replacement match found. Source Label: {label}, Match Data: {file_info}')
                    match_found = True
                    new_sources[key] = {
                        'label': file_info.get('highres_label')
                    }
                    if file_info.get('asset_name'):
                        new_sources[key]['asset'] = file_info.get('asset_name')
                    break
            # If no match was found then lets use the source data from the EDL or Manifest
            if not match_found:
                new_sources[key] = value

        return new_sources

    @staticmethod
    def get_cuts_from_tbmd(tbmd_label, outputs_identifier_data, framerate):
        """
        Extracts all the AME Output Cuts from a TBMD file, typically generated from an Access
        session. Data returned here can be looped through to create the AmeOutput objects via the 'from_cuts' method
        which can then be added to the Rally Config via the 'add_ame_output_to_rally_config' function.


        :param tbmd_label: TBMD file that contains the AME Output Cuts data.
        :param outputs_identifier_data: dict that describes how to identify an AME Output Cut from the TBMD event.
            Keys:
                'output_identifier_expression': jmespath expression that points to a TBMD key that signifies an AME Cut
                'output_identifier_value': Expected value for the above key that signifies an AME Cut.
                    NOTE: Accepts '*' for any value
                'output_filename_expression': Optional - jmespath expression that points to a TBMD Key to use in the
                    Output Filename. Will default to an incrementing number if no expression.
                    Please use prefix and suffix to control naming convention with this number.
                    Exception will be raised if expression specified but TBMD key could not be found.
                'output_filename_prefix': Prefix for Output Filename
                'output_filename_suffix': Suffix for Output Filename
                'output_label_expression': Optional - jmespath expression that points to a TBMD Key to use in the
                    Output Label. Will default to an incrementing number if no expression.
                    Please use prefix and suffix to control naming convention with this number.
                    Exception will be raised if expression specified but TBMD key could not be found.
                'output_label_prefix': Prefix for Output Label
                'output_label_suffix': Suffix for Output Label

            Example:
                {
                    'output_identifier_expression': 'markerType',
                    'output_identifier_value': 'Segment',
                    'output_filename_expression': 'segmentNumber',
                    'output_filename_prefix': 'New_Movie_File_Segment_',
                    'output_filename_suffix': '',
                    'output_label_expression': 'segmentNumber',
                    'output_label_prefix': 'New_Movie_Segment_',
                    'output_label_suffix': '',
                }
        :param framerate: framerate needed to convert TBMD start and end timecodes to frames

        :return: json list of Ame Output Cuts
            Example:
                [
                    {
                        'label': 'my_label_1',
                        'filename': 'my_name_1',
                        'cuts': [
                            {
                                'inpoint': 0,
                                'outpoint': 100
                            }
                        ]
                    },
                    {
                        'label': 'my_label_2',
                        'filename': 'my_name_2',
                        'cuts': [
                            {
                                'inpoint': 101,
                                'outpoint': 200
                            }
                        ]
                    }
                ]
        """

        tbmd_data = rally_files.get_content_as_dict(label=tbmd_label)
        output_identifier_expression = outputs_identifier_data.get('output_identifier_expression')
        output_identifier_value = outputs_identifier_data.get('output_identifier_value', '*')
        output_filename_expression = outputs_identifier_data.get('output_filename_expression', None)
        output_filename_prefix = outputs_identifier_data.get('output_filename_prefix', '') or ''
        output_filename_suffix = outputs_identifier_data.get('output_filename_suffix', '') or ''
        output_label_expression = outputs_identifier_data.get('output_label_expression', None)
        output_label_prefix = outputs_identifier_data.get('output_label_prefix', '') or ''
        output_label_suffix = outputs_identifier_data.get('output_label_suffix', '') or ''

        ame_cuts_data = []
        ame_cuts_data_errors = []
        # Output counter used for default filename
        output_counter = 0
        # Loop through TBMD markers looking for an output match
        for event in tbmd_data.get('events', []):
            logger.debug(f'Current TBMD Event Data: {event}')
            if jmespath.search(output_identifier_expression, event):
                tbmd_search = jmespath.search(output_identifier_expression, event)
                if tbmd_search == output_identifier_value or output_identifier_value == '*':
                    logger.info(f'Output Found in TBMD Event: {event}')
                    start_timecode = jmespath.search('location.start', event)
                    end_timecode = jmespath.search('location.end', event)
                    if start_timecode and end_timecode:
                        output_counter += 1
                        start_frames = tech_report.convert_tc_to_frames(timecode_str=start_timecode, framerate=framerate)
                        end_frames = tech_report.convert_tc_to_frames(timecode_str=end_timecode, framerate=framerate)
                        filename = output_counter
                        if output_filename_expression:
                            filename = jmespath.search(output_filename_expression, event)
                            if not filename:
                                error = f'Expected Filename Key: {output_filename_expression} not found in TBMD Marker: {event}'
                                logger.info(error)
                                ame_cuts_data_errors.append(error)
                        filename = f'{output_filename_prefix}{filename}{output_filename_suffix}'
                        label = output_counter
                        if output_label_expression:
                            label = jmespath.search(output_label_expression, event)
                            if not label:
                                error = f'Expected Label Key: {output_label_expression} not found in TBMD Marker: {event}'
                                logger.info(error)
                                ame_cuts_data_errors.append(error)
                        label = f'{output_label_prefix}{label}{output_label_suffix}'
                        event_output_data = {
                            'filename': filename,
                            'label': label,
                            'cuts': [
                                {
                                    'inPoint': start_frames,
                                    'outPoint': end_frames
                                }
                            ]
                        }
                        logger.info(f'AME Cut Data From TBMD: {event_output_data}')
                        ame_cuts_data.append(event_output_data)

        if ame_cuts_data_errors:
            raise Exception(f'Errors found generating cuts from TBMD: {json.dumps(ame_cuts_data_errors, indent=4)}')
        return ame_cuts_data

    @staticmethod
    def get_framerate_from_edl(edl_label):
        """
        Extract framerate from the output Access EDL.
        Useful for the 'get_cuts_from_tbmd' function which requires framerate.
        :param edl_label: EDL label to extract from
        :return: <float> framerate
        """

        edl_data = rally_files.get_content_as_dict(label=edl_label)
        framerate = jmespath.search('edl.editRate', edl_data)
        logger.info(f'Framerate: {framerate} extracted from EDL Label: {edl_label}')
        return framerate

    @staticmethod
    def get_sequence_token_from_edl(edl_label):
        """
        Extracts the Premiere Sequence Token from the output Access EDL.
        Useful for creating the AmeOutputFromPrPRoj object.
        :param edl_label: EDL label to extract from
        :return: <string> Sequence Token
        """

        edl_data = rally_files.get_content_as_dict(label=edl_label)
        value = jmespath.search('metadata.token', edl_data)
        logger.info(f'Sequence Token: {value} extracted from EDL Label: {edl_label}')
        return value

    @staticmethod
    def get_sequence_name_from_edl(edl_label):
        """
        Extracts the Premiere Sequence Name from the output Access EDL.
        Useful for creating the AmeOutputFromPrPRoj object.
        :param edl_label: EDL label to extract from
        :return: <string> Sequence Name
        """

        edl_data = rally_files.get_content_as_dict(label=edl_label)
        value = jmespath.search('edl.segments[0].segmentName', edl_data)
        logger.info(f'Sequence Name: {value} extracted from EDL Label: {edl_label}')
        return value

    @staticmethod
    def get_manifest_sources(manifest_label):
        """
        Extracts the sources from the output Access Manifest file.
        :param manifest_label: output Access Manifest file label to extract from
        :return: returns a dictionary of source tokens and labels
        """

        data = rally_files.get_content_as_dict(label=manifest_label)
        sources = data.get('sources')
        logger.debug(f'Extracted Manifest Sources: {sources}')
        return sources

    @staticmethod
    def get_edl_sources(edl_label):
        """
        Extracts the sources from the output Access EDL file.
        :param edl_label: output Access EDL file label to extract from
        :return: returns a dictionary of source tokens and labels
        """

        data = rally_files.get_content_as_dict(label=edl_label)
        sources = data.get('sources')
        logger.debug(f'Extracted EDL Sources: {sources}')
        return sources


@dataclass
class AmeCut:
    """
    Internal Data Class used by the AmeOutput 'from_cuts' class method.
    """

    label: str
    filename: str
    cuts: list = field(default_factory=list)

    @classmethod
    def from_cuts_data(cls, cuts_data):
        """
        Creates an instance of the AmeCut class from one of the cuts generated from the
        'get_cuts_from_tbmd' function.
        :param cuts_data: cut generated from the 'get_cuts_from_tbmd' function
        """

        label = cuts_data.get('label')
        filename = cuts_data.get('filename')
        cuts = cuts_data.get('cuts')
        return cls(label, filename, cuts)


class AmeOutput:
    """
    Class that represents a single AME Output, and contains all the data to be added to the Rally Config in an
    instance of the AmeRallyConfig.

    NOTE: This base class is not meant to be instantiated, but rather one of the following children classes.
        AmeOutputFromPrProj
        AmeOutputFromEdl
        AmeOutputFromFile
    """

    def __init__(self, rsl, label='AME_Output', filename='AME_Output_File', output_spec_prefix='', tags=None, cuts=None):
        self.rsl = rsl
        self.label = label
        self.filename = filename
        self.output_spec_prefix = output_spec_prefix
        self.tags = tags or []
        self.cuts = cuts or []
        self.sources = {}
        self.token_type = None
        self.token_label = None
        self.sequence_token = None
        self.sequence_name = None

    def __str__(self):
        """
        Used for logging messages
        """

        data = {
            'rsl': self.rsl,
            'label': self.label,
            'filename': self.filename,
            'output_spec_prefix': self.output_spec_prefix,
            'tags': self.tags,
            'cuts': self.cuts,
            'sources': self.sources,
            'token_type': self.token_type,
            'token_label': self.token_label,
            'sequence_token': self.sequence_token,
            'sequence_name': self.sequence_name
        }
        return f'Ame Output Data: {json.dumps(data, indent=4)}'

    def _get_sources(self, token_type, token_label, manifest_label=None, edl_label=None):
        """
        Internal function called by one of the AmeOutput classes that creates a sources object
        :param token_type: Set by one of the AmeOutput classes (project, edl, file)
        :param token_label: Associated label based on AmeOutput class (project, edl, file)
        :param manifest_label: Output Access Manifest label (used for AmeOutputFromPrProj)
        :param edl_label: Output Access Edl label (used for AmeOutputFromEdl or AmeOutputFromPrProj)
        :return: Sources object that will be used in the AmeRallyConfig inputSpec
        """

        # Base source from AmeOutput type (project, edl, or file)
        sources = {
            token_type: {
                'label': token_label
            }
        }

        # Prioritize Manifest label over EDL label
        if manifest_label:
            manifest_sources = AmeRallyConfig.get_manifest_sources(manifest_label)
            sources.update(manifest_sources)
            return sources

        if edl_label:
            edl_sources = AmeRallyConfig.get_edl_sources(edl_label)
            sources.update(edl_sources)
            return sources

        # Return base source if no EDL or Manifest
        return sources


class AmeOutputFromPrProj(AmeOutput):
    """
    AmeOutput subclass used for creating a single AME Output based on a Premiere Project
    """

    def __init__(self,
                 prproj_label,
                 rsl,
                 manifest_label=None,
                 edl_label=None,
                 sequence_token=None,
                 sequence_name=None,
                 label='AME_Output',
                 filename='AME_Output_File',
                 output_spec_prefix='',
                 tags=None,
                 cuts=None):

        super().__init__(rsl, label=label, filename=filename, output_spec_prefix=output_spec_prefix, tags=tags, cuts=cuts)
        self.token_type = 'project'
        self.token_label = prproj_label
        self.sources = self._get_sources(self.token_type, self.token_label, manifest_label=manifest_label, edl_label=edl_label)
        self.sequence_token = sequence_token
        self.sequence_name = sequence_name

    @classmethod
    def from_cuts(cls,
                  cuts_data,
                  prproj_label,
                  rsl,
                  manifest_label=None,
                  edl_label=None,
                  sequence_token=None,
                  sequence_name=None,
                  output_spec_prefix='',
                  tags=None):
        """
        Creates an instance of the AmeOutputFromPrProj class from one of the cuts generated from the
        'get_cuts_from_tbmd' function.

        NOTE: 'get_cuts_from_tbmd' returns a list of multiple outputs, and so should be looped through when
        creating this class.
        """

        output = AmeCut.from_cuts_data(cuts_data)
        return cls(prproj_label=prproj_label,
                   rsl=rsl,
                   manifest_label=manifest_label,
                   edl_label=edl_label,
                   sequence_token=sequence_token,
                   sequence_name=sequence_name,
                   label=output.label,
                   filename=output.filename,
                   output_spec_prefix=output_spec_prefix,
                   tags=tags,
                   cuts=output.cuts)


class AmeOutputFromEdl(AmeOutput):
    """
    AmeOutput subclass used for creating an AME Output based on an EDL
    """

    def __init__(self,
                 edl_label,
                 rsl,
                 label='AME_Output',
                 filename='AME_Output_File',
                 output_spec_prefix='',
                 tags=None,
                 cuts=None):

        super().__init__(rsl, label=label, filename=filename, output_spec_prefix=output_spec_prefix, tags=tags, cuts=cuts)
        self.token_type = 'edl'
        self.token_label = edl_label
        self.sources = self._get_sources(self.token_type, self.token_label, edl_label=edl_label)

    @classmethod
    def from_cuts(cls,
                  cuts_data,
                  edl_label,
                  rsl,
                  output_spec_prefix='',
                  tags=None):
        """
        Creates an instance of the AmeOutputFromEDL class from one of the cuts generated from the
        'get_cuts_from_tbmd' function.

        NOTE: 'get_cuts_from_tbmd' returns a list of multiple outputs, and so should be looped through when
        creating this class.
        """

        output = AmeCut.from_cuts_data(cuts_data)
        return cls(edl_label=edl_label,
                   rsl=rsl,
                   label=output.label,
                   filename=output.filename,
                   output_spec_prefix=output_spec_prefix,
                   tags=tags,
                   cuts=output.cuts)


class AmeOutputFromFile(AmeOutput):
    """
    AmeOutput subclass used for creating an AME Output based on a File
    """

    def __init__(self,
                 file_label,
                 rsl,
                 label='AME_Output',
                 filename='AME_Output_File',
                 output_spec_prefix='',
                 tags=None,
                 cuts=None):

        super().__init__(rsl, label=label, filename=filename, output_spec_prefix=output_spec_prefix, tags=tags, cuts=cuts)
        self.token_type = 'file'
        self.token_label = file_label
        self.sources = self._get_sources(self.token_type, self.token_label)

    @classmethod
    def from_cuts(cls,
                  cuts_data,
                  file_label,
                  rsl,
                  output_spec_prefix='',
                  tags=None):
        """
        Creates an instance of the AmeOutputFromFile class from one of the cuts generated from the
        'get_cuts_from_tbmd' function.

        NOTE: 'get_cuts_from_tbmd' returns a list of multiple outputs, and so should be looped through when
        creating this class.
        """

        output = AmeCut.from_cuts_data(cuts_data)
        return cls(file_label=file_label,
                   rsl=rsl,
                   label=output.label,
                   filename=output.filename,
                   output_spec_prefix=output_spec_prefix,
                   tags=tags,
                   cuts=output.cuts)
