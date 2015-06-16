"""This XBlock provides an HTML page fragment to display a button
   allowing the Course user to launch an external course Container
   via Appsembler's Container deploy API.
"""

import pkg_resources

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
        default=0, scope=Scope.content,
        help=("The name of the container's Project as defined in the "
             "Appsembler API"),
    )

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    def student_view(self, context=None):
        """
        The primary view of the LaunchContainerXBlock, shown to students
        when viewing courses.
        """
        html = self.resource_string("static/html/launchcontainer.html")
        frag = Fragment(html.format(self=self))
        # frag.add_css(self.resource_string("static/css/launchcontainer.css"))
        frag.add_javascript(self.resource_string("static/js/src/launchcontainer.js"))
        frag.initialize_js('LaunchContainerXBlock')
        return frag
