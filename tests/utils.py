"""Utilities for testing"""

def get_queued_jobs(redis_client, queue='default'):
    """Get the list of jobs queued for a fakeredis rq client"""
    lrange = redis_client.lrange('rq:queue:%s' % queue, 0, -1)
    return [redis_client.hgetall('rq:job:%s' % uuid)['description'] for uuid in lrange]
