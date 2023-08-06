"""Metakernel magic for evaluating cell code using PySaprk."""
from __future__ import absolute_import, division, print_function

import os
from metakernel import ExceptionWrapper
from metakernel import Magic
from metakernel import MetaKernel
from metakernel import option
from metakernel.process_metakernel import TextOutput
from tornado import ioloop, gen
from textwrap import dedent

class PySparkMagic(Magic):
    """Line and cell magic that supports PySpark code execution.
    Attributes
    ----------
    TODO
    """
    def __init__(self, kernel):
        super(PySparkMagic, self).__init__(kernel)
        self.magic_called = False
        self.sc = None

    def _initiliaze_pyspark(self):
        """Initializing pyspark. This includes the SparkContext
        """
        if self.sc is None:
            self.kernel.Display(TextOutput("Intitializing PySpark ..."))
            from pyspark import SparkContext
            from pyspark.sql import SparkSession
            
            self.sc = SparkContext()
            self.ss = SparkSession.builder.getOrCreate()

            self.kernel.cell_magics['python'].env['spark'] = self.ss
            self.kernel.cell_magics['python'].env['sc'] = self.sc

            # Display information about the Spark session from PySpark
            self.kernel.Display(TextOutput(dedent("""\
                Spark Web UI available at {webui}
                SparkContext available as 'sc' (version = {version}, master = {master}, app id = {app_id})
                SparkSession available as 'spark'
                """.format(
                    version=self.sc.version,
                    master=self.sc.master,
                    app_id=self.sc.applicationId,
                    webui=self.sc.uiWebUrl
                )
            )))

        return self.sc

    def line_pyspark(self, *args):
        """%pysprak - Prints out the args passed after magic command
        Parameters
        ----------
        *args : list of string
            Line magic arguments joined into a single-space separated string
        Examples
        --------
        %pysaprk test string
        """
        self.kernel.Print(args)

    # Use optparse to parse the whitespace delimited cell magic options
    # just as we would parse a command line.
    @option(
        "-e", "--eval_output", action="store_true", default=False,
        help="Evaluate the return value from the Scala code as Python code"  
    )
    @option(
         "-b", "--blah", action="store", type="string", default="",
        help="Testing blah"
    )
    def cell_pyspark(self, eval_output=False, blah=""):
        """%%pyspark - Evaluate contents of cell.
        This cell magic will take content of a cell and perform some
        manipulation to it.
        Examples
        --------
        %%pyspark
        testing
        """
        self.magic_called = True
        self.kernel.Print(self.code)
        self.kernel.Print(eval_output)
        self.kernel.Print(blah)
        
    def line_pyspark_interactive_datatable(self, dataframe):
        python_magic = self.kernel.line_magics['python']
        df = python_magic.eval(dataframe+".toPandas()")
        
        import ipydatatable
        table = ipydatatable.InteractiveTable()
        table.table = df
        self.kernel.Display(table)
          
    def line_pyspark_add_to_cell(self, text):
        self.kernel.payload.append({"source": "set_next_input",
                                        "text": text,
                                        "replace": True}) 

    def post_process(self, retval):
        """Processes the output of one or stacked magics.
        Parameters
        ----------
        TODO
        Returns
        -------
        TODO
        """
        self.magic_called = False
        self.kernel.Print("Magic Completed")
