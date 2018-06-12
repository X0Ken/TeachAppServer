import json
import uuid
import copy

from models import Question
from tests import TestBase


class TestQuestion(TestBase):
    def get_count(self):
        session = self.session
        count = session.query(Question).count()
        return count

    def add(self, quesion_id):
        session = self.session
        q = Question(uuid=quesion_id)
        info = q.get_info()
        session.add(q)
        session.commit()
        return info

    def delete(self, question_id):
        session = self.session
        q = session.query(Question).filter_by(uuid=question_id).first()
        session.delete(q)
        session.commit()

    def test_list(self):
        count = self.get_count()
        response = self.fetch('/questions')
        self.assertEqual(response.code, 200)
        self.assertEqual(len(json.loads(response.body)['questions']), count)

    def test_add(self):
        req_body = {
            "question": {
                "keywords": "keywords",
                "context": 'context',
                "pay": 'pay',
            }
        }
        res_body = copy.deepcopy(req_body)
        res_body['question']['id'] = 'id'
        response = self.fetch('/questions', method="POST",
                              body=json.dumps(req_body))
        self.assertEqual(response.code, 200)
        self.assertListEqual(sorted(res_body['question'].keys()),
                             sorted(json.loads(response.body)['question'].keys()))
        self.delete(json.loads(response.body)['question']['id'])

    def test_get(self):
        q_id = uuid.uuid4().hex
        q = self.add(q_id)
        print(q)
        response = self.fetch('/questions/{}'.format(q['id']))
        self.assertEqual(response.code, 200)
        self.assertListEqual(sorted(['keywords', 'id', 'context', 'pay']),
                             sorted(json.loads(response.body)['question'].keys()))
        self.delete(json.loads(response.body)['question']['id'])
