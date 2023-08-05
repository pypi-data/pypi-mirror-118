# coding=utf-8
# Copyright 2020 The TF-Agents Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tests TF-Agents API root."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf
import tf_agents


class RootAPITest(tf.test.TestCase):

  def test_entries(self):
    # Ensure that some of the basics exist
    # pylint: disable=pointless-statement
    tf_agents.agents
    tf_agents.experimental
    tf_agents.policies
    tf_agents.networks
    tf_agents.bandits.agents
    tf_agents.bandits.policies
    tf_agents.bandits.networks
    # pylint: disable=pointless-statement


if __name__ == '__main__':
  tf.test.main()
