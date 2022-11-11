************
Contributing
************

Development workflow
####################

1. Fork the `repository on GitHub <https://github.com/kerkelae/micromodelsim/>`_.

2. Clone your fork:
    
.. code-block:: bash

    git clone git@github.com:{YOUR-USERNAME}/micromodelsim.git

.. note::

   When making changes, it is helpful to install ``micromodelsim`` in editable
   mode by executing the following in the root directory of the cloned
   repo:

   .. code-block:: bash
        
        pip install -e .

3. Configure Git to sync your fork with the main repo:

.. code-block:: bash
       
    git remote add upstream https://github.com/kerkelae/micromodelsim.git

4. Create a branch with a descriptive name:

.. code-block:: bash
        
    git checkout -b {BRANCH-NAME}

5. Write code, commit changes with clear messages, and push the changes to
your fork.

6. Open a pull request `on GitHub <https://github.com/kerkelae/micromodelsim/>`_.

GitHub docs provide more information on `forking a repository
<https://docs.github.com/en/get-started/quickstart/fork-a-repo>`_ and `creating
pull requests
<https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/
proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request-from-
a-fork>`_.

Code style
##########

All code should be formatted with `Black <https://github.com/psf/black>`_ using
the default settings and documented following the `NumPy docstring conventions
<https://numpydoc.readthedocs.io/en/latest/format.html>`_.

Tests
#####

Please run the tests to make sure your changes have not broken anything. This
can be done with ``pytest`` by executing the following in the root directory
of the repository:   

.. code-block::
    
    pytest

Documentation
#############

Documentation can be built locally by executing the following in
``micromodelsim/docs``:

.. code-block::

    make clean
    make html

Note that generating the documentation locally requires the packages listed
in ``micromodelsim/docs/source/requirements.txt``.
