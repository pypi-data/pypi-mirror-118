"""Authors: Luiz Tauffer"""
import random
import string
import pytz
from typing import Union, Optional
from pathlib import Path
import spikeextractors as se
from pynwb import NWBFile
from pynwb.ecephys import ElectricalSeries

from ..baserecordingextractorinterface import BaseRecordingExtractorInterface
from ..basesortingextractorinterface import BaseSortingExtractorInterface
from ....utils.json_schema import get_schema_from_hdmf_class, get_schema_from_method_signature
from .brpylib import NsxFile

PathType = Union[str, Path]
OptionalPathType = Optional[PathType]


class BlackrockRecordingExtractorInterface(BaseRecordingExtractorInterface):
    """Primary data interface class for converting a BlackrockRecordingExtractor."""

    RX = se.BlackrockRecordingExtractor

    @classmethod
    def get_source_schema(cls):
        """Compile input schema for the RecordingExtractor."""
        source_schema = get_schema_from_method_signature(
            class_method=cls.__init__, exclude=["block_index", "seg_index"]
        )
        source_schema["properties"]["filename"]["format"] = "file"
        source_schema["properties"]["filename"]["description"] = "Path to Blackrock file."
        return source_schema

    def __init__(self, filename: PathType, nsx_override: PathType = None):
        super().__init__(filename=filename, nsx_override=nsx_override)
        if self.source_data["nsx_override"] is not None:
            # if 'nsx_override' is specified as a path, then the 'filename' argument is ignored
            # This filename be used to extract the version of nsx: ns3/4/5/6 from the filepath
            self.data_filename = self.source_data["nsx_override"]
        else:
            self.data_filename = self.source_data["filename"]

    def get_metadata_schema(self):
        """Compile metadata schema for the RecordingExtractor."""
        metadata_schema = super().get_metadata_schema()
        metadata_schema["properties"]["Ecephys"]["properties"].update(
            ElectricalSeries_raw=get_schema_from_hdmf_class(ElectricalSeries),
            ElectricalSeries_processed=get_schema_from_hdmf_class(ElectricalSeries),
        )
        return metadata_schema

    def get_metadata(self):
        """Auto-fill as much of the metadata as possible. Must comply with metadata schema."""
        metadata = super().get_metadata()

        # Open file and extract headers

        nsx_file = NsxFile(datafile=self.data_filename)
        session_start_time = nsx_file.basic_header["TimeOrigin"]
        session_start_time_tzaware = pytz.timezone("EST").localize(session_start_time)
        comment = nsx_file.basic_header["Comment"]

        # Updates basic metadata from files
        metadata["NWBFile"] = dict(
            session_start_time=session_start_time_tzaware.strftime("%Y-%m-%dT%H:%M:%S"),
            session_description=comment,
        )

        # Checks if data is raw or processed
        if self.data_filename.split(".")[-1][-1] == "6":
            metadata["Ecephys"]["ElectricalSeries_raw"] = dict(name="ElectricalSeries_raw")
        else:
            metadata["Ecephys"]["ElectricalSeries_processed"] = dict(name="ElectricalSeries_processed")

        return metadata

    def run_conversion(
        self,
        nwbfile: NWBFile,
        metadata: dict = None,
        stub_test: bool = False,
        use_times: bool = False,
        save_path: OptionalPathType = None,
        overwrite: bool = False,
        buffer_mb: int = 500,
        write_as: str = "raw",
        es_key: str = None,
    ):
        """
        Primary function for converting recording extractor data to nwb.
        Parameters
        ----------
        nwbfile: NWBFile
            nwb file to which the recording information is to be added
        metadata: dict
            metadata info for constructing the nwb file (optional).
            Should be of the format
                metadata['Ecephys']['ElectricalSeries'] = {'name': my_name,
                                                           'description': my_description}
        use_times: bool
            If True, the timestamps are saved to the nwb file using recording.frame_to_time(). If False (default),
            the sampling rate is used.
        write_as_lfp: bool (optional, defaults to False)
            If True, writes the traces under a processing LFP module in the NWBFile instead of acquisition.
        save_path: PathType
            Required if an nwbfile is not passed. Must be the path to the nwbfile
            being appended, otherwise one is created and written.
        overwrite: bool
            If using save_path, whether or not to overwrite the NWBFile if it already exists.
        stub_test: bool, optional (default False)
            If True, will truncate the data to run the conversion faster and take up less memory.
        """
        if self.data_filename.split(".")[-1][-1] == "6":
            write_as = "raw"
        elif write_as not in ["processed", "lfp"]:
            write_as = "processed"

        print(f"Converting Blackrock {write_as} traces...")

        super().run_conversion(
            nwbfile=nwbfile,
            metadata=metadata,
            use_times=use_times,
            write_as=write_as,
            es_key=es_key,
            save_path=save_path,
            overwrite=overwrite,
            stub_test=stub_test,
            buffer_mb=buffer_mb,
        )


class BlackrockSortingExtractorInterface(BaseSortingExtractorInterface):
    """Primary data interface class for converting Blackrock spiking data."""

    SX = se.BlackrockSortingExtractor

    @classmethod
    def get_source_schema(cls):
        """Compile input schema for the RecordingExtractor."""
        metadata_schema = get_schema_from_method_signature(
            class_method=cls.SX.__init__, exclude=["block_index", "seg_index", "nsx_to_load"]
        )
        metadata_schema["additionalProperties"] = True
        metadata_schema["properties"]["filename"]["format"] = "file"
        metadata_schema["properties"]["filename"]["description"] = "Path to Blackrock file."
        return metadata_schema

    def __init__(self, filename: PathType, nsx_to_load: Optional[int] = None, nev_override: PathType = None):
        super().__init__(filename=filename, nsx_to_load=nsx_to_load, nev_override=nev_override)
