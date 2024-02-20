# from-pdf-pt

* domain(s): pretrain
* generates: ldc.api.pretrain.PretrainData

Extracts text from PDF files to use for pretraining.

```
usage: from-pdf-pt [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                   [-N LOGGER_NAME] [-i [INPUT [INPUT ...]]]
                   [-I [INPUT_LIST [INPUT_LIST ...]]] [-p RANGE] [-V]

Extracts text from PDF files to use for pretraining.

optional arguments:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  -i [INPUT [INPUT ...]], --input [INPUT [INPUT ...]]
                        Path to the PDF file(s) to read; glob syntax is
                        supported (default: None)
  -I [INPUT_LIST [INPUT_LIST ...]], --input_list [INPUT_LIST [INPUT_LIST ...]]
                        Path to the text file(s) listing the data files to use
                        (default: None)
  -p RANGE, --page_range RANGE
                        The range of pages to read; 1-based range, e.g.,
                        'first-last' or '1-12,20,22,25-last'; available
                        placeholders: first, second, third, last_2, last_1,
                        last;last_1: second to last, last_2: third to last
                        (default: first-last)
  -V, --invert          Whether to invert the page range, i.e., discard rather
                        than keep. (default: False)
```
