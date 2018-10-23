import os
from lxml import etree

def test_validate_svg():
    for root, _dirs, files in os.walk('media'):
        for filename in files:
            if filename.endswith('.svg'):
                with open(os.path.join(root, filename)) as svg_handle:
                    etree.parse(svg_handle)

if __name__ == '__main__':
    test_validate_svg()
