import timeit

import click
from click.testing import CliRunner

from board import click_main as board_main


@click.command()
@click.option(
    '--n',
    default=100,
    help='Number of runs')
@click.option(
    '--print-output',
    default=False,
    help='Print output of each run')
def main(n, print_output):
    runner = CliRunner()

    if print_output:
        def run():
            print(runner.invoke(board_main).stdout)
    else:
        def run():
            runner.invoke(board_main).stdout

    elapsed = timeit.timeit(run, number=n)
    print(f'Total time for {n} runs: {elapsed} seconds.')
    print(f'Average time per run: {elapsed / n} seconds.')


if __name__ == '__main__':
    main()
