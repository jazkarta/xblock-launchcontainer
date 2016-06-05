
"""This XBlock provides an HTML page fragment to display a button
   allowing the Course user to launch an external course Container
   via Appsembler's Container deploy API.
"""

import pkg_resources
import logging

from django.conf import settings
from django.template import Context, Template

from xblock.core import XBlock
from xblock.fields import Scope, String
from xblock.fragment import Fragment


log = logging.getLogger(__name__)


API_URL_DEFAULT = 'http://isc.appsembler.com/isc/newdeploy'  # BBB


class LaunchContainerXBlock(XBlock):
    """
    Provide a Fragment with associated Javascript to display to 
    Students a button that will launch a configurable external course
    Container via a call to Appsembler's container deploy API.
    """

    display_name = String(help="Display name of the component", 
                          default="Container Launcher",
                          scope=Scope.settings)

    project = String(
        display_name='Project name',
        default=u'(EDIT THIS COMPONENT TO SET PROJECT NAME)', 
        scope=Scope.content,
        help=(u"The name of the container's Project as defined for the "
             "Appsembler API"),
    )

    project_friendly = String(
        display_name='Project Friendly name',
        default=u'', 
        scope=Scope.content,
        help=(u"The name of the container's Project as displayed to the end "
             "user"),
    )

    api_url = String(
        default=u'',
        scope=Scope.content,
    )

    @property
    def block_course_org(self):
        return self.runtime.course_id.org
    
    @property
    def student_email(self):
        if hasattr(self, "runtime"):
            user = self.runtime._services['user'].get_current_user()
            return user.emails[0]
        else:
            return None

    def _get_API_url(self):
        api_conf = settings.ENV_TOKENS.get('LAUNCHCONTAINER_API_CONF', None)
        if not api_conf:
            return API_URL_DEFAULT  # BBB
        else:
            try:
                return api_conf[self.block_course_org]
            except KeyError:
                return api_conf['default']

    def student_view(self, context=None):
        """
        The primary view of the LaunchContainerXBlock, shown to students
        when viewing courses.
        """
        
        context = {
            'project': self.project,
            'project_friendly': self.project_friendly,
            'user_email' : self.student_email,
            'API_url': self.api_url
        }
        frag = Fragment()
        frag.add_content(
            render_template('static/html/launchcontainer.html', context)
        )
        frag.add_javascript(render_template("static/js/src/launchcontainer.js",
                                            context))
        frag.initialize_js('LaunchContainerXBlock')
        return frag

    def studio_view(self, context=None):
        """
        Return fragment for editing block in studio.
        """
        try:
            cls = type(self)

            def none_to_empty(data):
                """
                Return empty string if data is None else return data.
                """
                return data if data is not None else ''
           
            edit_fields = (
               (field, none_to_empty(getattr(self, field.name)), validator)
               for field, validator in (
                   (cls.project, 'string'), 
                   (cls.project_friendly, 'string'), )
            )

            context = {
                'fields': edit_fields
            }
            fragment = Fragment()
            fragment.add_content(
                render_template(
                    'static/html/launchcontainer_edit.html',
                    context
                )
            )
            fragment.add_javascript(
                load_resource("static/js/src/launchcontainer_edit.js"))
            fragment.initialize_js('LaunchContainerEditBlock')

            return fragment
        except:  # pragma: NO COVER
            log.error("Don't swallow my exceptions", exc_info=True)
            raise

    @XBlock.json_handler
    def studio_submit(self, data, suffix=''):
        log.info(u'Received data: {}'.format(data))
        try:
            self.project = data['project']
            self.project_friendly = data['project_friendly']
            self.api_url = self._get_API_url()

            return {
                'result': 'success',
            }
        except Exception as e:
            return {
                'result': 'Error saving data:{0}'.format(str(e))
            }

    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("A single launchcontainer",
             """\
                <vertical_demo>
                    <launchcontainer/>
                </vertical_demo>
             """)
        ]

def load_resource(resource_path):  # pragma: NO COVER
     """
     Gets the content of a resource
     """
     resource_content = pkg_resources.resource_string(__name__, resource_path)
     return unicode(resource_content)


def render_template(template_path, context=None):  # pragma: NO COVER
    """
    Evaluate a template by resource path, applying the provided context.
    """
    if context is None:
        context = {}

    template_str = load_resource(template_path)
    template = Template(template_str)
    return template.render(Context(context))
