from datetime import datetime


class TelegramMessage:
    def __init__(self, filtered_dfs):
        self.raw_date = datetime.now()
        self.message_limit = 3800
        self.header = (
            f"📅 Vagas atualizadas dia: *{self.raw_date.strftime('%d/%m/%Y')}*\n"
            f"Período: *{'Manhã 🌅' if self.raw_date.hour < 12 else 'Tarde 🌇'}*\n\n"
            "No grupo são postadas somente vagas Jr Remotas e Híbridas\n"
            "[Para ver a lista completa acesse a planilha online](https://docs.google.com/spreadsheets/d/1yii99T2zZtG_OFarL_OxuhDVW0uvMmMhw9I2MygaLqc/edit?usp=sharing)\n\n"
            f"Gosta do projeto? Você pode contribuir com uma ⭐️ no repositório:\n"
            "[GitHub \- Junior Zone](https://github.com/Moscarde/Junior_Zone)"
        )

        self.section_dados_image = open(f"pictures/section_dados.jpg", "rb")
        self.section_dev_image = open(f"pictures/section_dev.jpg", "rb")

        self.section_dados_messages = self.contruct_message(
            df_remote=filtered_dfs["dados_remote"],
            df_hybrid=filtered_dfs["dados_hybrid"],
        )

        self.section_dev_messages = self.contruct_message(
            df_remote=filtered_dfs["dev_remote"],
            df_hybrid=filtered_dfs["dev_hybrid"],
        )


    def contruct_message(self, df_remote, df_hybrid):
        message = []
        split_index = 0

        if (len(df_remote) == 0) and (len(df_hybrid) == 0):
            message = (
                "🚫* Nenhuma nova vaga remota / hibrida foi encontrada para essa busca\. *🚫"
                "\n\n"
                "Confira a planilha para ver todas as vagas presenciais, remotas e híbridas através do link:\n"
                "[Planilha com todas as vagas atualizadas](https://docs.google.com/spreadsheets/d/1yii99T2zZtG_OFarL_OxuhDVW0uvMmMhw9I2MygaLqc/edit?usp=sharing)"
        )

        if len(df_remote) > 0:
            message.append(f"🌐 *Vagas Remotas* 🌐 \n\n")

            formatted_vacancies_remote = self.formatter_vacancies(
                df_remote, vacancy_type="remote"
            )

            for vacancy in formatted_vacancies_remote:
                if len(message[split_index]) > self.message_limit:
                    message.append("")
                    split_index += 1

                message[split_index] += vacancy

        if len(df_hybrid) > 0:
            message.append(f"🌍 *Vagas Híbridas* 🌍 \n\n")
            split_index = len(message) - 1

            formatted_vacancies_hybrid = self.formatter_vacancies(
                df_hybrid, vacancy_type="hybrid"
            )

            for vacancy in formatted_vacancies_hybrid:
                if len(message[split_index]) > self.message_limit:
                    message.append("")
                    split_index += 1

                message[split_index] += vacancy
            

        return message

    def formatter_vacancies(self, df, vacancy_type):
        formatted_vacancies = []
        for _, row in df.iterrows():
            job_company_name = self.formatter_string(row["career_page_name"])
            job_title = self.formatter_string(row["title"])
            job_url = row["job_url"]
            job_city = self.formatter_string(row["city"])
            job_state = self.formatter_string(row["state"])

            vacancy = f"🏢 {job_company_name}\n"

            if vacancy_type == "hybrid":
                vacancy += f"📍 Local: {job_city} \- {job_state}\n"

            vacancy += f"🔗 [{job_title}]({job_url})\n\n"

            formatted_vacancies.append(vacancy)

        return formatted_vacancies

    @staticmethod
    def formatter_string(string):
        return (
            str(string)
            .replace(".", "\.")
            .replace("_", "\_")
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

