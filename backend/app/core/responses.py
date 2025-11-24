from typing import Any, Optional
from datetime import datetime
from fastapi.responses import JSONResponse

class APIResponse:
    @staticmethod
    def create(status_code: int, data: Any = None, message: Optional[str] = None):
        content = {
            "status_code": status_code,
            "response_time": datetime.now().isoformat(),
            "data" : data,
            "message" : message,
        }

        # if data is not None:
        #     content["data"] = data

        # if message is not None:
        #     content["message"] = message
            
        return JSONResponse(status_code=status_code, content=content)
