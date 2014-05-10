import json
from devmine.app.models.feature import Feature
from devmine.app.controllers.application_controller import (
    ApplicationController
)
from devmine.app.helpers import application_helper as ah


class FeaturesController(ApplicationController):
    """Class for handling requests on the feature resource."""

    def by_category(self, db):
        """Return all features sorted by category as a JSON string
        like the following:
            {'category1': ['feature1': {...}, ...], 'category2': [...]}
        """
        features = db.query(Feature).order_by(
            Feature.category, Feature.name).all()

        if len(features) == 0:
            return ""

        retval = {}
        for f in features:
            if f.category not in retval:
                retval[f.category] = []
            retval[f.category].append(ah.obj_to_json(f))

        return json.dumps(retval)