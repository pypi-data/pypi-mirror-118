===========
Clustercron
===========

.. image:: https://img.shields.io/pypi/v/clustercron.svg
        :target: https://pypi.python.org/pypi/clustercron

.. image:: https://results.pre-commit.ci/badge/github/pre-commit/action/master.svg
        :target: https://results.pre-commit.ci/latest/github/maartenq/clustercron/master

.. image:: https://readthedocs.org/projects/clustercron/badge/?version=latest
        :target: https://clustercron.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


**Clustercron** is cronjob wrapper that tries to ensure that a script gets run
only once, on one host from a pool of nodes of a specified loadbalancer.
**Clustercron** select a *master* from all nodes and will run the cronjob only
on that node.

* Free software: ISC license
* Documentation: https://clustercron.readthedocs.org/en/latest/

Features
--------

Supported load balancers (till now):

    * AWS Elastic Load Balancing (ELB)
    * AWS Elastic Load Balancing v2 (ALB)
