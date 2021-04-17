# CK repository for AI and ML systems

[![compatibility](https://github.com/ctuning/ck-guide-images/blob/master/ck-compatible.svg)](https://github.com/ctuning/ck)
[![automation](https://github.com/ctuning/ck-guide-images/blob/master/ck-artifact-automated-and-reusable.svg)](https://cTuning.org/ae)

Linux/MacOS: [![Travis Build Status](https://travis-ci.org/ctuning/ck-ml.svg)](https://travis-ci.org/ctuning/ck-ml)
Windows: [![Windows Build status](https://ci.appveyor.com/api/projects/status/gl53cle5dvkskvgr?svg=true)](https://ci.appveyor.com/project/gfursin/ck-ml)


*There are numerous CK components spread across numerous GitHub repositories. 
Based on the feedback from the community, we have created this repository 
to collect all main CK components related to AI and ML Systems in one place. 
These components are also uploaded to the [cKnowledge.io platform](https://cKnowledge.io) 
similar to PyPI to help you search for specific components and see their connections!*

This repository contains a collection of **dev** CK components for ML systems 
in the [CK format](https://arxiv.org/pdf/2011.01149.pdf):

* CK modules with automation actions: [[list](https://github.com/ctuning/ck/tree/master/ck/repo/module)]
* CK program workflows: [[list]( https://cKnowledge.io/programs )]
* CK meta packages: [[list]( https://cKnowledge.io/packages )]
* CK software detection: [[list]( https://cKnowledge.io/soft )]
* CK datasets: [[list]( https://cKnowledge.io/c/dataset )]
* CK adaptive containers: [[list]( https://cKnowledge.io/c/docker )]
* CK OS: [[list]( https://cKnowledge.io/c/os )]
* CK MLPerf system descriptions: [[list]( https://cKnowledge.io/c/sut )]
* CK MLPerf benchmark CMD generators: [[list]( https://cKnowledge.io/c/cmdgen )]

You can find **stable** CK components aggregated in [this repository](https://github.com/ctuning/ai).

# Docs

* CK automation framework: 
  [[GitHub]( https://github.com/ctuning/ck )] 
  [[Online docs](https://ck.readthedocs.io)] 
  [[Overview](https://arxiv.org/pdf/2011.01149.pdf)]

# Usage

## Without Docker

Install the [CK framework](https://cKnowledge.org) as described [here](https://ck.readthedocs.io/en/latest/src/installation.html).

Pull this repository:
```bash
ck pull repo:ck-ml
```
Test the installation using the simple image corner detection program:

```bash
ck ls program:*susan*

ck search dataset --tags=jpeg

ck compile program:cbench-automotive-susan2 --speed

ck run program:cbench-automotive-susan2 --cmd_key=corners --repeat=1 --env.MY_ENV=123 --env.TEST=xyz

# view output
ls `ck find program:cbench-automotive-susan2`/tmp/output.pgm
```

Try [portable AI/ML workflows](https://cKnowledge.io/solutions), [program pipelines](https://cKnowledge.io/programs)
and [adaptive CK containers](https://cKnowledge.io/c/docker).
*Note that you do not need to pull other repositories anymore
 since all the components are aggregated here.*

Check [public dashboards](https://cKnowledge.io/reproduced-results) with reproduced results from [research papers](https://cKnowledge.io/reproduced-papers).

See real use cases from the community: [MLPerf, Arm, General Motors, IBM, Raspberry Pi foundation, ACM, dividiti and others](https://cknowledge.org/partners.html).

Read about the [CK concept and format](https://arxiv.org/abs/2011.01149).

## With Docker

We have prepared a CK container with all CK components from this repository: 
[[Docker](https://hub.docker.com/r/ctuning/ck-ml)], [[CK meta](https://github.com/ctuning/ck-ml/tree/main/docker/ck-ml)]

You can start it as follows:

```bash
docker run --rm -it ctuning/ck-ml:ubuntu-20.04
```

You can then prepare and run these [portable AI/ML workflows](https://cKnowledge.io/solutions) 
and [program pipelines](https://cKnowledge.io/programs).


# License

BSD 3-clause. We are discussing the possibility to relicense the CK framework and components to Apache 2.0.

# Contributions

Please contribute as described [here](https://ck.readthedocs.io/en/latest/src/how-to-contribute.html)
and submit your PRs [here](https://github.com/ctuning/ck-ml/pulls).

# Acknowledgments

We would like to thank all [collaborators](https://cKnowledge.org/partners.html) for their support, fruitful discussions, 
and useful feedback! See more acknowledgments in the [CK journal article](https://arxiv.org/abs/2011.01149).


# Contacts

Don't hesitate to get in touch with the [CK community](https://cknowledge.org/contacts.html) 
if you have questions or comments.
