mkdir -p coverage

SUMMARY="$(python3 -m pytest --cov=tests)"
result="$(echo "$SUMMARY" | tail -3 | head -1)"

total=($result)
echo "$total"
COVERAGE=$(echo ${total[3]})
echo "$COVERAGE"

# save in a json file
jq -n --arg cov "$COVERAGE" \
  --arg lab "$LABEL" \
  '{coverage: $cov}' >"coverage/coverage.json"

# change coverage on readme.md
python3 utils/get_coverage.py