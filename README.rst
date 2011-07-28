===============
 tau.zthreader
===============

Introduction
============

The tau.zthreader is a simple package that adds to Zope2 the ability of a
developer to instantiate a background thread at startup time, for handling any
arbitrary processing desired.  Such a background thread participates in the
Zope transaction machinery (i.e. can begin/commit/rollback itself) and has
access to the ZODB.

Additional ZCML directives are implemented by tau.zthreader to make defining
your own threads easy.  Just add the following to your etc/site.zcml or into
your buildout part definition that constructs your etc/site.zcml file::


  [buildout]
  eggs = tau.zthreader

  [Zope2_instance]
  recipe = plone.recipe.zope2instance
  zcml += tau.zthreader-meta

  zcml-additional =
                    <configure
                        xmlns="http://namespaces.zope.org/zope"
                        i18n_domain="tau.zthreader">

                        <background-thread callable=".yourmodule.yourthreadfunc">

                            <additional-argument
                                label="keepalive-host"
                                value="127.0.0.1"
                                />

                            <additional-argument
                                label="ping-interval-secs"
                                value="30"
                                />

                        </background-thread>

                    </configure>

The background thread is started when Zope2 emits the event that the ZODB is
ready, and continues forever or until your thread terminates itself.


.. sidebar:: Obtaining Development Versions

   In addition to the PyPI downloads, the development version of this
   component is available via its `project on Github`_.

.. _`project on Github`:
.. https://github.com/xanalogica/tau.zthreader#egg=tau.zthreader-dev
