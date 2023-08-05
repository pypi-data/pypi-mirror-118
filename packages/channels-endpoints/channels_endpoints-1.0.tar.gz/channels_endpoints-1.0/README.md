# Django channels endpoints

This package provides endpoints as functions for 
[django-channels](https://github.com/django/channels)
package. Like this:

```python
from channels_endpoints.main import endpoint, Response
from django.contrib.auth.models import User
users_logger = logging.getLogger('users')


@endpoint(logger=users_logger, permissions=[UsersPermissions], timeout=42)
async def get_users(request):
    def _get():
        return User.objects.all()
    return Response(
        request,
        await sync_to_async(_get)()
    )
```

# Installation

```shell
pip install channels-endpoints
```

# Usage

See django project example [chat_project](https://github.com/avigmati/chat_project)