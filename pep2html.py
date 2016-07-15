#!/usr/bin/env python3
"""
Quick hack to render PEPs in these repositories
"""

# Warning: hacks ahead!
# The distutils PEP handling is not really friendly to changes...


import glob
import re
import os
import tempfile
import shutil
from email.parser import HeaderParser
from docutils import core, nodes
from docutils.transforms.peps import Headers
from docutils.parsers import rst
from docutils.parsers.rst import directives
from docutils.writers import pep_html
from docutils.readers import pep
from docutils.transforms import peps

file_re = re.compile("(.*/)?pep-(?P<num>[^/]*).(rst|html)")

def get_pepnum(filename):
    return file_re.match(filename).group('num')

class Writer(pep_html.Writer):
    default_template = 'template.txt'

    def __init__(self, pep_num):
        super().__init__()
        self._pep_num = pep_num

    def interpolation_dict(self):
        result = super().interpolation_dict()
        index = self.document.first_child_matching_class(nodes.field_list)
        self.document[index][0][1].text = '-1'
        result['pepnum'] = result['pep'] = self._pep_num
        result['pephome'] = 'https://github.com/fedora-python/pep-drafts/blob/master'
        result['pepindex'] = 'index.html'
        result['banner'] = 0
        return result

class Reader(pep.Reader):
    def get_transforms(self):
        transforms = super().get_transforms()
        transforms.remove(peps.Headers)
        return transforms

def fix_rst_pep(input_lines, outfile, inpath, pepnum):

    class XXXDirective(rst.Directive):
        has_content = True
        def run(self):
            # Raise an error if the directive does not have contents.
            self.assert_has_content()
            text = '\n'.join(self.content)
            # Create the admonition node, to be populated by `nested_parse`.
            admonition_node = nodes.admonition(rawsource=text)
            # Parse the directive contents.
            self.state.nested_parse(self.content, self.content_offset,
                                    admonition_node)
            title = nodes.title('', 'XXX')
            admonition_node.insert(0, title)
            return [admonition_node]
    directives.register_directive('xxx', XXXDirective)

    handle, template_file_name = tempfile.mkstemp(text=True)
    try:
        orig_template_name = pep_html.Writer.default_template_path
        with open(orig_template_name) as inf, open(handle, 'w') as outf:
            content = inf.read()
            content = content.replace('%(pepnum)s.txt', '%(pepnum)s.rst')
            content = content.replace("%(pepindex)s/", "%(pepindex)s")
            outf.write(content)

        output = core.publish_string(
            source=''.join(input_lines),
            source_path=inpath,
            destination_path=outfile.name,
            reader=Reader(),
            parser_name='restructuredtext',
            writer=Writer(pepnum),
            settings=None,
            # Allow Docutils traceback if there's an exception:
            settings_overrides={
                'traceback': 1,
                'template': template_file_name,
            })
        outfile.write(output.decode('utf-8'))
    finally:
        os.unlink(template_file_name)


def main():
    outdir = os.path.join(os.path.dirname('__file__'), 'build')
    try:
        shutil.rmtree(outdir)
    except FileNotFoundError:
        pass
    os.mkdir(outdir)
    filenames = []
    names = {}
    for filename in sorted(glob.glob("pep-*.rst")):
        outbasename = os.path.basename(filename[:-4] + '.html')
        filenames.append(outbasename)
        outfilename = os.path.join(outdir, outbasename)
        pepnum = get_pepnum(outfilename)
        print(filename, '->', outfilename)
        with open(filename) as inf, open(outfilename, 'w') as outf:
            fix_rst_pep(inf, outf, filename, pepnum)
        with open(filename) as inf:
            parser = HeaderParser()
            metadata = parser.parse(inf)
        names[pepnum] = metadata['Title']

    index_filename = os.path.join(outdir, 'index.html')
    print(index_filename)
    with open(index_filename, 'w') as f:
        f.write('<html><head><title>Draft PEP index</title></head>')
        f.write('<body><h1>Draft PEP index</h1><ul>')
        for filename in filenames:
            pepnum = get_pepnum(filename)
            f.write('<li>{num}: <a href="{link}">{name}</a></li>'.format(
                link=filename, num=pepnum, name=names[pepnum]))
        f.write('</ul></body></html>')



if __name__ == "__main__":
    main()
