#!/bin/bash
(echo -e 'Hack-IDE\n============';sed -e 's/</\&lt;/g' -e 's/>/\&gt;/g' hackide.1 | man2html | pandoc -f html -t markdown )> README.md
