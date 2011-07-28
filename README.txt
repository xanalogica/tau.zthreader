===============
 tau.zthreader
===============

The tau.zthreader is a simple package that adds to Zope2 the ability of a
developer to instantiate a background thread at startup time, for handling any
arbitrary processing desired.  Such a background thread participates in the
Zope transaction machinery (i.e. can begin/commit/rollback itself) and has
access to the ZODB.

Additional ZCML directives are implemented by tau.zthreader to make defining
your own threads easy.  Just add the following to your etc/zope.conf or into
your buildout part definition that constructs your etc/zope.conf file:

[Zope2_instance]
recipe = plone.recipe.zope2instance
zope-conf-additional =
   %import tau.zthreader
   <background-thread>
       secs-per-inspect 3600
       strategy traceonly
       logging  on
   </background-thread>

A background thread starts when Zope2 begins execution and continues forever
or until your thread terminates itself.
