# Simple_Compiler

"コンピュータシステムの理論と実装"という本をもとにしてアセンブラとコンパイラーをPythonを使って構築しようという試み。
基本的には本の内容に忠実にPythonを使って実装をしている。本の中の機械語とオブジェクト指向言語のJackの仕様を流用している。

This project is tring to implement the assembler and compiler by Python based on the content of Japanese version of "The Elements of Computing Systems"(Noam Nisan, Shimon Schocken). In this project, Jack language and machine language of referenced book is used.

    * アセンブラは参考文献にある通り4つのモジュールに分割して実装した。参考文献内ではオブジェクト指向に近い形でパーサーのapiが提示されており、
    　イテレーターを実装するのが無難だと思われたが、できるだけ関数のみによって処理を記述したかったのでモジュール間のデータの共有には
      辞書のリストを使用している。ちなみにシンボルテーブルは専用のクラスを作ったが、Pythonの辞書で代用可能である。
    　Assembler is implemented in 4 modules as it is suggested in referenced book. In the book, Parser API was give as Object-Oriented 
      like pattern, and it looks like iterator should be used, however, since this project want to process the data as list, list of 
      dictionaly is used for the data trasfered between modules. SimbolTable is implemented as wrapper class of the dictionary, therefore,
      dictionary in Python can be directly used instead of this class.

    * VM実装に際して参考文献と同じく二段階で構築を行った。演算部分とメモリアクセスのみを担当するシンプルバージョンを実装したのち、完成版の
      VM変換器のほうでプログラムフローと関数呼び出しの制御をつけ足してVM言語からアセンブリ言語へと変換する変換器を完成させた。完成品の
      VM変換器は二つあるがOld.Verのほうが生成するアセンブリコードの長さが少しだけ長い。具体的には最新版の完成品のほうはreturnの処理の部分を
      少しだけ洗練させて、生成するコードが短くなるようにしてある。しかしごく小さな違いのでどちらを使っても問題ない。VM変換器は基本的には
      アセンブラと同じような構造となっている。ただし、コードライターは内部的に異なるアセンブリ言語のラベルを生成するためにカウントを
      覚えておく必要があったため、関数ではなくクラスとして実装した。また変換器のメソッドはお互いにある程度独立しており、変換を完了するには
      全メソッドを順番に呼ぶ必要がある。
      The project construct the VM translator in 2 steps as it is suggested in referenced book. First version implemented Arithmetic 
      operation and Memory accsess, and final version added implementation of Program flow and Function call. There are two version of 
      completed VM traslator. Version without "oldVer" produces less amount of Assembler code, since its "return" part of implementation is
      little improved. However, both Version should work propery since, there is no big difference between these two. The structure of 
      VM translator is basically same with Assembler. However, CodeWriter is implemented as class, since it need to record number of command
      called to generate the different Assembler Label. In addition, there is no one method which will translate the code at once. 
      Instead of that, each methods have to be called in appropriate order.

    * コンパイラーは参考文献の進捗方法と同じく先にJack言語をXMLで表せる構文木へと分解するプログラムを作成、その後そこで培った技術を拡張して
      完成品のコンパイラーを実装した。モジュールの構造なども基本的には参考文献の内容に即したものとなっている。
      The Compiler was constructed in 2 steps as referenced book suggested. First, a Parser which convert Jack language to XML which represents
      the syntax tree is implemented. After that, the Compiler was written by extending the Parser. The structure of the modules in Compiler
      program is bassically following the suggestion in referenced book.

Reference lists:  
コンピュータシステムの理論と実装 ―モダンなコンピュータの作り方　オライリージャパン (2015/3/25)