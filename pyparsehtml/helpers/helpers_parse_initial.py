import re

html_tags = ['<!--...-->', '<!DOCTYPE>', '<a>', '<abbr>', '<acronym>', '<address>', '<applet>', '<area>', '<article>', '<aside>', '<audio>', '<b>', '<base>', '<basefont>', '<bdi>', '<bdo>', '<big>', '<blockquote>', '<body>', '<br>', '<button>', '<canvas>', '<caption>', '<center>', '<cite>', '<code>', '<col>', '<colgroup>', '<data>', '<datalist>', '<dd>', '<del>', '<details>', '<dfn>', '<dialog>', '<dir>', '<div>', '<dl>', '<dt>', '<em>', '<embed>', '<fieldset>', '<figcaption>', '<figure>', '<font>', '<footer>', '<form>', '<frame>', '<frameset>', '<h1> to <h6>', '<head>', '<header>', '<hr>', '<html>', '<i>', '<iframe>', '<img>', '<input>', '<ins>', '<kbd>', '<label>', '<legend>', '<li>', '<link>', '<main>', '<map>', '<mark>', '<meta>', '<meter>', '<nav>', '<noframes>', '<noscript>', '<object>', '<ol>', '<optgroup>', '<option>', '<output>', '<p>', '<param>', '<picture>', '<pre>', '<progress>', '<q>', '<rp>', '<rt>', '<ruby>', '<s>', '<samp>', '<script>', '<section>', '<select>', '<small>', '<source>', '<span>', '<strike>', '<strong>', '<style>', '<sub>', '<summary>', '<sup>', '<svg>', '<table>', '<tbody>', '<td>', '<template>', '<textarea>', '<tfoot>', '<th>', '<thead>', '<time>', '<title>', '<tr>', '<track>', '<tt>', '<u>', '<ul>', '<var>', '<video>', '<wbr>']
html_tags_stripped = ['!--...--', '!DOCTYPE', 'a', 'abbr', 'acronym', 'address', 'applet', 'area', 'article', 'aside', 'audio', 'b', 'base', 'basefont', 'bdi', 'bdo', 'big', 'blockquote', 'body', 'br', 'button', 'canvas', 'caption', 'center', 'cite', 'code', 'col', 'colgroup', 'data', 'datalist', 'dd', 'del', 'details', 'dfn', 'dialog', 'dir', 'div', 'dl', 'dt', 'em', 'embed', 'fieldset', 'figcaption', 'figure', 'font', 'footer', 'form', 'frame', 'frameset', 'h1 to h6', 'head', 'header', 'hr', 'html', 'i', 'iframe', 'img', 'input', 'ins', 'kbd', 'label', 'legend', 'li', 'link', 'main', 'map', 'mark', 'meta', 'meter', 'nav', 'noframes', 'noscript', 'object', 'ol', 'optgroup', 'option', 'output', 'p', 'param', 'picture', 'pre', 'progress', 'q', 'rp', 'rt', 'ruby', 's', 'samp', 'script', 'section', 'select', 'small', 'source', 'span', 'strike', 'strong', 'style', 'sub', 'summary', 'sup', 'svg', 'table', 'tbody', 'td', 'template', 'textarea', 'tfoot', 'th', 'thead', 'time', 'title', 'tr', 'track', 'tt', 'u', 'ul', 'var', 'video', 'wbr']
all_attributes_list = ['accept', 'accept-charset', 'accesskey', 'action', 'alt', 'async', 'autocomplete', 'autofocus', 'autoplay', 'charset', 'checked', 'cite', 'class', 'cols', 'colspan', 'contenteditable', 'controls', 'coords', 'data', 'data-*', 'datetime', 'default', 'defer', 'dir', 'dirname', 'disabled', 'download', 'draggable', 'enctype', 'for', 'form', 'formaction', 'headers', 'height', 'hidden', 'high', 'href', 'hreflang', 'http-equiv', 'id', 'ismap', 'kind', 'label', 'lang', 'list', 'loop', 'low', 'max', 'maxlength', 'media', 'method', 'min', 'multiple', 'muted', 'name', 'novalidate', 'onabort', 'onafterprint', 'onbeforeprint', 'onbeforeunload', 'onblur', 'oncanplay', 'oncanplaythrough', 'onchange', 'onclick', 'oncontextmenu', 'oncopy', 'oncuechange', 'oncut', 'ondblclick', 'ondrag', 'ondragend', 'ondragenter', 'ondragleave', 'ondragover', 'ondragstart', 'ondrop', 'ondurationchange', 'onemptied', 'onended', 'onerror', 'onfocus', 'onhashchange', 'oninput', 'oninvalid', 'onkeydown', 'onkeypress', 'onkeyup', 'onload', 'onloadeddata', 'onloadedmetadata', 'onloadstart', 'onmousedown', 'onmousemove', 'onmouseout', 'onmouseover', 'onmouseup', 'onmousewheel', 'onoffline', 'ononline', 'onpagehide', 'onpageshow', 'onpaste', 'onpause', 'onplay', 'onplaying', 'onpopstate', 'onprogress', 'onratechange', 'onreset', 'onresize', 'onscroll', 'onsearch', 'onseeked', 'onseeking', 'onselect', 'onstalled', 'onstorage', 'onsubmit', 'onsuspend', 'ontimeupdate', 'ontoggle', 'onunload', 'onvolumechange', 'onwaiting', 'onwheel', 'open', 'optimum', 'pattern', 'placeholder', 'poster', 'preload', 'readonly', 'rel', 'required', 'reversed', 'rows', 'rowspan', 'scope', 'selected', 'shape', 'size', 'sizes', 'span', 'spellcheck', 'src', 'srcdoc', 'srclang', 'srcset', 'start', 'step', 'style', 'tabindex', 'target', 'title', 'translate', 'type', 'usemap', 'value', 'width', 'wrap']
attributes = {'accept': ['<input />'], 'accept-charset': ['<form>'], 'accesskey': ['global attribute'], 'action': ['<form>'], 'alt': ['<area />', '<img />', '<input />'], 'async': ['<script>'], 'autocomplete': ['<form>', '<input />'], 'autofocus': ['<button>', '<input />', '<select>', '<textarea>'], 'autoplay': ['<audio>', '<video>'], 'charset': ['<meta />', '<script>'], 'checked': ['<input />'], 'cite': ['<blockquote>', '<del>', '<ins>', '<q>'], 'class': ['global attribute'], 'cols': ['<textarea>'], 'colspan': ['<td>', '<th>'], 'contenteditable': ['global attribute'], 'controls': ['<audio>', '<video>'], 'coords': ['<area />'], 'data': ['<object>'], 'data-*': ['global attribute'], 'datetime': ['<del>', '<ins>', '<time>'], 'default': ['<track />'], 'defer': ['<script>'], 'dir': ['global attribute'], 'dirname': ['<input />', '<textarea>'], 'disabled': ['<button>', '<fieldset>', '<input />', '<optgroup>', '<option>', '<select>', '<textarea>'], 'download': ['<a>', '<area />'], 'draggable': ['global attribute'], 'enctype': ['<form>'], 'for': ['<label>', '<output>'], 'form': ['<button>', '<fieldset>', '<input />', '<label>', '<meter>', '<object>', '<output>', '<select>', '<textarea>'], 'formaction': ['<button>', '<input />'], 'headers': ['<td>', '<th>'], 'height': ['<canvas>', '<embed />', '<iframe>', '<img />', '<input />', '<object>', '<video>'], 'hidden': ['global attribute'], 'high': ['<meter>'], 'href': ['<a>', '<area />', '<base />', '<link />'], 'hreflang': ['<a>', '<area />', '<link />'], 'http-equiv': ['<meta />'], 'id': ['global attribute'], 'ismap': ['<img />'], 'kind': ['<track />'], 'label': ['<track />', '<option>', '<optgroup>'], 'lang': ['global attribute'], 'list': ['<input />'], 'loop': ['<audio>', '<video>'], 'low': ['<meter>'], 'max': ['<input />', '<meter>', '<progress>'], 'maxlength': ['<input />', '<textarea>'], 'media': ['<a>', '<area />', '<link />', '<source />', '<style>'], 'method': ['<form>'], 'min': ['<input />', '<meter>'], 'multiple': ['<input />', '<select>'], 'muted': ['<video>', '<audio>'], 'name': ['<button>', '<fieldset>', '<form>', '<iframe>', '<input />', '<map>', '<meta />', '<object>', '<output>', '<param />', '<select>', '<textarea>'], 'novalidate': ['<form>'], 'onabort': ['<audio>', '<embed />', '<img />', '<object>', '<video>'], 'onafterprint': ['<body>'], 'onbeforeprint': ['<body>'], 'onbeforeunload': ['<body>'], 'onblur': ['All visible'], 'oncanplay': ['<audio>', '<embed />', '<object>', '<video>'], 'oncanplaythrough': ['<audio>', '<video>'], 'onchange': ['All visible'], 'onclick': ['All visible'], 'oncontextmenu': ['All visible'], 'oncopy': ['All visible'], 'oncuechange': ['<track />'], 'oncut': ['All visible'], 'ondblclick': ['All visible'], 'ondrag': ['All visible'], 'ondragend': ['All visible'], 'ondragenter': ['All visible'], 'ondragleave': ['All visible'], 'ondragover': ['All visible'], 'ondragstart': ['All visible'], 'ondrop': ['All visible'], 'ondurationchange': ['<audio>', '<video>'], 'onemptied': ['<audio>', '<video>'], 'onended': ['<audio>', '<video>'], 'onerror': ['<audio>', '<body>', '<embed />', '<img />', '<object>', '<script>', '<style>', '<video>'], 'onfocus': ['All visible'], 'onhashchange': ['<body>'], 'oninput': ['All visible'], 'oninvalid': ['All visible'], 'onkeydown': ['All visible'], 'onkeypress': ['All visible'], 'onkeyup': ['All visible'], 'onload': ['<body>', '<iframe>', '<img />', '<input />', '<link />', '<script>', '<style>'], 'onloadeddata': ['<audio>', '<video>'], 'onloadedmetadata': ['<audio>', '<video>'], 'onloadstart': ['<audio>', '<video>'], 'onmousedown': ['All visible'], 'onmousemove': ['All visible'], 'onmouseout': ['All visible'], 'onmouseover': ['All visible'], 'onmouseup': ['All visible'], 'onmousewheel': ['All visible'], 'onoffline': ['<body>'], 'ononline': ['<body>'], 'onpagehide': ['<body>'], 'onpageshow': ['<body>'], 'onpaste': ['All visible'], 'onpause': ['<audio>', '<video>'], 'onplay': ['<audio>', '<video>'], 'onplaying': ['<audio>', '<video>'], 'onpopstate': ['<body>'], 'onprogress': ['<audio>', '<video>'], 'onratechange': ['<audio>', '<video>'], 'onreset': ['<form>'], 'onresize': ['<body>'], 'onscroll': ['All visible'], 'onsearch': ['<input />'], 'onseeked': ['<audio>', '<video>'], 'onseeking': ['<audio>', '<video>'], 'onselect': ['All visible'], 'onstalled': ['<audio>', '<video>'], 'onstorage': ['<body>'], 'onsubmit': ['<form>'], 'onsuspend': ['<audio>', '<video>'], 'ontimeupdate': ['<audio>', '<video>'], 'ontoggle': ['<details>'], 'onunload': ['<body>'], 'onvolumechange': ['<audio>', '<video>'], 'onwaiting': ['<audio>', '<video>'], 'onwheel': ['All visible'], 'open': ['<details>'], 'optimum': ['<meter>'], 'pattern': ['<input />'], 'placeholder': ['<input />', '<textarea>'], 'poster': ['<video>'], 'preload': ['<audio>', '<video>'], 'readonly': ['<input />', '<textarea>'], 'rel': ['<a>', '<area />', '<form>', '<link />'], 'required': ['<input />', '<select>', '<textarea>'], 'reversed': ['<ol>'], 'rows': ['<textarea>'], 'rowspan': ['<td>', '<th>'], 'scope': ['<th>'], 'selected': ['<option>'], 'shape': ['<area />'], 'size': ['<input />', '<select>'], 'sizes': ['<img />', '<link />', '<source />'], 'span': ['<col />', '<colgroup>'], 'spellcheck': ['global attribute'], 'src': ['<audio>', '<embed />', '<iframe>', '<img />', '<input />', '<script>', '<source />', '<track />', '<video>'], 'srcdoc': ['<iframe>'], 'srclang': ['<track />'], 'srcset': ['<img />', '<source />'], 'start': ['<ol>'], 'step': ['<input />'], 'style': ['global attribute'], 'tabindex': ['global attribute'], 'target': ['<a>', '<area />', '<base />', '<form>'], 'title': ['global attribute'], 'translate': ['global attribute'], 'type': ['<a>', '<button>', '<embed />', '<input />', '<link />', '<menu>', '<object>', '<script>', '<source />', '<style>'], 'usemap': ['<img />', '<object>'], 'value': ['<button>', '<input />', '<li>', '<option>', '<meter>', '<progress>', '<param />'], 'width': ['<canvas>', '<embed />', '<iframe>', '<img />', '<input />', '<object>', '<video>'], 'wrap': ['<textarea>']}
html_tags_incl_attributes = {'<!--...-->': [], '<!DOCTYPE>': [], '<a>': ['download', 'href', 'hreflang', 'media', 'rel', 'target', 'type'], '<abbr>': [], '<acronym>': [], '<address>': [], '<applet>': [], '<article>': [], '<aside>': [], '<audio>': ['autoplay', 'controls', 'loop', 'muted', 'onabort', 'oncanplay', 'oncanplaythrough', 'ondurationchange', 'onemptied', 'onended', 'onerror', 'onloadeddata', 'onloadedmetadata', 'onloadstart', 'onpause', 'onplay', 'onplaying', 'onprogress', 'onratechange', 'onseeked', 'onseeking', 'onstalled', 'onsuspend', 'ontimeupdate', 'onvolumechange', 'onwaiting', 'preload', 'src'], '<b>': [], '<basefont>': [], '<bdi>': [], '<bdo>': [], '<big>': [], '<blockquote>': ['cite'], '<body>': ['onafterprint', 'onbeforeprint', 'onbeforeunload', 'onerror', 'onhashchange', 'onload', 'onoffline', 'ononline', 'onpagehide', 'onpageshow', 'onpopstate', 'onresize', 'onstorage', 'onunload'], '<button>': ['autofocus', 'disabled', 'form', 'formaction', 'name', 'type', 'value'], '<canvas>': ['height', 'width'], '<caption>': [], '<center>': [], '<cite>': [], '<code>': [], '<colgroup>': ['span'], '<data>': [], '<datalist>': [], '<dd>': [], '<del>': ['cite', 'datetime'], '<details>': ['ontoggle', 'open'], '<dfn>': [], '<dialog>': [], '<dir>': [], '<div>': [], '<dl>': [], '<dt>': [], '<em>': [], '<fieldset>': ['disabled', 'form', 'name'], '<figcaption>': [], '<figure>': [], '<font>': [], '<footer>': [], '<form>': ['accept-charset', 'action', 'autocomplete', 'enctype', 'method', 'name', 'novalidate', 'onreset', 'onsubmit', 'rel', 'target'], '<frame>': [], '<frameset>': [], '<h1> to <h6>': [], '<head>': [], '<header>': [], '<html>': [], '<i>': [], '<iframe>': ['height', 'name', 'onload', 'src', 'srcdoc', 'width'], '<ins>': ['cite', 'datetime'], '<kbd>': [], '<label>': ['for', 'form'], '<legend>': [], '<li>': ['value'], '<main>': [], '<map>': ['name'], '<mark>': [], '<meter>': ['form', 'high', 'low', 'max', 'min', 'optimum', 'value'], '<nav>': [], '<noframes>': [], '<noscript>': [], '<object>': ['data', 'form', 'height', 'name', 'onabort', 'oncanplay', 'onerror', 'type', 'usemap', 'width'], '<ol>': ['reversed', 'start'], '<optgroup>': ['disabled', 'label'], '<option>': ['disabled', 'label', 'selected', 'value'], '<output>': ['for', 'form', 'name'], '<p>': [], '<picture>': [], '<pre>': [], '<progress>': ['max', 'value'], '<q>': ['cite'], '<rp>': [], '<rt>': [], '<ruby>': [], '<s>': [], '<samp>': [], '<script>': ['async', 'charset', 'defer', 'onerror', 'onload', 'src', 'type'], '<section>': [], '<select>': ['autofocus', 'disabled', 'form', 'multiple', 'name', 'required', 'size'], '<small>': [], '<span>': [], '<strike>': [], '<strong>': [], '<style>': ['media', 'onerror', 'onload', 'type'], '<sub>': [], '<summary>': [], '<sup>': [], '<svg>': [], '<table>': [], '<tbody>': [], '<td>': ['colspan', 'headers', 'rowspan'], '<template>': [], '<textarea>': ['autofocus', 'cols', 'dirname', 'disabled', 'form', 'maxlength', 'name', 'placeholder', 'readonly', 'required', 'rows', 'wrap'], '<tfoot>': [], '<th>': ['colspan', 'headers', 'rowspan', 'scope'], '<thead>': [], '<time>': ['datetime'], '<title>': [], '<tr>': [], '<tt>': [], '<u>': [], '<ul>': [], '<var>': [], '<video>': ['autoplay', 'controls', 'height', 'loop', 'muted', 'onabort', 'oncanplay', 'oncanplaythrough', 'ondurationchange', 'onemptied', 'onended', 'onerror', 'onloadeddata', 'onloadedmetadata', 'onloadstart', 'onpause', 'onplay', 'onplaying', 'onprogress', 'onratechange', 'onseeked', 'onseeking', 'onstalled', 'onsuspend', 'ontimeupdate', 'onvolumechange', 'onwaiting', 'poster', 'preload', 'src', 'width'], '<area />': ['alt', 'coords', 'download', 'href', 'hreflang', 'media', 'rel', 'shape', 'target'], '<base />': ['href', 'target'], '<br />': [], '<col />': ['span'], '<embed />': ['height', 'onabort', 'oncanplay', 'onerror', 'src', 'type', 'width'], '<hr />': [], '<img />': ['alt', 'height', 'ismap', 'onabort', 'onerror', 'onload', 'sizes', 'src', 'srcset', 'usemap', 'width'], '<input />': ['accept', 'alt', 'autocomplete', 'autofocus', 'checked', 'dirname', 'disabled', 'form', 'formaction', 'height', 'list', 'max', 'maxlength', 'min', 'multiple', 'name', 'onload', 'onsearch', 'pattern', 'placeholder', 'readonly', 'required', 'size', 'src', 'step', 'type', 'value', 'width'], '<link />': ['href', 'hreflang', 'media', 'onload', 'rel', 'sizes', 'type'], '<meta />': ['charset', 'http-equiv', 'name'], '<param />': ['name', 'value'], '<source />': ['media', 'sizes', 'src', 'srcset', 'type'], '<track />': ['default', 'kind', 'label', 'oncuechange', 'src', 'srclang'], '<wbr />': []}
global_attributes = ['accesskey', 'class', 'contenteditable', 'data-*', 'dir', 'draggable', 'hidden', 'id', 'lang', 'onblur', 'onchange', 'onclick', 'oncontextmenu', 'oncopy', 'oncut', 'ondblclick', 'ondrag', 'ondragend', 'ondragenter', 'ondragleave', 'ondragover', 'ondragstart', 'ondrop', 'onfocus', 'oninput', 'oninvalid', 'onkeydown', 'onkeypress', 'onkeyup', 'onmousedown', 'onmousemove', 'onmouseout', 'onmouseover', 'onmouseup', 'onmousewheel', 'onpaste', 'onscroll', 'onselect', 'onwheel', 'spellcheck', 'style', 'tabindex', 'title', 'translate']
self_closing_tags = ['<area />', '<base />', '<br />', '<col />', '<embed />', '<hr />', '<img />', '<input />', '<link />', '<meta />', '<param />', '<source />', '<track />', '<wbr />']
self_closer = [['<area />', '<area>'], ['<base />', '<base>'], ['<br />', '<br>'], ['<col />', '<col>'], ['<embed />', '<embed>'], ['<hr />', '<hr>'], ['<img />', '<img>'], ['<input />', '<input>'], ['<link />', '<link>'], ['<meta />', '<meta>'], ['<param />', '<param>'], ['<source />', '<source>'], ['<track />', '<track>'], ['<wbr />', '<wbr>']]
css_properties = ['align-content', 'align-items', 'align-self', 'animation', 'animation-delay', 'animation-direction', 'animation-duration', 'animation-fill-mode', 'animation-iteration-count', 'animation-name', '@keyframes', 'animation-play-state', 'animation-timing-function', 'backface-visibility', 'background', 'background-attachment', 'background-clip', 'background-color', 'background-image', 'background-origin', 'background-position', 'background-repeat', 'background-size', 'border', 'border-bottom', 'border-bottom-color', 'border-bottom-left-radius', 'border-bottom-right-radius', 'border-bottom-style', 'border-bottom-width', 'border-collapse', 'border-color', 'border-image', 'border-image-outset', 'border-image-repeat', 'border-image-slice', 'border-image-source', 'border-image-width', 'border-left', 'border-left-color', 'border-left-style', 'border-left-width', 'border-radius', 'border-right', 'border-right-color', 'border-right-style', 'border-right-width', 'border-spacing', 'border-style', 'border-top', 'border-top-color', 'border-top-left-radius', 'border-top-right-radius', 'border-top-style', 'border-top-width', 'border-width', 'bottom', 'box-shadow', 'box-sizing', 'caption-side', 'clear', 'clip', 'color', 'column-count', 'column-fill', 'column-gap', 'column-rule', 'column-rule-color', 'column-rule-style', 'column-rule-width', 'column-span', 'column-width', 'columns', 'column-width', 'column-count', 'content', 'counter-increment', 'counter-reset', 'cursor', 'direction', 'display', 'empty-cells', 'flex', 'flex-basis', 'flex-direction', 'flex-flow', 'flex-direction', 'flex-wrap', 'flex-grow', 'flex-shrink', 'flex-wrap', 'float', 'font', 'font-family', 'font-size', 'font-size-adjust', 'font-stretch', 'font-style', 'font-variant', 'font-weight', 'height', 'justify-content', 'left', 'letter-spacing', 'line-height', 'list-style', 'list-style-image', 'list-style-position', 'list-style-type', 'margin', 'margin-bottom', 'margin-left', 'margin-right', 'margin-top', 'max-height', 'max-width', 'min-height', 'min-width', 'opacity', 'order', 'outline', 'outline-color', 'outline-offset', 'outline-style', 'outline-width', 'overflow', 'overflow-x', 'overflow-y', 'padding', 'padding-bottom', 'padding-left', 'padding-right', 'padding-top', 'page-break-after', 'page-break-before', 'page-break-inside', 'perspective', 'perspective-origin', 'position', 'quotes', 'resize', 'right', 'tab-size', 'table-layout', 'text-align', 'text-align-last', 'text-align', 'justify', 'text-decoration', 'text-decoration-color', 'text-decoration-line', 'text-decoration-line', 'text-decoration-style', 'text-decoration-line', 'text-indent', 'text-justify', 'text-align', 'justify', 'text-overflow', 'text-shadow', 'text-transform', 'top', 'transform', 'transform-origin', 'transform-style', 'transition', 'transition-delay', 'transition-duration', 'transition-property', 'transition-timing-function', 'vertical-align', 'visibility', 'white-space', 'width', 'word-break', 'word-spacing', 'word-wrap', 'z-index', 'animation', 'animation-delay', 'animation-direction', 'animation-duration', 'animation-fill-mode', 'animation-iteration-count', 'animation-name', '@keyframes', 'animation-play-state', 'animation-timing-function', 'background', 'background-attachment', 'background-clip', 'background-color', 'background-image', 'background-origin', 'background-position', 'background-repeat', 'background-size', 'border', 'border-bottom', 'border-bottom-color', 'border-bottom-left-radius', 'border-bottom-right-radius', 'border-bottom-style', 'border-bottom-width', 'border-color', 'border-image', 'border-image-outset', 'border-image-repeat', 'border-image-slice', 'border-image-source', 'border-image-width', 'border-left', 'border-left-color', 'border-left-style', 'border-left-width', 'border-radius', 'border-right', 'border-right-color', 'border-right-style', 'border-right-width', 'border-style', 'border-top', 'border-top-color', 'border-top-left-radius', 'border-top-right-radius', 'border-top-style', 'border-top-width', 'border-width', 'color', 'opacity', 'height', 'max-height', 'max-width', 'min-height', 'min-width', 'width', 'content', 'quotes', 'counter-reset', 'counter-increment', 'align-content', 'align-items', 'align-self', 'flex', 'flex-basis', 'flex-direction', 'flex-flow', 'flex-direction', 'flex-wrap', 'flex-grow', 'flex-shrink', 'flex-wrap', 'justify-content', 'order', 'font', 'font-family', 'font-size', 'font-size-adjust', 'font-stretch', 'font-style', 'font-variant', 'font-weight', 'list-style', 'list-style-image', 'list-style-position', 'list-style-type', 'margin', 'margin-bottom', 'margin-left', 'margin-right', 'margin-top', 'column-count', 'column-fill', 'column-gap', 'column-rule', 'column-rule-color', 'column-rule-style', 'column-rule-width', 'column-span', 'column-width', 'columns', 'column-width', 'column-count', 'outline', 'outline-color', 'outline-offset', 'outline-style', 'outline-width', 'padding', 'padding-bottom', 'padding-left', 'padding-right', 'padding-top', 'page-break-after', 'page-break-before', 'page-break-inside', 'border-collapse', 'border-spacing', 'caption-side', 'empty-cells', 'table-layout', 'direction', 'tab-size', 'text-align', 'text-align-last', 'text-align', 'justify', 'text-decoration', 'text-decoration-color', 'text-decoration-line', 'text-decoration-line', 'text-decoration-style', 'text-decoration-line', 'text-indent', 'text-justify', 'text-align', 'justify', 'text-overflow', 'text-shadow', 'text-transform', 'line-height', 'vertical-align', 'letter-spacing', 'word-spacing', 'white-space', 'word-break', 'word-wrap', 'backface-visibility', 'perspective', 'perspective-origin', 'transform', 'transform-origin', 'transform-style', 'transition', 'transition-delay', 'transition-duration', 'transition-property', 'transition-timing-function', 'display', 'position', 'top', 'right', 'bottom', 'left', 'float', 'clear', 'z-index', 'overflow', 'overflow-x', 'overflow-y', 'resize', 'clip', 'visibility', 'cursor', 'box-shadow', 'box-sizing']


