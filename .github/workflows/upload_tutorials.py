import asyncio
import time
import os
import typesense
import json

async def main():

    typesense_client = typesense.Client({
        'api_key': os.environ['TYPESENSE_TUTORIALS_API_KEY'],
        'nodes': [{
            'host': 'cgnvrk0xwyj9576lp-1.a1.typesense.net',
            'port': '443',
            'protocol': 'https'
        }],
        'connection_timeout_seconds': 2
    })

    time_now = int(time.time())

    # Get tutorials from tutorials/typesense.json
    with open('tutorials/typesense.json') as f:
        resources = json.load(f)
        for r in resources:
            print("RESOURCE")
            r["date"] = int(r["date"])
            print(r)
            r["last_updated"] = time_now
            print(r)
            insert_resp = typesense_client.collections['tutorials'].documents.upsert(r)
            print("INSERTED")
            print(insert_resp)

    # Deleting documents that didn't get updated (presumably deleted)
    try:
        res = typesense_client.collections['tutorials'].documents.delete({'filter_by': 'last_updated: <' + str(time_now)})
        print("Resources deleted")
        print(res)
    except Exception as e:
        print(e)
        pass


if __name__ == '__main__':
    asyncio.run(main())
