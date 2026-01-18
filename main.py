import markdown2
import os


class File:
    HTML_FOLDER = "./html"
    HTML_TEMPLATE_PATH = "./templates/template.html"

    get_html = None

    def __init__(self, md_file_path: str):
        # Markdown information
        self.md_file_path = md_file_path
        self.md_content = self._get_md_file_content()
        # HTML information
        self.html_file_path = self._get_html_path()
        self._load_get_html_lambda()
        self.html_data = self._get_html_data()

    def generate_html_file(self) -> None:
        # Create the content of the HTML file
        html_content = self.get_html(content=self.html_data.get("content", ""),
                                     title=self.html_data.get("title", ""))
        # Delete the HTML file if it already exists to "refresh"
        if os.path.exists(self.html_file_path):
            os.remove(self.html_file_path)
        # Write the content to the file
        with open(self.html_file_path, "w") as file:
            file.write(html_content)

    ############################################################################
    # Initial & Setup methods
    ############################################################################
    def _get_md_file_content(self) -> str:
        with open(self.md_file_path, "r") as file:
            return file.read()

    def _get_html_path(self) -> str:
        # Get the file name
        file_name = self.md_file_path.split(r"/")[-1:][0]
        # Concat the html folder path with the file name, but replace the .md
        # extension with an .html extension
        return f"{self.HTML_FOLDER}/{file_name[:-3]}.html"

    def _load_get_html_lambda(self) -> None:
        # Check if the template has alread been loaded
        if self.get_html != None:
            return

        # Load the HTML template
        with open(self.HTML_TEMPLATE_PATH, "r") as file:
            template_content = file.read()

        # Create the lambda function
        self.get_html = lambda title, content: template_content.replace(
            "[[title]]", title).replace("[[content]]", content)

    def _get_html_data(self) -> dict:
        # Prepare markdown content
        ## Replace .md links to refer to .md links
        prepared_md_content = self.md_content.replace(".md)", ".html)")
        # Convert the markdown file
        html_content = markdown2.markdown(
            prepared_md_content,
            extras=["metadata", "footnotes", "tables"],
            footnote_title="Reiru al %d en la teksto.",
            footnote_return_symbol="&#8617;")
        metadata = html_content.metadata

        # Construct the result structure
        return {
            "content":
            str(html_content),
            "title":
            metadata.get(
                "title",
                self.md_file_path.split("/")[-1:][0].split("..")[-1:][0][:-3]),
            "created_at":
            metadata.get("created_at", "N/A"),
            "last_updated_at":
            metadata.get("last_created_at", "N/A")
        }


class Folder:
    FOLDER_PATH = "./md"

    def __init__(self):
        self.md_files = self._load_md_files()

    def convert_markdown_to_html(self):
        for file in self.md_files:
            file.generate_html_file()

    ############################################################################
    # Initial & Setup methods
    ############################################################################

    def _load_md_files(self) -> list:
        result = []

        for file in os.listdir(self.FOLDER_PATH):
            if file.endswith(".md"):
                result.append(File(f"{self.FOLDER_PATH}/{file}"))

        return result


if __name__ == "__main__":
    md_f = Folder()
    md_f.convert_markdown_to_html()
