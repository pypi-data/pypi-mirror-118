# A Pygments Lexer for the Woma Programming Language
|[![PyPI](https://img.shields.io/pypi/v/pygments-woma-lexer?style=for-the-badge)](https://pypi.org/project/pygments-woma-lexer/)|[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pygments-woma-lexer?style=for-the-badge)](https://pypi.org/project/pygments-woma-lexer/)|[![PyPI - Wheel](https://img.shields.io/pypi/wheel/pygments-woma-lexer?style=for-the-badge)](https://pypi.org/project/pygments-woma-lexer/)|![GitHub repo size](https://img.shields.io/github/repo-size/rjdbcm/pygments_woma_lexer?style=for-the-badge)|[![logo](https://raw.githubusercontent.com/rjdbcm/Aspidites/main/docs/_static/aspidites_logo_45_45.png)](https://github.com/rjdbcm/Aspidites#logomascot)|
|----------|:-------------:|------:|-:|-:|
--------------------------------------
## How to Use
Just add the following lines to your docs/conf.py:
```python
from pygments_woma_lexer import WomaLexer
from sphinx.highlighting import lexers
lexers.update(woma=WomaLexer())
```

Now you can use it like this in ReStructured Text:
```rst
.. code:: woma

  [code goes here]
```
## License
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.  
See [LICENSE.txt](https://github.com/rjdbcm/pygments_woma_lexer/blob/main/LICENSE.txt) for more info.