def mergeDict(dictionaries):
  base = dictionaries[0]
  for d in range(1, len(dictionaries)):
    base.update(dictionaries[d])
  return base


def isSelfCloser(to_match):
  res = False
  for o in self_closer:
    if to_match == o[0] or to_match == o[1]:
      res = True
  return res

def addGlobalAttributes():
  attributes = {}
  for g in global_attributes:
    if g == 'style':
      attributes[g] = {}
      for prop in css_properties:
        attributes[g][prop] = ""
     
    else:
      attributes[g] = ""
  return attributes

def addSpecificAttributes(meta_tag):
  attributes = {}
  for a in html_tags_incl_attributes[meta_tag['as_tag_identifier']]:
    attributes[a] = ""
  return attributes

def sortTags(tags):
  return sorted(tags, key = lambda i: i['start_idx'])


def hasClosingTags(collected):
  result = False
  for no, c in enumerate(collected): 
    if c['tag_role'] == 'close' and no != 1:
      result = True
  return result


def getInnerContents(tags_up, input):
  for t in tags_up:
    if t['tag_role'] == 'open_close' or t['tag_role'] == 'open_close_alt':
      continue
    else:
      t['innerContent'] = input[t['end_idx']+1:t['closer']['start_idx']]
  return tags_up


def identifyTags(input):
  collected_tags = []
  for tag in html_tags_stripped:
    as_open = re.findall(f'<{tag}(?=\s)', input)
    as_close = re.findall(f'</{tag}', input)
    ##handle openers
    current_idx = 0
    for o in as_open:
      meta_tag = {}
      meta_tag['tag_type'] = tag
      matcher = f"<{tag} />"
      meta_tag['start_idx'] = input.index(o, current_idx)
      meta_tag['end_idx'] = input.index('>', meta_tag['start_idx'])   
      meta_tag['with_attributes'] = input[meta_tag['start_idx']:meta_tag['end_idx'] +1]
      if isSelfCloser(matcher):
        meta_tag['tag_role'] = 'open_close'
        meta_tag['as_tag_identifier'] = matcher
      else:
        meta_tag['as_tag_identifier'] = f"<{tag}>"
        if meta_tag['end_idx'] > input.index('/', meta_tag['start_idx']):
          meta_tag['tag_role'] = 'open_close_alt'
        else:
          meta_tag['tag_role'] = 'open'
      specific = addSpecificAttributes(meta_tag)
      globals = addGlobalAttributes()
      meta_tag['allowed_attributes'] = mergeDict([globals, specific])  
      current_idx = meta_tag['end_idx']
      collected_tags.append(meta_tag)
    ##handle closers
    current_idx = 0
    for c in as_close:
      meta_tag = {}
      meta_tag['tag_type'] = tag
      meta_tag['tag_role'] = 'close'
      meta_tag['as_tag_identifier'] = f"{o}>"
      meta_tag['start_idx'] = input.index(c, current_idx)
      meta_tag['end_idx'] = input.index('>', meta_tag['start_idx'])
      meta_tag['with_attributes'] = ""
      collected_tags.append(meta_tag) 
      current_idx = meta_tag['end_idx'] +1
  return collected_tags


