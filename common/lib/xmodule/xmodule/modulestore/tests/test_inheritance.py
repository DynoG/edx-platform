"""
Unit tests for testing inheritance mixins
"""
from __future__ import absolute_import

import ddt
import unittest

from mock import Mock
from django.utils.timezone import now, timedelta
from xblock.core import XBlock
from xblock.fields import ScopeIds
from xblock.runtime import DictKeyValueStore, KvsFieldData, Runtime
from xblock.test.tools import TestRuntime

from xmodule.modulestore.inheritance import InheritanceMixin


class TestXBlock:
    pass


@ddt.ddt
class TestInheritanceMixin(unittest.TestCase):

    def setUp(self):
        """
        Create a test xblock with mock runtime.
        """
        runtime = TestRuntime(
            Mock(entry_point=XBlock.entry_point), mixins=[InheritanceMixin], services={'field-data': {}}
        )
        self.xblock = runtime.construct_xblock_from_class(
            TestXBlock, ScopeIds('user', 'TestXBlock', 'def_id', 'usage_id')
        )
        super(TestInheritanceMixin, self).setUp()

    def add_submission_deadline_information(self, due_date, graceperiod, self_paced):
        """
        Helper function to add pacing, due date and graceperiod to DnDXblock.
        """
        self.xblock.due = due_date
        self.xblock.graceperiod = graceperiod
        self.xblock.self_paced = self_paced

    @ddt.data(
        (False, now(), None, True),
        (True, now(), None, False),
        (False, now(), timedelta(days=1), False),
        (True, now(), timedelta(days=1), False),
        (False, now() - timedelta(hours=1), None, True),
    )
    @ddt.unpack
    def test_submission_deadline(self, self_paced, due_date, graceperiod, is_submission_due):
        """
        Verifies the deadline passed boolean value w.r.t pacing and due date.

        Given the pacing information, due date and graceperiod,
        confirm if the submission deadline has passed or not.
        """
        self.add_submission_deadline_information(due_date, graceperiod, self_paced)
        self.assertEqual(is_submission_due, self.xblock.has_deadline_passed())
