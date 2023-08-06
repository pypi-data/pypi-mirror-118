# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Environment helpers."""

import contextlib
import os

from clusterfuzz._internal.system import environment

# Inverted SANITIZER_NAME_MAP.
SANITIZER_MAP = {v: k for k, v in environment.SANITIZER_NAME_MAP.items()}


class Environment:
  """Environment helpers."""

  def __init__(self, engine, sanitizer, target_path):
    self._previous_values = {}
    self._engine = engine
    self._sanitizer = sanitizer
    self._target_path = target_path

    if self._sanitizer not in SANITIZER_MAP:
      raise ValueError('Invalid sanitizer value ' + self.sanitizer)

  def __enter__(self):
    """Enter environment."""
    job_name = (
        self._engine.lower() + '_' + SANITIZER_MAP[self._sanitizer] + '_job')
    self.set_value('JOB_NAME', job_name)
    self.set_value('BUILD_DIR', os.path.dirname(self._target_path))
    return self

  def __exit__(self, *exc):
    """Exit environment."""
    del exc

    for key, value in self._previous_values.items():
      if value is None:
        os.environ.pop(key)
      else:
        os.environ[key] = value

    return False

  def set_value(self, key, value):
    if key not in self._previous_values:
      self._previous_values[key] = os.getenv(key)

    os.environ[key] = value
