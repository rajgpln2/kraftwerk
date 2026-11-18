"""Execute all notebook cells in a fresh IPython process and save rich outputs.

This runner avoids a notebook server and local communication ports. It uses the
same IPython cell execution and matplotlib inline display used by Jupyter.
"""
from pathlib import Path
import os
import tempfile

ROOT = Path(__file__).resolve().parent
os.chdir(ROOT)
os.environ.setdefault('IPYTHONDIR', str(Path(tempfile.gettempdir()) / 'lamination_ipython'))
os.environ.setdefault('MPLCONFIGDIR', str(Path(tempfile.gettempdir()) / 'lamination_mpl'))

import nbformat
from IPython.core.interactiveshell import InteractiveShell
from IPython.utils.capture import capture_output


def main():
    notebook_path = ROOT / 'bondline_oos_capstone.ipynb'
    notebook = nbformat.read(notebook_path, as_version=4)
    shell = InteractiveShell.instance()
    import matplotlib
    matplotlib.use('module://matplotlib_inline.backend_inline')
    from matplotlib_inline.backend_inline import configure_inline_support
    configure_inline_support(shell, 'inline')
    execution_count = 0
    for cell_index, cell in enumerate(notebook.cells, start=1):
        if cell.cell_type != 'code':
            continue
        execution_count += 1
        cell.execution_count = execution_count
        cell.outputs = []
        with capture_output() as captured:
            result = shell.run_cell(cell.source, store_history=False)
        for name, content in [('stdout', captured.stdout), ('stderr', captured.stderr)]:
            if content:
                cell.outputs.append(nbformat.v4.new_output('stream', name=name, text=content))
        for output in captured.outputs:
            cell.outputs.append(nbformat.v4.new_output('display_data',
                                                       data=output.data,
                                                       metadata=output.metadata))
        error = result.error_before_exec or result.error_in_exec
        if error is not None:
            nbformat.write(notebook, notebook_path)
            raise RuntimeError(f'Notebook cell {cell_index} failed') from error
        print(f'Executed code cell {execution_count}', flush=True)
    nbformat.validate(notebook)
    nbformat.write(notebook, notebook_path)
    print(f'Saved {notebook_path.name} with outputs')


if __name__ == '__main__':
    main()