def parseStyleString(styles_, tag_styles):
  for val in styles_.split(";"):
    if (val == ""):
      continue
    else: 
      idx = val.index(":")
      kee = val[:idx].strip()
      value = val[idx+1:].strip()
      tag_styles[kee] = value
  return tag_styles

def parseAttributes(tags):
  for tag in tags: 
    #loop through the attribute keys
    for kee in tag['allowed_attributes'].keys():
      tag_with = tag['with_attributes']
      if f"{kee}=" not in tag_with:
        continue
        
      else:
        idx = tag_with.index(f"{kee}=")
        idx_equ = tag_with.index("=", idx)
        quot_type = tag_with[idx_equ + 1]
        idx_end = tag_with.index(quot_type, idx_equ + 2)
        if kee == 'style':
          tag['allowed_attributes'][kee] = parseStyleString(tag_with[idx_equ+2:idx_end], tag['allowed_attributes'][kee])
        else:
          tag['allowed_attributes'][kee] = tag_with[idx_equ+2:idx_end]
  return tags




def createSequence(sorted_tags):
  sequence = []
  for i, t in enumerate(sorted_tags):
    t['seq_id'] = f"{str(i)}-$$_{t['tag_type']}"
    sequence.append(t['seq_id'])
  return (sequence, sorted_tags)


