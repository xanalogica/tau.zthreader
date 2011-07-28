##############################################################################
#
# Copyright (c) 2011 Tau Productions Inc.
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
"""Implementation of a complex top/sub directive pair.

   ZCML directives can be divided into two kinds; simple and complex.  A
   simple directive is a standalone XML tag.  A complex directive acts as a
   container of other ZCML directives, giving them context and allowing for
   the factoring out of redundant XML tags.

   A simple directive has a handler implemented as a simple function, which is
   called in the XML-tag closure phase.

   A complex directive has a handler that is a class instantiated at XML-tag
   open with the XML tag attributes, and the instance called at XML tag
   closure.

   For the complex directive::

      <background-thread name="sitedocs" threadfunc=".module.func">
          <argument name="libpath", value="/usr/share/public" />
          <argument name="csspath", value="/home/jeff/works" />
      </background-thread>

   And then you reference the declared background threads as a Zope vocabulary named with
   the cluster name using a Choice-type of schema dropdown widget::

      from zope.schema import Choice
      class ILibrary(Interface):
          sitedocs = Choice(title=u"Path to Site Documents",
                            vocabulary="sitedocs")
"""

from threading import Thread
from zope.interface import implements
from zope.component import queryUtility, provideUtility, provideHandler

from .interfaces import IThreadDefinition

####
# Provide a logging instance for producing error or status messages into the
# Zope logfile during the parsing of any ZCML configuration file.  This is
# standard for any ZCML parser under Zope.

import logging
log = logging.getLogger("tau.zthreader")


class backgroundthread_ComplexDirectiveHandler(object):
    """Handler for a complex ZCML directive, including any subdirectives.

       NOTE: A handler does NOT execute an action immediately but instead
       registers an action to occur at the end of the configuration process.
       This is because the system should go through all of the configuration
       first, detecting potential conflicts and implementing possible
       overrides.  Only after the configuration is fully determined are the
       registered actions performed.

       Subdirectives (i.e. nested ones) are handled as methods on this class,
       where the name of the method *MUST* match the name of the subdirective.
    """

    def __init__(self, _context, name, threadfunc):
        """Handle of a complex directive.

           Takes as arguments any attributes of the complex (outer) directive,
           after they have been automatically validated by Zope against the
           directive's schema.
        """
        self.__context  = _context
        self.threadname = name
        self.threadfunc = threadfunc
        self.threadargs = {}

        _context.action( # register an action to occur at the end of the configuration process
            discriminator=('backgroundthread', name),  # must be unique!
            callable=self.deferred__instantiate_thread_defn,
            args=(_context, name, threadfunc),
            )

    def deferred__instantiate_thread_defn(self, _context, threadname, threadfunc):
        """The actual handling that is performed at the -END- of configuration.

           Create one 'backgroundthread' object for each unique threadname
           seen as they are parsed from a ZCML file.
        """

        self.thread_defn = queryUtility(IThreadDefinition, name=threadname)
        if self.thread_defn is not None: # not first time this threadname has been seen
            log.info("ERROR - Duplicate background thread declaration with name %r." % threadname)

        log.info("Defining thread named %r for function %r" % (threadname, threadfunc))
        self.thread_defn = ThreadDefinition(threadname, threadfunc, self.threadargs)

        provideUtility(self.thread_defn, provides=IThreadDefinition, name=threadname)

        self.thread_defn.start()

    def argument(self, _context, name, value):
        """Handler for the 'argument' subdirective.

           Handlers for subdirectives also must AVOID executing an action
           immediately but instead register an action to occur at the end of
           the configuration process.
        """

        self.threadargs[name] = value

    def __call__(self):
        """Called when the complex directive is *** empty ***.

           Use of this method is optional and we don't need it as we don't do
           anything special if our complex directive has no subdirectives
           within it.
        """
        return ()


class ThreadDefinition(Thread):
    """Modeled after implementation in the zope.sendmail package.
    """
    implements(IThreadDefinition)

    def __init__(self, threadname, threadfunc, threadargs):
        Thread.__init__(self)

        self.name = threadname
        self.func = threadfunc
        self.args = threadargs

    def __repr__(self):
        return "%s(%r, id=%r)" % (
            self.__class__.__name__, self.name, id(self))

    def run(self, forever=True):
        self.func(self.args)
