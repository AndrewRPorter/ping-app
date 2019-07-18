========
ping-app
========

About
-----

This application is responsible for delivering SMS questions to participants in order to replicate and extend
`Wandering Mind Is an Unhappy Mind
<http://science.sciencemag.org/content/330/6006/932>`_.

**ping-app** creates a cron job that tries to send question data to the participants every *1* minute(s).

User responses are saved in FireBase, you will need to configure a config.yml file to interact with an external FireBase instance.

Usage
-----

The application can be spawned via cron jobs. Start by calling `python3 schedule.py`

This will schedule the creation of users and initialize the `start-cron.py` file at 9:00am everyday, until stopped
