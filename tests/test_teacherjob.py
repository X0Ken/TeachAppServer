import json
import uuid
import copy

from models import TeacherJob
from tests import TestBase


class TestJob(TestBase):
    def count(self):
        session = self.session
        count = session.query(TeacherJob).count()
        return count

    def add(self, job_id):
        session = self.session
        job = TeacherJob(uuid=job_id)
        session.add(job)
        session.commit()
        job = session.query(TeacherJob).filter_by(uuid=job_id).first()
        info = job.get_info()
        return info

    def delete(self, job_id):
        session = self.session
        job = session.query(TeacherJob).filter_by(uuid=job_id).first()
        session.delete(job)
        session.commit()

    def test_get(self):
        j_id = uuid.uuid4().hex
        j = self.add(j_id)
        response = self.fetch('/teacherjobs/{}'.format(j['id']))
        self.assertEqual(response.code, 200)
        self.assertListEqual(sorted(['create_at', 'gender', 'highest_education', 'id', 'method',
                                     'pay', 'region', 'school', 'subject', 'time', 'offer_user_id']),
                             sorted(json.loads(response.body)['teacherjob'].keys()))
        self.delete(json.loads(response.body)['teacherjob']['id'])

    def test_list(self):
        count = self.count()
        response = self.fetch('/teacherjobs')
        self.assertEqual(response.code, 200)
        self.assertEqual(len(json.loads(response.body)['teacherjobs']), count)

    def test_add(self):
        user = self.add_user()
        req_body = {
            "teacherjob": {
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
        res_body['teacherjob']['id'] = 'id'
        res_body['teacherjob']['create_at'] = 'create_at'
        res_body['teacherjob']['offer_user_id'] = 'offer_user_id'
        response = self.fetch('/teacherjobs', method="POST",
                              body=json.dumps(req_body),
                              headers={"token-id": user['token_id']})
        self.assertEqual(response.code, 200)
        print(response.body)
        self.assertListEqual(sorted(res_body['teacherjob'].keys()),
                             sorted(json.loads(response.body)['teacherjob'].keys()))
        self.delete(json.loads(response.body)['teacherjob']['id'])
