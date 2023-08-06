import redis
from data_verifier.utils.persist_cookies import PersistCookies
from data_verifier.model.rm_model import RMLoginManager
from data_verifier.identities.rm_internships.jobs.job_list import RMJobs


class RMApplication(RMJobs):
    application_url = "https://rm.dtu.ac.in/api/application/myApplications"
    progress_url = 'https://rm.dtu.ac.in/api/company/progressPost?jobId={}'

    def __init__(self, to_verify, **kwargs):
        super().__init__(to_verify, **kwargs)
        self.applications = []
        self.applied_job_ids = []
        self.notif = self.safe_dict(kwargs, 'notif', False)
        self.alert = self.safe_dict(kwargs, 'alert', False)
        self.get_jobs()

    def jobs_query(self):
        response = self.smart_request('GET', self.application_url, headers=self.headers)
        json = self.safe_json(response)

        return self.extract_jobs(json.get('data'))

    def extract_jobs(self, jobs):
        for i in jobs:
            self.applied_job_ids.append(i.get('post').get('_id'))

        if self.alert:
            for i in self.job_filter_list:
                if i.get('_id') in self.applied_job_ids and not 0 < i.get('seconds') < 3600:
                    self.job_filter_list.pop(self.job_filter_list.index(i))

            return self.job_filter_list

        if self.notif:
            nofifi = dict()
            for i in self.notifications:
                if i.get('jobPost') in self.applied_job_ids:
                    response = self.smart_request('GET', self.progress_url.format(i.get('jobPost')),
                                                  headers=self.headers)
                    if response.ok:
                        nofifi[i.get('jobPost')] = self.safe_json(response).get('data', [])

            return nofifi

        applied_jobs = []
        for i in self.jobs:
            if i.get('_id') in self.applied_job_ids:
                i['status'] = jobs[self.applied_job_ids.index(i.get('_id'))].get('status')
                applied_jobs.append(i)

        return applied_jobs

    @classmethod
    def extract_data(cls, db_ob, **kwargs):
        return cls(db_ob, **kwargs).jobs_query()


def test():
    applicant = RMLoginManager()
    applicant.username = '2K19/ME/051'
    applicant.password = 'April@2000'

    r = redis.StrictRedis()

    persistor = PersistCookies(r, 'api-manager-verifier:{}'.format(applicant.username.replace('/', '_')))

    return RMApplication.extract_data(applicant, persistor=persistor,alert=True)


if __name__ == '__main__':
    print(test())
