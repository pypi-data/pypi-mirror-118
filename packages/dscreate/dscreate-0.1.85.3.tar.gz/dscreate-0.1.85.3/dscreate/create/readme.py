import nbformat
from nbconvert import MarkdownExporter
from nbconvert.writers import FilesWriter
from traitlets.config import Config
    
def generate_readme(notebook_path, dir_path, filename):
    """
    Saves a jupyter notebook as a README.md file using nbformat and nbconvert

    Inputs:
    1. The path for a jupyter notebook to be converted into markdown. str.
    2. The directory path for saving the README.md file. str.
    3. The name of the file without the `.filetype` (README instead of README.md). str.

    Returns:
    None
    """
    output_path = os.path.join(dir_path, 'README.md')
    index_files = os.path.join(dir_path, 'index_files')
    input_path = os.path.join(index_files, filename + '.md')
    notebook = nbformat.read(notebook_path, nbformat.NO_CONVERT)
    mark_exporter = MarkdownExporter()
    (output, resources) = mark_exporter.from_notebook_node(notebook)


    if not os.path.isdir(index_files):
        os.mkdir(index_files)
    if os.path.isfile(output_path):
        os.remove(output_path)
    if os.path.isfile(input_path):
        os.remove(input_path)

    c = Config()
    c.FilesWriter.build_directory = index_files
    fw = FilesWriter(config=c)
    fw.write(output, resources, notebook_name=filename)
    shutil.move(input_path, output_path)