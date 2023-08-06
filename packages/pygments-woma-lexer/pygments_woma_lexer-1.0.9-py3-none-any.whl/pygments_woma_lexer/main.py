# Copyright 2021 Ross J. Duff
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO 
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, 
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
# SOFTWARE.
from pygments import token
from pygments.lexer import RegexLexer, bygroups, combined, include


class WomaLexer(RegexLexer):
    name = 'woma'
    mimetype = 'text/woma'
    startinline = True

    def innerstring_rules(ttype):
        return [
            # the old style '%s' % (...) string formatting (still valid in Py3)
            (r'%(\(\w+\))?[-#0 +]*([0-9]+|[*])?(\.([0-9]+|[*]))?'
             '[hlL]?[E-GXc-giorsaux%]', token.String.Interpol),
            # the new style '{}'.format(...) string formatting
            (r'\{'
             r'((\w+)((\.\w+)|(\[[^\]]+\]))*)?'  # field name
             r'(\![sra])?'                       # conversion
             r'(\:(.?[<>=\^])?[-+ ]?#?0?(\d+)?,?(\.\d+)?[E-GXb-gnosx%]?)?'
             r'\}', token.String.Interpol),

            # backslashes, quotes and formatting signs must be parsed one at a time
            (r'[^\\\'"%{\n]+', ttype),
            (r'[\'"\\]', ttype),
            # unhandled string formatting sign
            (r'%|(\{{1,2})', ttype)
            # newlines are an error (use "nl" state)
        ]

    def fstring_rules(ttype):
        return [
            # Assuming that a '}' is the closing brace after format specifier.
            # Sadly, this means that we won't detect syntax error. But it's
            # more important to parse correct syntax correctly, than to
            # highlight invalid syntax.
            (r'\}', token.String.Interpol),
            (r'\{', token.String.Interpol, 'expr-inside-fstring'),
            # backslashes, quotes and formatting signs must be parsed one at a time
            (r'[^\\\'"{}\n]+', ttype),
            (r'[\'"\\]', ttype),
            # newlines are an error (use "nl" state)
        ]

    tokens = {
        'root': [
            (r'\*|\*\*|\+|\-|!|%|\/|=', token.Operator),
            (r'>=|<=|!=|>|<|==', token.Operator),
            (r'print', token.Name.Builtin),
            (r"\bmain:", token.Name.Label),
            (
            r'procedure|coroutine|int|list|float|finite|number|np_scalar_uint|np_uint8|np_uint16|np_uint32|np_uint64|np_scalar_int|np_int8|np_int16|np_int32|np_int64',
            token.Keyword.Type),
            (r'[ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_][ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_]*', token.Name.Decorator),
            (r"`(?:[^`\n\r\\]|(?:``)|(?:\\(?:[^x]|x[0-9a-fA-F]+)))*`", token.Comment),
            (r'[<\^>]|[<\*>]|<@>|->|[<-]|\)\)|#|(?<=[\)\]\}])\.{3,}|nullit', token.Keyword),
            (r'(?<=\w)\.(?=\w)', token.Punctuation),
            (r'[]{}:(),;[]', token.Punctuation),
            (r'(\d(?:_?\d)*\.(?:\d(?:_?\d)*)?|(?:\d(?:_?\d)*)?\.\d(?:_?\d)*)([eE][+-]?\d(?:_?\d)*)?', token.Number.Float),
            (r'\d(?:_?\d)*[eE][+-]?\d(?:_?\d)*j?', token.Number.Float),
            (r'0[oO](?:_?[0-7])+', token.Number.Oct),
            (r'0[bB](?:_?[01])+', token.Number.Bin),
            (r'0[xX](?:_?[a-fA-F0-9])+', token.Number.Hex),
            (r'\d(?:_?\d)*', token.Number.Integer),
            ('([uUbB]?)(""")', bygroups(token.String.Affix, token.String.Double),
             combined('stringescape', 'tdqs')),
            ("([uUbB]?)(''')", bygroups(token.String.Affix, token.String.Single),
             combined('stringescape', 'tsqs')),
            ('([uUbB]?)(")', bygroups(token.String.Affix, token.String.Double),
             combined('stringescape', 'dqs')),
            ("([uUbB]?)(')", bygroups(token.String.Affix, token.String.Single),
             combined('stringescape', 'sqs')),

            (r'[^\S\n]+', token.Text),
        ],
        'strings-single': innerstring_rules(token.String.Single),
        'strings-double': innerstring_rules(token.String.Double),
        'stringescape': [
            (r'\\([\\abfnrtv"\']|\n|N\{.*?\}|u[a-fA-F0-9]{4}|'
             r'U[a-fA-F0-9]{8}|x[a-fA-F0-9]{2}|[0-7]{1,3})', token.String.Escape)
        ],
        'tdqs': [
            (r'"""', token.String.Double, '#pop'),
            include('strings-double'),
            (r'\n', token.String.Double)
        ],
        'tsqs': [
            (r"'''", token.String.Single, '#pop'),
            include('strings-single'),
            (r'\n', token.String.Single)
        ],
        'dqs': [
            (r'"', token.String.Double, '#pop'),
            (r'\\\\|\\"|\\\n', token.String.Escape),  # included here for raw strings
            include('strings-double')
        ],
        'sqs': [
            (r"'", token.String.Single, '#pop'),
            (r"\\\\|\\'|\\\n", token.String.Escape),  # included here for raw strings
            include('strings-single')
        ],
    }
