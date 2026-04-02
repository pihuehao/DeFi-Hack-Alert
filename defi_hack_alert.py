# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

from genlayer import *

import json
import typing


class DeFiHackAlert(gl.Contract):
    has_scanned: bool
    threat_level: str
    latest_hack: str
    analysis: str
    param: str

    def __init__(self, param: str):
        self.has_scanned = False
        self.threat_level = "LOW"
        self.latest_hack = "none"
        self.analysis = "Awaiting scan"
        self.param = param

    @gl.public.write
    def scan_hacks(self) -> typing.Any:

        if self.has_scanned:
            return "Already scanned"

        def nondet() -> str:
            fng = gl.nondet.web.render("https://alternative.me/crypto/fear-and-greed-index/", mode="text")
            print(fng)

            task = f"""You are a DeFi security analyst. Based on market fear levels, assess the DeFi security threat landscape.
            Here is current crypto market data:
            {fng[:1500]}

            Respond with the following JSON format:
            {{
                "threat_level": str,
                "latest_hack": str,
                "amount_lost": str,
                "summary": str
            }}
            threat_level: one of LOW, MODERATE, HIGH, CRITICAL.
            latest_hack: most notable recent security event or "none".
            amount_lost: estimated recent losses as string or "0".
            summary: one sentence about DeFi security landscape.
            It is mandatory that you respond only using the JSON format above,
            nothing else. Don't include any other words or characters,
            your output must be only JSON without any formatting prefix or suffix.
            This result should be perfectly parsable by a JSON parser without errors.
            """
            result = gl.nondet.exec_prompt(task).replace("```json", "").replace("```", "")
            print(result)
            return json.dumps(json.loads(result), sort_keys=True)

        result_json = json.loads(gl.eq_principle.strict_eq(nondet))

        self.has_scanned = True
        self.threat_level = result_json["threat_level"]
        self.latest_hack = result_json["latest_hack"]
        self.analysis = result_json["summary"]

        return result_json
