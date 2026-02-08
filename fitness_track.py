import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

class FitnessTracker:
    def __init__(self, inp_file):
        self.data = pd.read_csv(inp_file)

    def calculate_normalise_score(self, score, min_score, max_score):
        normalised_score = int(max(((score - min_score) / (max_score - min_score)), 0) * 100)
        return normalised_score

    def calculate_average_scores(self, *args):
        return round(sum(args)/len(args),0)

    def process_results(self):
        results = []

        for _, row in self.data.iterrows():
            pull_up_norm = self.calculate_normalise_score(row['pull_up'], 1, 14)
            fivekm_time_norm = self.calculate_normalise_score(row['fivekm_time'], 32, 22.5)
            bench_press_norm = self.calculate_normalise_score(row['bench_press'], 47, 98)
            squat_norm = self.calculate_normalise_score(row['squat'], 60, 130)
            overhead_press_norm = self.calculate_normalise_score(row['overhead_press'], 30, 64)
            deadlift_norm = self.calculate_normalise_score(row['deadlift'], 90, 150)

            overall_score = self.calculate_average_scores(
                 pull_up_norm, fivekm_time_norm,
                 bench_press_norm, squat_norm, overhead_press_norm, deadlift_norm
            )

            results.append({
                'date': row['date'],
                'overall_score': overall_score,
                'pull_up_norm': pull_up_norm,
                'fivekm_time_norm': fivekm_time_norm,
                'bench_press_norm': bench_press_norm,
                'squat_norm': squat_norm,
                'overhead_press_norm': overhead_press_norm,
                'deadlift_norm':deadlift_norm,
            })

        results_df = pd.DataFrame.from_dict(results)
        return results_df

    def plot_results(self, results_df):
        data = results_df
        data['date'] = pd.to_datetime(
                data['date'],
                format='%d/%m/%Y',
            )
        data.set_index('date', inplace=True)
        ax = sns.lineplot(
            data=data[['pull_up_norm',
                       'fivekm_time_norm',
                       'bench_press_norm',
                       'squat_norm',
                       'overhead_press_norm',
                       'deadlift_norm'
                       ]],
                       )

        sns.lineplot(data=data['overall_score'], color='black', linewidth=3, label='Overall Score')
        for line in ax.lines:
            x_data = line.get_xdata()
            y_data = line.get_ydata()
            if len(x_data) > 0:
                x = x_data[-1]
                y = y_data[-1]
                is_overall = line.get_label() == 'Overall Score'
                ax.annotate(
                    f'{y:.0f}',
                    xy=(x, y),
                    xytext=(7, 0),
                    textcoords="offset points",
                    color=line.get_color(),
                    va="center",
                    fontweight='bold' if is_overall else 'normal',
                    fontsize=10 if is_overall else 9
                )

        plt.title('Fitness level over time')
        plt.xlabel('Date')
        plt.ylabel('Level')
        plt.ylim(0, 100)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('plots/fitness_score.png')
        plt.close()

    def run(self):
        # process results
        results_df = self.process_results()
        self.plot_results(results_df)

inp_file = 'input_pbs.csv'
fitness_tracker = FitnessTracker(inp_file)
fitness_tracker.run()