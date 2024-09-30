# Copyright 2013 Red Hat, Inc.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import pecan
from urllib.parse import urljoin
from wsme import types as wtypes

from magnum.api.controllers import base


def build_url(resource, resource_args, bookmark=False, base_url=None):
    if base_url is None:
        base_url = urljoin(pecan.request.host_url, pecan.request.path)

    if bookmark:
        url = urljoin(base_url, resource)
    else:
        url = urljoin(base_url, 'v1/%s' % resource)

    # FIXME(lucasagomes): I'm getting a 404 when doing a GET on
    # a nested resource that the URL ends with a  '/'.
    # https://groups.google.com/forum/#!topic/pecan-dev/QfSeviLg5qs
    if resource_args.startswith('?'):
         url += resource_args
    else:
        url = urljoin(url, resource_args)

    return url


class Link(base.APIBase):
    """A link representation."""

    href = wtypes.text
    """The url of a link."""

    rel = wtypes.text
    """The name of a link."""

    type = wtypes.text
    """Indicates the type of document/link."""

    @staticmethod
    def make_link(rel_name, url, resource, resource_args,
                  bookmark=False, type=wtypes.Unset):
        href = build_url(resource, resource_args,
                         bookmark=bookmark, base_url=url)
        return Link(href=href, rel=rel_name, type=type)

    @classmethod
    def sample(cls):
        sample = cls(href="http://localhost:9511/clusters/"
                          "eaaca217-e7d8-47b4-bb41-3f99f20eed89",
                     rel="bookmark")
        return sample
