# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['auth_framework',
 'auth_framework.backends',
 'auth_framework.migrations',
 'auth_framework.oauth',
 'auth_framework.serializers',
 'auth_framework.signals',
 'auth_framework.social',
 'auth_framework.social.providers',
 'auth_framework.social.providers.apple',
 'auth_framework.social.providers.facebook',
 'auth_framework.social.providers.google',
 'auth_framework.views']

package_data = \
{'': ['*'], 'auth_framework': ['templates/auth/*']}

install_requires = \
['django-oauth-toolkit>=1.5.0,<2.0.0',
 'django>=2.2.0',
 'djangorestframework>=3,<4',
 'requests']

setup_kwargs = {
    'name': 'django-auth-framework',
    'version': '1.0.2',
    'description': 'An open source, one-stop authentication framework for Django and ready for production.',
    'long_description': '\n[![Contributors][contributors-shield]][contributors-url]\n\n[comment]: <> ([![Forks][forks-shield]][forks-url])\n\n[comment]: <> ([![Stargazers][stars-shield]][stars-url])\n[![Issues][issues-shield]][issues-url]\n\n\n\n<br />\n<p align="center">\n\n  <h3 align="center">Django Auth Framework</h3>\n\n  <p align="center">\n    An open source, one-stop authentication framework for Django and ready for production.\n  </p>\n</p>\n\n\n\n<!-- TABLE OF CONTENTS -->\n<details open="open">\n  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>\n  <ol>\n    <li>\n      <a href="#about-the-project">About The Project</a>\n      <ul>\n        <li><a href="#built-with">Built With</a></li>\n        <li><a href="#features">Features</a></li>\n      </ul>\n    </li>\n    <li>\n      <a href="#getting-started">Getting Started</a>\n      <ul>\n        <li><a href="#prerequisites">Prerequisites</a></li>\n        <li><a href="#installation">Installation</a></li>\n      </ul>\n    </li>\n    <li><a href="#api-endpoints-and-examples">API Endpoints and Examples</a></li>\n    <li><a href="#license">License</a></li>\n  </ol>\n</details>\n\n\n\n<!-- ABOUT THE PROJECT -->\n## About The Project\nDjango Auth Framework is an open source, one-stop framework for Django applications providing the most essential APIs for \nauthentication and authorization. APIs also cover Oauth2 protocol, social login and user management with options allows \nto easily customize and override for working on most scenarios. It supports multiple\nauthentication ways to make your auth server scalable from a monolithic server using Token/Session authentication to\nservice mesh such like [Istio](https://istio.io/latest/docs/tasks/security/authorization/authz-jwt/) on Kubernetes Cluster with JWT authentication.\n\nThis framework was originally developed by me to help\nDjango projects in our company fast setup. Now, it has scaled our service over a million users. I am \nhappy to open soucre this project, hope it is helpful in your projects or startups\n\n### Built With\n\n* [Django OAuth Toolkit](https://github.com/jazzband/django-oauth-toolkit)\n* [Django REST framework](https://github.com/encode/django-rest-framework)\n\n### Features\n* Production-ready, optimized by reducing unnecessary queries write to db during authentication and authorization.\n* Extends [Django OAuth Toolkit\'s](https://github.com/jazzband/django-oauth-toolkit) default `Oauth2Validator` to allow\n  authorization with multiple types of credentials like email, phone number.\n* Pure RESTFUL API endpoints implemented with [Django REST framework](https://github.com/encode/django-rest-framework),\n  the framework doesn\'t contain or use any traditional Django components(eg: forms, html).\n* Supports the most popular social login(Google,Apple and Facebook) followed by up to date guidelines, users at frontend\n  can be authorized by either id_token, code or access_token.  \n* **NO FULL DOCUMENTATION** atm.\n\n<!-- GETTING STARTED -->\n## Getting Started\n\nTo get a local copy up and running follow these simple steps.\n\n### Installation\n\n  ```sh\n  pip install django-auth-framework\n  ```\n\n### Configurations\n1. Edit `settings.py` file:\n   \n   ```python\n    #in your my_auth/models.py\n     # from auth_framework.models import AbstractUser\n     # class MyUser(AbstractUser):\n     #     custom_fields ...\n    AUTH_USER_MODEL = \'my_auth.MyUser\'\n   ```\n   or just try with\n   ```python\n    AUTH_USER_MODEL = \'auth_framework.User\'\n   ```\n   add required apps and configuration for rest_framework:\n   ```python\n   # ...\n   REQUIRED_APPS = [\n        \'rest_framework\',\n        \'oauth2_provider\',\n        \'auth_framework\',\n    ]\n   LOCAL_APPS = [\n        \'my_auth\'\n   ]\n    INSTALLED_APPS += REQUIRED_APPS\n    INSTALLED_APPS += LOCAL_APPS\n    # ...\n    REST_FRAMEWORK = {\n    \'DEFAULT_AUTHENTICATION_CLASSES\': (\n        \'oauth2_provider.contrib.rest_framework.OAuth2Authentication\',\n        \'rest_framework.authentication.SessionAuthentication\',\n\n    ),\n    }\n    ```\n   if you need other unique fields: `email` or `phone_number` not just`username`as credentials:\n   ```python\n    AUTHENTICATION_BACKENDS = [\n        "auth_framework.backends.auth_backends.AuthenticationBackend",\n    ]\n    \n    OAUTH2_PROVIDER = {\n        "OIDC_ENABLED": True,\n        "OIDC_RSA_PRIVATE_KEY": os.environ.get(\'OIDC_RSA_PRIVATE_KEY\'),\n        \'SCOPES\': {\n            "openid": "OpenID Connect scope",\n            \'read\': \'Read scope\',\n            \'write\': \'Write scope\',\n        },\n        \'OAUTH2_VALIDATOR_CLASS\': \'auth_framework.oauth.oauth2_validators.OauthValidator\',\n        \'OAUTH2_BACKEND_CLASS\': \'auth_framework.oauth.oauth2_backends.OAuthLibCore\',\n    }\n    ```\n2. Edit the `urls.py`:\n   ```python\n    from django.contrib import admin\n    from django.urls import path, include\n    \n    urlpatterns = [\n        path(\'admin/\', admin.site.urls),\n        path(\'account/\', include(\'auth_framework.urls\'))\n    ]\n    \n    ```\n3. Sync Database and createsuperuser:\n    ```sh\n   python manage.py migrate\n   python manage.py createsuperuser\n   ```\n4. Login to the admin page http://localhost:8000/admin/oauth2_provider/application/add/\n   and add a default `Application`. if it\'s only open to your first party apps, then just choose `Resource owner password-based`\n   as the grant type (No one likes to login with password but still having a redirect web page on a native app)\n\n\n\n\n<!-- API Endpoints and Examples -->\n## API Endpoints and Examples\n \n\n\n<!-- CONTRIBUTING -->\n## Contributing\n\nContributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.\n\n1. Fork the Project\n2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)\n3. Commit your Changes (`git commit -m \'Add some AmazingFeature\'`)\n4. Push to the Branch (`git push origin feature/AmazingFeature`)\n5. Open a Pull Request\n\n\n\n<!-- LICENSE -->\n## License\n\nDistributed under the BSD License. See `LICENSE` for more information.\n\n\n\n<!-- CONTACT -->\n## Contact\n\nEdward C. - edwardc@acrossor.com\n\nProject Link: [https://github.com/DrChai/django-auth-framework](https://github.com/DrChai/django-auth-framework)\n\n\n\n\n\n<!-- MARKDOWN LINKS & IMAGES -->\n<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->\n[contributors-shield]: https://img.shields.io/github/contributors/DrChai/repo.svg?style=for-the-badge\n[contributors-url]: https://github.com/DrChai/django-auth-framework/graphs/contributors\n[forks-shield]: https://img.shields.io/github/forks/DrChai/repo.svg?style=for-the-badge\n[forks-url]: https://github.com/DrChai/django-auth-framework/network/members\n[stars-shield]: https://img.shields.io/github/stars/DrChai/repo.svg?style=for-the-badge\n[stars-url]: https://github.com/DrChai/django-auth-framework/stargazers\n[issues-shield]: https://img.shields.io/github/issues/DrChai/repo.svg?style=for-the-badge\n[issues-url]: https://github.com/DrChai/django-auth-framework/issues\n[license-shield]: https://img.shields.io/github/license/DrChai/repo.svg?style=for-the-badge\n[license-url]: https://github.com/DrChai/django-auth-framework/blob/master/LICENSE.txt\n',
    'author': 'Edward Chai',
    'author_email': 'edwardc@acrossor.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/DrChai/django-auth-framework',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
