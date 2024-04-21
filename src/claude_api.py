from anthropic import AnthropicBedrock
import os
def call_api(prompt, question):
    client = AnthropicBedrock(
        # Authenticate by either providing the keys below or use the default AWS credential providers, such as
        # using ~/.aws/credentials or the "AWS_SECRET_ACCESS_KEY" and "AWS_ACCESS_KEY_ID" environment variables.
        aws_access_key = "ASIATTIULSRD3LLDPPCG",
        aws_secret_key = "JWDfygqbiqxEbg8+MvwB/d5ZFME0M9UIWBVS9ZSd",
        # Temporary credentials can be used with aws_session_token.
        # Read more at https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp.html.
        aws_session_token = "IQoJb3JpZ2luX2VjEO///////////wEaCXVzLWVhc3QtMSJHMEUCIQDF68STdxrVTgY/wVHTqj8ouhnZBx0jSFAlSgjtWRuyZgIgdXo+aJxKxzxhk5ro/jnqef7zgjza2kEgNdYLHe8h2iEqmQIINxACGgwyNDc1NDAxOTIzMjciDEmVaphJ65NoQiXXeir2AXty+z8aMfS/FjrIRzdrsFGiFdvUBHYFtCNkjm19KlPUkS1U9WrZOiUowpbSqGjMpBpwWbVy+4Fgi+4Dq8zJL8Z34FwP0ivABaTUgaGwhgHBBbkm0CSTlJ4+ujyED3r1sQFIHXsGiUn+MnEQdxNeJOB+NDGff3tMbp84TxEpWivl7CbcCnLNvskY7rC3jhw2JlpB2MUWN/1U53Sue17i6bTXF6OHJCSnbFaLRHAAr5TaQe9yn4qMr3yB0C7kTs8xCvuEXNFrudFensPKvF7FMR7h60sXfchiXIp47q3y4of5pt8GGubhUrsekFbgA9zwUjjnh1O7kTDr/JCxBjqdAfkb+oiM/my8EacwheiRSABzJxWc5n6KZs8EBBjsvV7VMDDlqSvLmbRt5CHMSMT1Q1Ndubm6FQCVC6IkORETvBarHMRe12P9aziXhnGVTCQcirsQWPGuYTI95mwdDthKgRUoNioFFHCbu93BMutJn+333L1LyC9C+xd0VUywDnUJ02HFURZTMMW46klGXcnexnY0jJEAoluiDP+bg8c=",
        # aws_region changes the aws region to which the request is made. By default, we read AWS_REGION,
        # and if that's not present, we default to us-east-1. Note that we do not read ~/.aws/config for the region.
        aws_region ="us-west-2",
    )
    prompt = "Μέ βάση τα δεδομένα: " + prompt + "Απάντησε στην εξής ερώτηση:" + question + \
    "Προσπάθησε να χρησιμοποιείς ιστορικά δεδομένα και αφαίρεσε όλους τους ειδικους" + \
    "χαρακτήρες οπως ' slash n'. Κάνε το κείμενο φιλικό προς τον χρήστη και ολοκλήρωσε ολες τις προτάσεις με σημεία στίξης. Αν δεν βρίσκεις απάντηση από τα δεδομένα που σου εδωσα απάντησε με τις γνώσεις σου που έχεις"
    message = client.messages.create(
        model="anthropic.claude-3-sonnet-20240229-v1:0",
        max_tokens=256,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content