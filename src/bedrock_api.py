import boto3

bedrock_agent_runtime = boto3.client(
    service_name = "bedrock-agent-runtime"
)

def retrieve(query, numberOfResults=1):
    return bedrock_agent_runtime.retrieve(
        retrievalQuery= {
            'text': query
        },
        knowledgeBaseId='CF1F6BN5VD',
        retrievalConfiguration= {
            'vectorSearchConfiguration': {
                'numberOfResults': numberOfResults
            }
        }
    )
def return_response(question):
    response = retrieve(question)["retrievalResults"][0]['content']['text']
    return response

