import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pathlib import Path
import json


class FitnessTracker:
    def __init__(self):
        self.BASE_DIR = Path(__file__).resolve().parent
        inp_file = self.BASE_DIR / "input_pbs.csv"
        target_file = self.BASE_DIR / "target.json"
        self.data = pd.read_csv(inp_file)

        self.score_bounds = self.load_targets(target_file)

    def load_targets(self, path):
        with open(path) as file:
            return json.load(file)

    def calculate_normalise_score(self, score, min_score, max_score):
        normalised_score = int(max(((score - min_score) / (max_score - min_score)), 0) * 100)
        return normalised_score

    def calculate_average_scores(self, *args):
        return round(sum(args)/len(args),0)

    def process_results(self):
        results = []

        for _, row in self.data.iterrows():
            pull_up_norm = self.calculate_normalise_score(
                row['pull_up'], 
                self.score_bounds['pull_up']['min'], 
                self.score_bounds['pull_up']['max']
            )

            fivekm_time_norm = self.calculate_normalise_score(
                row['fivekm_time'], 
                self.score_bounds['fivekm_time']['min'], 
                self.score_bounds['fivekm_time']['max']
            )

            bench_press_norm = self.calculate_normalise_score(
                row['bench_press'], 
                self.score_bounds['bench_press']['min'], 
                self.score_bounds['bench_press']['max']
            )

            squat_norm = self.calculate_normalise_score(
                row['squat'], 
                self.score_bounds['squat']['min'], 
                self.score_bounds['squat']['max']
            )

            overhead_press_norm = self.calculate_normalise_score(
                row['overhead_press'], 
                self.score_bounds['overhead_press']['min'], 
                self.score_bounds['overhead_press']['max']
            )

            deadlift_norm = self.calculate_normalise_score(
                row['deadlift'], 
                self.score_bounds['deadlift']['min'], 
                self.score_bounds['deadlift']['max']
            )


            overall_score = self.calculate_average_scores(
                 pull_up_norm, fivekm_time_norm,
                 bench_press_norm, squat_norm, overhead_press_norm, deadlift_norm
            )

            results.append({
                'date': row['date'],
                'Overall Score': overall_score,
                'Pull up': pull_up_norm,
                '5K': fivekm_time_norm,
                'Bench press': bench_press_norm,
                'Squat': squat_norm,
                'Overhead press': overhead_press_norm,
                'Deadlift':deadlift_norm,
                'Pull up_raw': row['pull_up'],
                '5K_raw': row['fivekm_time'],
                'Bench press_raw': row['bench_press'],
                'Squat_raw': row['squat'],
                'Overhead press_raw': row['overhead_press'],
                'Deadlift_raw': row['deadlift']

            })

        results_df = pd.DataFrame.from_dict(results)
        print(results_df)
        return results_df

    def plot_results(self, results_df):
        data = results_df
        data['date'] = pd.to_datetime(
                data['date'],
                format='%d/%m/%Y',
            )
        data.set_index('date', inplace=True)

        metrics = ['5K', 'Bench press', 'Deadlift', 'Overhead press', 'Pull up', 'Squat']
        fig, ax = plt.subplots(figsize=(8, 10))
        sns.lineplot(
            data=data[[
                       '5K',
                       'Bench press',
                       'Deadlift',
                       'Overhead press',
                       'Pull up',
                       'Squat'
                       ]],
                       )
        

        sns.lineplot(data=data['Overall Score'], color='black', linewidth=3, label='Overall Score')
        last_row = data.iloc[-1]
        last_date = data.index[-1]
        table_rows = []
        for metric in metrics:
            y_norm = data[metric].iloc[-1]      # Position on the graph
            label_raw = data[f'{metric}_raw'].iloc[-1] # The text to show
             # Collect values for the summary table
            table_rows.append([metric, f"{label_raw}", f"{y_norm:.2f}"])

            
            ax.annotate(
                f' {y_norm}', 
                xy=(last_date, y_norm),
                textcoords="offset points", 
                xytext=(5, 0), 
                va='center',
                fontweight='bold',
                color='grey'
            )
        
        ax.annotate(
            f' {last_row["Overall Score"]:.0f}', # Show the normalised result
            xy=(last_date, last_row["Overall Score"]),
            textcoords="offset points", xytext=(5, 0), va='center', 
            fontsize=10, fontweight='bold', color='black'
        )



        # Month + year labels (e.g. Jan 2025)
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
        plt.title('Fitness level over time')
        plt.xlabel('Date')
        plt.ylabel('Fitness Level')
        plt.ylim(0, 100)
        plt.xticks(rotation=45)

        # Convert your collected data into a matrix/list format for matplotlib
        columns = ["Metric",  "Raw Score", "Normalised Score"]

        # Move the plot area up to leave 45% space at the bottom for the table
        plt.subplots_adjust(bottom=0.45)

        # Render the table under the x-axis
        summary_table = plt.table(
            cellText=table_rows,
            colLabels=columns,
            loc="bottom",
            cellLoc="center",
            bbox=[0.0, -0.70, 1.0, 0.45]
        )

        summary_table.set_fontsize(11)  

        for cell in [summary_table[0, c] for c in range(3)]:
            cell.set_text_props(fontweight="bold", color="#1A365D")

        # plt.tight_layout()
        out_file = self.BASE_DIR /"fitness_score.png"
        if out_file.exists():
            out_file.unlink()
        plt.savefig(out_file)
        plt.close()

    def run(self):
        # process results
        results_df = self.process_results()
        self.plot_results(results_df)


fitness_tracker = FitnessTracker()
fitness_tracker.run()