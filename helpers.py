RESULT_OK = 'OK'
RESULT_WARNING = 'WARNING'
RESULT_CRITICAL = 'CRITICAL'
RESULT_UNKNOWN = 'UNKNOWN'

def exit_with_monitoring_result(result, message):
    result_to_exit_code = {
        RESULT_OK: 0,
        RESULT_WARNING: 1,
        RESULT_CRITICAL: 2
    }
    exit_code = result_to_exit_code.get(result, 3)
    
    print(f"{result}: {message}")
    exit(exit_code)

def exit_with_OK(message):
    exit_with_monitoring_result(RESULT_OK, message)

def exit_with_CRITICAL(message):
    exit_with_monitoring_result(RESULT_CRITICAL, message)