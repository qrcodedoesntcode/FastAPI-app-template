#!/usr/bin/env python
import base64
import datetime
import os.path
import sys
import uuid

from jose.constants import ALGORITHMS

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from jose import jwt

from app.core.config import settings

if __name__ == "__main__":
    jwt_secret = base64.urlsafe_b64decode(settings.JWT_KEY)

    token = jwt.encode({
        "sub": "antoine",
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1),
    }, jwt_secret, ALGORITHMS.HS384)
    print(token)
