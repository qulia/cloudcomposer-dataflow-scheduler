# Copyright 2019 Google LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Adapted from https://cloud.google.com/pubsub/docs/pubsub-dataflow#python

# [START pubsub_to_gcs]
import argparse
from datetime import datetime
import logging
import random
import os
from apache_beam import DoFn, GroupByKey, io, ParDo, Pipeline, PTransform, WindowInto, WithKeys
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.value_provider import RuntimeValueProvider

from apache_beam.io import WriteToText

class UserOptions(PipelineOptions):
    @classmethod
    def _add_argparse_args(cls, parser):
        parser.add_argument(
            "--input_path"
            )
        parser.add_argument(
            "--output_path",
            help="Path of the output GCS file including the prefix.",
        )
        parser.add_value_provider_argument(
            '--suffix', 
            type=str)

class AppendFn(DoFn):
    def __init__(self, suffix):
      self.suffix = suffix

    def process(self, word):
      suffix_str = self.suffix.get()
      logging.info(f"contents: {word} {suffix_str}")
      yield f"{word} {suffix_str}"


def run():
    # Set `save_main_session` to True so DoFns can access globally imported modules.
    pipeline_options = PipelineOptions(save_main_session=True)
    logging.info("All option: %s", pipeline_options.get_all_options())
    user_options = pipeline_options.view_as(UserOptions)
    with Pipeline(options=pipeline_options) as pipeline:
        (
            pipeline
            # Because `timestamp_attribute` is unspecified in `ReadFromPubSub`, Beam
            # binds the publish time returned by the Pub/Sub server for each message
            # to the element's timestamp parameter, accessible via `DoFn.TimestampParam`.
            # https://beam.apache.org/releases/pydoc/current/apache_beam.io.gcp.pubsub.html#apache_beam.io.gcp.pubsub.ReadFromPubSub
            | "Read from GCS" >> io.ReadFromText(user_options.input_path)
            | "Append suffix" >> ParDo(AppendFn(user_options.suffix))
            | "Write to GCS" >> WriteToText(user_options.output_path)
        )


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)

    run()
# [END pubsub_to_gcs]

