import pandas as pd
from datetime import datetime
import re, os

class DataHandler:
    def __init__(self, date, filter_labels):
        self.date = date
        self.base_df = pd.read_csv(f"data/responses/{date}.csv")
        self.filter_labels = filter_labels
        self.telegram_text = self.process_data(self.base_df)

    def process_data(self, df):
        df_jr = df[
            (~df["title"].str.upper().str.contains("PLENO"))
            & (~df["title"].str.upper().str.contains("SÊNIOR"))
            & (~df["title"].str.upper().str.contains("SENIOR"))
            & (~df["title"].str.upper().str.contains("SR"))
            & (~df["title"].str.upper().str.contains("PL"))
            & ((df["country"] == "Brasil") | (df["country"].isna()))
            & (df["submitted"] == False)
        ]
        df_jr = df_jr.sort_values(by="state")

        print("Total de vagas:", len(df))
        print("Vagas filtradas:", len(df_jr))

        self.df_jr_remote = df_jr[(df_jr["is_remote_work"] == True)]
        self.df_jr_hybrids = df_jr[(df_jr["workplace_type"] == "hybrid")]

        if (len(self.df_jr_remote) == 0) and (len(self.df_jr_hybrids) == 0):
            message = (
                "🚫 Nenhuma nova vaga remota / hibrida foi encontrada até o momento"
                "\n"
                "Confira a planilha para ver todas as vagas presenciais e remotas através do link:\n"
                "[Planilha com todas as vagas atualizadas](https://docs.google.com/spreadsheets/d/1yii99T2zZtG_OFarL_OxuhDVW0uvMmMhw9I2MygaLqc/edit?usp=sharing)"
            )
        else:
            message = self.contruct_message(
                [
                    {
                        "title_section": "🌐 Vagas Jr - Remotas 🌐 ",
                        "data": self.df_jr_remote,
                        "type": "remote ",
                    },
                    {
                        "title_section": "🌍 Vagas Jr - Híbridas 🌍",
                        "data": self.df_jr_hybrids,
                        "type": "hybrid",
                    },
                ]
            )

        return message

    def contruct_message(self, list_of_dict):
        raw_date = datetime.now()
        message = []
        message.append(
            f"📅 Vagas atualizadas dia: *{raw_date.strftime('%d/%m/%Y')}*\n"
            f"Período: *{'Manhã 🌅' if raw_date.hour < 12 else 'Tarde 🌇'}*\n\n"
            "Nesse grupo são postadas apenas vagas Jr remotas e híbridas que passaram pelo filtro:\n"
            f"_{', '.join(self.filter_labels)}_\n"
            "Em breve teremos mais filtros ou outros grupos\n\n"
        )
        message_splitted_index = 0
        for dict in list_of_dict:
            if len(dict["data"]) == 0:
                continue
            message[
                message_splitted_index
            ] += f"*{text_converter(dict['title_section'])}*\n"
            for _, row in dict["data"].iterrows():
                if len(message[message_splitted_index]) > 3800:
                    message.append("")
                    message_splitted_index += 1

                job_company_name = text_converter(row["career_page_name"])
                job_title = text_converter(row["title"])
                job_url = str(row["job_url"])
                job_city = text_converter(row["city"])
                job_state = text_converter(row["state"])

                message[message_splitted_index] += f"🏢 {job_company_name}\n"

                if dict["type"] == "hybrid":
                    message[
                        message_splitted_index
                    ] += f"📍 Local: {job_city} \- {job_state}\n"

                message[message_splitted_index] += f"🔗 [{job_title}]({job_url})\n\n"

        message[message_splitted_index] += (
            "\n"
            f"Gostou do projeto? Você pode contribuir com uma ⭐️ no repositório:\n"
            "[GitHub \- Junior Zone](https://github.com/Moscarde/Junior_Zone)"
        )
        return message

    def tag_as_submitted(self):
        self.base_df["submitted"] = "True"
        self.base_df.to_csv(f"data/responses/{self.date}.csv", index=False)


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
        df["date"] = pd.to_datetime(df["published_date"]).dt.strftime("%d/%m/%Y")
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


def text_converter(text):
    #'_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!' must be escaped with the preceding character '\'.
    return (
        str(text)
        .replace(".", "\.")
        .replace("(", "\(")
        .replace(")", "\)")
        .replace("|", "\|")
        .replace("-", "\-")
        .replace("+", "\+")
        .replace("[", "\[")
        .replace("]", "\]")
        .replace("{", "\{")
        .replace("}", "\}")
        .replace("!", "\!")
        .replace("#", "\#")
        .replace("~", "\~")
        .replace("`", "\`")
        .replace(">", "\>")
        .replace("*", "\*")
        .replace("=", "\=")
        .replace("'", "'")
        .replace('"', '"')
        .replace("<", "\<")
    )


if __name__ == "__main__":
    from pprint import pprint
    data = DataHandler("data/2023-11-21", ["dev"])
    pprint(data)
