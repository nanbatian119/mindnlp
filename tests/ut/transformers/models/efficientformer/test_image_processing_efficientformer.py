# coding=utf-8
# Copyright 2021 HuggingFace Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
""" Testing suite for EfficientFormerImageProcessor. """


import unittest

from mindnlp.utils.testing_utils import require_mindspore, require_vision
from mindnlp.utils.import_utils import is_vision_available

from ...test_image_processing_common import ImageProcessingTestMixin, prepare_image_inputs


if is_vision_available():
    from mindnlp.transformers import ViTImageProcessor


class EfficientFormerImageProcessorTester(unittest.TestCase):
    def __init__(
        self,
        parent,
        batch_size=13,
        num_channels=3,
        image_size=224,
        min_resolution=30,
        max_resolution=400,
        do_resize=True,
        size=None,
        do_normalize=True,
        image_mean=[0.5, 0.5, 0.5],
        image_std=[0.5, 0.5, 0.5],
    ):
        size = size if size is not None else {"height": 18, "width": 18}
        self.parent = parent
        self.batch_size = batch_size
        self.num_channels = num_channels
        self.image_size = image_size
        self.min_resolution = min_resolution
        self.max_resolution = max_resolution
        self.do_resize = do_resize
        self.size = size
        self.do_normalize = do_normalize
        self.image_mean = image_mean
        self.image_std = image_std

    def prepare_image_processor_dict(self):
        return {
            "image_mean": self.image_mean,
            "image_std": self.image_std,
            "do_normalize": self.do_normalize,
            "do_resize": self.do_resize,
            "size": self.size,
        }

    def expected_output_image_shape(self, images):
        return self.num_channels, self.size["height"], self.size["width"]

    def prepare_image_inputs(self, equal_resolution=False, numpify=False, torchify=False):
        return prepare_image_inputs(
            batch_size=self.batch_size,
            num_channels=self.num_channels,
            min_resolution=self.min_resolution,
            max_resolution=self.max_resolution,
            equal_resolution=equal_resolution,
            numpify=numpify,
            torchify=torchify,
        )


@require_mindspore
@require_vision
class EfficientFormerImageProcessorTest(ImageProcessingTestMixin, unittest.TestCase):
    image_processing_class = ViTImageProcessor if is_vision_available() else None

    def setUp(self):
        self.image_processor_tester = EfficientFormerImageProcessorTester(self)

    @property
    def image_processor_dict(self):
        return self.image_processor_tester.prepare_image_processor_dict()

    def test_image_proc_properties(self):
        image_processor = self.image_processing_class(**self.image_processor_dict)
        self.assertTrue(hasattr(image_processor, "image_mean"))
        self.assertTrue(hasattr(image_processor, "image_std"))
        self.assertTrue(hasattr(image_processor, "do_normalize"))
        self.assertTrue(hasattr(image_processor, "do_resize"))
        self.assertTrue(hasattr(image_processor, "size"))
