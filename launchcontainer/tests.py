"""
Tests for launchcontainer
"""
import json
import mock
import os
import unittest

from xblock.field_data import DictFieldData
from opaque_keys.edx.locations import Location, SlashSeparatedCourseKey


class DummyResource(object):
    """
     A Resource class for use in tests
    """
    def __init__(self, path):
        self.path = path

    def __eq__(self, other):
        return isinstance(other, DummyResource) and self.path == other.path


class LaunchContainerXBlockTests(unittest.TestCase):
    """
    Create a launchcontainer block with mock data.
    """
    def setUp(self):
        """
        Creates a test course ID, mocks the runtime, and creates a fake storage
        engine for use in all tests
        """
        super(LaunchContainerXBlockTests, self).setUp()
        self.course_id = SlashSeparatedCourseKey.from_deprecated_string(
            'foo/bar/baz'
        )
        self.runtime = mock.Mock(anonymous_student_id='MOCK')
        self.scope_ids = mock.Mock()

    def make_one(self, display_name=None, **kw):
        """
        Creates a launchcontainer XBlock for testing purpose.
        """
        from launchcontainer import LaunchContainerXBlock as cls
        field_data = DictFieldData(kw)
        block = cls(self.runtime, field_data, self.scope_ids)
        block.location = Location(
            'org', 'course', 'run', 'category', 'name', 'revision'
        )
        block.xmodule_runtime = self.runtime
        block.course_id = self.course_id
        block.scope_ids.usage_id = 'XXX'

        if display_name:
            block.display_name = display_name

        block.project = 'Foo project'
        block.project_friendly = 'Foo Project Friendly Name'
        return block

    @mock.patch('launchcontainer.launchcontainer.load_resource', DummyResource)
    @mock.patch('launchcontainer.launchcontainer.render_template')
    @mock.patch('launchcontainer.launchcontainer.Fragment')
    def test_student_view(self, fragment, render_template):
        # pylint: disable=unused-argument
        """
        Test student view renders correctly.
        """
        block = self.make_one("Custom name")
        fragment = block.student_view()
        render_template.assert_called_once()
        template_arg = render_template.call_args_list[0][0][0]
        self.assertEqual(
            template_arg,
            'static/html/launchcontainer.html'
        )
        context = render_template.call_args_list[0][0][1]
        self.assertEqual(context['project'], 'Foo project')
        self.assertEqual(context['project_friendly'], 'Foo Project Friendly Name')
        self.assertEqual(context['user_email'], None)
        fragment.initialize_js.assert_called_once_with(
            "LaunchContainerXBlock")

    @mock.patch('launchcontainer.launchcontainer.load_resource', DummyResource)
    @mock.patch('launchcontainer.launchcontainer.render_template')
    @mock.patch('launchcontainer.launchcontainer.Fragment')
    def test_studio_view(self, fragment, render_template):
        # pylint: disable=unused-argument
        """
        Test studio view is displayed correctly.
        """
        block = self.make_one()
        fragment = block.studio_view()
        render_template.assert_called_once()
        template_arg = render_template.call_args[0][0]
        self.assertEqual(
            template_arg,
            'static/html/launchcontainer_edit.html'
        )
        cls = type(block)
        context = render_template.call_args[0][1]
        self.assertEqual(tuple(context['fields']), (
            (cls.project, 'Foo project', 'string'),
            (cls.project_friendly, 'Foo Project Friendly Name', 'string')
        ))
        fragment.add_javascript.assert_called_once_with(
            DummyResource("static/js/src/launchcontainer_edit.js"))
        fragment.initialize_js.assert_called_once_with(
            "LaunchContainerEditBlock")

    def test_save_launchcontainer(self):
        """
        Tests save launchcontainer block on studio.
        """
        proj_str = 'Baz Project shortname'
        proj_friendly_str = 'Baz Project Friendly Name'
        block = self.make_one()
        block.studio_submit(mock.Mock(body='{}'))
        self.assertEqual(block.display_name, "Container Launcher")
        self.assertEqual(block.project, 'Foo project')
        self.assertEqual(block.project_friendly, 'Foo Project Friendly Name')
        block.studio_submit(mock.Mock(method="POST", body=json.dumps({
            "project": proj_str,
            "project_friendly": proj_friendly_str})))
        self.assertEqual(block.display_name, "Container Launcher")
