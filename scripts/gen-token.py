#!/usr/bin/env python
import datetime
import os.path
import sys
import uuid

from jose.constants import ALGORITHMS

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from jose import jwt

from app.core.config import settings

if __name__ == "__main__":
    token = jwt.encode({
        "iat": datetime.datetime.utcnow(),
        "nbf": datetime.datetime.utcnow(),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1),
        "sub": "", # Empty for now
        "jti": str(uuid.uuid4())
    }, settings.JWT_SECRET, ALGORITHMS.HS384)
    print(token)
