Sleuth metrics export
=====================

This is a script to export raw Accelerate/DORA metrics from Sleuth into a CSV, suitable to load into a spreadsheet.

The final CSV is formatted with the following columns: Project, Metric, Period, Value

Installation
------------

1. Install Python 3.9 (https://docs.python.org/3.9/)
2. In the script directory, run:
````
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
````


Usage
-----

In order to run the script, you'll need a couple bits of information:

1. Your Sleuth organization API key, found in your organization settings
2. Your Sleuth organization slug, usually found in the URL as in https://app.sleuth.io/ORG

With this information, you can run the script:

````
python sleuth-export.py --api-key=YOUR_API_KEY --org-slug=YOUR_ORG_SLUG [CSV_FILE]
````

For example, to create a file called `report.csv` for the `myorg` Sleuth organization, it would look like:

````
python sleuth-export.py --api-key=not-a-real-key --org-slug=myorg report.csv
````


