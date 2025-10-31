from extensions.diff import commit_diff

from pyndakaas import Handler, handler, process_dir
import mistune

from pathlib import Path


markdown = mistune.create_markdown(plugins=[commit_diff('https://github.com/rubenvannieuwpoort/vulture')])

@handler()
class Markdown(Handler):
    template = 'lesson'

    @staticmethod
    def should_handle(input_path: Path) -> bool:
        return input_path.is_file() and input_path.suffix == '.md'

    def transform(self) -> None:
        body = markdown(self.source)
        assert isinstance(body, str)
        self.body = body


process_dir(Path('src'), Path('build'))
