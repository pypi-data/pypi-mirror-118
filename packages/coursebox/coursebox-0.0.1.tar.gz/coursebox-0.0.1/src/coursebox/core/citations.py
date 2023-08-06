import os
import pybtex
import io
import six
from coursebox.core.info_paths import get_paths

def get_references(bibfile, gi):

    """
    Import and convert slides dynamically.
    """
    # base_dir = paths['02450public'] + "/Notes/Latex"
    bibf = bibfile #base_dir + "/library.bib"
    if not os.path.exists(bibf):
        return None

    pybtex_style = pybtex.plugin.find_plugin('pybtex.style.formatting', 'alpha')()
    pybtex_html_backend = pybtex.plugin.find_plugin('pybtex.backends', 'html')()
    pybtex_plain_backend = pybtex.plugin.find_plugin('pybtex.backends', 'plaintext')()

    pybtex_parser = pybtex.database.input.bibtex.Parser()

    with open(bibf, 'r', encoding='utf8') as f:
        data = pybtex_parser.parse_stream(f)

    itv = six.itervalues(data.entries)
    data_formatted = pybtex_style.format_entries(itv)
    refs = {}

    if 'auxfile' in gi:
        all_references = parse_aux(gi['auxfile'], bibtex=gi['bibtex'])
    else:
        all_references = {}

    for entry in data_formatted:
        output = io.StringIO()
        output_plain = io.StringIO()
        pybtex_plain_backend.output = output_plain.write
        pybtex_html_backend.output = output.write
        pybtex_html_backend.write_entry(entry.key, entry.label, entry.text.render(pybtex_html_backend))

        pybtex_plain_backend.write_entry(entry.key, entry.label, entry.text.render(pybtex_plain_backend))

        html = output.getvalue()
        plain = output_plain.getvalue()

        entry.text.parts[-2].__str__()
        url = ""
        for i,p in enumerate(entry.text.parts):
            if "\\url" in p.__str__():
                url = entry.text.parts[i+1]
                break
        url = url.__str__()
        i1 = html.find("\\textbf")
        i2 = html.find("</span>", i1)
        dht = html[i1:i2]
        dht = dht[dht.find(">")+1:]
        html = html[:i1] + " <b>"+dht+"</b> " + html[i2+7:]

        plain = plain.replace("\\textbf ", "")
        iu = plain.find("URL")
        if iu > 0:
            plain = plain[:iu]

        refs[entry.key] = {'html': html,
                           'plain': plain,
                            'label': entry.label,
                            'filename': url,
                            'references': all_references}

    newref = {}
    ls = lambda x: x if isinstance(x, list) else [x]
    if 'tex_command' in gi:
        for cmd, aux, display in zip( ls(gi['tex_command']), ls(gi['tex_aux'] ), ls( gi['tex_display'] ) ):
            ax = parse_aux(aux, bibtex=gi['bibtex'])
            for k in ax:
                ax[k]['pyref'] = display%(ax[k]['nicelabel'],)
            newref[cmd] = ax

    return refs, newref


def parse_aux(auxfile, bibtex):
    paths = get_paths()
    auxfile = os.path.join(paths['02450public'], auxfile)
    if not os.path.exists(auxfile):
        print(auxfile)
        from warnings import warn
        warn("Could not find file")
        return {}

    with open(auxfile, 'r') as f:
        items = f.readlines()
    entries = {}
    for e in items:
        e = e.strip()
        if e.startswith("\\newlabel") and "@cref" in e:
            # print(e)
            i0 = e.find("{")
            i1 = e.find("@cref}")
            key = e[i0+1:i1]

            j0 = e.find("{{[", i0)+3
            j1 = e.find("}", j0)

            val = e[j0:j1]

            label = val[:val.find("]")]
            number = val[val.rfind("]")+1:]

            if label == "equation":
                nlabel = f"eq. ({number})"
            else:
                nlabel = label.capitalize() + " " + number

            coderef = "\\cite[%s]{%s}"%(nlabel, bibtex) if bibtex is not None else None
            entries[key] = {'pyref': coderef, 'nicelabel': nlabel, 'rawlabel': label, 'number': number}

    return entries
