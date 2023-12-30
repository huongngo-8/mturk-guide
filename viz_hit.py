import boto3
import xmltodict

# these are base links to view/access HITs that have been published
MTURK_SANDBOX = "https://mturk-requester-sandbox.us-east-1.amazonaws.com"
MTURK_PROD = "https://mturk-requester.us-east-1.amazonaws.com"
MTURK_PROD_VIZ = "https://worker.mturk.com/mturk/preview?groupId="
MTURK_SB_VIZ = "https://workersandbox.mturk.com/mturk/preview?groupId="

# a toggle to specify whether you're in sandbox mode or not
sandbox = True

# for security purposes, these keys shouldn't be public
ACCESS_KEY_ID = "AKIA3UFVESAJ72RDFVIB"
SECRET_ACCESS_KEY = "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"

mturk = boto3.client(
    "mturk",
    aws_access_key_id=ACCESS_KEY_ID,
    aws_secret_access_key=SECRET_ACCESS_KEY,
    region_name="us-east-1",
    endpoint_url=MTURK_SANDBOX
    if sandbox
    else MTURK_PROD,  # if you're in sandbox mode, the client will use the sandbox endpoint
)

# to sanity check that you're in sandbox mode, your account balance will always be $10000
print(
    "I have $"
    + mturk.get_account_balance()["AvailableBalance"]
    + " in my Sandbox account"
)

with open("logs/published_hits.txt", "r") as f:
    hit_ids = [line.strip() for line in f]

hit_id = hit_ids[0]
# if you want to check info about the specific HIT
hit_info = mturk.get_hit(HITId=hit_id)
# looking at results from assignments that have been submitted from a specific HIT
worker_results = mturk.list_assignments_for_hit(
    HITId=hit_id, AssignmentStatuses=["Submitted"]
)["Assignments"]

for result in worker_results:
    d = xmltodict.parse(result["Answer"])
