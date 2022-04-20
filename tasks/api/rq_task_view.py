from __future__ import division

import json
from math import ceil

from django.contrib import admin, messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core import management
from django.http import Http404, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django_rq.queues import get_queue_by_index
from django_rq.settings import API_TOKEN
from django_rq.utils import get_statistics, get_jobs

from redis.exceptions import ResponseError
from rest_framework.decorators import api_view, schema
from rest_framework.response import Response
from rq import requeue_job
from rq.exceptions import NoSuchJobError
from rq.job import Job, JobStatus
from rq.registry import (
    DeferredJobRegistry,
    FailedJobRegistry,
    FinishedJobRegistry,
    ScheduledJobRegistry,
    StartedJobRegistry,
)
from rq.worker import Worker
from rq.worker_registration import clean_worker_registry


def jobs_to_dictionary(jobs):
    JOBS = []
    for _job in jobs:
        JOBS.append(job_to_dictionary(_job))
    return JOBS


def job_to_dictionary(_job):
    job = _job.to_dict()
    data = job.pop('data')
    d = job.update({"id": _job.get_id()})
    try:
        d = job.pop('exc_info')
    except Exception:
        pass
    _a = job.copy()
    _a.update(_job.kwargs)
    return _a


@never_cache
@staff_member_required
@api_view(['GET'])
@schema(None)
def stats(request):
    context_data = {
        **admin.site.each_context(request),
        **get_statistics(run_maintenance_tasks=True)
    }
    # return render(request, 'django_rq/stats.html', context_data)
    return Response(context_data)


def stats_json(request, token=None):
    if request.user.is_staff or (token and token == API_TOKEN):
        return JsonResponse(get_statistics())

    return JsonResponse({
        "error": True,
        "description": "Please configure API_TOKEN in settings.py before accessing this view."
    })


@never_cache
@staff_member_required
@api_view(['GET'])
@schema(None)
def jobs(request, queue_index):
    queue_index = int(queue_index)
    queue = get_queue_by_index(queue_index)

    items_per_page = 100
    num_jobs = queue.count
    page = int(request.GET.get('page', 1))

    if num_jobs > 0:
        last_page = int(ceil(num_jobs / items_per_page))
        page_range = range(1, last_page + 1)
        offset = items_per_page * (page - 1)
        jobs = queue.get_jobs(offset, items_per_page)
    else:
        jobs = []
        page_range = []

    context_data = {
        'queue_index': queue_index,
        'jobs': jobs_to_dictionary(jobs),
        'num_jobs': num_jobs,
        'page': page,
        'job_status': 'Queued',
    }

    # return render(request, 'django_rq/jobs.html', context_data)
    return Response(context_data)


@never_cache
@staff_member_required
@api_view(['GET'])
@schema(None)
def finished_jobs(request, queue_index):
    queue_index = int(queue_index)
    queue = get_queue_by_index(queue_index)

    registry = FinishedJobRegistry(queue.name, queue.connection)

    items_per_page = 100
    num_jobs = len(registry)
    page = int(request.GET.get('page', 1))
    jobs = []

    if num_jobs > 0:
        last_page = int(ceil(num_jobs / items_per_page))
        page_range = range(1, last_page + 1)
        offset = items_per_page * (page - 1)
        job_ids = registry.get_job_ids(offset, offset + items_per_page - 1)
        jobs = get_jobs(queue, job_ids, registry)

    else:
        page_range = []

    context_data = {
        'queue_index': queue_index,
        'jobs': jobs_to_dictionary(jobs),
        'num_jobs': num_jobs,
        'page': page,
        'job_status': 'Finished',
    }
    return Response(context_data)


@never_cache
@staff_member_required
@api_view(['GET'])
@schema(None)
def failed_jobs(request, queue_index):
    queue_index = int(queue_index)
    queue = get_queue_by_index(queue_index)
    registry = FailedJobRegistry(queue.name, queue.connection)
    items_per_page = 100
    num_jobs = len(registry)
    page = int(request.GET.get('page', 1))
    jobs = []
    if num_jobs > 0:
        last_page = int(ceil(num_jobs / items_per_page))
        page_range = range(1, last_page + 1)
        offset = items_per_page * (page - 1)
        job_ids = registry.get_job_ids(offset, offset + items_per_page - 1)
        jobs = get_jobs(queue, job_ids, registry)

    else:
        page_range = []

    context_data = {
        'queue_index': queue_index,
        'jobs': jobs_to_dictionary(jobs),
        'num_jobs': num_jobs,
        'page': page,
        'job_status': 'Failed',
    }
    return Response(context_data)


