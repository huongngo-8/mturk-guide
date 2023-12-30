import boto3

# these are base links to view/access HITs that have been published
MTURK_SANDBOX = "https://mturk-requester-sandbox.us-east-1.amazonaws.com"
MTURK_PROD = "https://mturk-requester.us-east-1.amazonaws.com"
MTURK_PROD_VIZ = "https://worker.mturk.com/mturk/preview?groupId="
MTURK_SB_VIZ = "https://workersandbox.mturk.com/mturk/preview?groupId="

# a toggle to specify whether you're in sandbox mode or not
sandbox = True

# for security purposes, these keys shouldn't be public
ACCESS_KEY_ID = ""
SECRET_ACCESS_KEY = ""

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

# this will read in your question interface script
question = open(file="questions.xml", mode="r").read()

# this defines a list of qualification requirements
qr = [
    {
        "QualificationTypeId": "000000000000000000L0",  # Worker Percentage Approval Rate
        "Comparator": "GreaterThanOrEqualTo",
        "IntegerValues": [95],  # 95% approval rate
    },
    {
        "QualificationTypeId": "00000000000000000040",  # Number of HITs Approved
        "Comparator": "GreaterThanOrEqualTo",
        "IntegerValues": [1000],  # At least 1000 HITs completed
    },
    {
        "QualificationTypeId": "00000000000000000071",  # Worker Locale
        "Comparator": "EqualTo",
        "LocaleValues": [{"Country": "US"}],  # Located in the United States
    },
]

# this creates a new hit
new_hit = mturk.create_hit(
    Title="Rank a series of images",
    Description="Rank a series images from 1 to 10",
    Keywords="rank, image, quick, labeling, easy, simple, fast",
    Reward="0.1",
    MaxAssignments=3,
    LifetimeInSeconds=259200,
    AssignmentDurationInSeconds=120,
    AutoApprovalDelayInSeconds=86400,
    Question=question,
    QualificationRequirements=[]
    if sandbox
    else qr,  # for sandbox, best not to have requirements so you can access it yourself (if you don't meet the requirements)
)

# if you need to create multiple hits, prepare a csv/txt file of links or unique IDs that reference your data
with open("data/imgs.csv", "r") as f:
    data = [line.strip().split(",") for line in f]

for series in data:
    for i, img in enumerate(series):
        question = question.replace("img" + str(i + 1) + ".png", img + ".png")

    new_hit = mturk.create_hit(
        Title="Rank a series of images",
        Description="Rank a series images from 1 to 10",
        Keywords="rank, image, quick, labeling, easy, simple, fast",
        Reward="0.45",
        MaxAssignments=10,
        LifetimeInSeconds=23300,
        AssignmentDurationInSeconds=130,
        AutoApprovalDelayInSeconds=2100,
        Question=question,
        QualificationRequirements=[]
        if sandbox
        else qr,  # for sandbox, best not to have requirements so you can access it yourself (if you don't meet the requirements)
    )

    # logging hits published to later access it
    with open("logs/published_hits.txt", "a") as f:
        f.write(new_hit["HIT"]["HITId"] + "\n")


# verbose setting in sandbox that will return a link to see how workers interact with your task
if sandbox:
    print("A new HIT has been created. You can preview it here:")
    print((MTURK_SB_VIZ if sandbox else MTURK_PROD_VIZ) + new_hit["HIT"]["HITGroupId"])
    print("HITID = " + new_hit["HIT"]["HITId"] + " (Use to Get Results)")
