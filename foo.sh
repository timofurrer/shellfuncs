bar() {
    local STDOUT="$1"
    local STDERR="$2"

    echo "${STDOUT}"
    echo "${STDERR}" >&2

    return 0
}
