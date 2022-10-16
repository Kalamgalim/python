import requests

url = "https://solana-gateway.moralis.io/nft/mainnet/6NqLaD1U3N3rsUm42XyPRfd9Nd4TiygYvpcWwkiuC4Yf/metadata"

headers = {

    "accept": "application/json",
    "X-API-Key": "test"

}

response = requests.get(url, headers=headers)

print(response.text)