@never_cache
@staff_member_required
@api_view(['GET'])
@schema(None)
def scheduled_jobs(request, queue_index):
    queue_index = int(queue_index)
    queue = get_queue_by_index(queue_index)

    registry = ScheduledJobRegistry(queue.name, queue.connection)

    items_per_page = 100
    num_jobs = len(registry)
    page = int(request.GET.get('page', 1))
    jobs = []

    if num_jobs > 0:
        last_page = int(ceil(num_jobs / items_per_page))
        page_range = range(1, last_page + 1)
        offset = items_per_page * (page - 1)
        job_ids = registry.get_job_ids(offset, offset + items_per_page - 1)

        jobs = get_jobs(queue, job_ids, registry)
        for job in jobs:
            job.scheduled_at = registry.get_scheduled_time(job)

    else:
        page_range = []

    context_data = {
        'queue_index': queue_index,
        'jobs': jobs_to_dictionary(jobs),
        'num_jobs': num_jobs,
        'page': page,
        'job_status': 'Scheduled',
    }
    return Response(context_data)


@never_cache
@staff_member_required
@api_view(['GET'])
@schema(None)
def started_jobs(request, queue_index):
    queue_index = int(queue_index)
    queue = get_queue_by_index(queue_index)

    registry = StartedJobRegistry(queue.name, queue.connection)

    items_per_page = 100
    num_jobs = len(registry)
    page = int(request.GET.get('page', 1))
    jobs = []

    if num_jobs > 0:
        last_page = int(ceil(num_jobs / items_per_page))
        page_range = range(1, last_page + 1)
        offset = items_per_page * (page - 1)
        job_ids = registry.get_job_ids(offset, offset + items_per_page - 1)
        jobs = get_jobs(queue, job_ids, registry)

    else:
        page_range = []

    context_data = {
        'queue_index': queue_index,
        'jobs': jobs_to_dictionary(jobs),
        'num_jobs': num_jobs,
        'page': page,
        'job_status': 'Started',
    }
    return Response(context_data)


@never_cache
@staff_member_required
@api_view(['GET'])
@schema(None)
def workers(request, queue_index):
    queue_index = int(queue_index)
    queue = get_queue_by_index(queue_index)
    clean_worker_registry(queue)
    all_workers = Worker.all(queue.connection)
    workers = [worker for worker in all_workers
               if queue.name in worker.queue_names()]

    context_data = {
        'queue_index': queue_index,
        'workers': worker_to_json(workers),
    }

    return Response(context_data)


def worker_to_json(workers):
    WORKERS = []
    for worker in workers:
        if isinstance(worker, Worker):
            WORKERS.append(
                {
                    "name": worker.name,
                    "total_working_time": worker.total_working_time,
                    "queues": worker.queue_names(),
                    "state": worker.get_state(),
                    "failed_job_count": worker.failed_job_count,
                    "successful_job_count": worker.successful_job_count,
                    "pid": worker.pid,
                }
            )
    return WORKERS


@never_cache
@staff_member_required
def worker_details(request, queue_index, key):
    queue_index = int(queue_index)
    queue = get_queue_by_index(queue_index)
    worker = Worker.find_by_key(key, connection=queue.connection)
    # Convert microseconds to milliseconds
    worker.total_working_time = worker.total_working_time / 1000

    queue_names = ', '.join(worker.queue_names())

    context_data = {
        **admin.site.each_context(request),
        'queue': queue,
        'queue_index': queue_index,
        'worker': worker,
        'queue_names': queue_names,
        'job': worker.get_current_job(),
        'total_working_time': worker.total_working_time * 1000
    }
    return render(request, 'django_rq/worker_details.html', context_data)


@never_cache
@staff_member_required
@api_view(['GET'])
@schema(None)
def deferred_jobs(request, queue_index):
    queue_index = int(queue_index)
    queue = get_queue_by_index(queue_index)

    registry = DeferredJobRegistry(queue.name, queue.connection)

    items_per_page = 100
    num_jobs = len(registry)
    page = int(request.GET.get('page', 1))
    jobs = []

    if num_jobs > 0:
        last_page = int(ceil(num_jobs / items_per_page))
        page_range = range(1, last_page + 1)
        offset = items_per_page * (page - 1)
        job_ids = registry.get_job_ids(offset, offset + items_per_page - 1)

        for job_id in job_ids:
            try:
                jobs.append(Job.fetch(job_id, connection=queue.connection))
            except NoSuchJobError:
                pass

    else:
        page_range = []

    context_data = {
        'queue_index': queue_index,
        'jobs': jobs_to_dictionary(jobs),
        'num_jobs': num_jobs,
        'page': page,
        'job_status': 'Deferred',
    }
    return Response(context_data)


@never_cache
@staff_member_required
def job_detail(request, queue_index, job_id):
    queue_index = int(queue_index)
    queue = get_queue_by_index(queue_index)
    try:
        job = Job.fetch(job_id, connection=queue.connection)
    except NoSuchJobError:
        raise Http404("Couldn't find job with this ID: %s" % job_id)

    try:
        job.func_name
        data_is_valid = True
    except:
        data_is_valid = False

    context_data = {
        **admin.site.each_context(request),
        'queue_index': queue_index,
        'job': job,
        'dependency_id': job._dependency_id,
        'queue': queue,
        'data_is_valid': data_is_valid
    }
    return render(request, 'django_rq/job_detail.html', context_data)


