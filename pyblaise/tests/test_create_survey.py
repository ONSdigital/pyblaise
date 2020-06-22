from pyblaise import (create_survey_manifest,
                      create_survey_from_existing)

def test_create_survey_manifest_returns_manifest():
  x, _ = create_survey_manifest("dummy")
  assert x is not None
  assert len(x) > 2


def test_create_survey_manifest_returns_uuid():
  import re
  _, id = create_survey_manifest("dummy")
  assert id is not None
  assert re.match(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", id) is not None


def test_create_survey_manifest_contains_name():
  from time import time
  from hashlib import md5
  r = md5(str(time()).encode()).hexdigest()
  manifest, _ = create_survey_manifest(r)
  assert r in manifest
