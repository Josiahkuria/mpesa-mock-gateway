import time
from fastapi import FastAPI, HTTPException, Header, status
from pydantic import BaseModel
from typing import Optional

app = FastAPI(
    title="Daraja M-Pesa Mock Gateway",
    description="Offline high-fidelity flight simulator for Safaricom Daraja API testing.",
    version="1.0.0"
)

# Standard Safaricom STK Push Request Structure
class STKPushRequest(BaseModel):
    BusinessShortCode: str
    Password: str
    Timestamp: str
    TransactionType: str
    Amount: float
    PartyA: str
    PartyB: str
    PhoneNumber: str
    CallBackURL: str
    AccountReference: str
    TransactionDesc: str

# 1. Mock Authorization Token Endpoint
@app.get("/oauth/v1/generate")
def generate_token(authorization: Optional[str] = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization Header")
    
    return {
        "access_token": "mock_secret_token_abcdef1234567890",
        "expires_in": "3599"
    }

# 2. Mock STK Push Process Request Endpoint
@app.post("/mpesa/stkpush/v1/processrequest")
def process_stk_push(payload: STKPushRequest):
    amount = payload.Amount

    # SCENARIO A: Simulate System Latency / Network Timeout
    if amount == 504.0:
        time.sleep(5)  # Pause execution for 5 seconds to test client timeouts
        return {
            "MerchantRequestID": "mock-req-9999",
            "CheckoutRequestID": "mock-chk-9999",
            "ResponseCode": "0",
            "ResponseDescription": "Gateway timeout simulation complete",
            "CustomerMessage": "Success"
        }

    # SCENARIO B: Simulate Insufficient Funds (Daraja Error Code 4001)
    elif amount == 4001.0:
        return {
            "MerchantRequestID": "mock-req-4001",
            "CheckoutRequestID": "mock-chk-4001",
            "ResponseCode": "4001",
            "ResponseDescription": "The balance is insufficient for the transaction.",
            "CustomerMessage": "The balance is insufficient for the transaction."
        }

    # SCENARIO C: Simulate Invalid PIN (Daraja Error Code 2001)
    elif amount == 2001.0:
        return {
            "MerchantRequestID": "mock-req-2001",
            "CheckoutRequestID": "mock-chk-2001",
            "ResponseCode": "2001",
            "ResponseDescription": "The initiator details/credentials are invalid.",
            "CustomerMessage": "The initiator details/credentials are invalid."
        }

    # DEFAULT SCENARIO: Clean Success Loop Path
    else:
        return {
            "MerchantRequestID": f"mock-req-id-{int(time.time())}",
            "CheckoutRequestID": f"ws_CO_30052026_mock_{int(time.time())}",
            "ResponseCode": "0",
            "ResponseDescription": "Accept the service request successfully.",
            "CustomerMessage": "Success. Request accepted for processing"
        }