@never_cache
@api_view(['POST'])
@schema(None)
def delete_job(request):
    print(request.data['queue_id'])
    print(str(request.data['task_ids']))
    args = [
        '--job-ids', request.data['task_ids'],
        '--queue-index', request.data['queue_id']
    ]

    print(args)

    management.call_command('delete_job_bulk', *args)
    return Response(request.data)


@never_cache
@staff_member_required
@api_view(['POST'])
@schema(None)
def requeue_job_view(request, queue_index, job_id):
    queue_index = int(queue_index)
    queue = get_queue_by_index(queue_index)
    job = Job.fetch(job_id, connection=queue.connection)

    if request.method == 'POST':
        requeue_job(job_id, connection=queue.connection)
        messages.info(request, 'You have successfully requeued %s' % job.id)
        return redirect('rq_job_detail', queue_index, job_id)

    context_data = {
        'queue_index': queue_index,
        'job': job_to_dictionary(job),
    }
    return Response(context_data)


@never_cache
@staff_member_required
@api_view(['POST'])
@schema(None)
def clear_queue(request, queue_index):
    queue_index = int(queue_index)
    queue = get_queue_by_index(queue_index)

    if request.method == 'POST':
        try:
            queue.empty()
            messages.info(request, 'You have successfully cleared the queue %s' % queue.name)
        except ResponseError as e:
            if 'EVALSHA' in e.message:
                messages.error(request,
                               'This action is not supported on Redis versions < 2.6.0, please use the bulk delete command instead')
            else:
                raise e
        return redirect('rq_jobs', queue_index)

    context_data = {
        'queue_index': queue_index,
    }
    return Response(context_data)


@never_cache
@staff_member_required
@api_view(['POST'])
@schema(None)
def requeue_all(request, queue_index):
    queue_index = int(queue_index)
    queue = get_queue_by_index(queue_index)
    registry = FailedJobRegistry(queue=queue)

    if request.method == 'POST':
        job_ids = registry.get_job_ids()
        count = 0
        # Confirmation received
        for job_id in job_ids:
            try:
                requeue_job(job_id, connection=queue.connection)
                count += 1
            except NoSuchJobError:
                pass

        messages.info(request, 'You have successfully requeued %d jobs!' % count)
        return redirect('rq_jobs', queue_index)

    context_data = {
        'queue_index': queue_index,
        'total_jobs': len(registry),
    }

    return Response(context_data)


@never_cache
@staff_member_required
def confirm_action(request, queue_index):
    queue_index = int(queue_index)
    queue = get_queue_by_index(queue_index)
    next_url = request.META.get('HTTP_REFERER') or reverse('rq_jobs', args=[queue_index])

    if request.method == 'POST' and request.POST.get('action', False):
        # confirm action
        if request.POST.get('_selected_action', False):
            context_data = {
                **admin.site.each_context(request),
                'queue_index': queue_index,
                'action': request.POST['action'],
                'job_ids': request.POST.getlist('_selected_action'),
                'queue': queue,
                'next_url': next_url,
            }
            return render(request, 'django_rq/confirm_action.html', context_data)

    return redirect(next_url)


@never_cache
@staff_member_required
def actions(request, queue_index):
    queue_index = int(queue_index)
    queue = get_queue_by_index(queue_index)
    next_url = request.POST.get('next_url') or reverse('rq_jobs', args=[queue_index])

    if request.method == 'POST' and request.POST.get('action', False):
        # do confirmed action
        if request.POST.get('job_ids', False):
            job_ids = request.POST.getlist('job_ids')

            if request.POST['action'] == 'delete':
                for job_id in job_ids:
                    job = Job.fetch(job_id, connection=queue.connection)
                    # Remove job id from queue and delete the actual job
                    queue.connection.lrem(queue.key, 0, job.id)
                    job.delete()
                messages.info(request, 'You have successfully deleted %s jobs!' % len(job_ids))
            elif request.POST['action'] == 'requeue':
                for job_id in job_ids:
                    requeue_job(job_id, connection=queue.connection)
                messages.info(request, 'You have successfully requeued %d  jobs!' % len(job_ids))

    return redirect(next_url)


@never_cache
@staff_member_required
def enqueue_job(request, queue_index, job_id):
    """ Enqueue deferred jobs
    """
    queue_index = int(queue_index)
    queue = get_queue_by_index(queue_index)
    job = Job.fetch(job_id, connection=queue.connection)

    if request.method == 'POST':
        queue.enqueue_job(job)

        # Remove job from correct registry if needed
        if job.get_status() == JobStatus.DEFERRED:
            registry = DeferredJobRegistry(queue.name, queue.connection)
            registry.remove(job)
        elif job.get_status() == JobStatus.FINISHED:
            registry = FinishedJobRegistry(queue.name, queue.connection)
            registry.remove(job)

        messages.info(request, 'You have successfully enqueued %s' % job.id)
        return redirect('rq_job_detail', queue_index, job_id)

    context_data = {
        **admin.site.each_context(request),
        'queue_index': queue_index,
        'job': job,
        'queue': queue,
    }
    return render(request, 'django_rq/delete_job.html', context_data)
