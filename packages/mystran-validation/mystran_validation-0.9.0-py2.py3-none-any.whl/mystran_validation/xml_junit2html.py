from io import StringIO
from pathlib import Path
import xml.etree.ElementTree as ET
from collections import defaultdict
from jinja2 import Environment, BaseLoader


class TestSuite:
    """TestSuite: container for all testsuite test cases. Normally, this is only one."""

    def __init__(self, xml):
        self.meta = xml.attrib
        self.testcases = defaultdict(list)
        for tc in xml.findall("./testcase"):
            tcobject = TestCase(tc)
            self.testcases[tcobject.classname].append(tcobject)
        self.testcases = dict(self.testcases)

    def __repr__(self):
        return "testsuite errors={errors} failures={failures} skipped={skipped} tests={tests} time={time} timestamp={timestamp}".format(
            **self.meta
        )


class TestCase:
    def __init__(self, xml):
        for k, v in xml.attrib.items():
            setattr(self, k, v)
        self.properties = {}
        for prop in xml.findall("./properties/property"):
            self.properties[prop.attrib["name"]] = prop.attrib["value"]
        # ---------------------------------------------------------------
        # skipped
        skipped = xml.find("./skipped")
        if skipped is not None:
            self.skipped = skipped.attrib
        else:
            self.skipped = None
        # ---------------------------------------------------------------
        # failed
        failure = xml.find("./failure")
        if failure is not None:
            self.failure = failure.attrib
        else:
            self.failure = None

    def __repr__(self):
        s = f"{self.classname}::{self.name}"
        if self.skipped:
            s += " (skipped)"
        if self.failure:
            s += " (failed)"
        return s


def parse_xml(filepath):
    """parse JUnit  XML file and return a tuple of `TestSuite` instances"""
    fpath = Path(filepath)
    assert fpath.exists()
    tree = ET.parse(filepath)
    root = tree.getroot()
    # get all testsuites
    return tuple((TestSuite(ts) for ts in root.findall("./testsuite")))


MASTER_MS_TPL = """
MYSTRAN TESTING
===============

{% for testsuite in testsuites %}
Test Suite "{{ testsuite.meta["name"] }}"
----------------------------------

{% for ini_name, testcases in testsuite.testcases.items() %}
### {{ ini_name }}
{% for tc in testcases %}
#### {{ tc }}
{% if tc.skipped %}**SKIPPED**: {{tc.skipped['message']}} {% endif %}
{% if tc.failure %}**FAILED**: \n{{tc.failure['message']}} {% endif %}
{% endfor %}

{% endfor %}{# end of test cases #}
{% endfor %}{# end of test suites #}
"""

MASTER_HTML_TPL = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>mystran-testing.xml</title>
    <style type="text/css">
        body {
    background-color: white;
    padding-bottom: 20em;
    margin: 0;
    min-height: 15cm;
}

h1, h2, h3, h4, h5, h6, h7 {
    font-family: sans-serif;
}

h1 {
    background-color: #007acc;
    color: white;
    padding: 3mm;
    margin-top: 0;
    margin-bottom: 1mm;
}

.footer {
    font-style: italic;
    font-size: small;
    text-align: right;
    padding: 1em;
}

.testsuite {
    padding-bottom: 2em;
    margin-left: 1em;
}

.proplist {
    width: 100%;
    margin-bottom: 2em;
    border-collapse: collapse;
    border: 1px solid grey;
}

.proplist th {
    background-color: silver;
    width: 5em;
    padding: 2px;
    padding-right: 1em;
    text-align: left;
}

.proplist td {
    padding: 2px;
}

.index-table {
    width: 90%;
    margin-left: 1em;
}

.index-table td {
    vertical-align: top;
    width: 50%;
}

.failure-index {

}

.toc {
    margin-bottom: 2em;
    font-family: monospace;
}

.stdio, pre {
    min-height: 1em;
    background-color: #1e1e1e;
    color: silver;
    padding: 0.5em;
}
.tdpre {
    background-color: #1e1e1e;
}

.test {
    margin-left: 0.5cm;
}

.outcome {
    border-left: 1em;
    padding: 2px;
}

.outcome-failed {
    border-left: 1em solid lightcoral;
}

.stats-table {
}

.stats-table td {
    min-width: 4em;
    text-align: right;
}

.stats-table .failed {
    background-color: lightcoral;
}

.stats-table .passed {
    background-color: lightgreen;
}

.matrix-table {
    table-layout: fixed;
    border-spacing: 0;
    width: available;
    margin-left: 1em;
}

.matrix-table td {
    vertical-align: center;
}

.matrix-table td:last-child {
    width: 0;
}

.matrix-axis-name {
    white-space: nowrap;
    padding-left: 0.5em;
    border-left: 1px solid black;
    border-top: 1px solid black;
}

.matrix-axis-line {
    border-left: 1px solid black;
    width: 0.5em;
}

.matrix-classname {
    text-align: left;
    width: 100%;
    border-top: 2px solid grey;
    border-bottom: 1px solid silver;
}

.matrix-casename {
    text-align: left;
    font-weight: normal;
    font-style: italic;
    padding-left: 1em;
    border-bottom: 1px solid silver;
}

.matrix-result {
    display: block;
    width: 1em;
    text-align: center;
    padding: 1mm;
    margin: 0;
}

.matrix-result-combined {
    white-space: nowrap;
    padding-right: 0.2em;
    text-align: right;
}

.matrix-result-failed {
    background-color: lightcoral;
}

.matrix-result-passed {
    background-color: lightgreen;
}

.matrix-result-skipped {
    background-color: lightyellow;
}
    </style>
</head>
<body style="margin-bottom: 0px !important>
<h1>MYSTRAN TESTING</h1>

{% for testsuite in testsuites %}
<div class="testsuite">
<h2>Test Suite "{{ testsuite.meta["name"] }}"</h2>

{% for ini_name, testcases in testsuite.testcases.items() %}
<hr/>
<h3>Test-case {{ ini_name }}</h3>
{% for tc in testcases %}
<h4>Test {{ tc }}</h4>
<p>
{% if tc.skipped %}<b>SKIPPED</b>: {{tc.skipped['message']}} {% endif %}
{% if tc.failure %}<b>FAILED</b>: 
    <pre>{{tc.failure['message']}}</pre>
{% endif %}
</p>
{% endfor %}

{% endfor %}{# end of test cases #}
</div>
{% endfor %}{# end of test suites #}
</body>
</html>
"""


def xml2md(xmlfpath):
    tss = parse_xml(xmlfpath)
    rtemplate = Environment(loader=BaseLoader).from_string(MASTER_MS_TPL)
    return rtemplate.render({"testsuites": tss})


def xml2html(xmlfpath):
    tss = parse_xml(xmlfpath)
    rtemplate = Environment(loader=BaseLoader).from_string(MASTER_HTML_TPL)
    return rtemplate.render({"testsuites": tss})
