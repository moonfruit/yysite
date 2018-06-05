# -*- coding: utf-8 -*-
import logging

from django_cron import CronJobBase, Schedule

from .base import FetcherJob

logger = logging.getLogger(__name__)


class HearthstoneJob(CronJobBase, FetcherJob):
    RUN_EVERY_MINS = 59
    RETRY_AFTER_FAILURE_MINS = 9

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS,
                        retry_after_failure_mins=RETRY_AFTER_FAILURE_MINS)
    code = 'yyfeed.fetcher.hearthstone'

    def name(self):
        return 'hearthstone'


class OoxxJob(CronJobBase, FetcherJob):
    RUN_EVERY_MINS = 59
    RETRY_AFTER_FAILURE_MINS = 9

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS,
                        retry_after_failure_mins=RETRY_AFTER_FAILURE_MINS)
    code = 'yyfeed.fetcher.ooxx'

    def name(self):
        return 'ooxx'


class IAppsJob(CronJobBase, FetcherJob):
    RUN_EVERY_MINS = 59
    RETRY_AFTER_FAILURE_MINS = 9

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS,
                        retry_after_failure_mins=RETRY_AFTER_FAILURE_MINS)
    code = 'yyfeed.fetcher.iapps'

    def name(self):
        return 'iapps'


class SmzdmJob(CronJobBase, FetcherJob):
    RUN_EVERY_MINS = 59
    RETRY_AFTER_FAILURE_MINS = 9

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS,
                        retry_after_failure_mins=RETRY_AFTER_FAILURE_MINS)
    code = 'yyfeed.fetcher.smzdm'

    def name(self):
        return 'smzdm'


class TtrssJob(CronJobBase, FetcherJob):
    RUN_EVERY_MINS = 59
    RETRY_AFTER_FAILURE_MINS = 359

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS,
                        retry_after_failure_mins=RETRY_AFTER_FAILURE_MINS)
    code = 'yyfeed.fetcher.ttrss'

    def name(self):
        return 'ttrss'


class RosiyyJob(CronJobBase, FetcherJob):
    RUN_EVERY_MINS = 59
    RETRY_AFTER_FAILURE_MINS = 1439

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS,
                        retry_after_failure_mins=RETRY_AFTER_FAILURE_MINS)
    code = 'yyfeed.fetcher.rosiyy'

    def name(self):
        return 'rosiyy'
