import asyncio
import httpx

async def get_fajr_timings():
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "http://localhost:8000/v1/hijriCalenderByAddress/1446/4",
            params={
                "address": "170 Ranwood Court, Hamilton, Ontario",
                "adjustment": 19
            }
        )

        # Check if the response is successful
        if response.status_code == 200:
            # Get the JSON response
            json_response = response.json()

            # Extract the timings
            fajr_timings = json_response.get("fajr_timings", [])

            # Create your own list for Fajr prayers
            fajr_prayers = []

            # Add the Fajr timings to your own list
            for timing in fajr_timings:
                # Assuming the Fajr timings are in the format you want, e.g., "05:30"
                fajr_prayers.append(timing)

            # Print the Fajr prayers list
            print("Fajr Prayers Timings:", fajr_prayers)
        else:
            print(f"Failed to fetch data: {response.status_code}")

# Execute the async function
if __name__ == "__main__":
    asyncio.run(get_fajr_timings())
