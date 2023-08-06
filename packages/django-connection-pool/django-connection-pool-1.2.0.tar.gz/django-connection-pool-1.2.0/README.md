# README

## settings

```python

{
    'pool_class': 'django_connection_pool.mysql.DjangoQueuePool',  # customized from sqlalchemy queue pool
    'reset_on_return': True,  # reset by rollback only when necessary
    'core_pool_size': 5,  # retire no conn if achieving core size
    'unload_timeout': 2,  # wait some random time before overload
    'retire_interval': 5,  # retire few non-core conn per interval
    'retire_quantity': 1,  # retire few non-core conn per interval
    'show_status': 'show_status',
    'show_status_interval': 'show_status_interval',
    'pool_size': 30,  # daily traffic: recycle or retire conn
    'max_overflow': 0,  # burst traffic: put overflow into pool
    'timeout': 30,  # burst traffic: > external api timeout
    'recycle': 3600,  # to be much smaller than mysql timeout
    'dialect': None,  # sqlalchemy's mysql dialect instance
    'pre_ping': False,  # sqlalchemy pre ping requires dialect
    'reset_on_return': None,  # do not use sqlalchemy reset on return
}

```