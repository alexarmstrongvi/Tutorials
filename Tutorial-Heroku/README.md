# Heroku Tutorial

## Overview
* Why use Heroku?
    * Deploying an application so that others can access it is rarely worth doing on your personal computer
    * Heroku is a PaaS cloud service for deploying and scaling your applications
    * Heroku is one of the first PaaS providers of its kind and offers many features but price, containerization, scalability, and other needs may drive one to competitors like Back4app, Google App Engine, or Dokku.
* What is Heroku?
    * Container-based PaaS service built on top of AWS that supports several application languages 
    * Founded in 2007 and acquired by Salesforce in 2010

## Quickstart
* Logging in
    * `heroku login`
* Deploying 
    * `heroku create` - creates git remote `heroku` with randomly generated name (e.g. https://git.heroku.com/limitless-castle-02895.git)
    * Repo Requirements: `Procfile`, `requirements.txt`
    * `git push heroku main`
    * Set config variables if needed (see below)
    * `heroku ps:scale web=1`
    * `heroku open`
* Viewing logs
    * `heroku logs --tail`
* Procfile
    * `web: gunicorn gettingstarted.wsgi`
* Scaling the app
    * `heroku ps:scale web=0`
    * `heroku ps:scale web=N` (N>1 requires non-free dyno)
* Dependencies
    * `requirements.txt` indicates python app to Heroku and it runs `pip install -r` when deploying
* Run app locally
    * `heroku local web` or just `heroku web`
* Push local changes
    * `git push heroku main`
* Provision add-ons
    * Requires "account verification" (i.e. add billing info to account)
    * `heroku addons:create papertrail` - papertrail is a logging service
    * `heroku addons`
    * `heroku addons:open papertrail`
* Start a console
    * `heroku run bash`
    * `heroku run python manage.py shell`
* Define config vars
    * Update `.env` file
    * `heroku config:set MY_VAR=val`
    * `heroku config`
* Provision a database
    * Many database add-ons available. `heroku-postgresql` is free
    * `heroku config`
    * `heroku pg`
    * `heroku pg:psql`

## Heroku Architecture Details

* Deployment
    * Procfile - process file declaring processes to execute against your built application
    * Buildpacks - program for building slugs from Procfile and dependency specification (e.g. `requirements.txt`)
    * Slug - bundle of all the code, runtime environment, and build outputs needed to run an application
    * Config vars - configuration data accessible to application through environment variables
    * Add-ons - 3rd party cloud services
    * Release - slug + configuration + add-ons. Releases are stored by Heroku and appended every tie a new slug is deployed
* Runtime
    * Dyno - lightweight Unix container that contains your application slug
        * Created from scratch every time based on slug 
        * Ephemeral filesystem - temporary filesystem setup for each dyno such that changes are never propogated to other dynos
        * Sleep state - shutdown application that must be re-initialized to respond to request. Only occurs to free dyno types
        * One-off dynos - temperary dyno that attaches I/O to local terminal for debugging
    * Process types 
        * web - able to receive and respond to HTTP traffic
            * Heroku's HTTP routers manage the forwarding of incoming requests to available dynos
        * queue - 
    * Dyno formation - total number of executing (i.e. not sleeping) dynos broken down by process type
    * Dyno manager - Component of Heroku platform that manages dynos
    * Logging
        * Logplex - logging program that receives the log streams of all dynos and Heroku platform components and maintains a buffer of recent logs.
        * Add-ons needed to persist logs
* Unix process model - abstraction of how server-side programs are run
    * Process - 
    * Process management -
    * Daemon - 
    * Process types
    * Scale vs. workload diversity = Number of dynos of a given type versus the number of types of dynos

## CLI
* `heroku run`
* `heroku create`
* `heroku open`
* `heroku local`
* `heroku ps` - manage dyno formation
* `heroku addons`
* `heroku logs`
* `heroku config`
* `heroku pg`
* `heroku releases`

## Python Specifics

## Questions
* What are the different types of dynos (e.g. queue)?
* How do dynos communicate with other dynos or services?

# References
* [Offical Heroku Docs](https://devcenter.heroku.com/categories/reference)
* [Official Heroku "Getting Started" page](https://devcenter.heroku.com/articles/getting-started-with-python)
