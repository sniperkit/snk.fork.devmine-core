"""This file provides abstraction over the source of data used in the server"""

import random
import json
import datetime


class DataSource:
    """This class abstracts the underlying system that stores the computed
    features about the developers"""
    def __init__(self):
        pass


class RandomData(DataSource):
    def __init__(self, seed=None):
        r = random.Random(seed)
        #print(r.random())

        self.scores = {}
        self.features = ['Python', 'Cookies', 'Chocolate',
                         'Superpowers', 'Doge']
        self.developers = ['Robin', 'Kevin', 'Laurent', 'Xuan',
                           'Frederik', 'Daniel', 'Clément']

        for developer in self.developers:
            scores = {}
            for feature in self.features:
                scores[feature] = r.random()
            self.scores[developer] = scores


class JsonData(DataSource):
    def __init__(self, dev_file, repo_file):

        devs = json.load(open(dev_file))
        repos = json.load(open(repo_file))

        self.developers = []
        self.scores = {}

        for dev in devs:
            dev_repos = [repo for repo in repos
                         if repo['owner']['login'] == dev['login']]

            self.developers.append(dev['login'])
            self.scores[dev['login']] = self.compute_scores(dev, dev_repos)

        # Compute the list of features
        self.features = []
        for v in self.scores.values():
            for k in v.keys():
                self.features.append(k)

    def compute_scores(self, dev, repos):
        score = {}

        score['followers'] = dev['followers']
        score['public_repos'] = dev['public_repos']

        created = datetime.datetime.strptime(dev['created_at'],
                                             "%Y-%m-%dT%H:%M:%SZ")
        updated = datetime.datetime.strptime(dev['updated_at'],
                                             "%Y-%m-%dT%H:%M:%SZ")
        score['created_at'] = int(created.timestamp())
        score['updated_at'] = int(updated.timestamp())

        score['number_languages'] = 0

        for repo in repos:
            if repo['language'] is not None:
                if repo['language'] in score.keys():
                    score[repo['language']] += int(repo['size'])
                else:
                    score['number_languages'] += 1
                    score[repo['language']] = int(repo['size'])

        return score