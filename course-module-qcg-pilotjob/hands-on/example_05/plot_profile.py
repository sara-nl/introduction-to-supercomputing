import sys
import matplotlib.pyplot as plt
import matplotlib
"""
Create a profile plot based on the Slurm outputfile of example_05
Usage

module load 2024
module load SciPy-bundle/2024.05-gfbf-2024a

python plot_profile.py <<<slurm_output_file>>>
"""


def extract_profile(fname):
    """
    Extract profile from Slurm output file
    @param fname: filename
    @returns duration of slurm job, list of events
    """
    start = None
    end = None
    events = []
    with open(fname, "r") as fp:
        for line in fp:
            cols = line.split()
            if cols[0] == "START":
                start = float(cols[1])
            if cols[0] == "END":
                end = float(cols[1])
            if cols[0] == "TASK":
                cpu = int(cols[1])
                a = float(cols[2])
                b = float(cols[3])
                events += [(cpu, a, b)]
    return (end-start, [(e[0], e[1]-start, e[2]-start) for e in events])


def plot_profile(total_duration, events, file_name=None):
    """
    Plot the profile.
    @param total_duration
    @param events list if events
    @param file_name: PNG file name
    """
    min_cpu = 100000
    max_cpu = -1
    for e in events:
        if e[0] < min_cpu:
            min_cpu = e[0]
        if e[0] > max_cpu:
            max_cpu = e[0]
    num_cpus = max_cpu - min_cpu + 1
    colors = matplotlib.colormaps.get_cmap('Set3')
    num_colors = 12

    plt.figure(figsize=(12, (0.2 * (1 + num_cpus))))
    plt.axis([0, total_duration, -0.5, num_cpus])

    i = 0
    for e in events:
        y = e[0] - min_cpu
        left = e[1]
        right = e[2]
        plt.barh(y,
                 right-left,
                 left=left,
                 color=colors(i % num_colors),
                 height=1.0,
                 edgecolor='black')
        i = i + 1

    plt.yticks(ticks=range(num_cpus + 1))
    plt.title('')
    plt.xlabel('time')
    plt.ylabel('CPU')
    plt.grid(True, which='both', axis='x', linestyle='--', alpha=0.3)
    plt.tight_layout()
    if file_name is None:
        plt.show()
    else:
        plt.savefig(file_name)


def main():
    input_file = sys.argv[1]
    (job_duration, events) = extract_profile(input_file)
    plot_profile(job_duration, events, f'{input_file}.png')


if __name__ == "__main__":
    main()
