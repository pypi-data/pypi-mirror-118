>>> from namefiles import disassemble_filename
>>> from doctestprinter import print_pandas
>>> from pandas import DataFrame
>>> test_filenames = [
...     "A",
...     "A#SOURCE0IDENT",
...     "A#_4_var_group",
...     "A.context.txt",
...     "A#1",
...     "A#12",
...     "A#123",
...     "A#1234",
...     "A#1#SOURCE78",
...     "A#12#SOURCE7",
...     "A#123#SOURCE",
...     "A#1234#SOURC",
...     "A.txt",
...     "A#1.txt",
...     "A#12.txt",
...     "A#123.txt",
...     "A#1234.txt",
...     "A#1#SOURCE78.txt",
...     "A#12#SOURCE7.txt",
...     "A#123#SOURCE.txt",
...     "A#1234#SOURC.txt",
... ]
>>> sample_parts = [disassemble_filename(test_name) for test_name in test_filenames]
>>> sample_frame = DataFrame(sample_parts)
>>> column_order = [
...     "identifier", "sub_id", "source_id", "context", "extension", "vargroup"
... ]
>>> print_pandas(sample_frame[column_order])
    identifier  sub_id     source_id  context  extension               vargroup
 0           A
 1           A          SOURCE0IDENT
 2           A                                            ['4', 'var', 'group']
 3           A                        context       .txt
 4           A       1
 5           A      12
 6           A     123
 7           A    1234
 8           A       1      SOURCE78
 9           A      12       SOURCE7
10           A     123        SOURCE
11           A    1234         SOURC
12           A                                      .txt
13           A       1                              .txt
14           A      12                              .txt
15           A     123                              .txt
16           A    1234                              .txt
17           A       1      SOURCE78                .txt
18           A      12       SOURCE7                .txt
19           A     123        SOURCE                .txt
20           A    1234         SOURC                .txt
