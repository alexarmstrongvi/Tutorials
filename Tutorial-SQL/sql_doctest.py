#!/usr/bin/env python
from pathlib import Path
import sqlite3
from time import perf_counter_ns
from typing import Iterable
import logging
import argparse

log = logging.getLogger('SQL-Doctest')


################################################################################
def main():
    args = parse_argv()
    logging.basicConfig(
        level  = args.log_level,
        # format = "%(levelname)8s | %(name)s :: %(message)s",
        format = "%(message)s",
        force  = True,
    )
    assert args.path.is_file()
    with args.path.open('r') as fp:
        lines = fp.readlines()

    n_failures = 0
    elapsed = {}
    i = 0
    with sqlite3.connect(':memory:') as conn:
        cur = conn.cursor()
        for i, (sql_script, test_query, answer) in enumerate(iterate_tests(lines)):
            if sql_script:
                try:
                    cur.executescript(sql_script)
                except sqlite3.OperationalError:
                    log.critical(f'Exception running SQL setup commands:\n{sql_script}')
                    raise
            try:
                start = perf_counter_ns()
                result = cur.execute(test_query).fetchall()
                elapsed[(i, test_query)] = perf_counter_ns() - start
            except sqlite3.OperationalError:
                log.critical(f'Exception running SQL query:\n{test_query}')
                raise
            if result != answer: 
                n_failures += 1
                log.warning('❌ Test Failed')
                log.warning(f'sqlite3> {test_query.strip()}')
                log.warning(repr(result))
                log.warning(f'\nExpected result:\n{answer!r}\n')

    elapsed = [
        (k[1], elapsed[k])
        for k in sorted(elapsed, key=elapsed.get, reverse=True)
    ]
    log.info('===== Summary =====')
    log.info('Slowest queries')
    n = 2
    for query, t in elapsed[:n]:
        log.info(f'{t/10**3}ms:\n{query}')
    log.info('Next slowest: ' + ', '.join(f'{t:,d}' for _, t in elapsed[n:n+5]))

    log.info('===== Result =====')
    if n_failures == 0:
        log.info(f'✅ All {i+1} tests passed!')
    else:
        log.info(f'🟨 {i+1-n_failures}/{i+1} tests passed!')


def iterate_tests(lines: list[str]) -> Iterable[tuple[str, str, str]]:

    i = 0
    nth_test = 0
    while i < len(lines):
        # Get SQL setup
        start, i = i, take_until(
            lambda l, i : l[i].startswith('SELECT') or l[i].startswith('WITH'),
            lines, i,
        )
        if i is None:
            break
        sql_script = ''.join(lines[start:i])

        # Get test query
        start, i = i, take_until(
            lambda l, i : (
                l[i].startswith('-- EQUALS')
                or l[i] == "\n"
                or (l[i+1].startswith('SELECT') and not l[i].startswith('WITH'))
            ),
            lines, i,
        )
        if i is None:
            break
        elif i == start: # Two SELECT lines back-to-back
            i += 1
        test_query = ''.join(lines[start:i])

        # Check
        if not lines[i].startswith('-- EQUALS'):
            nth_test += 1
            log.debug(f'\n==== TEST {nth_test} =====')
            log.debug('No answer. Skipping test query\n' + test_query)
            continue

        # Get test answer
        if lines[i].rstrip() != '-- EQUALS':
            # One-line answer
            answer = lines[i][len('-- EQUALS'):]
            i += 1
        else:
            start, i = i, take_until(
                lambda l, i : not l[i].startswith('-- '),
                lines, i,
            )
            if i is None:
                break
            answer = ''.join(x[3:] for x in lines[start+1:i])

        answer = answer.replace('NULL', 'None')

        # Checks
        if test_query == "" or answer == "":
            break

        # DEBUG
        nth_test += 1
        if any(l and not l.startswith('--') for l in sql_script.split('\n')):
            log.debug('\n==== SETUP =====')
            log.debug(f'sql_script:\n{sql_script}')
        log.debug(f'\n==== TEST {nth_test} =====')
        log.debug(f'sqlite3> {test_query.strip()}')
        log.debug(answer.strip())

        yield sql_script, test_query, eval(answer)

def take_until(pred, lines, i=0) -> int | None:
    while i < len(lines) and not pred(lines, i):
        i += 1
    if i >= len(lines):
        return None
    return i

def parse_argv() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'path',
        type = Path,
        help = 'SQL file to run',
    )
    parser.add_argument(
        "-l",
        "--log-level",
        choices = ("CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"),
        default = 'INFO',
        help    = "Root logging level",
    )
    return parser.parse_args()

if __name__ == '__main__':
    main()
