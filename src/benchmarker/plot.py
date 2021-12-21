import pandas as pd


class Plotter:
    def __init__(self, config, benchmarks):
        self.height = config["height"]
        self.width = config["width"]
        self.theme = config["theme"]
        self.label = config["label"]

        self.benchmarks = benchmarks

        df = pd.DataFrame(benchmarks)
        self.benchmark_df = df
        self.parallel_df = df[df.sequential_time.notnull()]

    def plot_metrics(self):
        plots = []

        df = self.parallel_df

        sizes = df["size"].unique()

        for size in sizes:
            plots.append(self.plot_scatter(df, size, "speedup"))
            plots.append(self.plot_scatter(df, size, "efficiency"))

        return plots

    def plot_scatter(self, df, size, field):
        size_df = df[df["size"] == size]

        pivot = size_df.pivot("threads", "language", field)
        plot = pivot.plot(ylim=(0, None), style=".-", figsize=(8, 8))

        return {"size": size, "metric": field, "figure": plot.figure}

    def plot_times(self):
        return self.plot_bar("time")

    def plot_gflops(self):
        return self.plot_bar("gflops")

    def plot_bar(self, metric):
        plots = []
        sizes = self.benchmark_df["size"].unique()

        for size in sorted(sizes):
            df = self.benchmark_df
            size_df = df[df["size"] == size]

            pivot = size_df.pivot("threads", self.label, metric)

            plot = pivot.plot.bar(
                title=f"N={size}",
                ylabel=metric.capitalize(),
                xlabel="Threads",
                figsize=(self.width, self.height),
                rot=0,
                colormap=self.theme,
            )

            plots.append(
                {
                    "size": size,
                    "figure": plot.figure,
                    "metric": metric,
                }
            )

        return plots
