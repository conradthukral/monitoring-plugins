#!/usr/bin/python3
"""
Runs rspamc stat and parses its output.

Example output:
Results for command: stat (0.004 seconds)
Messages scanned: 37908
Messages with action reject: 14302, 37.72%
Messages with action soft reject: 0, 0.00%
Messages with action rewrite subject: 0, 0.00%
Messages with action add header: 4519, 11.92%
Messages with action greylist: 3884, 10.24%
Messages with action no action: 15203, 40.10%
Messages treated as spam: 18821, 49.64%
Messages treated as ham: 19087, 50.35%
Messages learned: 3
Connections count: 10121
Control connections count: 153
Pools allocated: 238626
Pools freed: 238606
Bytes allocated: 34.81MiB
Memory chunks allocated: 129
Shared chunks allocated: 16
Chunks freed: 0
Oversized chunks: 2640
Statfile: BAYES_SPAM type: redis; length: 0; free blocks: 0; total blocks: 0; free: 0.00%; learned: 3; users: 1; languages: 0
Statfile: BAYES_HAM type: redis; length: 0; free blocks: 0; total blocks: 0; free: 0.00%; learned: 0; users: 0; languages: 0
Total learns: 3
"""
import re
import itertools
import helpers


def get_stats_output():
    return helpers.run_subprocess('rspamd stats', 'sudo rspamc stat')


def parse_actions(stats_output):
    regex = re.compile(r"Messages with action ([^:]+): (\d+)")
    for name, count in regex.findall(stats_output):
        sanitized_name = name.replace(' ', '_')
        prefixed_name = f"action_{sanitized_name}"
        yield (prefixed_name, int(count))


def parse_results(stats_output):
    regex = re.compile(r"Messages treated as ([^:]+): (\d+)")
    for name, count in regex.findall(stats_output):
        sanitized_name = name.replace(' ', '_')
        prefixed_name = f"result_{sanitized_name}"
        yield (prefixed_name, int(count))


def parse_single_value(value_name, stats_output):
    regex = re.compile(f"{value_name}: (\\d+)")
    results = regex.findall(stats_output)
    if len(results) != 1:
        raise Exception(
            f"Error reading rspamc stat output - expected exactly one {value_name} in {stats_output}"
        )
    return int(results[0])


def parse_simple_values(stats_output):
    yield ('messages_scanned', parse_single_value("Messages scanned", stats_output))
    yield ('messages_learned', parse_single_value("Messages learned", stats_output))


def parse_stats(stats_output):
    return itertools.chain(
        parse_simple_values(stats_output),
        parse_actions(stats_output),
        parse_results(stats_output)
    )


try:
    stats_output = get_stats_output()
except Exception as e:
    helpers.exit_with_CRITICAL(e)

message = stats_output.splitlines()[0]
helpers.exit_with_OK(message, parse_stats(stats_output))
