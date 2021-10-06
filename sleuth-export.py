import argparse
import csv
import os
import sys
from datetime import datetime, timedelta, date
from enum import Enum
from typing import Tuple, List

from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

parser = argparse.ArgumentParser(
    description="Extract Accelerate metrics from Sleuth by project"
)
parser.add_argument(
    "file", default="report.csv", nargs="?", help="the csv file to create"
)
parser.add_argument(
    "--api-key", dest="api_key", required=True, help="Your Sleuth API key"
)
parser.add_argument(
    "--org-slug", dest="org_slug", required=True, help="Your Sleuth organization slug"
)

args = parser.parse_args()


class Metric(Enum):
    LEAD_TIME = "MetricLeadTimeChartType"
    FREQUENCY = "MetricFrequencyChartType"
    FAILURE_RATE = "MetricFailureRateChartType"
    MTTR = "MetricMTTRChartType"


def main():
    client = get_client()

    with open(args.file, "w") as f:
        writer = csv.writer(f)
        writer.writerow(["Project", "Metric", "Period", "Value"])

        for project_slug, project_name in find_project_slugs(client):
            print(f"Processing project {project_name}")
            for metric in Metric:
                print(f"... metric {metric.name}")
                data: List[Tuple[str, float]] = get_metric_data(
                    client, project_slug, metric
                )
                for label, val in data:
                    writer.writerow([project_name, metric.name, label, val])

    print(f"Wrote {args.file}")


def get_client():
    transport = RequestsHTTPTransport(
        url="https://app.sleuth.io/graphql",
        headers=dict(authorization=f"apikey {args.api_key}"),
    )
    return Client(transport=transport)


def find_project_slugs(client) -> List[Tuple[str, str]]:
    query = gql(
        f"""
        query {{
            projects(orgSlug:"{args.org_slug}") {{
                slug
                name
            }}
        }}    
    """
    )

    # Execute the query on the transport
    result = client.execute(query)
    return [(p["slug"], p["name"]) for p in result["projects"]]


def get_metric_data(client, project_slug, chart_type: Metric):
    now = date.today()
    past = now - timedelta(days=14)
    query = gql(
        f"""
        query {{
            metric(orgSlug:"{args.org_slug}", 
                projectSlug:"{project_slug}", 
                environmentSlug:"production", 
                metricType:{chart_type.name}, 
                deploymentSlugs:[],
                startDate:"{past.isoformat()}",
                endDate:"{now.isoformat()}"
                ) {{
                
                ... on {chart_type.value} {{
                    labels
                    datapoints
                }}
            }}
        }}    
    """
    )

    # Execute the query on the transport
    result = client.execute(query)
    return zip(result["metric"]["labels"], result["metric"]["datapoints"])


if __name__ == "__main__":
    main()
