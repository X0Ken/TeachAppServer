import json
import uuid
import copy

from models import Job
from tests import TestBase


class TestJob(TestBase):
    def count(self):
        session = self.session
        count = session.query(Job).count()
        return count

    def add(self, job_id):
        session = self.session
        job = Job(uuid=job_id)
        session.add(job)
        session.commit()
        job = session.query(Job).filter_by(uuid=job_id).first()
        info = job.get_info()
        return info

    def delete(self, job_id):
        session = self.session
        job = session.query(Job).filter_by(uuid=job_id).first()
        session.delete(job)
        session.commit()

    def test_get(self):
        j_id = uuid.uuid4().hex
        j = self.add(j_id)
        response = self.fetch('/jobs/{}'.format(j['id']))
        self.assertEqual(response.code, 200)
        self.assertListEqual(sorted(['create_at', 'gender', 'highest_education', 'id', 'method',
                                     'pay', 'region', 'school', 'subject', 'time']),
                             sorted(json.loads(response.body)['job'].keys()))
        self.delete(json.loads(response.body)['job']['id'])

    def test_list(self):
        count = self.count()
        response = self.fetch('/jobs')
        self.assertEqual(response.code, 200)
        self.assertEqual(len(json.loads(response.body)['jobs']), count)

    def test_add(self):
        req_body = {
            "job": {
                'gender': "a",
                'highest_education': "ed",
                'method': "",
                'pay': "",
                'region': "",
                'school': "",
                'subject': "",
                'time': ""
            }
        }
        res_body = copy.deepcopy(req_body)
        res_body['job']['id'] = 'id'
        res_body['job']['create_at'] = 'create_at'
        response = self.fetch('/jobs', method="POST",
                              body=json.dumps(req_body))
        self.assertEqual(response.code, 200)
        print(response.body)
        self.assertListEqual(sorted(res_body['job'].keys()),
                             sorted(json.loads(response.body)['job'].keys()))
        self.delete(json.loads(response.body)['job']['id'])
