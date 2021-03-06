from django.db.models import Q
from django import template
from django.utils.html import format_html
import json
from rq import Queue
from redis import Redis
from rq.registry import StartedJobRegistry, FailedJobRegistry, FinishedJobRegistry

register = template.Library()
redis_conn = Redis()
started = StartedJobRegistry('stir_fry', connection=redis_conn)
failed = FailedJobRegistry('default', connection=redis_conn)
finished = FinishedJobRegistry('stir_fry', connection=redis_conn)

_q = Queue('stir_fry', connection=redis_conn)


@register.simple_tag
def fetch_job(id):
    try:
        _job = _q.fetch_job(id)
        job = _job.to_dict()
        data = job.pop('data')

        _a = job.copy()
        _a.update(_job.kwargs)
        return _a
    except Exception:
        return 0


@register.simple_tag
def get_queued_jobs():
    jobs = _q.get_job_ids()
    print(jobs)
    return jobs


@register.simple_tag
def get_started_jobs():
    jobs = started.get_job_ids()
    print(jobs)
    return jobs


@register.simple_tag
def get_failed_jobs():
    jobs = failed.get_job_ids(end=100)
    return jobs


@register.simple_tag
def get_finished_jobs():
    jobs = finished.get_job_ids()
    return jobs