def seqIdtoDict(id):
  return {
      'seq_tag_type': id[id.index('_')+1:],
      'seq_unique': id[:id.index('-')],
      'seq_tag_role': id[id.index('-')+1: id.index('_')] 
  }



def matchTags(tags_collected):
  tags = sortTags(tags_collected)
  updated_tags = []
  to_remove = []
  #sequence id = count-role_id_tagtype
  #count is unique in sequence for pair or self-closing
  #role_ids: 1 = open, 2 = close (needs to have same count), 3 = self-closing
  (seq, tags) = createSequence(tags)
  #fish out all self-closing tags

  for t in tags:
    if t['tag_role'] == 'open_close':
      s = t['seq_id']
      t['seq_id'] = s.replace('$$', "3")
      s_idx = seq.index(s)
      seq[s_idx] = t['seq_id']
      updated_tags.append(t)
      to_remove.append(t)
    if t['tag_role'] == 'open_close_alt':
      s = t['seq_id']
      t['seq_id'] = s.replace('$$', "3")
      s_idx = seq.index(s)
      seq[s_idx] = t['seq_id']
      updated_tags.append(t)
      to_remove.append(t)
  for item in to_remove:
    tags.remove(item)
  current_length = len(tags)
  # even though a while loop could work, it's lagging behind whith the remove statements and slips into an infinite loop
  for count in range(0, current_length):
    current_length = len(tags)
    for i in reversed(range(0, current_length)):
      if i <= 1:
        break
      if tags[i]['tag_role'] == 'close' and tags[i-1]['tag_role'] == 'open':
        s = tags[i-1]['seq_id']
        s_close = tags[i]['seq_id']
        item_open = tags[i-1]
        item_open['seq_id'] = s.replace('$$', "1")
        seqIdAsDict = seqIdtoDict(item_open['seq_id'])
        item_close = tags[i]
        item_close['seq_id'] = f"{seqIdAsDict['seq_unique']}-2_{seqIdAsDict['seq_tag_type']}"
        seq[seq.index(s)] = item_open['seq_id']
        seq[seq.index(s_close)] = item_close['seq_id']
        item_open['closer'] = item_close
        updated_tags.append(item_open)
        tags.remove(item_open)
        tags.remove(item_close)
  # finish the last tags (what if the first tag is self-closing?)
  if len(tags) == 2:
    s = tags[0]['seq_id']
    s_close = tags[1]['seq_id']
    tags[0]['seq_id'] = s.replace('$$', "1")
    seq[seq.index(s)] = tags[0]['seq_id']    
    seqIdAsDict = seqIdtoDict(tags[0]['seq_id'])
    tags[1]['seq_id'] = f"{seqIdAsDict['seq_unique']}-2_{seqIdAsDict['seq_tag_type']}"
    seq[seq.index(s_close)] = tags[1]['seq_id']
    tags[0]['closer'] = tags[1]
    updated_tags.append(tags[0])
  return (seq, updated_tags)


# lifts style, id, class attributes to top level

def liftAttributes(tags):
  rel_attr = ['id', 'style', 'class']
  for tag in tags:
    for att in rel_attr:
      tag[att] = tag['allowed_attributes'][att]
      tag['allowed_attributes'].pop(att)
  return tags





def mapHTMLString(input):
  tags = identifyTags(input)
  (seq, tags) = matchTags(tags)
  tags = getInnerContents(tags, input)
  tags = parseAttributes(tags)
  return (seq, liftAttributes(tags))