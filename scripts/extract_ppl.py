# call examples: assuming you in the mt-exercise-4/scripts folder:
#   python extract_ppl.py ../logs/deen_transformer_regular

import os
import argparse, re
import matplotlib.pyplot as plt


def parse_logs(log_folder):
    log_files = [f for f in os.listdir(log_folder)]

    perplexities = {}
    for log_file in log_files:
        with open(os.path.join(log_folder,log_file), 'r') as file:
            content = file.read()
            pattern = r'ppl:\s+(\d+\.\d+)'

            ppl = list(re.findall(pattern, content))
            perplexities[log_file] = [round(float(p), 4) for p in ppl]

    return perplexities

def print_table(perplexities):
    log_files = list(perplexities.keys())
    header = ['Validation ppl'] + log_files

    print('\t|\t'.join(header))
    print('---' * (sum(len(column) for column in header) + len(header) - 1))

    epochs = [str((i+1)*500) for i in range(len(perplexities[log_files[0]]))]
    for i, epoch in enumerate(epochs):
        row = [str(epoch)]
        for ppl in perplexities.values():
            row.append(str(ppl[i]))
        print('\t|\t'.join(row))

def plot_line_chart(perplexities, output_file="line_plot.png"):
    plt.figure(figsize=(10, 6))
    for log_file, ppl in perplexities.items():
        epochs = [(i+1)*500 for i in range(len(ppl))]
        print(len(epochs))
        plt.plot(epochs, ppl, label=f'{log_file}')

    plt.xlabel('Steps')
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
    lengths = []
    for l, p in perplexities.items():
        print(l, len(p))
        lengths.append(len(p))
    # for each key truncate the list values to the min(lengths)
    for l, p in perplexities.items():
        perplexities[l] = p[:min(lengths)]
    print_table(perplexities)
    # print(perplexities)
    plot_line_chart(perplexities)