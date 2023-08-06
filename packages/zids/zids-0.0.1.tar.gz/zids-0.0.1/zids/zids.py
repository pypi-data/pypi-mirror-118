import markdown
import jinja2

import argparse
import sys

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{{{ title }}}</title>
    <link rel="stylesheet" href="https://zgul.de/interactive-docs.min.css" />
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <div class="container-fluid">
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarSupportedContent">
                <ul class="navbar-nav">
                    <li class="nav-item d-flex align-items-center">
                        <button
                            class="btn btn-sm btn-primary"
                            data-bs-toggle="modal"
                            data-bs-target="#customize-docs">
                            Customize Docs
                        </button>
                    </li>
                </ul>
            </div> <!-- /.collapse .navbar-collapse -->
        </div> <!-- /.container-fluid -->
    </nav>

    <div id="app" class="container space-y">
        {% if title %}<h1 class="text-center">{{{ title }}}</h1>{% endif %}
        {% if preamble %}{{{ preamble }}}{% endif %}
        {% if prereqs %}
            <div class="alert alert-info">
                <button type="button" class="btn-close float-end" data-bs-dismiss="alert" aria-label="Close"></button>
                <h2>Prerequisites</h2>
                <ul>
                    {% for prereq in prereqs %}
                    <li>{{{ prereq }}}</li>
                    {% endfor %}
                </ul>
            </div>
        {% endif %}

        {{{ body }}}

        <div class="modal fade" id="customize-docs" tabindex="-1" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Customize These Docs</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">

                        <div class="form-group" v-for="k in Object.keys(vars)">
                            <label for="domain">{{ k }}</label>
                            <input class="form-control"
                                   v:id="k"
                                   v-model="vars[k]"
                                   v-bind:class="{'is-invalid': vars[k].length === 0}" />
                        </div>

                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        <button
                            @click="updateQueryParams"
                            type="button"
                            class="btn btn-primary"
                            data-bs-dismiss="modal"
                            data-bs-toggle="tooltip"
                            data-bs-placement="top"
                            title="Persist these values in the url query string so they can be shared" >
                            Save changes
                        </button>
                    </div>
                </div>
            </div>
        </div>

    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/js/bootstrap.bundle.min.js" integrity="sha384-JEW9xMcG8R+pH31jmWH6WWP0WintQrMb4s7ZOdauHnUtxwoG2vI5DkLtS3qm9Ekf" crossorigin="anonymous"></script>
    <script src="https://unpkg.com/vue@next"></script>
    <script>window.pandocMetaData = {{{ meta | tojson }}}</script>
    <script src="https://zgul.de/interactive-docs.js"></script>
</body>
</html>
'''

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--infile', nargs='?', default=sys.stdin, type=argparse.FileType(mode='r'))
    parser.add_argument('-o', '--outfile', nargs='?', default=sys.stdout, type=argparse.FileType(mode='w'))
    args = parser.parse_args()

    contents: str = args.infile.read()

    template = jinja2.Template(HTML_TEMPLATE, variable_start_string='{{{', variable_end_string='}}}')

    markdown.markdown(contents, extensions=['meta'])

    md = markdown.Markdown(extensions=['full_yaml_metadata', 'admonition', 'fenced_code'])
    html = md.convert(contents)

    data = {} if md.Meta is None else {**md.Meta}
    data['body'] = html
    data['meta'] = {**data, 'body': ''}

    output = template.render(**data)

    args.outfile.write(output)
