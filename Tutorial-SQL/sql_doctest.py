#!/usr/bin/env python

# Standard library
from pathlib import Path
import sqlite3
from sqlite3 import OperationalError
from time import perf_counter_ns
from typing import Iterable
import logging
import difflib
import argparse
import itertools

# Globals
log = logging.getLogger('doctest')

################################################################################
def main():
    args = parse_argv()
    logging.basicConfig(
        level  = args.log_level,
        # format = "%(levelname)8s | %(name)s :: %(message)s",
        format = "%(message)s",
        force  = True,
    )
    with args.path.open('r') as fp:
        lines = fp.readlines()

    n_failures = 0
    n_passed = 0
    n_skipped = 0
    query_durations = {}
    i = 0
    with sqlite3.connect(':memory:') as conn:
        cur = conn.cursor()
        for i, (sql_script, test_query, answer, test_type) in enumerate(iterate_tests(lines)):
            # DEBUG
            if any(l and not l.startswith('--') for l in sql_script.split('\n')):
                log.debug('\n==== SETUP =====')
                log.debug(f'sql_script:\n{sql_script}')
            log.debug(f'\n==== TEST {i+1} =====')
            log.debug(f'sqlite3> {test_query.strip()}')
            log.debug(repr(answer))

            # # Determine test type
            # test_type = None
            # if isinstance(answer, list):
            #     test_type = 'EQUALS'
            # elif isinstance(answer, tuple):
            #     test_type = 'RAISES'
            # elif answer is None:
            #     test_type = None
            # else:
            #     log.error('Unable to determine test type')

            # Run any setup statements
            if sql_script:
                try:
                    cur.executescript(sql_script)
                except OperationalError:
                    log.critical(f'Exception running SQL setup commands:\n{sql_script}')
                    raise

            # Run test query
            elapsed = 0
            try:
                start = perf_counter_ns()
                result = cur.execute(test_query).fetchall()
                elapsed = perf_counter_ns() - start
                query_durations[(i, test_query)] = elapsed
            except sqlite3.OperationalError as e:
                if test_type == 'RAISES':
                    # NOTE: Exceptions cannot be checked for equality so they
                    # need to have their type and str compared separately
                    result = (type(e), str(e))
                else:
                    log.critical(f'Exception running SQL query:\n{test_query}')
                    raise

            # Check answer
            if test_type == 'DEBUG':
                print(f'sqlite3> {test_query.strip()}')
                headers = tuple(x[0] for x in cur.description)
                print_tuple_table(result, headers)
                print(f'{elapsed/10**3}ms')
                print()
            elif answer is None:
                log.debug('Query has no test:\nsqlite3>%s', test_query)
                n_skipped += 1
            elif result != answer:
                n_failures += 1
                log.warning('❌ Test Failed')
                log.warning(f'sqlite3> {test_query.strip()}')
                if test_type == 'EQUALS':
                    result_str = [repr(x) for x in result]
                    expected_str = [repr(x) for x in answer]
                    diff_gen = difflib.ndiff(expected_str, result_str)
                    diff = diff_gen
                    # diff = [l for l in diff_gen if l[0] in {'+','-'}]
                    log.warning('\n'.join(diff) + '\n')
                    # log.warning('Expected vs Result\n%s', '\n'.join(diff))
                else:
                    log.warning(repr(result))
                    log.warning(f'\nExpected result:\n{answer!r}\n')

            else:
                n_passed += 1

    elapsed_list = [
        (k[1], query_durations[k])
        for k in sorted(query_durations, key=query_durations.get, reverse=True)
    ]
    log.info('===== Summary =====')
    log.info('Slowest queries')
    n = 2
    for query, t in elapsed_list[:n]:
        log.info(f'{t/10**3}ms:\n{query}')
    log.info('Next slowest: ' + ', '.join(f'{t/10**3}ms' for _, t in elapsed_list[n:n+5]))

    log.info('===== Result =====')
    n_tests = n_passed + n_failures
    if n_skipped > 0:
        log.info(f'{n_skipped}/{i+1} queries not tested!')
    if n_failures == 0:
        log.info(f'✅ All {n_tests} tests passed!')
    else:
        log.info(f'🟨 {n_passed}/{n_tests} tests passed!')

def iterate_tests(lines):
    in_comment   = False
    in_statement = False
    i_script     = 0
    i_query      = None

    i = -1
    while (i := i+1) < len(lines):
        line = lines[i].split('--', maxsplit=1)[0].strip()

        if line == '':
            continue

        # Skip comments
        if line.startswith('/*'):
            in_comment = True
        if line.endswith('*/'):
            in_comment = False
            continue
        if in_comment:
            continue

        # Flag start of SQL statement
        if not in_statement:
            in_statement = True
            statement_type = line.split(maxsplit=1)[0].upper()
            if statement_type in {'SELECT', 'VALUES', 'WITH'}:
                i_query = i

        # Handle end of SQL statement
        if line.endswith(';'):
            in_statement = False
            if i_query is None:
                continue

            # Extract script setup and query
            sql_script = ''.join(lines[i_script:i_query])
            sql_query  = ''.join(lines[i_query:i+1])

            # Parse answer
            test_keyword = None
            for keyword in ['EQUALS', 'RAISES', 'DEBUG']:
                if lines[i+1].startswith(f'-- {keyword}'):
                    test_keyword = keyword
                    break

            answer = None
            if test_keyword is not None and test_keyword != 'DEBUG':
                i += 1

                answer_lines = [lines[i][len(f'-- {test_keyword}'):].strip()]
                while i+1 < len(lines) and lines[i+1].startswith('--'):
                    i += 1
                    answer_lines.append(lines[i][len('--'):].strip())
                answer_str = '\n'.join(answer_lines)

                if test_keyword == "EQUALS":
                    answer_str = answer_str.replace('NULL', 'None')
                answer = eval(answer_str)

            yield sql_script, sql_query, answer, test_keyword

            # Reset trackers
            i_script = i+1
            i_query = None

################################################################################
def iterate_tests_old(lines: list[str]) -> Iterable[tuple[str, str, str]]:
    i = 0
    nth_test = 0
    while i < len(lines):
        # Get SQL setup
        start, i = i, take_until(
            lambda l, i : any(l[i].startswith(x) for x in ('SELECT', 'WITH', 'VALUES')),
            lines, i,
        )
        if i is None:
            break
        sql_script = ''.join(lines[start:i])

        # Get test query
        start, i = i, take_until(
            lambda l, i : (
                (i > 0 and l[i-1].split('--', maxsplit=1)[0].rstrip().endswith(';'))
                # or l[i].startswith('-- EQUALS')
                # or l[i] == "\n"
                # or (i+1 < len(l) and l[i+1].startswith('SELECT') and not l[i].startswith('WITH'))
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

def print_tuple_table(tuple_list, headers=None):
    """
    Print a list of tuples as a formatted table.

    Args:
        tuple_list (list): List of tuples to print
    """
    if not tuple_list:
        return

    # Determine column widths if not provided
    column_widths = [
        max(len(str(item)) for item in col)
        for col in zip(*tuple_list)
    ]

    # Print header separator
    separator = '+' + '+'.join('-' * (width + 2) for width in column_widths) + '+'
    print(separator)

    # Print each row
    it = zip(itertools.repeat(False),tuple_list)
    if headers is not None:
        it = itertools.chain([(True,headers)], it)
    for is_header, row in it:
        formatted_row = '| ' + ' | '.join(
            f'{str(item):^{width}}' for item, width in zip(row, column_widths)
        ) + ' |'
        print(formatted_row)
        if is_header:
            print(separator)
    print(separator)

################################################################################
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
