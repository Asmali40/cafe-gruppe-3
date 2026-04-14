# Copyright (C) 2023 - present Juergen Zimmermann, Hochschule Karlsruhe
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# Aufruf:   uvx locust -f .\tests\lasttest\locustfile.py

#           http://localhost:8089
#           z.B. $env:LOGURU_LEVEL = 'INFO'
#                export LOGURU_LEVEL='INFO'
#           Number of users: 50
#           Ramp Up (users started/second): 5
#           Host: https://localhost:8000

"""Lasttest mit Locust für Cafe."""

from typing import Final, Literal

import urllib3
from locust import HttpUser, constant_throughput, task

# https://stackoverflow.com/questions/27981545/suppress-insecurerequestwarning-unverified-https-request-is-being-made-in-pytho#answer-44615889
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# https://docs.locust.io/en/stable/api.html#httpuser-class
class GetUser(HttpUser):
    """Lasttest für GET-Requests (Cafe)."""

    # https://docs.locust.io/en/stable/writing-a-locustfile.html#wait-time-attribute
    # https://docs.locust.io/en/stable/api.html#locust.User.wait_time
    # https://docs.locust.io/en/stable/api.html#locust.wait_time.constant_throughput
    # 50 "Task Iterations" pro Sekunde
    wait_time = constant_throughput(0.1)
    MIN_USERS: Final = 500
    MAX_USERS: Final = 500

    # https://docs.locust.io/en/stable/writing-a-locustfile.html#on-start-and-on-stop-methods
    def on_start(self) -> None:
        """JWT holen und Header setzen."""
        self.client.verify = False

        # https://docs.locust.io/en/stable/api.html#httpsession-class
        # https://docs.locust.io/en/stable/api.html#response-class
        # https://requests.readthedocs.io/en/latest/api#requests.Response
        response: Final = self.client.post(
            url="/auth/token",
            json={"username": "admin", "password": "p"},
        )

        body: Final[dict[Literal["token"], str]] = response.json()
        token: Final = body["token"]

        self.client.headers = {"Authorization": f"Bearer {token}"}

    @task(100)
    def get_id(self) -> None:
        """GET /cafe/{id}."""
        for cafe_id in [1, 20, 30, 40, 50, 60]:
            response = self.client.get(f"/rest/{cafe_id}")
            print(f"{response.json()['id']}")

    @task(200)
    def get_name(self) -> None:
        """GET mit name Query."""
        for teil in ["cafe", "berlin", "munich", "ham"]:
            self.client.get("/rest", params={"name": teil})

    @task(150)
    def get_email(self) -> None:
        """GET mit email Query."""
        for email in [
            "admin@cafe.com",
            "cafeberlin@cafe.de",
            "cafemunich@cafe.de",
            "cafehamburg@cafe.de",
            "cologne@cafe.de",
            "frankfurt@cafe.de",
        ]:
            self.client.get("/rest", params={"email": email})
