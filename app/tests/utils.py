from datetime import datetime, timedelta

import jwt


def generate_test_access_token(user_id: str) -> str:
    payload = {"exp": datetime.now() + timedelta(days=30), "sub": user_id}
    secret_key = "CHANGE THIS IN PRODUCTION"
    return jwt.encode(payload, secret_key, algorithm="HS256")
