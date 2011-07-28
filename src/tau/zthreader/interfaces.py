##############################################################################
#
# Copyright (c) 2010 Tau Productions Inc.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Declaration of various object interfaces.
"""

from zope.interface import Interface
from zope.schema import TextLine
from zope.configuration.fields import GlobalObject

class IBackgroundThreadDirective(Interface):
    """Schema for a complex, nested ZCML directive containing optional arguments.

       This schema determines the XML attributes accepted by the ZCML
       directive and how they are parsed/validated.

       Example of the directive:

         <background-thread                <---- just the outer directive
             name="keepalive"
             threadfunc=".module.func">

             <extra-argument
                 label="remote-url"
                 value="http://127.0.0.1/keepalive"
                 />

             <extra-argument
                 label="ping-interval-secs"
                 value="60"
                 />

         </background-thread>
    """

    name = TextLine(
        title=u"Name of Thread",
        description=u"A name for the thread, meaningful to the developer.",
        required=True,
        )

    threadfunc = GlobalObject(
        title=u"Dotted Module/Function Reference of Thread Function",
        description=u"A callable that becomes the body of the background thread.",
        required=True,
        )


class IBackgroundThreadArgumentSubdirective(Interface):
    """Schema for the ZCML directives nested inside the top-level directive.

       This schema determines the XML attributes accepted by the ZCML
       directive and how they are parsed/validated.

       Example of the directive:

         <background-thread
             name="keepalive"
             threadfunc=".module.func">

             <extra-argument              <---- just the inner directive
                 argname="remote-url"
                 argvalue="http://127.0.0.1/keepalive"
                 />

             <extra-argument
                 argname="ping-interval-secs"
                 argvalue="60"
                 />

         </background-thread>
    """

    name = TextLine(
        title=u"Argument Name",
        description=u"Name of the additional argument.",
        required=False,
        )

    value = TextLine(
        title=u"Argument Value",
        description=u"Value (string) of the additional argument.",
        required=True,
        )


class IThreadDefinition(Interface):
    """An empty interface for tracking registered clusters in the registry.

       We tag instances of our Cluster class with this interface so we can
       retrieve them again from Zope's interface registry.  This retrieval
       also uses a name along with the interface where the name reflects the
       name of the cluster.

       Example::

         cluster = queryUtility(IBackgroundThreadDeclarations, name=threadname)
    """
