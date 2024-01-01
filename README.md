# mturk-guide

This serves as a simple and quickstart guide to using MTurk. You should use this along with AWS' Boto3 API documentation. 

If you have any questions or suggestions, feel free to submit a pull request. 

# Setup

You should setup your MTurk **Requester** account through your AWS account as MTurk billing works through AWS. Then, go to the Developer tab the MTurk website.

![Developer Tab](./images/Screenshot 2023-12-31 at 11.05.36 PM.png "This is an image")

Follow the instructions outlined on the page, especially Step 2 which entails getting your **AWS access keys**. You will need them to use the MTurk client from AWS' boto3 API.

Make sure to also register for the **MTurk Developer Sandbox** and **MTurk Worker Sandbox** to test out your task interfaces before publishing HITs. You will need the developer sandbox to publish HITs to test and the worker sandbox to interact with the task itself. 

# Task Template

Refer to **questions.xml** to see an example of the task interface code. All you need to do is replace the HTML code in between ``YOUR HTML BEGINS`` and ``YOUR HTML ENDS``. However, make sure to **retain this chunk of code in your HTML code:**

```html
    <head>
        <meta http-equiv='Content-Type' content='text/html; charset=UTF-8'/>
        <script type='text/javascript' src='https://s3.amazonaws.com/mturk-public/externalHIT_v1.js'></script>
    </head>
    <body>
        <form name='mturk_form' method='post' id='mturk_form' 
        action='https://www.mturk.com/mturk/externalSubmit'><input type='hidden' value='' 
        name='assignmentId' id='assignmentId'/>
        
        <!-- You must include this JavaScript file -->
        <script src="https://assets.crowd.aws/crowd-html-elements.js"></script>
```

In order for the user to submit the task, you **MUST use the ``crowd-form`` element.**

It is highly recommended to edit your task interface on MTurk. You can do so by creating a project and replacing the HTML code there with yours. 

# Publishing HITs

HIT is short for **Human Intelligence Task**. In MTurk, publishing a HIT means to publish a task. For instance, a task can be asking a user to rank a series of images based on how aesthetically pleasing it is. For a HIT, you (the requester) can assign it to multiple workers. This is because one worker result might be biased, so we want to collect multiple results to get an average that's more representative. 

Below is the typical code block to publish a hit (using `mturk.create_hit`). The comments will describe what each parameter represents.

```python
    new_hit = mturk.create_hit(
        Title="Rank a series of images", # task title
        Description="Rank a series images from 1 to 10", # task description that is presented to worker before they accept task
        Keywords="rank, image, quick, labeling, easy, simple, fast", # keywords that workers might search for to work on tasks
        Reward="0.1", # reward for each assignment
        MaxAssignments=3, # number of assignments 
        LifetimeInSeconds=259200, # lifetime that the task will exist
        AssignmentDurationInSeconds=120, # how long the task should take
        AutoApprovalDelayInSeconds=86400, # time until auto approval of task submission
        Question=question, # question interface code
        QualificationRequirements=[] # qualification requirements
    )
```

You should set a reasonable amount of time for the task completion, auto approval time and lifetime of the task. It is recommended to give about 5 minutes for a task (depends), 3 - 7 days for auto approal time and 7 days for lifetime of the task. However, this will depend on how many assignments you need and your qualification requirements. 

## Qualification Requirements

Depending on your task, you might have **want to allocate them to a specific group of people who might be more capable of giving your expected results.** Defining your qualification requirements will allow you to control that. 

Below is an example, where we have set the 
- worker percentage approval rate to 95% or more
- the number of HITs approved to 1000 or more
- the worker location to be in the US 


You can ask GPT for the specific QualificationTypeIds. 

```python
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
```
# Obtaining HIT Results

The easiest way I've found is to log the HIT IDs each time a HIT is published and use that log to loop through and collect the results.

Depending on how you configure the input collection in your HTML code, you should modify to unpack the results. 

Refer to **viz_hit.py** to get an example of how the input is unpacked. 
Refer to **publish_hit.py** to get an example of how input is collected.
