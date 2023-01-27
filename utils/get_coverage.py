"""Get coverage."""
import json

with open('README.md', 'rb') as file:
    text = file.read()
    text = text.decode("utf-8")
    coverage_atual = text.split('-')[-2]

with open('coverage/coverage.json', 'rb') as json_:
    new_coverage = json.load(json_)['coverage'] + '25'
coverage = coverage_atual, new_coverage
color = 'brightgreen'
text = text.replace(
    f"coverage-{coverage[0]}-{color}", f"coverage-{coverage[1]}-{color}")


with open('README.md', 'wb') as file:
    file.write(bytes(text, "utf-8"))
