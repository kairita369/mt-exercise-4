import os
import argparse, re
import matplotlib.pyplot as plt


def parse_logs(log_folder):
    log_files = [f for f in os.listdir(log_folder) if f.startswith('perplexities_')]

    perplexities = {}
    for log_file in log_files:
        with open(log_file, 'r') as file:
            content = file.read()
            pattern = r'\b\d+\.\d+\b'

            ppl = list(re.findall(pattern, content))
            perplexities[log_file[-4]] = ppl

    return perplexities

def print_table(perplexities):
    log_files = list(perplexities.keys())
    header = ['Validation ppl'] + log_files
    print('\t|\t'.join(header))
    print('---' * (sum(len(column) for column in header) + len(header) - 1))

    for i, log_file in enumerate(log_files):
        print('\t|\t'.join([str((i+1)*500)]+perplexities[log_file]))

def plot_line_chart(perplexities, output_file="line_plot.png"):
    plt.figure(figsize=(10, 6))
    for log_file, ppl in perplexities.items():
        epochs = [str((i+1)*500) for i in range(len(ppl))]
        plt.plot(epochs, ppl, label=f'{log_file}')

    plt.xlabel('Epoch')
    plt.ylabel('Perplexity')
    plt.title('Perplexities per Epoch')
    plt.legend()
    plt.grid(True)
    plt.savefig(output_file)
    plt.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Read and print log files in a folder.')
    parser.add_argument('log_folder', type=str, help='Path to the folder containing log files')
    args = parser.parse_args()

    perplexities = parse_logs(args.log_folder)
    print_table(perplexities)
    print(perplexities)
    plot_line_chart(perplexities)