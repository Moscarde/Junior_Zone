import csv
import time
from datetime import datetime, timedelta

import pandas as pd
import requests


class GupyScraper:
    def __init__(self, search_labels):
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 OPR/100.0.0.0 (Edition std-1)"
        }
        self.search_labels = search_labels

        self.ids = set()

    def request_data(self, labels):
        print(labels)
        responses = []

        with requests.Session() as session:
            for label in labels:
                print(f"Requesting for '{label}'...")
                url = f"https://portal.api.gupy.io/api/job?name={label}&offset=0&limit=400"

                try:
                    request = session.get(url, headers=self.headers)
                    response = request.json().get("data", [])
                    responses.append(response)

                    pd.DataFrame(request.json().get("data", [])).to_csv(
                        f"data/staged_labels_responses/{label}.csv", index=False
                    )

                    print(f"Found {len(response)} results for '{label}'...")
                    time.sleep(0.5)

                except Exception as e:
                    print(e)

        return responses

    def request_and_save(self):
        labels_responses = self.request_data(self.search_labels)
        self.save_data_to_csv(labels_responses)

    def save_data_to_csv(self, labels_responses):
        csv_data = CsvData()
        csv_data.validate_and_write(labels_responses)


class VerifyData:
    def __init__(self):
        self.df = pd.DataFrame()
        job_ids_path = "data/job_ids.csv"
        self.df_job_ids = self.read_job_ids(job_ids_path)
        today = datetime.now().date()
        yesterday = today - timedelta(days=1)
        self.interval = (str(today), str(yesterday))

    def read_job_ids(self, job_ids_path):
        try:
            df = pd.read_csv(job_ids_path)
            return df
        except FileNotFoundError:
            df = pd.DataFrame(columns=["job_id", "published_date"])
        return df

    def validate_job_date(self, job):
        job_published_date = job["publishedDate"]

        if job_published_date.startswith(self.interval):
            return True
        else:
            return False

    def validadate_job_duplicate(self, job):
        if job["id"] not in self.df_job_ids["job_id"].values and job["id"] > 1000:
            self.df_job_ids.loc[len(self.df_job_ids)] = [
                job["id"],
                job["publishedDate"],
            ]
            return True
        else:
            return False

    def write_df_job_ids(self):
        self.df_job_ids.to_csv("data/job_ids.csv", index=False)


class CsvData:
    def __init__(self):
        self.csv_column_names = [
            "job_id",
            "published_date",
            "title",
            "description",
            "career_page_name",
            "type",
            "application_deadline",
            "is_remote_work",
            "city",
            "state",
            "country",
            "job_url",
            "disabilities",
            "workplace_type",
            "submitted",
        ]
        self.date = str(datetime.now().date())
        self.verify_data = VerifyData()

    def validate_and_write(self, labels_responses):
        with open(
            f"data/responses/{self.date}.csv", "a+", newline="", encoding="utf-8"
        ) as csvfile:
            writer = csv.writer(csvfile)
            if csvfile.tell() == 0:
                writer.writerow(self.csv_column_names)

            for label_response in labels_responses:
                for job in label_response:
                    if self.verify_data.validate_job_date(
                        job
                    ) and self.verify_data.validadate_job_duplicate(job):
                        row = [
                            job["id"],
                            job["publishedDate"],
                            job["name"],
                            job["description"]
                            .replace("\r", " ")
                            .replace("\n", " ")
                            .replace("&nbsp;", " "),
                            job["careerPageName"],
                            job["type"],
                            job["applicationDeadline"],
                            job["isRemoteWork"],
                            job["city"],
                            job["state"],
                            job["country"],
                            job["jobUrl"],
                            job["disabilities"],
                            job["workplaceType"],
                            "False",
                        ]
                        writer.writerow(row)
            self.verify_data.write_df_job_ids()


if __name__ == "__main__":
    filter_labels = [
        "analista",
        "dados",
        "python",
        "data",
        "Desenvolvedor",
        "Dev",
        "Front-end",
        "Back-end",
        "Full Stack",
        "FullStack",
        "Software",
        "DevOps",
        "Business Intelligence",
        "Machine Learning",
        "Inteligência Artificial",
    ]

    scraper = GupyScraper(filter_labels)
    scraper.request_and_save()
