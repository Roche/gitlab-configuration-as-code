.. _license:

#######
License
#######

**Only for Enterprise Edition or gitlab.com. FOSS/Community Edition instance will fail when trying to configure license**

*GCasC* offers a way to manage your GitLab instance licenses. The clue is that despite license is just a single file,
you need to configure other properties of license so *GCasC* do not upload new (but already used) license with every
execution. That way it is able to recognize that exactly the same license is already in use and skips uploading new one.
Otherwise you could end with very long license history.

**Reference:** https://docs.gitlab.com/12.4/ee/api/license.html

Properties
==========

| **Property**         | **Description**                                                                      | **Example**             |
|----------------------|--------------------------------------------------------------------------------------|-------------------------|
| ``license.starts_at``  | Date in format yyyy-MM-dd when license starts                                        | ``2019-11-21``            |
| ``license.expires_at`` | Date in format yyyy-MM-dd when license ends                                          | ``2019-12-21``            |
| ``license.plan``       | Plan of your GitLab instance license. Valid values: ``starter``, ``premium``, ``ultimate`` | ``premium``               |
| ``license.user_limit`` | Number of licensed users                                                             | ``120``                   |
| ``license.data``       | Content of your license file that you received from GitLab sales                     | ``azhxWFZqb1BsrTVxug...`` |

**Important!** Beware of storing your license in ``data`` field directly as text. This is insecure and may lead
to leakage of your license. Use ``!env`` or ``!include`` directives to inject license to ``license.data`` field securely from
external source. Also keep your license file itself safe and secure!

Examples
========

Full license configuration::

    license:
        starts_at: 2019-11-17
        expires_at: 2019-12-17
        plan: starter
        user_limit: 30
        data: |
            azhxWFZqbk1BOUsrTVxug6AdfzIzWXI1WUVsdWNKRk53V2hiV1FlTUN2TTRS
            NkhSVFFhZ3hCajd4bGlLMkhhcUxhd1EySHh2TjJTXG40U3ZNUWM0ZzhqYTE5
            T1lcbkJnNERFOVBORkpxK3FsaHZxNFFVSG9GL0NEWWF0elkyOE9SUE41Ny9v
            ...

Injecting license data from external file::

    license:
        starts_at: 2019-11-17
        expires_at: 2019-12-17
        plan: premium
        user_limit: 30
        data: !include /etc/gitlab/my_gitlab_license.lic

Injecting license data from environment variable::

    license:
        starts_at: 2019-11-17
        expires_at: 2019-12-17
        plan: ultimate
        user_limit: 30
        data: !env GITLAB_LICENSE

