# main.py
from fastapi import FastAPI, HTTPException
from mysql_handler import (
    get_all_customers, get_customer_transactions, insert_transaction, get_top_spenders, download_report_csv
)
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
import io

app = FastAPI()

class TransactionCreate(BaseModel):
    customer_id: int
    amount: float

@app.get("/customers")
def read_customers():
    return get_all_customers()

@app.get("/customers/{customer_id}/transactions")
def read_customer_transactions(customer_id: int):
    data = get_customer_transactions(customer_id)
    if not data:
        raise HTTPException(status_code=404, detail="Customer or transactions not found")
    return data

@app.post("/transactions")
def create_transaction(transaction: TransactionCreate):
    return insert_transaction(transaction.customer_id, transaction.amount)

@app.get("/analytics/top-spenders")
def top_spenders():
    return get_top_spenders()

@app.get("/analytics/download-report")
def download_report():
    csv_data = download_report_csv()
    return StreamingResponse(io.StringIO(csv_data), media_type="text/csv", headers={
        "Content-Disposition": "attachment; filename=transactions_report.csv"
    })
