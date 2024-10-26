# myapi.py

from fastapi import FastAPI, HTTPException
import httpx

from hijri_converter import Hijri
app = FastAPI()

# A quick definition of all possible API requests
# GET - GET AN INFORMATION
# POST - CREATE SOMETHING NEW
# PUT - UPDATE
# DELETE - DELETE SOMETHING 

hijri_date = Hijri.today().datetuple()

# year = hijri_date[0]
# month = hijri_date[1]
# adjustment = 19 - Hamilton Area
# Define the external API endpoint outside the function
EXTERNAL_API_URL = "http://api.aladhan.com/v1/hijriCalendarByAddress/{year}/{month}"

@app.get("/v1/hijriCalenderByAddress/{year}/{month}")
async def fetch_data(*, year: int, month: int, address: str, adjustment: int):
    try:
        formatted_url = EXTERNAL_API_URL.format(year=year, month=month)

        async with httpx.AsyncClient() as client:
            response = await client.get(formatted_url, params={"address": address, "adjustment": adjustment, "iso8601": True})
            response.raise_for_status()
            external_data = response.json()

            fajr_timings = [
                item["timings"]["Fajr"]
                for item in external_data.get("data", [])
                if "timings" in item and "Fajr" in item["timings"]
            ]

            if not fajr_timings:
                raise HTTPException(status_code=404, detail="Fajr timings not found")

            return {
                "code": external_data.get("code"),
                "status": external_data.get("status"),
                "fajr_timings": fajr_timings
            }

    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail="Error fetching data from external API")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


