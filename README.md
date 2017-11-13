# KDFT Fall 2017, Final Project: Question Answer Retrieval

Your task is to construct a system that allows a user to type in a
natural language question as a search query, and be presented with
sentences from Wikipedia that may answer that question.  The
deliverables of this project will include a working system, a writeup that
includes performance numbers on how well you can classify sentences as
to whether they answer a given question, and a presentation plus demo
to the rest of the class on the day scheduled for the final exam.

This project is broken into multiple checkpoints.  These are meant to
help structure the project, and to encourage you to
break up lead responsibility for different parts of the project among
team members. Each checkpoint as they are revealed should be added to
your repository as a GitHub Issue, assigned to a member of your team
(hopefully different members for different Issues).  You are all
responsible for the project's success, but each Issue should have a
leader that is taking responsibility for the item being accomplished.
When submitting a checkpoint to Gradescope you will include a saved
pdf of the given Issue.  The pdf should be called:

```
issue-checkpoint-NUMBER.pdf
```

(For example, `issue-checkpoint-0.pdf` for the initial checkpoint.)

You are encouraged to organize your project by creating other Issues
as well, but please track the main deliverables of your effort with a
due date and title corresponding to these checkpoints.  You are
encouraged to make use of Issues to track key communications with your
team members, rather than by email.

Data will be provided under `data/`, with the essential
data set coming from WikiQA, the same set that you partially
annotated in HW3.  Additional data may be released in future
checkpoints.  You should train on train, tune based on dev, and
test on test.  Please refrain from using test until the end of the
semester.  Make use of dev as your test set until time to write the
final report.  Only when explicitly told through instructions that
it is appropriate to run on test, should you run on test.

## Checkpoints

* [Checkpoint 0: Running provided system](checkpoint-0.md)
* [Checkpoint 1: Creating baseline search service](checkpoint-1.md)

## Docker Compose

Here we comment on new (to you) technology used in this checkpoint,
[Docker Compose](https://docs.docker.com/compose/overview/).

Docker Compose is one of the ways that Docker containers begin to be
especially useful.  A compose file allows you to start mixing and
matching components into larger workflows, on the assumption that the
individual components are containerized and working.  (In homework 1
we used a bash script, `run.bash`, to manage a network of Docker
containers: Docker Compose is a more robust way of doing this.)  In
this project, you have access to a UI, a fetch service, and a Lucene
index all pre-baked and assembled into a workflow.  In this checkpoint
you need to slightly modify the compose file to make use of the WikiQA
fetch service.  In the future you will add another container, your own
search service, as part of the larger workflow.

You will not be using them in this course, but be aware there is
experimental development within Docker for things called [stacks and
bundles](https://docs.docker.com/compose/bundles/).  We mention them
here only so you are aware that while currently there is Docker
Compose, in the future some related but different technology will
replace it.  However, the underlying concept of composing (or
"stacking" or "bundling") containers remains the same.
