import requests

print(
    requests.post(
        "http://127.0.0.1:10000",
        json={
            "from_email": "Adarsh@gmail.com",
            "content": """
            Dear Adarsh
                    I hope this message finds you well. I'm Adarsh from ABC company;

                    I'm looking to purchase some company T-shirst for my team, we are a team of 10k people and we want 2 t-shirt per personl

                    please let me know the price and timeline you can work with;

                    Looking forward

                    Adarsh
                """,
        },
    ).json()
)
