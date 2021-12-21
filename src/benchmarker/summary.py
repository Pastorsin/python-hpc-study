import pandas as pd


class Summary:
    DECIMAL_PLACES = 3

    def __init__(self, benchmarks, metric):
        self.benchmarks = benchmarks
        self.metric = metric
        self.df = pd.DataFrame(benchmarks)

    def generate(self):
        summaries = []

        for language in self.languages():
            summaries.append(
                {
                    "language": language,
                    "metric": self.metric,
                    "df": self._summary_df(
                        {**self.header(language), **self.body(language)}
                    ),
                }
            )

        return summaries

    def header(self, language):
        return {"T/N": self.threads(language)}

    def body(self, language):
        return {
            size: self.times(language, size) for size in self.sizes(language)
        }

    def languages(self):
        return set(self.df.language)

    def threads(self, language):
        df = self._language_df(language)

        return sorted(set(df["threads"].values))

    def sizes(self, language):
        df = self._language_df(language)

        return set(df["size"])

    def times(self, language, size):
        sizes_group = self._language_df(language).groupby("size")
        group_metrics = sizes_group.get_group(size)[self.metric]

        return group_metrics.round(self.DECIMAL_PLACES).values

    def _language_df(self, language):
        df = self.df

        return df[df.language == language][["threads", self.metric, "size"]]

    def _summary_df(self, summary_data):
        return pd.DataFrame(summary_data).set_index("T/N")
