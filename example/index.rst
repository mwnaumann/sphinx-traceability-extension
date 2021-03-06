.. Example documentation master file, created by
   sphinx-quickstart on Sat Sep  7 17:17:38 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Example's documentation!
===================================

Contents:

.. toctree::
    :maxdepth: 1

    rqts/SRS
    rqts/SSS

.. item:: r001 First requirement
    :class: functional requirement
    :status: Draft
    :level: ASIL-C ASPICE-3

    This is one item

    - More content
    - More again

        - And nested content
        - *other* with **emphasis** and

    .. note:: a note

        Yes, a note

.. item:: r002
    :class: critical
    :status: Reviewed

    We have to extend this section

This text is not part of any item

.. item:: r003 The great
    :class: secondary
    :trace: r002
    :ext_toolname: namespace:group:document
    :level: ASIL-A
    :status: Approved

    Clean up all this.

.. item:: r005 Another (does not show captions on the related items)
    :level: ASIL-C ASPICE-3
    :class: terciary
    :trace: r002 r002 r003
    :nocaptions:

    Clean up all this again

.. item:: r006 Depends on all
    :class: terciary
    :trace: r001
        r002
        r003
        r005

    To demonstrate that bug #2 is solved

.. item:: r007 Depends on all with stereotypes
    :level: ASIL-X
    :class: terciary
    :trace: r001
    :validates: r002
    :fulfills:  r003
        r005

    To demonstrate stereotype usage in relationships.

    To demonstrate invalid attribute, ASIL-X is not valid attribute (should not appear in e.g. item-list).


.. requirement:: r100 A requirement using the ``requirement`` type

    This item has been defined using other directive. It easily extends
    rst semantics

.. item:: r008 Requirement with invalid reference to other one
    :level: ASIL-D
    :trace: non_existing_requirement

    Ai caramba, this should report a broken link to an non existing requirement.

.. item:: r009 Requirement with invalid relation kind or attribute
    :non_existing_relation_or_attribute: r007

    Ai caramba, this should report a warning as the relation kind or attribute does not exist.

Item list
=========

No items
--------

.. item-list:: No items
    :filter: this_regex_doesnt_match_any_item

List all items
--------------

.. item-list:: All available items (no captions)
    :nocaptions:


List all items beginning with ``r00``
-------------------------------------

.. item-list::
    :filter: ^r00

List system requirements (beginning with SYS)
---------------------------------------------

.. item-list:: System requirements
    :filter: ^SYS

List all well-formed SYS and SRS requirements
---------------------------------------------

.. item-list:: System and software requirements
    :filter: ^S[YR]S_\d

List all items with ASIL attribute
----------------------------------

.. item-list:: All ASIL items
    :level: ASIL-[ABCD]

List all items with ASIL and Draft/Approved attribute
-----------------------------------------------------

.. item-list:: All Draft ASIL items
    :status: (Draft|Approved)
    :level: ASIL-[ABCD]

Item matrix
===========

No relationships
----------------

.. item-matrix:: None
    :source: source_regex_doesnt_match_anything
    :targettitle: nothing
    :sourcetitle: more of nothing
    :stats:

All relationships
-----------------

.. item-matrix:: All (no captions)
    :nocaptions:
    :stats:

Traceability from SRS to SSS
----------------------------

.. item-matrix:: Software requirements fulfilling system requirements
    :target: SYS
    :source: SRS
    :targettitle: system requirement
    :sourcetitle: software requirement
    :type: fulfills
    :stats:

Traceability from SSS to SRS
----------------------------

.. item-matrix:: System requirements fulfilled by software requirements
    :target: SRS
    :source: SYS
    :targettitle: software requirement
    :sourcetitle: system requirement
    :type: fulfilled_by
    :stats:

Another matrix that should spawn a warning as the relation in *type* does not exist
-----------------------------------------------------------------------------------

.. item-matrix:: System requirements traced to software requirements, using a non-existing relationship (=warning)
    :target: SRS
    :source: SYS
    :type: non_existing_relation
    :targettitle: system requirement
    :sourcetitle: software requirement

Item 2D matrix
==============

SRS to SSS
----------

.. item-2d-matrix:: System requirements fulfilled by software requirements
    :target: SRS
    :source: SYS
    :type: fulfilled_by

.. item-2d-matrix:: System requirements fulfilled by software requirements
    :target: SRS
    :source: SYS
    :hit: x
    :miss: o
    :type: fulfilled_by

SSS to SRS
----------

.. item-2d-matrix:: Software requirements fulfilling system requirements
    :target: SYS
    :source: SRS
    :hit: yes
    :miss:
    :type: fulfills

Another 2D matrix that should spawn a warning as the relation in *type* does not exist
--------------------------------------------------------------------------------------

.. item-2d-matrix:: System requirements traced to software requirements, using a non-existing relationship (=warning)
    :target: SRS
    :source: SYS
    :hit: yes
    :miss: no
    :type: non_existing_relation

Item tree
=========

Empty tree
----------

.. item-tree:: Empty
    :top: this_regex_doesnt_match_anything

Succesfull SYS tree
-------------------

.. item-tree:: SYS
    :top: SYS
    :top_relation_filter: depends_on
    :type: fulfilled_by

.. item-tree:: SYS (no captions)
    :top: SYS
    :top_relation_filter: depends_on
    :type: fulfilled_by
    :nocaptions:

Another tree that should spawn a warning as the relation in *top_relation_filter* does not exist.
-------------------------------------------------------------------------------------------------

.. item-tree:: warning for unknown relation
    :top: SYS
    :top_relation_filter: non_existing_relation
    :type: fulfilled_by

Another tree that should spawn a warning as the relation in *type* does not exist
---------------------------------------------------------------------------------

.. item-tree:: warning for unknown relation
    :top: SYS
    :top_relation_filter: depends_on
    :type: non_existing_relation

.. only:: TEST_FOR_ENDLESS_RECURSION

    Another tree that should spawn a warning as the forward and reverse relation are in the *type* field.

    .. item-tree:: warning for forward+reverse
        :top: SYS
        :top_relation_filter: depends_on
        :type: fulfilled_by fulfills

Links and references
====================

Item reference: :item:`r001`

:item:`Item reference with alternative text<r001>`


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
