from typing import *

from tecton_proto.args.new_transformation_pb2 import NewTransformationArgs
from tecton_proto.args.pipeline_pb2 import Pipeline
from tecton_proto.data.new_transformation_pb2 import NewTransformation
from tecton_proto.data.virtual_data_source_pb2 import VirtualDataSource
from tecton_spark.id_helper import IdHelper
from tecton_spark.materialization_context import BaseMaterializationContext


def pipeline_to_sql_string(
    pipeline: Pipeline,
    virtual_data_sources: List[VirtualDataSource],
    transformations: List[NewTransformation],
) -> str:
    return _PipelineBuilder(
        pipeline,
        virtual_data_sources,
        transformations,
    ).get_sql_string()


# This class is for Snowflake pipelines
class _PipelineBuilder:
    _CONSTANT_TYPE = Optional[Union[str, int, float, bool]]
    # The value of internal nodes in the tree
    _VALUE_TYPE = Union[_CONSTANT_TYPE, BaseMaterializationContext]

    def __init__(
        self,
        pipeline: Pipeline,
        virtual_data_sources: List[VirtualDataSource],
        # we only use mode and name from these
        transformations: Union[List[NewTransformation], List[NewTransformationArgs]],
    ):
        self._pipeline = pipeline
        self._id_to_vds = {IdHelper.to_string(vds.virtual_data_source_id): vds for vds in virtual_data_sources}
        self._id_to_transformation = {IdHelper.to_string(t.transformation_id): t for t in transformations}

    def get_sql_string(self) -> str:
        # (TODO): Return the sql string for the pipeline
        return ""
