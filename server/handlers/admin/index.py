import json
import uuid
from datetime import datetime
from datetime import timedelta

import sqlalchemy as sa
from tornado.gen import coroutine

from server.handlers.admin.base import BaseAdminHandler
from server.handlers.admin.base import admin_require
from server.models import Question
from server.models import TeacherJob
from server.models import User
from server.models import UserInfo


class IndexHandler(BaseAdminHandler):

    def last_7_date_user_growth(self, kwargs):
        session = self.session
        now = datetime.now()
        dates = [(now - timedelta(days=d)).strftime('%Y-%m-%d') for d in
                 range(7, 0, -1)]
        user_growth_labels = [(now - timedelta(days=d)).strftime('%d') for d in
                              range(7, 0, -1)]

        user_data = session.query(sa.func.DATE_FORMAT(User.create_at, '%d'),
                                  sa.func.count(User.id)).filter(
            sa.func.DATE_FORMAT(User.create_at, '%Y-%m-%d').in_(dates)
        ).group_by(
            sa.func.DATE_FORMAT(User.create_at, '%d')).all()

        user_growth_data = []
        user_data = {u[0]: u[1] for u in user_data}

        for d in user_growth_labels:
            user_growth_data.append(user_data.get(d, 0))
        kwargs.update(
            user_growth_labels=user_growth_labels,
            user_growth_data=user_growth_data,
        )

    def last_7_date_question_growth(self, kwargs):
        session = self.session
        now = datetime.now()
        dates = [(now - timedelta(days=d)).strftime('%Y-%m-%d') for d in
                 range(7, 0, -1)]
        question_growth_labels = [(now - timedelta(days=d)).strftime('%d')
                                  for d in range(7, 0, -1)]

        question_data = session.query(sa.func.DATE_FORMAT(Question.create_at, '%d'),
                                  sa.func.count(Question.id)).filter(
            sa.func.DATE_FORMAT(Question.create_at, '%Y-%m-%d').in_(dates)
        ).group_by(
            sa.func.DATE_FORMAT(Question.create_at, '%d')).all()

        question_growth_data = []
        question_data = {u[0]: u[1] for u in question_data}

        for d in question_growth_labels:
            question_growth_data.append(question_data.get(d, 0))
        kwargs.update(
            question_growth_labels=question_growth_labels,
            question_growth_data=question_growth_data,
        )

    def last_7_date_job_growth(self, kwargs):
        session = self.session
        now = datetime.now()
        dates = [(now - timedelta(days=d)).strftime('%Y-%m-%d') for d in
                 range(7, 0, -1)]
        job_growth_labels = [(now - timedelta(days=d)).strftime('%d') for d in
                              range(7, 0, -1)]

        job_data = session.query(sa.func.DATE_FORMAT(TeacherJob.create_at, '%d'),
                                  sa.func.count(TeacherJob.id)).filter(
            sa.func.DATE_FORMAT(TeacherJob.create_at, '%Y-%m-%d').in_(dates)
        ).group_by(
            sa.func.DATE_FORMAT(TeacherJob.create_at, '%d')).all()

        job_growth_data = []
        job_data = {u[0]: u[1] for u in job_data}

        for d in job_growth_labels:
            job_growth_data.append(job_data.get(d, 0))
        kwargs.update(
            job_growth_labels=job_growth_labels,
            job_growth_data=job_growth_data,
        )

    def user_top_edu(self, kwargs):
        session = self.session
        info = session.query(
            UserInfo.education, sa.func.count(UserInfo.id)
        ).group_by(UserInfo.education)
        data = {}
        for e, c in info:
            data[e] = c
        kwargs.update(
            data=data,
        )


    @coroutine
    @admin_require
    def get(self):
        kwargs = {}
        self.last_7_date_user_growth(kwargs)
        self.last_7_date_question_growth(kwargs)
        self.last_7_date_job_growth(kwargs)

        self.render(
            "index/index.html",
            **kwargs
        )
