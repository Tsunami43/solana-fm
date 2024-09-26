from typing import Dict, Optional
from .errors import NotFoundTransfers


class TransfersAmount:
    def __init__(self, data: Dict[str, float]):
        self.data = data

    @classmethod
    def from_json(cls, json_data: dict) -> "TransfersAmount":
        result = json_data.get("result")
        if result is None or result == []:
            raise NotFoundTransfers()
        else:
            output_data = {}
            for signature in result:
                flag = 0
                for data in signature["data"]:
                    if (
                        data["token"] == "So11111111111111111111111111111111111111112"
                        and data["action"] == "transfer"
                    ):
                        output_data[signature["transactionHash"]] = (
                            float(data["amount"]) / 10**9
                        )
                        flag = 1
                        break
                if flag == 0:
                    for data in signature["data"]:
                        if (
                            data["token"]
                            == "So11111111111111111111111111111111111111112"
                            and data["action"] == "transferChecked"
                        ):
                            output_data[signature["transactionHash"]] = (
                                float(data["amount"]) / 10**9
                            )
                            break
            return cls(output_data)

    def get(self, signature: str) -> Optional[float]:
        return self.data.get(signature)
