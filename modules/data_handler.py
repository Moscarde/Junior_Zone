import pandas as pd
from datetime import datetime
import re, os


class DataHandler:
    def __init__(self):
        self.date = datetime.now().date()
        self.base_dataset = pd.read_csv(f"data/responses/{self.date}.csv")
        self.filtered_dfs = self.process_dataset(self.base_dataset)

    def process_dataset(self, base_dataset):
        df_jr = self.apply_exclusion_filters(
            base_dataset, ["PLENO", "SÊNIOR", "SENIOR", "SR", "PL", "III", "lll", "ll", "II"]
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

        df_dados = self.apply_search_filters(df_jr, dados_filter)
        df_dados_remote = df_dados[(df_dados["workplace_type"] == "remote")]
        df_dados_hybrid = df_dados[(df_dados["workplace_type"] == "hybrid")]

        df_dev = self.apply_search_filters(df_jr, dev_filter)
        df_dev_remote = df_dev[(df_dev["is_remote_work"] == True)]
        df_dev_hybrid = df_dev[(df_dev["workplace_type"] == "hybrid")]

        return {
            "dados_remote": df_dados_remote,
            "dados_hybrid": df_dados_hybrid,
            "dev_remote": df_dev_remote,
            "dev_hybrid": df_dev_hybrid,
        }

    def apply_exclusion_filters(self, df, filters):
        for f in filters:
            df = df[~df["title"].str.upper().str.contains(f.upper())]

        df = df[
            ((df["country"] == "Brasil") | (df["country"].isna()))
            & (df["submitted"] == False)
        ]

        return df

    def apply_search_filters(self, df, filters):
        temp_df_list = []
        for f in filters:
            temp_df_list.append(df[df["title"].str.upper().str.contains(f.upper())])

        df_final = pd.concat(temp_df_list, ignore_index=True)
        return df_final

    def tag_as_submitted(self):
        self.base_dataset["submitted"] = "True"
        self.base_dataset.to_csv(f"data/responses/{self.date}.csv", index=False)


def update_google_sheets_dataset():
    data_files = os.listdir("data/responses/")

    dfs = []
    for file in data_files:
        df = pd.read_csv(f"data/responses/{file}")
        dfs.append(df)

    df = pd.concat(dfs, ignore_index=True)
    df = df[
        (~df["title"].str.upper().str.contains("PLENO"))
        & (~df["title"].str.upper().str.contains("SÊNIOR"))
        & (~df["title"].str.upper().str.contains("SENIOR"))
        & (~df["title"].str.upper().str.contains("SR"))
        & (~df["title"].str.upper().str.contains("PL"))
        & ((df["country"] == "Brasil") | (df["country"].isna()))
    ]
    df["date"] = pd.to_datetime(df["published_date"])
    df = df.fillna("...")
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
    df["date"] = df["date"].dt.strftime("%d/%m/%Y")
    df["workplace_type"] = df["workplace_type"].apply(lambda x: x.split(".")[1])
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


# def text_converter(text):
#     #'_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!' must be escaped with the preceding character '\'.
#     return (
#         str(text)
#         .replace(".", "\.")
#         .replace("(", "\(")
#         .replace(")", "\)")
#         .replace("|", "\|")
#         .replace("-", "\-")
#         .replace("+", "\+")
#         .replace("[", "\[")
#         .replace("]", "\]")
#         .replace("{", "\{")
#         .replace("}", "\}")
#         .replace("!", "\!")
#         .replace("#", "\#")
#         .replace("~", "\~")
#         .replace("`", "\`")
#         .replace(">", "\>")
#         .replace("*", "\*")
#         .replace("=", "\=")
#         .replace("'", "'")
#         .replace('"', '"')
#         .replace("<", "\<")
#     )


if __name__ == "__main__":
    from pprint import pprint

    data = DataHandler()

