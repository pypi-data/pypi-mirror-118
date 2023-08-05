#!/usr/bin/env python
#  -*- mode: python; indent-tabs-mode: nil; -*- coding: iso-8859-1 -*-

"""

HTMLWriter.py

Copyright 2009 by Marcello Perathoner

Distributable under the GNU General Public License Version 3 or newer.

"""


import copy
import os
from urllib.parse import urlparse, urljoin
from lxml import etree

import libgutenberg.GutenbergGlobals as gg
from libgutenberg.GutenbergGlobals import xpath
from libgutenberg.Logger import debug, exception, info, error

from ebookmaker import writers
from ebookmaker.CommonCode import Options
from ebookmaker.writers import em
from ebookmaker.parsers import webify_url

options = Options()

class Writer(writers.HTMLishWriter):
    """ Class for writing HTML files. """

    def add_version(self, job, tree):
        for root in gg.xpath(tree, '//xhtml:html'):
            root['version'] = "XHTML+RDFa 1.1"

    def add_dublincore(self, job, tree):
        """ Add dublin core metadata to <head>. """
        source = gg.archive2files(
            options.ebook, job.url)

        if hasattr(options.config, 'FILESDIR'):
            job.dc.source = source.replace(options.config.FILESDIR, options.config.PGURL)

        for head in xpath(tree, '//xhtml:head'):
            for e in job.dc.to_html():
                e.tail = '\n'
                head.append(e)

    def add_moremeta(self, job, tree, url):

        self.add_prop(tree, "og:title", job.dc.title)

        for dcmitype in job.dc.dcmitypes:
            self.add_prop(tree, "og:type", dcmitype.id)
        info(job.main)
        web_url = urljoin(job.dc.canonical_url, job.outputfile)
        self.add_prop(tree, "og:url", web_url)
        canonical_cover_name = 'pg%s.cover.medium.jpg' % job.dc.project_gutenberg_id
        cover_url = urljoin(job.dc.canonical_url, canonical_cover_name)
        self.add_prop(tree, "og:image", cover_url)

    def outputfileurl(self, job, url):
        """ make the output path for the parser """

        if not job.main:
            # this is the main file
            job.main = url
            jobfilename = os.path.join(os.path.abspath(job.outputdir), job.outputfile)

            info("Creating HTML file: %s" % jobfilename)

            relativeURL = os.path.basename(url)
            if relativeURL != job.outputfile:
                # need to change the name for main file
                debug('changing %s to   %s', relativeURL, job.outputfile)
                job.link_map[relativeURL] = jobfilename
                relativeURL = job.outputfile

        else:
            relativeURL = gg.make_url_relative(job.main, url)

        info("source: %s relative: %s", url, relativeURL)
        return os.path.join(os.path.abspath(job.outputdir), relativeURL)


    def build(self, job):
        """ Build HTML file. """

        def rewrite_links(job, node):
            """ only needed if the mainsource filename has been changed """
            for renamed_path in job.link_map:
                for link in node.xpath('//xhtml:*[@href]', namespaces=gg.NSMAP):
                    old_link = link.get('href')
                    parsed_url = urlparse(old_link)
                    if os.path.basename(parsed_url.path) == renamed_path:
                        new_path = parsed_url.path[0:-len(renamed_path)]
                        new_link = job.link_map[renamed_path]
                        new_link = '%s%s#%s' % (new_path, new_link, parsed_url.fragment)
                        link.set('href', new_link)

        for p in job.spider.parsers:
            # Do html only. The images were copied earlier by PicsDirWriter.

            outfile = self.outputfileurl(job, p.attribs.url)

            if p.attribs.url.startswith(webify_url(job.outputdir)):
                debug('%s is same as %s: already there'
                      % (p.attribs.url, job.outputdir))
                continue
            if gg.is_same_path(p.attribs.url, outfile):
                debug('%s is same as %s: should not overwrite source'
                      % (p.attribs.url, outfile))
                continue

            gg.mkdir_for_filename(outfile)

            xhtml = None
            if hasattr(p, 'rst2html'):
                xhtml = p.rst2html(job)
                self.make_links_relative(xhtml, p.attribs.url)
                rewrite_links(job, xhtml)

            elif hasattr(p, 'xhtml'):
                p.parse()
                xhtml = copy.deepcopy(p.xhtml)
                self.make_links_relative(xhtml, p.attribs.url)
                rewrite_links(job, xhtml)

            else:
                p.parse()

            try:
                if xhtml is not None:
                    self.add_dublincore(job, xhtml)

                    # makes iphones zoom in
                    self.add_meta(xhtml, 'viewport', 'width=device-width')
                    self.add_meta_generator(xhtml)
                    self.add_moremeta(job, xhtml, p.attribs.url)

                    html = etree.tostring(xhtml,
                                          doctype=gg.XHTML_RDFa_DOCTYPE,
                                          method='html',
                                          encoding='utf-8',
                                          pretty_print=True)

                    self.write_with_crlf(outfile, html)
                    info("Done generating HTML file: %s" % outfile)
                else:
                    #images and css files
                    try:
                        with open(outfile, 'wb') as fp_dest:
                            fp_dest.write(p.serialize())
                    except IOError as what:
                        error('Cannot copy %s to %s: %s' % (job.attribs.url, outfile, what))

            except Exception as what:
                exception("Error building HTML %s: %s" % (outfile, what))
                if os.access(outfile, os.W_OK):
                    os.remove(outfile)
                raise what

        info("Done generating HTML: %s" % job.outputfile)
