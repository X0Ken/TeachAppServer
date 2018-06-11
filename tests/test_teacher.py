import json
import uuid
import copy

from models import Teacher
from tests import TestBase


class TestTeacher(TestBase):
    def count(self):
        session = self.session
        count = session.query(Teacher).count()
        return count

    def add(self, teacher_id):
        session = self.session
        teacher = Teacher(uuid=teacher_id)
        session.add(teacher)
        session.commit()
        teacher = session.query(Teacher).filter_by(uuid=teacher_id).first()
        info = teacher.get_info()
        return info

    def delete(self, teacher_id):
        session = self.session
        teacher = session.query(Teacher).filter_by(uuid=teacher_id).first()
        session.delete(teacher)
        session.commit()

    def test_get(self):
        j_id = uuid.uuid4().hex
        j = self.add(j_id)
        response = self.fetch('/teachers/{}'.format(j['user_id']))
        self.assertEqual(response.code, 200)
        self.assertListEqual(sorted(['create_at', 'gender', 'highest_education', 'method', 'idcard', 'self_evaluate',
                                     'pay', 'region', 'school', 'school_subject', 'subject', 'time', 'user_id']),
                             sorted(json.loads(response.body)['teacher'].keys()))
        self.delete(json.loads(response.body)['teacher']['user_id'])

    def test_list(self):
        count = self.count()
        response = self.fetch('/teachers')
        self.assertEqual(response.code, 200)
        self.assertEqual(len(json.loads(response.body)['teachers']), count)

    def test_add(self):
        user = self.add_user()
        req_body = {
            "teacher": {
                "idcard": "Value",
                "method": "Value",
                "gender": "Value",
                "school": "Value",
                "school_subject": "Value",
                "highest_education": "Value",
                "pay": "Value",
                "region": "Value",
                "subject": "Value",
                "time": "Value",
                "self_evaluate": "Value",
            }
        }
        res_body = copy.deepcopy(req_body)
        res_body['teacher']['user_id'] = 'id'
        res_body['teacher']['create_at'] = 'create_at'
        response = self.fetch('/teachers', method="POST",
                              body=json.dumps(req_body),
                              headers={"token-id": user['token_id']})
        self.assertEqual(response.code, 200)
        print(response.body)
        self.assertListEqual(sorted(res_body['teacher'].keys()),
                             sorted(json.loads(response.body)['teacher'].keys()))
        self.delete(json.loads(response.body)['teacher']['user_id'])
