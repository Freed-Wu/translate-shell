# shellcheck disable=all
history_complete() {
  local line history_file
  history_file="$($words[1] --print-setting history_file)"
  if [[ -f $history_file ]]; then
    while read -r line; do
      choices+=(${(q)line})
    done < $history_file
  fi
  _arguments "*:word:($choices)"
}
