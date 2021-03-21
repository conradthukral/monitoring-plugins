import subprocess


RESULT_OK = 'OK'
RESULT_WARNING = 'WARNING'
RESULT_CRITICAL = 'CRITICAL'
RESULT_UNKNOWN = 'UNKNOWN'


def format_metrics(metrics):
    if not metrics:
        return ""
    formatted_key_values = [f"'{name}'={value}" for name, value in metrics]
    space_separated = " ".join(formatted_key_values)
    return f"|{space_separated}"


def exit_with_monitoring_result(result, message, metrics):
    result_to_exit_code = {
        RESULT_OK: 0,
        RESULT_WARNING: 1,
        RESULT_CRITICAL: 2
    }
    exit_code = result_to_exit_code.get(result, 3)

    formatted_metrics = format_metrics(metrics)
    print(f"{result}: {message}{formatted_metrics}")
    exit(exit_code)


def exit_with_OK(message, metrics=None):
    exit_with_monitoring_result(RESULT_OK, message, metrics)


def exit_with_CRITICAL(message, metrics=None):
    exit_with_monitoring_result(RESULT_CRITICAL, message, metrics)


def run_subprocess(description, command):
    command = command.split(' ')
    process = subprocess.run(command, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, universal_newlines=True, check=False)
    if process.returncode != 0:
        raise Exception(
            f"Error running {description} - error code {process.returncode}, stderr: '{process.stderr.strip()}', stdout: '{process.stdout.strip()}'"
        )
    return process.stdout.strip()
