"""Librarian Edits
"""

import re
import json
import web

from openlibrary import accounts
from openlibrary.core.edits import CommunityEditsQueue
from infogami.utils import delegate
from infogami.utils.view import render_template


class community_edits_queue(delegate.page):
    path = '/pendingchanges'

    def POST(self):
        i = web.input(work_ids="", rtype="merge-works", comment=None)
        user = accounts.get_current_user()
        username = user['key'].split('/')[-1]
        if i.rtype == "merge-works":
            # normalization
            work_ids = [w for w in re.split("[ ,]", i.work_ids.replace("/works/", "")) if w]
            result = CommunityEditsQueue.submit_work_merge_request(
                work_ids,
                submitter=username,
                comment=i.comment
            )
            return delegate.RawText(json.dumps(result), content_type="application/json")

    def GET(self):
        i = web.input(page=1)
        user = web.ctx.site.get_user()
        if user:
            requests = CommunityEditsQueue.get_requests(page=i.page)
            return render_template('pendingchanges', requests=requests)


def setup():
    pass