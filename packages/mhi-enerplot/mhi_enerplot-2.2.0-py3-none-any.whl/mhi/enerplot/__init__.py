#===============================================================================
# Manitoba Hydro International / Power Technology Center
# Enerplot Automation Library
#===============================================================================
"""
Manitoba Hydro International

Enerplot Python Automation Library

Connect to already running application::

   import mhi.enerplot
   enerplot = mhi.enerplot.connect()
   enerplot.load_files('myproject')

Launch and connect to new application instance::

   import mhi.enerplot
   enerplot = mhi.enerplot.launch()
   enerplot.load_files('myproject')

Connect to application, launching a new instance if necessary::

   import mhi.enerplot
   enerplot = mhi.enerplot.application()
   enerplot.load_files('myproject')
"""

#===============================================================================
# Version Identifiers
#===============================================================================

VERSION = '2.2.0'
VERSION_HEX = 0x020200f0


#===============================================================================
# Imports
#===============================================================================

import os, sys, logging
from typing import List, Tuple

import mhi.common


#-------------------------------------------------------------------------------
# Submodules
#-------------------------------------------------------------------------------

from mhi.common.remote import Context #, Remotable #, deprecated
from mhi.common import config

from .application import Enerplot
from .progress import Progress
from .trace import Trace
from .component import Component
from .book import Book, Sheet
from .annotation import Line, TextArea
from .graph import GraphFrame, PlotFrame, FFTFrame, GraphPanel, Curve
from .datafile import DataFile, MutableDataFile, Channel


#===============================================================================
# Logging
#===============================================================================

_LOG = logging.getLogger(__name__)


#===============================================================================
# Options
#===============================================================================

OPTIONS = config.fetch("~/.mhi.enerplot.py")


#===============================================================================
# Connection and Application Start
#===============================================================================

def application():
    """
    This method will find try to find a currently running Enerplot application,
    and connect to it.  If no running Enerplot application can be found, or
    if it is unable to connect to that application, a new Enerplot application
    will be launched and a connection will be made to it.

    If running inside a Python environment embedded within an Enerplot
    application, the containing application instance is always returned.

    Returns:
        Enerplot: The Enerplot application proxy object

    Example::

        import mhi.enerplot
        enerplot = mhi.enerplot.application()
        enerplot.load_files('myproject')
    """

    return Context._application(connect, launch, 'Enerplot%.exe')

def connect(host='localhost', port=None, timeout=5):

    """
    This method will find try to find a currently running Enerplot application,
    and connect to it.

    Parameters:
        host (str): The host the Enerplot application is running on
            (defaults to the local host)

        port (int): The port to connect to.  Required if running multiple
            Enerplot instances.

        timeout (float): Seconds to wait for the connection to be accepted.

    Returns:
        Enerplot: The Enerplot application proxy object

    Example::

        import mhi.enerplot
        enerplot = mhi.enerplot.application()
        enerplot.load_files('myproject')
    """

    if host == 'localhost':
        if not port:
            ports = mhi.common.process.listener_ports_by_name('Enerplot%')
            if not ports:
                raise ProcessLookupError("No availiable Enerplot process")

            addr, port, pid, app = ports[0]
            _LOG.info("%s [%d] listening on %s:%d", app, pid, addr, port)

    _LOG.info("Connecting to %s:%d", host, port)

    return Context._connect(host=host, port=port, timeout=timeout)


def launch(port=None, silence=True, timeout=5, version=None, **options):

    """
    Launch a new Enerplot instance and return a connection to it.

    Parameters:
        port (int): The port to connect to.  Required if running multiple
            Enerplot instances.

        silence (bool): Suppresses dialogs which can block automation.

        timeout (float): Time (seconds) to wait for the connection to be
            accepted.

        version (str): Specific version to launch if multiple versions present.

        **options: Additional keyword=value options

    Returns:
        Enerplot: The Enerplot application proxy object

    Example::

        import mhi.enerplot
        enerplot = mhi.enerplot.launch()
        enerplot.load_files('myproject')
    """

    options = dict(OPTIONS, **options) if OPTIONS else options

    args = ["{exe}", "/nologo", "/port:{port}"]

    if 'exe' not in options:
        options['exe'] = mhi.common.process.find_exe('Enerplot', version)

    if not port:
        port = mhi.common.process.unused_tcp_port()
        _LOG.info("Automation server port: %d", port)

    mhi.common.process.launch(*args, port=port, **options)

    app = connect(port=port, timeout=timeout)

    if app and silence:
        app.silence = True

    return app

def versions() -> List[Tuple[str, bool]]:
    """
    Find the installed versions of PSCAD

    Returns:
        List[Tuple[str, bool]]: List of tuples of version string and 64-bit flag
    """

    import mhi.common.process          # pylint: disable=import-outside-toplevel

    return mhi.common.process.versions('Enerplot')


