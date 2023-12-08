import pandas as pd
from datetime import datetime
import re, os


class DataHandler:
    def __init__(self):
        self.date = datetime.now().date()
        self.base_dataset = pd.read_csv(f"data/responses/{self.date}.csv")
        self.filtered_dfs = self.process_dataset(self.base_dataset)

    def process_dataset(self, base_dataset):
        df_jr = apply_exclusion_filters(
            base_dataset,
            ["PLENO", "SÊNIOR", "SENIOR", "SR", "PL", "III", "lll", "ll", "II"],
        )

        df_jr = df_jr.sort_values(by="state")

        print("Total de vagas retornadas:", len(base_dataset))
        print("Vagas filtradas:", len(df_jr))

        dados_filter = [
            "analista",
            "dados",
            "data",
            "Machine Learning",
            "Inteligência Artificial",
            "Business Intelligence",
        ]

        dev_filter = [
            "Desenvolvedor",
            "Dev",
            "Front-end",
            "Back-end",
            "Full Stack",
            "Software",
            "fullstack",
            "DevOps",
        ]

        df_dados = apply_search_filters(df_jr, dados_filter)
        df_dados_remote = df_dados[(df_dados["workplace_type"] == "remote")]
        df_dados_hybrid = df_dados[(df_dados["workplace_type"] == "hybrid")]

        df_dev = apply_search_filters(df_jr, dev_filter)
        df_dev_remote = df_dev[(df_dev["is_remote_work"] == True)]
        df_dev_hybrid = df_dev[(df_dev["workplace_type"] == "hybrid")]

        return {
            "dados_remote": df_dados_remote,
            "dados_hybrid": df_dados_hybrid,
            "dev_remote": df_dev_remote,
            "dev_hybrid": df_dev_hybrid,
        }

    def tag_as_submitted(self):
        self.base_dataset["submitted"] = "True"
        self.base_dataset.to_csv(f"data/responses/{self.date}.csv", index=False)


def apply_exclusion_filters(df, filters, status=False):
    temp_df_list = []
    for f in filters:
        temp_df_list.append(df[df["title"].str.upper().str.contains(f.upper())])

    df = pd.concat(temp_df_list, ignore_index=True)

    df = df[
        ((df["country"] == "Brasil") | (df["country"].isna()))
        & (df["submitted"] == status)
    ]

    return df


def apply_search_filters(df, filters):
    temp_df_list = []
    for f in filters:
        temp_df_list.append(df[df["title"].str.upper().str.contains(f.upper())])

    df_final = pd.concat(temp_df_list, ignore_index=True)
    return df_final


def update_google_sheets_dataset():
    responses_datasets_filenames = os.listdir("data/responses/")

    df_list = []
    for filename in responses_datasets_filenames:
        print(filename)
        df_response = pd.read_csv(f"data/responses/{filename}")
        df_list.append(df_response)

    df = pd.concat(df_list, ignore_index=True)

    df = apply_exclusion_filters(
        df, ["PLENO", "SÊNIOR", "SENIOR", "SR", "PL", "III", "lll", "ll", "II"],
        status=True,
    )

    df = df.fillna("...")

    df["date"] = pd.to_datetime(df["published_date"]).dt.strftime("%Y/%m/%d")
    df["workplace_type"] = df["workplace_type"].replace(
        {"hybrid": "2.Híbrido", "remote": "1.Remoto", "on-site": "3.Presencial"}
    )
    df = df.sort_values(
        by=[
            "date",
            "workplace_type",
        ],
        ascending=[False, True],
    )
    df["date"] = pd.to_datetime(df["date"]).dt.strftime("%d/%m/%Y")
    df["workplace_type"] = df["workplace_type"].apply(lambda x: x.split(".")[1])

    df = df[
        [
            "date",
            "title",
            "career_page_name",
            "workplace_type",
            "job_url",
            "city",
            "state",
        ]
    ]

    df.columns = [
        "Data",
        "Vaga",
        "Nome da Empresa",
        "Tipo de Trabalho",
        "URL",
        "Cidade",
        "Estado",
    ]
    df.to_csv(f"data/googlesheets_dataset.csv", index=False)


if __name__ == "__main__":
    update_google_sheets_dataset()
