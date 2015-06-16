"""This XBlock provides an HTML page fragment to display a button
   allowing the Course user to launch an external course Container
   via Appsembler's Container deploy API.
"""

import pkg_resources

from django.template import Template

from xblock.core import XBlock
from xblock.fields import Scope, String
from xblock.fragment import Fragment


class LaunchContainerXBlock(XBlock):
    """
    Provide a Fragment with associated Javascript to display to 
    Students a button that will launch a configurable external course
    Container via a call to Appsembler's container deploy API.
    """

    # Fields are defined on the class.  You can access them in your code as
    # self.<fieldname>.

    # TO-DO: delete count, and define your own fields.
    project = String(
        display_name='Project name',
        default=u'', scope=Scope.content,
        help=(u"The name of the container's Project as defined for the "
             "Appsembler API"),
    )

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

    def student_view(self, context=None):
        """
        The primary view of the LaunchContainerXBlock, shown to students
        when viewing courses.
        """
        context = {
            "project" : self.project
        } 
        frag = Fragment()
        fragment.add_content(
            render_template('static/html/launchcontainer.html', context=context)
        )
        # html = self.resource_string("static/html/launchcontainer.html")
        # frag = Fragment(html.format(self=self))
        frag.add_javascript(self.resource_string("static/js/src/launchcontainer.js"))
        frag.initialize_js('LaunchContainerXBlock')
        return frag

    def studio_view(self, context=None):
        """
        Return fragment for editing block in studio.
        """
        import pdb;pdb.set_trace()
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
                    (cls.projecte, 'string'),
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
            return fragment
        except:  # pragma: NO COVER
            log.error("Don't swallow my exceptions", exc_info=True)
            raise
