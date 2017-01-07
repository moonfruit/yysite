# -*- coding: utf-8 -*-
import logging

from django_cron import CronJobBase, Schedule

from .base import FetcherJob

logger = logging.getLogger(__name__)


class HearthstoneJob(CronJobBase, FetcherJob):
    RUN_EVERY_MINS = 60
    RETRY_AFTER_FAILURE_MINS = 10

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS,
                        retry_after_failure_mins=RETRY_AFTER_FAILURE_MINS)
    code = 'yyfeed.fetcher.hearthstone'

    def name(self):
        return 'hearthstone'


class OoxxJob(CronJobBase, FetcherJob):
    RUN_EVERY_MINS = 60
    RETRY_AFTER_FAILURE_MINS = 10

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS,
                        retry_after_failure_mins=RETRY_AFTER_FAILURE_MINS)
    code = 'yyfeed.fetcher.ooxx'

    def name(self):
        return 'ooxx'
